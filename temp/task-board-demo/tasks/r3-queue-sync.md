---
task_id: "R3"
task_name: "队列字段同步（A3×19 + A2×21）"
parent_id: "KB-REPAIR"
phase: "kb-repair"
priority: "high"
status: "L2-pass"
depends_on: ["R2"]
done_criterion:
  - "A3 queue 的 kb_entry_id 全部更新至 KB-0105~0123 范围"
  - "A2 queue 的 MAT-0126/0127 target_kb_id 更新为 0101/0102"
  - "KB-REX-0001/0002 对应行未被修改"
  - "A2 queue 无任何行的 target_kb_id 落在 0061~0081 范围"
progress_items: 40
progress_done: 40
executor: "sub-agent"
verifier_l1: "commander"
verifier_l2: "cascade"
created_at: "2026-04-03"
updated_at: "2026-04-03"
prompt_file: "docs/dev-guides/prompts/kb-repair/r3-queue-sync-prompt-2026-04-03.md"
report_file: "docs/test-reports/completion-reports/BATCH-R3-queue-sync-report.md"
---

# R3 — 队列字段同步

将 A3 queue 的 `kb_entry_id` 和 A2 queue 的 `target_kb_id`
从旧编号（0061~0081）更新为新编号（0082~0123），
同时保护 KB-REX-0001/0002 和 A1 queue 不被修改。
