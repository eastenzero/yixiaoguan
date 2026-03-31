"""
知识库向量化脚本
读取 first-batch-entries.jsonl，调用 DashScope text-embedding-v3 生成向量，存入 ChromaDB。
"""

import json
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv

# ── 路径配置 ────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent.parent
SECRETS_ENV = ROOT / ".secrets" / ".env"
JSONL_PATH = ROOT / "knowledge-base" / "raw" / "first-batch-processing" / "converted" / "first-batch-entries.jsonl"
CHROMA_DIR = ROOT / "knowledge-base" / "raw" / "first-batch-processing" / "converted" / "chroma_db"

# ── 加载 API Key ─────────────────────────────────────────
load_dotenv(SECRETS_ENV)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    print("[错误] 未找到 DASHSCOPE_API_KEY，请检查 .secrets/.env")
    sys.exit(1)

import dashscope
from dashscope import TextEmbedding
import chromadb

dashscope.api_key = DASHSCOPE_API_KEY

# ── 参数配置 ────────────────────────────────────────────
EMBED_MODEL = "text-embedding-v3"
EMBED_DIM = 1024          # text-embedding-v3 支持 1024 / 1536 / 3072
BATCH_SIZE = 10           # DashScope text-embedding-v3 每次最多 10 条
COLLECTION_NAME = "kb_first_batch"

# ── 工具函数 ────────────────────────────────────────────

def load_entries(path: Path) -> list[dict]:
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    return entries


def embed_batch(texts: list[str], retry: int = 3) -> list[list[float]]:
    """调用 DashScope Embedding API，返回向量列表"""
    for attempt in range(retry):
        resp = TextEmbedding.call(
            model=EMBED_MODEL,
            input=texts,
            dimension=EMBED_DIM,
        )
        if resp.status_code == 200:
            # 按 text_index 排序确保顺序一致
            items = sorted(resp.output["embeddings"], key=lambda x: x["text_index"])
            return [item["embedding"] for item in items]
        else:
            print(f"  [警告] 第{attempt+1}次请求失败: {resp.code} {resp.message}")
            time.sleep(2)
    raise RuntimeError(f"Embedding 请求失败，已重试 {retry} 次")


def build_metadata(entry: dict) -> dict:
    """构造 ChromaDB metadata（只允许 str/int/float/bool）"""
    return {
        "title": entry.get("title", ""),
        "category": entry.get("category", ""),
        "audience": entry.get("audience", ""),
        "material_id": entry.get("material_id", ""),
        "rule_task_id": entry.get("rule_task_id", ""),
        "status": entry.get("status", "draft"),
    }


# ── 主流程 ──────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  医小管知识库向量化  (DashScope text-embedding-v3)")
    print("=" * 55)

    # 1. 加载条目
    entries = load_entries(JSONL_PATH)
    print(f"\n[1] 加载条目：{len(entries)} 条")

    # 2. 初始化 ChromaDB
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    # 若已存在同名集合则删除重建（支持重复运行）
    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        client.delete_collection(COLLECTION_NAME)
        print(f"[2] 已删除旧集合 '{COLLECTION_NAME}'，重建中…")
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )
    print(f"[2] ChromaDB 集合已创建：{COLLECTION_NAME}  存储路径：{CHROMA_DIR}")

    # 3. 批量 Embedding 并写入
    print(f"\n[3] 开始 Embedding（批大小={BATCH_SIZE}）…")
    total = len(entries)
    ids_all, docs_all, embeds_all, metas_all = [], [], [], []

    for i in range(0, total, BATCH_SIZE):
        batch = entries[i: i + BATCH_SIZE]
        batch_texts = [e.get("full_text", "") for e in batch]
        batch_ids = [e["entry_id"] for e in batch]

        print(f"  批次 {i//BATCH_SIZE + 1}：{batch_ids[0]} ~ {batch_ids[-1]}  ({len(batch)} 条) …", end=" ")
        t0 = time.time()
        embeddings = embed_batch(batch_texts)
        elapsed = time.time() - t0
        print(f"✅ ({elapsed:.1f}s)")

        ids_all.extend(batch_ids)
        docs_all.extend(batch_texts)
        embeds_all.extend(embeddings)
        metas_all.extend([build_metadata(e) for e in batch])

        time.sleep(0.3)  # 礼貌性限速

    # 4. 写入 ChromaDB
    collection.add(
        ids=ids_all,
        embeddings=embeds_all,
        documents=docs_all,
        metadatas=metas_all,
    )
    print(f"\n[4] 已写入 ChromaDB：{collection.count()} 条向量")

    # 5. 冒烟测试：用 3 条问题验证检索
    print("\n[5] 冒烟测试（Top-3 检索）…")
    smoke_queries = [
        "新生入学报到需要哪些材料？",
        "国家助学金如何申请？",
        "毕业生档案怎么转递？",
    ]
    for q in smoke_queries:
        q_embed = embed_batch([q])[0]
        results = collection.query(
            query_embeddings=[q_embed],
            n_results=3,
            include=["metadatas", "distances"],
        )
        print(f"\n  问：{q}")
        for j, (meta, dist) in enumerate(
            zip(results["metadatas"][0], results["distances"][0])
        ):
            sim = round(1 - dist, 4)
            print(f"    Top{j+1} [{sim:.4f}] {meta['title']}（{meta['category']}）")

    print("\n" + "=" * 55)
    print("  ✅ 向量化完成！ChromaDB 已就绪，可接入检索服务。")
    print("=" * 55)


if __name__ == "__main__":
    main()
