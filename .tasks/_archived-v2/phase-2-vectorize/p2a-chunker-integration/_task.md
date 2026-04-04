---
id: "p2a-chunker-integration"
parent: "phase-2-vectorize"
type: "bugfix"
status: "done"
tier: "T3"
priority: "high"
risk: "high"
foundation: true

scope:
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/app/core/kb_vectorize.py"
out_of_scope:
  - "services/ai-service/app/api/"
  - "services/ai-service/app/core/llm_chat.py"
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/data/chroma/"
  - "apps/"
  - "services/business-api/"
  - "knowledge-base/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/app/core/kb_vectorize.py"
  - ".tasks/_spec.yaml"

done_criteria:
  L0: "batch_ingest_kb.py 中存在对 chunker.py MarkdownTextSplitter 的 import"
  L1: "python -m py_compile scripts/batch_ingest_kb.py 无错误；python -m py_compile services/ai-service/app/core/chunker.py 无错误"
  L2: "对单条草稿文件跑入库逻辑，ChromaDB 中生成 ≥1 个 ID 格式为 {entry_id}__chunk_{index} 的记录"
  L3: "长条目（如奖助贷类）拆分后有 >1 个 chunk；短条目（纯问答类）保持 1 个 chunk；metadata 包含 entry_id、chunk_index、category 字段"

root_cause: "chunker.py 的 MarkdownTextSplitter 写了 300 行但 batch_ingest_kb.py 完全未引用，长条目作为整体向量严重降低检索精度（DEBT-01）"
affected_modules:
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
regression_test: "单条草稿入库后，ChromaDB 中 chunk 数量 > 0，ID 格式正确"

depends_on: ["phase-1-data-foundation"]
created_at: "2026-04-04 01:43:00"
---

# p2a：Chunker 接入入库流程

> `batch_ingest_kb.py` 已引用 `chunker.py` 的 `MarkdownTextSplitter`，单条草稿入库后生成 1~N 个 chunk，ID 格式为 `{entry_id}__chunk_{index}`。

## 背景

技术债 DEBT-01：`chunker.py` 写了 300 行但未被引用。当前入库是整条目拼一大段文本作为单向量，
长条目（如 2000 字的奖助贷政策）检索时精度极低。

改造后：按 `##` heading 切分，大段再按字数切，每 chunk 独立入库携带完整 metadata。

## 执行步骤

1. 阅读 `chunker.py` 了解 `MarkdownTextSplitter` 接口（`split(text)` → `List[str]`）
2. 修改 `batch_ingest_kb.py`：
   - import `MarkdownTextSplitter`
   - 入库前对条目文本调用 `splitter.split(text)`
   - 循环为每个 chunk 生成 `{entry_id}__chunk_{index}` ID
   - 清理旧的整条目向量逻辑
3. 保持 metadata 字段完整（entry_id、chunk_index、category、title 等）
4. 本地测试：对 1 条草稿跑入库，验证 ChromaDB 中 chunk ID 格式正确

## 已知陷阱

- 全量清空 + 重入库在 p2b 执行，本任务只做代码改造和单条验证
- 改造前先完整阅读 chunker.py，不要重写已有逻辑
- 旧的整条目 ID 格式（无 `__chunk_` 后缀）在 p2b 清空时会一并清除，不需要单独处理
- kb_vectorize.py 如果也有入库逻辑，需要同步更新
