#!/usr/bin/env python3
"""
清空 ChromaDB kb_entries 集合
用于全量重入库前的清理
"""

import os
import sys
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

def clear_collection():
    """清空 kb_entries 集合"""
    print("=" * 60)
    print("清空 ChromaDB kb_entries 集合")
    print("=" * 60)
    
    print(f"\n📁 ChromaDB 目录: {settings.chroma_persist_dir}")
    print(f"📚 集合名称: {settings.chroma_collection_kb}")
    
    # 初始化 ChromaDB 客户端
    client = chromadb.PersistentClient(
        path=settings.chroma_persist_dir,
        settings=chromadb.Settings(anonymized_telemetry=False),
    )
    
    # 检查集合是否存在
    try:
        collection = client.get_collection(settings.chroma_collection_kb)
        count_before = collection.count()
        print(f"\n📊 当前集合条目数: {count_before}")
        
        # 删除集合并重建
        client.delete_collection(settings.chroma_collection_kb)
        print("✅ 已删除旧集合")
        
        # 重新创建空集合
        new_collection = client.create_collection(
            name=settings.chroma_collection_kb,
            metadata={"description": "医小管知识库条目向量存储", "dimension": 1024},
        )
        count_after = new_collection.count()
        print(f"✅ 已创建新空集合，条目数: {count_after}")
        
        return True
        
    except Exception as e:
        if "does not exist" in str(e).lower() or "not found" in str(e).lower():
            # 集合不存在，直接创建
            print(f"\n⚠️  集合不存在，创建新集合...")
            new_collection = client.create_collection(
                name=settings.chroma_collection_kb,
                metadata={"description": "医小管知识库条目向量存储", "dimension": 1024},
            )
            print("✅ 已创建新空集合")
            return True
        else:
            print(f"❌ 错误: {e}")
            return False

if __name__ == "__main__":
    success = clear_collection()
    sys.exit(0 if success else 1)
