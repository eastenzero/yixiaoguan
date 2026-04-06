"""
批量知识库入库脚本 — 离线跑批流水线

功能：
- 扫描 knowledge-base/raw/first-batch-processing/converted/markdown/ 目录
- 读取 .md/.txt 文件，提取 frontmatter 元数据
- 切分长文本为 chunks（800字/100字重叠）
- 批量调用 upsert_kb_entry 入库
- 生成详细运行报告到 logs/ 目录

使用方法：
    cd services/ai-service
    python scripts/batch_ingestion.py [--source-dir PATH] [--dry-run]

作者: 医小管数据处理团队
"""

import os
import sys
import json
import time
import uuid
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

# 将项目根目录加入路径，确保能导入 app 模块
SCRIPT_DIR = Path(__file__).parent.resolve()
SERVICE_DIR = SCRIPT_DIR.parent.resolve()
sys.path.insert(0, str(SERVICE_DIR))

from app.core.chunker import (
    MarkdownTextSplitter,
    SimpleTextSplitter,
    parse_frontmatter,
    TextChunk,
)
from app.core.kb_vectorize import vector_store


# ==================== 配置常量 ====================

DEFAULT_SOURCE_DIR = Path(__file__).parent.parent.parent.parent / "knowledge-base" / "raw" / "first-batch-processing" / "converted" / "markdown"
LOGS_DIR = Path(__file__).parent.parent.parent.parent / "knowledge-base" / "raw" / "first-batch-processing" / "logs"

MATERIAL_INDEX_PATH = SERVICE_DIR.parent.parent / "deploy" / "materials" / "material-index.json"

def _load_material_index() -> dict:
    if not MATERIAL_INDEX_PATH.exists():
        print(f"[警告] material-index.json 不存在: {MATERIAL_INDEX_PATH}")
        return {}
    with open(MATERIAL_INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

SUPPORTED_EXTENSIONS = {'.md', '.txt', '.markdown'}


# ==================== 数据结构 ====================

class IngestionResult:
    """单个文件处理结果"""
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.success = False
        self.chunks_total = 0
        self.chunks_success = 0
        self.chunks_failed = 0
        self.error_message: Optional[str] = None
        self.chunk_details: List[Dict[str, Any]] = []
        self.processing_time_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "file_path": self.file_path,
            "success": self.success,
            "chunks_total": self.chunks_total,
            "chunks_success": self.chunks_success,
            "chunks_failed": self.chunks_failed,
            "error_message": self.error_message,
            "chunk_details": self.chunk_details,
            "processing_time_ms": round(self.processing_time_ms, 2),
        }


class BatchReport:
    """批次运行报告"""
    def __init__(self):
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.total_files = 0
        self.success_files = 0
        self.failed_files = 0
        self.total_chunks = 0
        self.success_chunks = 0
        self.failed_chunks = 0
        self.file_results: List[Dict[str, Any]] = []
        self.errors: List[Dict[str, Any]] = []

    def finalize(self):
        self.end_time = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time else 0
        return {
            "report_version": "1.0",
            "batch_id": f"batch_{self.start_time.strftime('%Y%m%d_%H%M%S')}",
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": round(duration, 2),
            "summary": {
                "total_files": self.total_files,
                "success_files": self.success_files,
                "failed_files": self.failed_files,
                "total_chunks": self.total_chunks,
                "success_chunks": self.success_chunks,
                "failed_chunks": self.failed_chunks,
            },
            "file_results": self.file_results,
            "errors": self.errors,
        }

    def save(self, output_dir: Path):
        """保存报告到文件"""
        output_dir.mkdir(parents=True, exist_ok=True)
        filename = f"ingestion_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = output_dir / filename
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
        return filepath


# ==================== 核心处理逻辑 ====================

def scan_source_files(source_dir: Path) -> List[Path]:
    """
    扫描源目录，收集所有支持的文件
    
    Args:
        source_dir: 源文件目录
    
    Returns:
        符合条件的文件路径列表
    """
    if not source_dir.exists():
        raise FileNotFoundError(f"源目录不存在: {source_dir}")
    
    files = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(source_dir.rglob(f"*{ext}"))
    
    # 去重并排序
    files = sorted(set(files))
    print(f"[扫描完成] 发现 {len(files)} 个待处理文件")
    return files


