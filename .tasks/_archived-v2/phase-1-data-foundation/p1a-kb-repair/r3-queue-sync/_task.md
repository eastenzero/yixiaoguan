---
id: "r3-queue-sync"
parent: "p1a-kb-repair"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv"
  - "docs/test-reports/completion-reports/BATCH-R3-queue-sync-report.md"
out_of_scope:
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv"
  - "knowledge-base/entries/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/r3-queue-sync-prompt-2026-04-03.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v3.csv"

done_criteria:
  L0: "docs/test-reports/completion-reports/BATCH-R3-queue-sync-report.md 存在"
  L1: "报告中 A3 queue 更新行数与 remap-plan-v3.csv 中 target_batch=BATCH-A3 的行数一致"
  L2: "A3 queue CSV 中 kb_entry_id 字段已从旧编号更新为新编号（0105~0123）；A2 queue target_kb_id 已更新（0101/0102）"
  L3: "随机抽查 3 行 A3 queue，kb_entry_id 与对应草稿文件名一致"

depends_on: ["r2-file-rename"]
created_at: "2026-04-04 01:43:00"
---

# R3：队列字段同步

> A3/A2 批次队列 CSV 中的 `kb_entry_id` / `target_kb_id` 字段已更新为 R2 重命名后的新编号。

## 背景

R2 完成后，草稿文件已重命名，但 A3/A2 队列 CSV 中的引用字段仍是旧编号。
R3 负责将队列字段与新文件名对齐，确保队列数据与磁盘文件一致。

**执行方式**：将 `docs/dev-guides/r3-queue-sync-prompt-2026-04-03.md` 中的提示词投给子 agent。

## 已知陷阱

- 禁止修改 A1 队列（batch-a1-award-aid-queue.csv），A1 由 R4 单独处理
- 只改队列 CSV 字段值，禁止改动草稿 .md 文件
- R3 与 R4 可并行执行（两者操作文件不重叠）
