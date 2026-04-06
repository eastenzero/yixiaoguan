---
id: "v4-kb-deploy"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

batches:
  - name: "batch-1"
    tasks: ["task1-kb-ingest", "task3-temp-cleanup"]
    parallel: true
  - name: "batch-2"
    tasks: ["task2-e2e-verify"]
    depends_on: "batch-1"
---

# V4 KB 部署与验收

> spec-v4-student-enhancement 代码层面已全部合入 main。本任务树负责剩余运维与验收工作：将22条新KB文件入库 ChromaDB，并进行端到端 AI 回答验证。

## 背景

T0 外科手术修复后（commit c88959d），22条新KB文件（KB-0150~KB-0171）已存在于
`knowledge-base/raw/first-batch-processing/converted/markdown/` 但**从未被 batch_ingest_kb.py 扫到**（脚本只扫 `entries/first-batch-drafts/`）。

当前 ChromaDB 状态：102个文件已入库，entry_count=1059 chunks。

## 批次编排

- **batch-1**（并行）：task1-kb-ingest + task3-temp-cleanup（无文件冲突）
- **batch-2**（串行）：task2-e2e-verify（依赖 batch-1 中 task1 完成）

## 已知陷阱

- batch_ingest_kb.py 使用 `upsert`，重入库已有条目无副作用，可安全全量重跑
- 165服务器无 git，通过 Mutagen 同步，文件需在Windows端移动后等 Mutagen 同步
- ai-service 须先停后起，避免 ChromaDB 写冲突
