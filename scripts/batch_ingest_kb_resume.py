#!/usr/bin/env python3
"""
知识库批量入库脚本 - 支持断点续传
将 knowledge-base/entries/ 下的 Markdown 文件向量化存入 ChromaDB
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
    """解析 Markdown 文件的 YAML frontmatter"""
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


def extract_section(content: str, section_name: str) -> str:
    """提取 Markdown 中特定章节的内容"""
    pattern = rf'## {section_name}\n(.*?)(?=\n## |\Z)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""


def ingest_kb_entry(file_path: Path, splitter: MarkdownTextSplitter = None) -> dict:
    """将单个知识条目入库（支持分块）"""
    try:
        content = file_path.read_text(encoding='utf-8')
        metadata, body = parse_frontmatter(content)
        
        entry_id = file_path.stem
        title = metadata.get('title', '')
        if not title:
            title = entry_id
        
        vector_content = f"""问题概述：{metadata.get('问题概述', '')}

标准答复：{extract_section(body, '标准答复')}

办理条件：{extract_section(body, '办理条件')}

办理流程：{extract_section(body, '办理流程')}

所需材料：{extract_section(body, '所需材料')}

时间节点：{extract_section(body, '时间节点')}

注意事项：{extract_section(body, '注意事项')}
"""
        
        base_metadata = {
            "title": title,
            "category": metadata.get('category', '未分类'),
            "audience": metadata.get('audience', '全体学生'),
            "rule_task_id": metadata.get('rule_task_id', ''),
            "material_id": metadata.get('material_id', ''),
            "status": metadata.get('status', 'draft'),
            "source_file": str(file_path.relative_to(Path(__file__).parent.parent)),
            "page_start": metadata.get('page_start', ''),
            "page_end": metadata.get('page_end', ''),
        }
        
        if splitter is None:
            splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
        
        chunks = splitter.split(
            text=vector_content,
            source_path=str(file_path),
            base_metadata=base_metadata
        )
        
        chunk_ids = []
        chunk_count = len(chunks)
        
        for chunk in chunks:
            chunk_id = f"{entry_id}__chunk_{chunk.index}"
            chunk_ids.append(chunk_id)
            
            chunk_metadata = {
                **chunk.metadata,
                "entry_id": entry_id,
                "chunk_index": chunk.index,
                "chunk_total": chunk_count,
            }
            
            chunk_text = f"{title}\n\n{chunk.content}".strip()
            
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
        
        return {
            "entry_id": entry_id,
            "title": title,
            "status": "success",
            "chunk_count": chunk_count,
        }
        
    except Exception as e:
        return {
            "entry_id": file_path.stem,
            "status": "error",
            "error": str(e),
        }


def get_existing_entry_ids() -> set:
    """获取已入库的 entry_id 集合（从 chunk ID 解析）"""
    try:
        result = vector_store._collection.get()
        if result and "ids" in result:
            entry_ids = set()
            for chunk_id in result["ids"]:
                # chunk_id format: {entry_id}__chunk_{index}
                if "__chunk_" in chunk_id:
                    entry_id = chunk_id.split("__chunk_")[0]
                    entry_ids.add(entry_id)
            return entry_ids
    except Exception as e:
        print(f"⚠️  获取已入库条目失败: {e}")
    return set()


def main():
    print("=" * 60)
    print("医小管知识库批量入库工具 - 断点续传版")
    print("=" * 60)
    
    print(f"\n📁 ChromaDB 目录: {settings.chroma_persist_dir}")
    print(f"📚 集合名称: {settings.chroma_collection_kb}")
    print(f"🔑 DashScope API: {'已配置' if settings.dashscope_api_key else '未配置'}")
    
    if not settings.dashscope_api_key:
        print("\n❌ 错误: DashScope API Key 未配置")
        sys.exit(1)
    
    print("\n🚀 初始化向量存储...")
    try:
        vector_store.initialize()
        stats = vector_store.get_stats()
        print(f"✅ 初始化完成，当前条目数: {stats['entry_count']}")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)
    
    print("📝 初始化 MarkdownTextSplitter...")
    splitter = MarkdownTextSplitter(chunk_size=800, chunk_overlap=100)
    print("✅ Chunker 初始化完成")
    
    # 获取已入库的条目
    existing_ids = get_existing_entry_ids()
    print(f"📊 已入库条目: {len(existing_ids)} 个")
    
    # 查找知识库文件
    kb_dir = Path(__file__).parent.parent / "knowledge-base" / "entries"
    md_files = sorted([f for f in kb_dir.glob("KB-*.md") if f.parent == kb_dir])
    print(f"\n📄 找到 {len(md_files)} 个知识条目文件")
    
    # 过滤出未入库的文件
    pending_files = [f for f in md_files if f.stem not in existing_ids]
    print(f"⏳ 待入库文件: {len(pending_files)} 个")
    
    if not pending_files:
        print("\n✨ 所有条目已入库完成!")
        return
    
    # 批量入库
    print(f"\n📥 开始批量入库...")
    print("-" * 60)
    
    success_count = 0
    error_count = 0
    total_chunks = 0
    errors = []
    
    for i, md_file in enumerate(pending_files, 1):
        print(f"[{i}/{len(pending_files)}] {md_file.name} ... ", end="", flush=True)
        
        result = ingest_kb_entry(md_file, splitter)
        
        if result['status'] == 'success':
            chunk_info = f" ({result.get('chunk_count', 1)} chunks)"
            print(f"✅ 入库成功{chunk_info}")
            success_count += 1
            total_chunks += result.get('chunk_count', 1)
        else:
            print(f"❌ 错误: {result.get('error', '未知错误')}")
            error_count += 1
            errors.append((md_file.name, result.get('error', '')))
    
    # 统计结果
    print("-" * 60)
    print(f"\n📊 本次入库完成!")
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
