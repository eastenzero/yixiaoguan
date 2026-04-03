---
task_id: "R2"
task_name: "文件重命名 + frontmatter 同步（21 文件）"
parent_id: "KB-REPAIR"
phase: "kb-repair"
priority: "high"
status: "L2-pass"
depends_on: ["R1"]
done_criterion:
  - "KB-0061~0081 旧文件已删除"
  - "KB-0101~0123 新文件已创建（21 个）"
  - "A3 文件（19 个）的 entry_id frontmatter 已更新"
  - "A2 文件（2 个）无 entry_id 字段（正常）"
  - "Cascade L2 抽查 3 个文件通过"
progress_items: 21
progress_done: 21
executor: "sub-agent"
verifier_l1: "commander"
verifier_l2: "cascade"
created_at: "2026-04-03"
updated_at: "2026-04-03"
prompt_file: "docs/dev-guides/prompts/kb-repair/r2-rename-execution-prompt-2026-04-03.md"
report_file: "docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md"
---

# R2 — 文件重命名 + frontmatter 同步

执行 R1-v3 方案中的 21 条 `rename` 操作：
- A3 文件（19 个）：重命名 + entry_id 更新
- A2 文件（2 个）：仅重命名
