---
id: "phase-2-vectorize"
parent: ""
type: "feature"
status: "pending"
tier: "T1"
priority: "high"
risk: "high"
foundation: true

scope:
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/app/core/kb_vectorize.py"
  - "services/ai-service/data/chroma/"
  - "knowledge-base/templates/knowledge-entry-template.md"
out_of_scope:
  - "apps/"
  - "services/business-api/"
  - "knowledge-base/entries/first-batch-drafts/"
  - "services/ai-service/app/api/"
  - "services/ai-service/app/core/llm_chat.py"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"
  - "services/ai-service/app/core/chunker.py"
  - "scripts/batch_ingest_kb.py"

done_criteria:
  L0: "p2a/p2b 子目录均存在 _report.md"
  L1: "python -m py_compile scripts/batch_ingest_kb.py 无错误"
  L2: "ChromaDB kb_entries 集合条目数 > 90（chunk 拆分后）；API GET /kb/stats 返回正确统计"
  L3: "抽查 5 条 chunk，metadata 包含正确 entry_id、chunk_index、category 字段"

depends_on: ["phase-1-data-foundation"]
created_at: "2026-04-04 01:43:00"

batches:
  - name: "batch-5"
    tasks: ["p2a-chunker-integration"]
    parallel: false
  - name: "batch-6"
    tasks: ["p2b-full-reingest"]
    depends_on: "batch-5"
---

# Phase 2：向量化入库管道

> `chunker.py` 已接入 `batch_ingest_kb.py`，ChromaDB 已全量重入库，条目数 > 90（每条按 heading 切分为 1~N 个 chunk）。

## 背景

技术债 DEBT-01：`chunker.py` 写了 300 行 `MarkdownTextSplitter` 但 `batch_ingest_kb.py` 完全未引用。
当前入库方式是将整条目拼成一大段文本入库，长条目作为单个向量严重降低检索精度。

Phase 1 完成后，KB 草稿文件已正确就位，可以执行全量清空 + 重新入库。

## 已知陷阱

- 执行 p2a 前务必确认 Phase 1 全部完成（特别是 p1c 格式统一），否则 extract_section 逻辑可能提取失败
- 全量清空 ChromaDB 之前必须确认没有其他进程正在读写（停掉 ai-service 容器）
- chunk ID 格式必须统一为 `{entry_id}__chunk_{index}`，避免与旧向量 ID 冲突