def read_file_with_encoding(file_path: Path) -> Tuple[str, bool]:
    """
    尝试多种编码读取文件
    
    Returns:
        (内容, 是否成功)
    """
    encodings = ['utf-8', 'gbk', 'gb2312', 'utf-16', 'latin-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read(), True
        except UnicodeDecodeError:
            continue
    
    # 所有编码都失败，尝试二进制读取后解码
    try:
        with open(file_path, 'rb') as f:
            content = f.read()
            return content.decode('utf-8', errors='replace'), True
    except Exception as e:
        return f"", False


def process_single_file(
    file_path: Path,
    splitter: MarkdownTextSplitter,
    dry_run: bool = False,
    material_index: dict = None,
) -> IngestionResult:
    """
    处理单个文件
    
    Args:
        file_path: 文件路径
        splitter: 文本切分器
        dry_run: 是否仅模拟运行（不实际入库）
    
    Returns:
        IngestionResult 处理结果
    """
    result = IngestionResult(str(file_path))
    start_time = time.time()
    
    try:
        # 1. 读取文件内容
        content, read_success = read_file_with_encoding(file_path)
        if not read_success:
            raise RuntimeError(f"文件编码无法识别，已尝试所有可用编码")
        
        # 2. 解析 frontmatter 元数据
        metadata, body_content = parse_frontmatter(content)
        
        # 提取关键元数据
        title = metadata.get('title', file_path.stem.replace('__', ' ').replace('_', ' '))
        material_id = metadata.get('material_id', '')
        material_info = (material_index or {}).get(material_id, {}) if material_id else {}
        material_pdf = material_info.get('pdf', '')
        material_file_url = f"/materials/{material_pdf}" if material_pdf else ""
        material_title_val = material_info.get('title', '') or title
        category = metadata.get('category', '')
        tags = metadata.get('tags', [])
        if isinstance(tags, str):
            tags = [tags]
        
        base_metadata = {
            "source_file": str(file_path.name),
            "category": category,
            "tags": tags,
        }
        
        # 3. 切分文本
        is_markdown = file_path.suffix.lower() in {'.md', '.markdown'}
        if is_markdown:
            chunks = splitter.split(
                text=body_content,
                source_path=str(file_path),
                base_metadata=base_metadata,
                title=title,
            )
        else:
            # 纯文本使用简单切分器
            txt_splitter = SimpleTextSplitter(CHUNK_SIZE, CHUNK_OVERLAP)
            chunks = txt_splitter.split(
                text=content,
                source_path=str(file_path),
                base_metadata=base_metadata,
            )
        
        result.chunks_total = len(chunks)
        
        if len(chunks) == 0:
            raise RuntimeError("文件内容为空或切分后无有效内容")
        
        # 4. 批量入库
        for chunk in chunks:
            chunk_id = f"{file_path.stem}__chunk_{chunk.index}"
            chunk_title = f"{title} (片段{chunk.index + 1}/{len(chunks)})"
            
            # 合并元数据
            chunk_metadata = {
                **chunk.metadata,
                "chunk_index": chunk.index,
                "total_chunks": len(chunks),
                "source_file": str(file_path.name),
                "material_file_url": material_file_url,
                "material_title": material_title_val,
            }
            
            chunk_result = {
                "chunk_id": chunk_id,
                "index": chunk.index,
                "success": False,
                "error": None,
            }
            
            if dry_run:
                # 模拟模式：仅记录，不实际调用
                chunk_result["success"] = True
                result.chunks_success += 1
            else:
                # 实际入库
                try:
                    vector_store.upsert_kb_entry(
                        entry_id=chunk_id,
                        title=chunk_title,
                        content=chunk.content,
                        metadata=chunk_metadata,
                    )
                    chunk_result["success"] = True
                    result.chunks_success += 1
                except Exception as e:
                    chunk_result["error"] = str(e)
                    result.chunks_failed += 1
                    print(f"    ⚠️ Chunk {chunk.index} 入库失败: {e}")
            
            result.chunk_details.append(chunk_result)
        
        # 5. 标记整体成功
        result.success = (result.chunks_failed == 0)
        
    except Exception as e:
        result.error_message = str(e)
        result.success = False
        print(f"    ❌ 文件处理失败: {e}")
    
    finally:
        result.processing_time_ms = (time.time() - start_time) * 1000
    
    return result


def run_batch_ingestion(
    source_dir: Optional[Path] = None,
    dry_run: bool = False,
) -> BatchReport:
    """
    执行批量入库流程
    
    Args:
        source_dir: 源文件目录，默认使用 DEFAULT_SOURCE_DIR
        dry_run: 是否仅模拟运行
    
    Returns:
        BatchReport 运行报告
    """
    source_dir = source_dir or DEFAULT_SOURCE_DIR
    report = BatchReport()
    material_index = _load_material_index()
    print(f"[材料索引] 加载完成，共 {len(material_index)} 条映射")
    
    print("=" * 60)
    print("医小管知识库批量入库脚本")
    print("=" * 60)
    print(f"源目录: {source_dir}")
    print(f"日志目录: {LOGS_DIR}")
    print(f"切分参数: {CHUNK_SIZE}字/{CHUNK_OVERLAP}字重叠")
    print(f"运行模式: {'模拟运行 (dry-run)' if dry_run else '实际入库'}")
    print("=" * 60)
    
    # 1. 扫描文件
    try:
        files = scan_source_files(source_dir)
    except FileNotFoundError as e:
        print(f"[错误] {e}")
        report.errors.append({"phase": "scan", "error": str(e)})
        report.finalize()
        return report
    
    if not files:
        print("[提示] 未发现待处理文件，流程结束")
        report.finalize()
        return report
    
    report.total_files = len(files)
    
    # 2. 初始化切分器
    splitter = MarkdownTextSplitter(CHUNK_SIZE, CHUNK_OVERLAP)
    
    # 3. 初始化向量存储（仅在非 dry-run 模式下）
    if not dry_run:
        try:
            print("[初始化] 正在连接 ChromaDB...")
            vector_store.initialize()
            stats = vector_store.get_stats()
            print(f"[初始化完成] 当前集合条目数: {stats['entry_count']}")
        except Exception as e:
            print(f"[错误] 向量存储初始化失败: {e}")
            report.errors.append({"phase": "init", "error": str(e)})
            report.finalize()
            return report
    
    # 4. 逐文件处理
    print(f"\n[开始处理] 共 {len(files)} 个文件\n")
    
    for i, file_path in enumerate(files, 1):
        print(f"[{i}/{len(files)}] 处理: {file_path.name}")
        
        result = process_single_file(file_path, splitter, dry_run, material_index=material_index)
        
        # 更新统计
        report.file_results.append(result.to_dict())
        report.total_chunks += result.chunks_total
        report.success_chunks += result.chunks_success
        report.failed_chunks += result.chunks_failed
        
        if result.success:
            report.success_files += 1
            print(f"    ✅ 成功: {result.chunks_success} chunks, {result.processing_time_ms:.0f}ms")
        else:
            report.failed_files += 1
            if result.error_message:
                report.errors.append({
                    "file": str(file_path),
                    "error": result.error_message,
                })
            print(f"    ❌ 失败: {result.error_message or f'{result.chunks_failed} chunks 失败'}")
    
    # 5. 生成报告
    report.finalize()
    report_path = report.save(LOGS_DIR)
    
    # 6. 打印汇总
    print("\n" + "=" * 60)
    print("处理完成汇总")
    print("=" * 60)
    print(f"总文件数: {report.total_files}")
    print(f"  ✅ 成功: {report.success_files}")
    print(f"  ❌ 失败: {report.failed_files}")
    print(f"总 chunks: {report.total_chunks}")
    print(f"  ✅ 入库成功: {report.success_chunks}")
    print(f"  ❌ 入库失败: {report.failed_chunks}")
    print(f"总耗时: {report.to_dict()['duration_seconds']:.2f} 秒")
    print(f"报告已保存: {report_path}")
    print("=" * 60)
    
    return report


# ==================== 入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description="医小管知识库批量入库脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python scripts/batch_ingestion.py
  python scripts/batch_ingestion.py --dry-run
  python scripts/batch_ingestion.py --source-dir ./my-docs
        """
    )
    parser.add_argument(
        "--source-dir",
        type=str,
        default=None,
        help=f"源文件目录 (默认: {DEFAULT_SOURCE_DIR})",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模拟运行模式（不实际入库，仅测试切分逻辑）",
    )
    
    args = parser.parse_args()
    
    source_dir = Path(args.source_dir) if args.source_dir else None
    
    report = run_batch_ingestion(
        source_dir=source_dir,
        dry_run=args.dry_run,
    )
    
    # 如果有失败，返回非零退出码
    if report.failed_files > 0 or report.failed_chunks > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
