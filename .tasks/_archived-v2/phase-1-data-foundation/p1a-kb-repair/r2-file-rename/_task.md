---
id: "r2-file-rename"
parent: "p1a-kb-repair"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "high"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0061.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0062.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0063.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0064.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0065.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0066.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0067.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0068.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0069.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0070.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0071.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0072.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0073.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0074.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0075.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0076.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0077.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0078.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0079.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0080.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0081.md"
  - "docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md"
out_of_scope:
  - "knowledge-base/raw/first-batch-processing/manifests/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/r2-rename-execution-prompt-2026-04-03.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v3.csv"

done_criteria:
  L0: "docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md 存在"
  L1: "报告中记录重命名总数=21，无 BLOCKED"
  L2: "旧编号文件 KB-20260324-0061~0081 均不存在；A3 文件 entry_id 已更新（抽查 3 条）；A2 文件（0101/0102）frontmatter 无 entry_id 字段"
  L3: "Cascade L2 签字：抽查 3 个 A3 文件 entry_id 正确，A2 文件 frontmatter 未被改动"

depends_on: []
created_at: "2026-04-04 01:43:00"
verified_by: "cascade-l2"
---

# R2：草稿文件重命名

> `KB-20260324-0061~0081` 的 21 个文件已按 `remap-plan-v3.csv` 重命名完毕，A3 文件 `entry_id` 字段已同步更新。

## 背景

R1-v3 provenance 分析已确认 21 条重命名映射的正确性（Cascade L2 已授权）。
这是 KB 修复管道的入口，R3/R4 均依赖本任务完成后才能执行。

**执行方式**：将 `docs/dev-guides/r2-rename-execution-prompt-2026-04-03.md` 中的"通用前置 + 子 agent Prompt"投给执行 AI，先收 STEP-PLAN 确认后再放行执行。

## 已知陷阱

- 执行前必须先收 STEP-PLAN，确认子 agent 列出了全部 21 条映射再放行
- 如果某个源文件不存在，子 agent 应输出 BLOCKED 并停止，不得跳过继续
- 禁止改动 frontmatter 中的 material_id、title、source 等字段（只改 entry_id）
- A2 文件（0080→0101，0081→0102）无 entry_id 字段，只改文件名，跳过 frontmatter 更新
