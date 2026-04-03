---
task_id: "R4"
task_name: "A1 队列修复 + 候补条目分析"
parent_id: "KB-REPAIR"
phase: "kb-repair"
priority: "high"
status: "L2-pass"
depends_on: ["R2"]
done_criterion:
  - "A1 queue 7 行 kb_draft_id 更新为 0124~0130，status=rebuild_needed"
  - "5 个候补条目（queue_seq=8~12）CSV 字段未被修改"
  - "5 个候补条目均已分类为 UNIQUE（seq=10/11 合并决策已确认）"
progress_items: 12
progress_done: 12
executor: "sub-agent"
verifier_l1: "commander"
verifier_l2: "cascade"
created_at: "2026-04-03"
updated_at: "2026-04-03"
prompt_file: "docs/dev-guides/prompts/kb-repair/r4-a1-rebuild-analysis-prompt-2026-04-03.md"
report_file: "docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md"
---

# R4 — A1 队列修复 + 候补条目分析

**任务一**：重新分配 7 个 A1 缺失条目的 kb_draft_id（0124~0130），
标记为 rebuild_needed。

**任务二**：分析 5 个 candidate-pool 条目，确认归属类型（UNIQUE/DUPLICATE/UNCERTAIN）。
注：seq=10/11 为同文件名不同路径，已决策合并为一个 KB 条目。
