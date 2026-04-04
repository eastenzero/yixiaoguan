---
id: "p3b-threshold-tuning"
parent: "phase-3-tuning"
type: "bugfix"
status: "done"
tier: "T3"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/app/core/llm_chat.py"
  - "temp/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/data/chroma/"
  - "apps/"
  - "services/business-api/"
  - "knowledge-base/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/app/core/llm_chat.py"
  - "docs/test-reports/eval-set-v1.yaml"

done_criteria:
  L0: "docs/test-reports/completion-reports/P3B-threshold-tuning-report.md 存在；config.py 参数已修改"
  L1: "python -m py_compile services/ai-service/app/core/config.py 无错误"
  L2: "在评测集上跑完整验证：Recall@5 ≥ 0.85；拒答准确率 ≥ 0.90"
  L3: "抽查 5 条边界情况问题，均返回友好拒答而非幻觉内容；调参前后 Recall 和拒答率的对比记录在报告中"

root_cause: "config.py 中的 RAG 阈值参数（rag_min_score 等）在 90 条整条目库中设定，chunk 拆分后检索分布改变，原参数可能过严或过松"
affected_modules:
  - "services/ai-service/app/core/config.py"
  - "services/ai-service/app/core/llm_chat.py"

depends_on: ["p3a-eval-set"]
created_at: "2026-04-04 01:43:00"
---

# p3b：RAG 阈值调参

> 基于评测集调优后，`config.py` 中的 RAG 参数使 Recall@5 ≥ 0.85，拒答准确率 ≥ 0.90。

## 背景

需调优的参数（`services/ai-service/app/core/config.py`）：
- `rag_min_score`：单 chunk 最低相似度阈值
- `rag_min_best_score`：最高分 chunk 的最低阈值（当前 0.62）
- `rag_min_avg_score`：平均分阈值
- `rag_min_source_count`：最少来源条目数（当前 2）

chunk 拆分后，每个问题会检索到更多候选 chunk（同一条目的多个 chunk），
`rag_min_source_count=2` 的逻辑需要重新评估（chunk 和 entry 是不同粒度）。

## 执行步骤

1. 先阅读 `llm_chat.py` 中如何使用这些阈值参数（门控逻辑）
2. 用评测集跑基线测试，记录当前参数下的 Recall@5 和拒答率
3. 按以下顺序逐步调整：先调 `rag_min_best_score`，再调 `rag_min_source_count`，最后微调其余
4. 每轮调整后跑评测集验证，达标后停止
5. 将调参过程和最终参数记录在报告中

## 已知陷阱

- 不能只看 Recall，拒答准确率同等重要（防幻觉是核心目标）
- `rag_min_source_count` 的语义在 chunk 模式下需要重新定义（是 chunk 数还是 entry 数）
- 参数调整要有记录，不能无文档地改
- 不要因为某几个测试用例失败就过度调宽阈值（会引入幻觉）
