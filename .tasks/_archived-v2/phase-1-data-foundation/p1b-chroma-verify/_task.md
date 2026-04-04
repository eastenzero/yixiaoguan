---
id: "p1b-chroma-verify"
parent: "phase-1-data-foundation"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "low"
foundation: true

scope:
  - "scripts/"
  - "temp/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "services/ai-service/data/chroma/"
  - "knowledge-base/entries/"
  - "apps/"
  - "services/business-api/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - ".tasks/_spec.yaml"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/config.py"

done_criteria:
  L0: "docs/test-reports/completion-reports/P1B-chroma-verify-report.md 存在"
  L1: "验证脚本 python -m py_compile 无错误"
  L2: "报告输出 ChromaDB 实际 entry_id 列表；报告明确列出：多余条目 / 缺失条目 / 一致条目数量"
  L3: "若存在不一致，报告已说明处置建议（等 Phase 2 全量重入库时一并修复，或立即清理）"

depends_on: []
created_at: "2026-04-04 01:43:00"
note: "本任务仅做只读验证，不执行写操作。写操作（清空+重入库）在 Phase 2 执行。"
---

# p1b：ChromaDB 一致性验证

> 输出 ChromaDB `kb_entries` 集合的实际条目列表，与 `first-batch-drafts/*.md` 做 diff，报告差异项。

## 背景

ChromaDB `chroma.sqlite3` 约 3MB，有数据，但不确定：
1. 是否全部 90 条草稿都已入库
2. 向量内容是否与修复后的 `.md` 文件一致
3. 编号空洞（0061-0100）的旧向量是否残留

本任务写一个临时验证脚本（放 `temp/`，用完可删）查询 ChromaDB 并输出对比报告。

## 执行步骤

1. 写验证脚本 `temp/chroma_verify.py`，连接 ChromaDB `kb_entries` 集合，列出所有 `entry_id`
2. 与 `knowledge-base/entries/first-batch-drafts/` 中的文件名做 diff
3. 输出三列表：多余（ChromaDB 有但磁盘无）/ 缺失（磁盘有但 ChromaDB 无）/ 一致
4. 将结果写入 `docs/test-reports/completion-reports/P1B-chroma-verify-report.md`
5. 脚本可留存或清理（不强制，视情况）

## 已知陷阱

- ChromaDB 路径：`services/ai-service/data/chroma/`（bind mount），ai-service 容器须启动或直接用 Python 访问
- 本任务不执行清空或重入库，只验证并报告
- 如 ai-service 未启动，可用 `chromadb` Python 包直接读取本地路径
