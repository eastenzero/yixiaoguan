---
id: "r5-a1-rebuild-exec"
parent: "p1a-kb-repair"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0124.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0125.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0126.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0127.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0128.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0129.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0130.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0131.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0132.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0133.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0134.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0135.md"
  - "docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md"
out_of_scope:
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0001.md"
  - "knowledge-base/raw/first-batch-processing/manifests/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/r5-a1-rebuild-exec-prompt-2026-04-03.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv"
  - "knowledge-base/templates/knowledge-entry-template.md"

done_criteria:
  L0: "BATCH-R5-a1-rebuild-exec-report.md 存在；报告中实际新建文件数 + BLOCKED 数 = 12"
  L1: "所有成功新建的文件 frontmatter 包含 entry_id、category、source 字段（queue_seq 8~12 无 material_id 的条目允许 material_id 留空）"
  L2: "queue_seq 1~7（KB-20260324-0124~0130）全部新建或 BLOCKED 有说明；queue_seq 8~12（KB-20260324-0131~0135）各有处置结果"
  L3: "抽查 2 个 queue_seq 1~7 的新建文件，内容与对应 material_id 源材料主题一致；queue_seq 10&11（同文件名不同路径）处置一致性说明"

depends_on: ["r4-a1-rebuild-analysis"]
created_at: "2026-04-04 01:43:00"
---

# R5：A1 草稿文件重建（范围已更新：12 文件）

> A1 队列 12 行中，成功重建的条目已在 `first-batch-drafts/` 生成对应 `.md` 文件；BLOCKED 的条目在报告中有明确说明。

## 背景

R4 最终结论：**rebuild_needed=12**（非预期的 7，原因是 5 条候补条目 queue_seq 8~12 均无匹配现有条目）。

文件 ID 分配：
- **queue_seq 1~7**（有 material_id）：KB-20260324-0124~0130，源文件为 `converted/markdown/MAT-20260324-0024~0029、0055`
- **queue_seq 8~12**（无 material_id）：KB-20260324-0131~0135，源文件为原始 DOC/PDF，**可能不在 converted/markdown/ 中**

**执行方式**：将 `docs/dev-guides/r5-a1-rebuild-exec-prompt-2026-04-03.md` 提示词投给子 agent，并附上本任务文件说明范围扩充。

## ⚠️ 高风险提示（T1 注入）

1. **queue_seq 8~12 高 BLOCKED 风险**：源文件为附件表格（申请表、承诺书、弃权声明），原始文档可能未经 MinerU 转换，converted/markdown/ 中可能不存在。子 agent 遇到 BLOCKED 时继续处理其余条目，不要整体停止。

2. **queue_seq 10 与 11 同文件名异路径**：两行均为 `贫困认定弃权声明 (2).docx`，路径不同。若内容一致，可只建一个文件并在报告中注明 queue_seq 11 合并至 0133；若内容不同，分别建 0133/0134。子 agent 必须在 STEP-PLAN 中说明处置方案。

3. **p4a 编号影响**：本任务新建文件最多至 KB-20260324-0135，`p4a-handbook-extract` 的起始编号已相应调整为 **0136**。

## 已知陷阱

- 若某条目源文件找不到，输出 BLOCKED（单条），继续处理其余条目
- 禁止修改已存在的草稿文件
- 新建文件格式使用 `##` 标题，frontmatter 参考 knowledge-entry-template.md
- entry_id 字段值必须与文件名对应（`entry_id: KB-20260324-0131` 等）
- queue_seq 8~12 的条目无 material_id，frontmatter 中该字段可留空或省略
