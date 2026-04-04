#!/usr/bin/env python3
"""
随机抽查 chunk metadata
"""

import os
import sys
import random
from pathlib import Path

# 添加 ai-service 到路径
AI_SERVICE_PATH = Path(__file__).parent.parent / "services" / "ai-service"
sys.path.insert(0, str(AI_SERVICE_PATH))

# 加载环境变量
from dotenv import load_dotenv
env_path = AI_SERVICE_PATH / ".env"
if env_path.exists():
    load_dotenv(env_path)
else:
    secrets_env = Path(__file__).parent.parent / ".secrets" / ".env"
    if secrets_env.exists():
        load_dotenv(secrets_env)

import chromadb
from app.core.config import settings

def sample_chunks():
    """随机抽查 5 条 chunk 的 metadata"""
    print("=" * 60)
    print("随机抽查 5 条 chunk metadata")
    print("=" * 60)
    
    # 初始化 ChromaDB 客户端
    client = chromadb.PersistentClient(
        path=settings.chroma_persist_dir,
        settings=chromadb.Settings(anonymized_telemetry=False),
    )
    
    collection = client.get_collection(settings.chroma_collection_kb)
    count = collection.count()
    print(f"\n📊 总条目数: {count}")
    
    # 获取所有条目
    all_items = collection.get()
    ids = all_items['ids']
    metadatas = all_items['metadatas']
    
    # 随机选择 5 条
    sample_indices = random.sample(range(len(ids)), min(5, len(ids)))
    
    print("\n📋 随机抽查 5 条 chunk metadata:")
    print("-" * 60)
    
    for i, idx in enumerate(sample_indices, 1):
        chunk_id = ids[idx]
        metadata = metadatas[idx]
        
        print(f"\n[{i}] Chunk ID: {chunk_id}")
        print(f"    entry_id: {metadata.get('entry_id', 'N/A')}")
        print(f"    chunk_index: {metadata.get('chunk_index', 'N/A')}")
        print(f"    chunk_total: {metadata.get('chunk_total', 'N/A')}")
        print(f"    category: {metadata.get('category', 'N/A')}")
        print(f"    title: {metadata.get('title', 'N/A')}")
        print(f"    audience: {metadata.get('audience', 'N/A')}")
        print(f"    status: {metadata.get('status', 'N/A')}")

if __name__ == "__main__":
    sample_chunks()
