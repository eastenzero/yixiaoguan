---
id: "phase-3-tuning"
parent: ""
type: "feature"
status: "pending"
tier: "T1"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/app/core/llm_chat.py"
  - "docs/test-reports/"
  - "knowledge-base/entries/first-batch-drafts/"
out_of_scope:
  - "apps/"
  - "services/business-api/"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/app/core/llm_chat.py"

done_criteria:
  L0: "p3a/p3b/p3c 子目录均存在 _report.md；评测集文件存在"
  L1: "评测脚本 python -m py_compile 无错误"
  L2: "评测集 Recall@5 ≥ 0.85；拒答准确率 ≥ 0.90"
  L3: "抽查 5 条边界问题（相关但信息不足），均返回友好拒答而非幻觉回答"

depends_on: ["phase-2-vectorize"]
created_at: "2026-04-04 01:43:00"

batches:
  - name: "batch-7"
    tasks: ["p3a-eval-set", "p3c-manual-qa"]
    parallel: true
    note: "p3a 由 AI 构建；p3c 由用户人工执行，互不阻塞"
  - name: "batch-8"
    tasks: ["p3b-threshold-tuning"]
    depends_on: "batch-7（仅 p3a）"
---

# Phase 3：检索质量调优

> 构建 ≥30 对黄金评测集，基于评测结果调优 RAG 阈值参数，Recall@5 ≥ 0.85，拒答准确率 ≥ 0.90。

## 背景

Phase 2 完成后 ChromaDB 已有正确的 chunk 向量。但 `config.py` 中的阈值参数（`rag_min_score`、
`rag_min_best_score`、`rag_min_avg_score`、`rag_min_source_count`）是在 90 条整条目库中设的，
chunk 拆分后需要重新校准。

p3c（人工抽查）与 p3a/p3b 并行，owner 是用户，不阻塞 AI 侧任务。

## 已知陷阱

- 评测集必须包含四类问题：应命中 / 应拒答 / 边界情况 / 生活服务（当前无覆盖，应拒答）
- 调参时不要只看 Recall，拒答准确率同样重要（防幻觉）
- 阈值改动后必须在评测集上跑完整验证，不能凭感觉调
