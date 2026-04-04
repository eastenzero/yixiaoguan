#!/usr/bin/env python3
"""
知识库批量入库脚本
将 knowledge-base/entries/ 下的 Markdown 文件向量化存入 ChromaDB

用法:
    cd scripts
    python batch_ingest_kb.py
"""

import os
import sys
import re
import json
import yaml
from pathlib import Path
from datetime import datetime

# 添加 ai-service 到路径
AI_SERVICE_PATH = Path(__file__).parent.parent / "services" / "ai-service"
sys.path.insert(0, str(AI_SERVICE_PATH))

# 加载环境变量
from dotenv import load_dotenv
env_path = AI_SERVICE_PATH / ".env"
if env_path.exists():
    load_dotenv(env_path)
    print(f"✅ 已加载环境变量: {env_path}")
else:
    # 尝试 .secrets
    secrets_env = Path(__file__).parent.parent / ".secrets" / ".env"
    if secrets_env.exists():
        load_dotenv(secrets_env)
        print(f"✅ 已加载环境变量: {secrets_env}")

from app.core.kb_vectorize import vector_store
from app.core.config import settings

# 引入 chunker 的 MarkdownTextSplitter
sys.path.insert(0, str(AI_SERVICE_PATH / "app" / "core"))
from chunker import MarkdownTextSplitter


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """
    解析 Markdown 文件的 YAML frontmatter
    
    返回: (frontmatter_dict, body_content)
    """
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            yaml_content = parts[1].strip()
            body = parts[2].strip()
            try:
                metadata = yaml.safe_load(yaml_content) or {}
                if not isinstance(metadata, dict):
                    metadata = {}
            except yaml.YAMLError:
                metadata = {}
                for line in yaml_content.splitlines():
                    if line.startswith('title:'):
                        metadata['title'] = line[6:].strip().strip('"').strip("'")
                        break
            return metadata, body
    
    return {}, content


def ingest_kb_entry(file_path: Path, dry_run: bool = False, splitter: MarkdownTextSplitter = None) -> dict:
    """
    将单个知识条目入库（支持分块）
    
    Args:
        file_path: Markdown 文件路径
        dry_run: 是否为测试模式（不入库）
        splitter: MarkdownTextSplitter 实例
    
    Returns:
        处理结果信息
    """
    try:
        content = file_path.read_text(encoding='utf-8')
        metadata, body = parse_frontmatter(content)
        
        # 提取 entry_id（从文件名）
        entry_id = file_path.stem  # 例如: KB-20260324-0001
        
        # 获取标题（优先使用 frontmatter 中的 title）
        title = metadata.get('title', '')
        if not title:
            title = entry_id
        
        # 组合向量化内容：标题 + 正文
        # 提取正文中的关键部分（标准答复、办理流程等）
        vector_content = f"""问题概述：{metadata.get('问题概述', '')}

标准答复：{extract_section(body, '标准答复')}

办理条件：{extract_section(body, '办理条件')}

办理流程：{extract_section(body, '办理流程')}

所需材料：{extract_section(body, '所需材料')}

时间节点：{extract_section(body, '时间节点')}

注意事项：{extract_section(body, '注意事项')}
"""
        
        # 构建基础元数据
        base_metadata = {
            "title": title,
            "category": metadata.get('category', '未分类'),
            "audience": metadata.get('audience', '全体学生'),
            "rule_task_id": metadata.get('rule_task_id', ''),
            "material_id": metadata.get('material_id', ''),
            "status": metadata.get('status', 'draft'),
            "source_file": str(file_path.relative_to(Path(__file__).parent.parent)),
        }
        
        result = {
            "entry_id": entry_id,
            "title": title,
            "content_length": len(vector_content),
            "status": "success",
            "dry_run": dry_run,
        }
        
        if not dry_run:
            # 使用 chunker 对内容进行分块
            if splitter is None:
                splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
            
            chunks = splitter.split(
                text=vector_content,
                source_path=str(file_path),
                base_metadata=base_metadata
            )
            
            # 逐个 chunk 入库
            chunk_ids = []
            chunk_count = len(chunks)
            
            for chunk in chunks:
                # 生成 chunk ID: {entry_id}__chunk_{index}
                chunk_id = f"{entry_id}__chunk_{chunk.index}"
                chunk_ids.append(chunk_id)
                
                # 构建 chunk 的 metadata，包含 chunk_index
                chunk_metadata = {
                    **chunk.metadata,
                    "entry_id": entry_id,
                    "chunk_index": chunk.index,
                    "chunk_total": chunk_count,
                }
                
                # 组合标题和 chunk 内容进行向量化
                chunk_text = f"{title}\n\n{chunk.content}".strip()
                
                # 生成向量并入库存储
                try:
                    embedding = vector_store.generate_embedding(chunk_text)
                    vector_store._collection.upsert(
                        ids=[chunk_id],
                        embeddings=[embedding],
                        documents=[chunk_text],
                        metadatas=[chunk_metadata],
                    )
                except Exception as e:
                    return {
                        "entry_id": entry_id,
                        "status": "error",
                        "error": f"Chunk {chunk.index} 入库失败: {str(e)}",
                    }
            
            result["message"] = f"入库成功，共 {chunk_count} 个 chunks"
            result["chunk_count"] = chunk_count
            result["chunk_ids"] = chunk_ids[:3]  # 仅记录前3个用于调试
        else:
            result["message"] = "测试模式，未实际入库"
            result["preview"] = vector_content[:500] + "..." if len(vector_content) > 500 else vector_content
        
        return result
        
    except Exception as e:
        return {
            "entry_id": file_path.stem,
            "status": "error",
            "error": str(e),
        }


