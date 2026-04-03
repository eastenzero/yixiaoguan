---
task_id: "B1-DISC"
task_name: "竞赛/评优新批次文件扫描建档"
parent_id: "KB-EXPANSION"
phase: "kb-expansion"
priority: "medium"
status: "pending"
depends_on: ["KB-REPAIR"]
done_criterion:
  - "batch-b1-competition-eval-queue.csv 已创建，列名与 batch-a1 一致"
  - "material_id 格式为 MAT-B1-XXXX，无重复"
  - "排除条目列表已记录（含排除原因）"
  - "转换需求评估已完成（是否需要补充 MinerU 转换）"
  - "Cascade L2 抽查 5 条分类通过"
progress_items: 1
progress_done: 0
executor: "sub-agent"
verifier_l1: "commander"
verifier_l2: "cascade"
created_at: "2026-04-03"
updated_at: "2026-04-03"
prompt_file: "docs/dev-guides/prompts/kb-expansion/batch-b1-competition-eval-discovery-prompt-2026-04-03.md"
report_file: "docs/test-reports/completion-reports/BATCH-B1-discovery-report.md"
---

# B1-DISC — 竞赛/评优新批次文件扫描建档

扫描 `_references/数据库部分材料/` 目录，
识别竞赛申报、评优评选、综合测评相关文档，
建立 `batch-b1-competition-eval-queue.csv`。
