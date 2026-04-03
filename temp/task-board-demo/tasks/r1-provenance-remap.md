---
task_id: "R1"
task_name: "来源溯源重映射方案（v3）"
parent_id: "KB-REPAIR"
phase: "kb-repair"
priority: "high"
status: "L2-pass"
depends_on: []
done_criterion:
  - "batch-r1-kb-id-remap-plan-v3.csv 存在，含 21 条 rename 记录"
  - "batch-r1-kb-draft-rebuild-needed-v3.csv 存在，含 7 条 A1 缺失 + 2 条 REX 记录"
  - "Cascade L2 签字通过"
progress_items: 1
progress_done: 1
executor: "sub-agent"
verifier_l1: "commander"
verifier_l2: "cascade"
created_at: "2026-04-03"
updated_at: "2026-04-03"
prompt_file: "docs/dev-guides/prompts/kb-repair/r1-v3-provenance-remap-prompt-2026-04-03.md"
report_file: "docs/test-reports/completion-reports/BATCH-R1-v3-provenance-remap-report.md"
---

# R1 — 来源溯源重映射方案（v3）

基于 `material_id` 校验 KB-0061~0081 的实际归属，
生成可执行重映射方案，区分"可直接 rename"与"需重建"两类。