def extract_section(content: str, section_name: str) -> str:
    """提取 Markdown 中特定章节的内容"""
    pattern = rf'## {section_name}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def main():
    """主函数"""
    print("=" * 60)
    print("医小管知识库批量入库工具")
    print("=" * 60)
    
    # 检查配置
    print(f"\n📁 ChromaDB 目录: {settings.chroma_persist_dir}")
    print(f"📚 集合名称: {settings.chroma_collection_kb}")
    print(f"🔑 DashScope API: {'已配置' if settings.dashscope_api_key else '未配置'}")
    
    if not settings.dashscope_api_key:
        print("\n❌ 错误: DashScope API Key 未配置")
        print("请检查 .env 文件或环境变量")
        sys.exit(1)
    
    # 初始化向量存储
    print("\n🚀 初始化向量存储...")
    try:
        vector_store.initialize()
        stats = vector_store.get_stats()
        print(f"✅ 初始化完成，当前条目数: {stats['entry_count']}")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    # 初始化 chunker
    print("📝 初始化 MarkdownTextSplitter...")
    splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
    print("✅ Chunker 初始化完成")
    
    # 查找知识库文件
    kb_dir = Path(__file__).parent.parent / "knowledge-base" / "entries" / "first-batch-drafts"
    if not kb_dir.exists():
        print(f"\n❌ 知识库目录不存在: {kb_dir}")
        sys.exit(1)
    
    md_files = sorted(kb_dir.glob("KB-*.md"))
    print(f"\n📄 找到 {len(md_files)} 个知识条目文件")
    
    if not md_files:
        print("❌ 没有找到任何 KB-*.md 文件")
        sys.exit(1)
    
    # 检查命令行参数
    dry_run = "--dry-run" in sys.argv
    skip_confirm = "--yes" in sys.argv
    
    if dry_run:
        print("\n🧪 测试模式 - 预览前3个文件:")
        for md_file in md_files[:3]:
            result = ingest_kb_entry(md_file, dry_run=True, splitter=splitter)
            print(f"\n条目: {result['entry_id']}")
            print(f"标题: {result['title']}")
            print(f"内容长度: {result['content_length']} 字符")
            print("-" * 40)
        print("\n使用 --yes 参数执行正式入库")
        return
    
    if not skip_confirm:
        print(f"\n⚠️  即将向量化并入库 {len(md_files)} 个知识条目")
        print("使用 --yes 参数跳过此确认")
        # 非交互环境，默认继续
        print("自动继续...\n")
    
    dry_run = False
    
    # 批量入库
    print(f"\n📥 开始批量入库...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    total_chunks = 0
    errors = []
    
    for i, md_file in enumerate(md_files, 1):
        print(f"[{i}/{len(md_files)}] {md_file.name} ... ", end="", flush=True)
        
        result = ingest_kb_entry(md_file, dry_run=dry_run, splitter=splitter)
        
        if result['status'] == 'success':
            chunk_info = f" ({result.get('chunk_count', 1)} chunks)" if 'chunk_count' in result else ""
            print(f"✅ {result['message']}{chunk_info}")
            success_count += 1
            total_chunks += result.get('chunk_count', 1)
        else:
            print(f"❌ 错误: {result.get('error', '未知错误')}")
            error_count += 1
            errors.append((md_file.name, result.get('error', '')))
    
    # 统计结果
    print("-" * 60)
    print(f"\n📊 入库完成!")
    print(f"   成功: {success_count} 条")
    print(f"   失败: {error_count} 条")
    print(f"   总 chunks: {total_chunks} 个")
    
    if errors:
        print(f"\n❌ 失败的条目:")
        for name, error in errors:
            print(f"   - {name}: {error}")
    
    # 最终统计
    print("\n📝 最终知识库统计:")
    final_stats = vector_store.get_stats()
    print(f"   总条目数: {final_stats['entry_count']}")
    print(f"   向量维度: {final_stats['embedding_dimension']}")
    print(f"   存储路径: {settings.chroma_persist_dir}")
    
    print("\n✨ 完成!")


if __name__ == "__main__":
    main()
