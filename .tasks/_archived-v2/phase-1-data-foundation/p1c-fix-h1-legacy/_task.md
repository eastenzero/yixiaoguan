---
id: "p1c-fix-h1-legacy"
parent: "phase-1-data-foundation"
type: "bugfix"
status: "done"
tier: "T3"
priority: "medium"
risk: "low"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0105.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0106.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0107.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0108.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0109.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0110.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0111.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0112.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0113.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0114.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0115.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0116.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0117.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0118.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0119.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0120.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0121.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0122.md"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0123.md"
  - "docs/test-reports/completion-reports/P1C-fix-h1-legacy-report.md"
out_of_scope:
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0001.md"
  - "knowledge-base/raw/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "knowledge-base/templates/knowledge-entry-template.md"
  - "docs/test-reports/completion-reports/P1C-format-unify-report.md"

done_criteria:
  L0: "docs/test-reports/completion-reports/P1C-fix-h1-legacy-report.md 存在"
  L1: "报告记录处理文件数=19，无 BLOCKED"
  L2: "对 KB-20260324-0105~0123 随机抽查 3 个文件，正文第一个标题行为 `## ` 开头，无 `# ` 开头的非 frontmatter 行"
  L3: "batch_ingest_kb.py 的 extract_section 不再因 h1 标题跳过章节内容（代码审查确认）"

root_cause: "R2 重命名时继承了旧批次的 h1 格式正文，p1c 格式校验已识别，本任务执行批量修复"
depends_on: ["r2-file-rename"]
created_at: "2026-04-04 02:28:00"
---

# p1c-fix-h1-legacy：修复 19 个遗留 h1 文件

> KB-20260324-0105~0123 共 19 个文件的正文第一个标题行已从 `# 标题` 改为 `## 标题`（或直接删除，因 frontmatter 已有 title 字段）。

## 背景

p1c 格式校验脚本发现这 19 个文件（全部为 R2 重命名后的 A3 批次文件）正文起始为 `# 标题`（h1）。
`batch_ingest_kb.py` 的 `extract_section` 函数按 `##` 提取章节内容，h1 标题行会被跳过，
导致 Phase 2 入库时这 19 条条目的第一个 heading 级别异常。

## 执行步骤

**【执行模式：强约束】**
1. 只能修改 scope 中列出的 19 个文件，不允许修改其他文件
2. 必须先输出 STEP-PLAN（列出全部 19 个文件的修改内容），等回复"继续"后再执行
3. 执行后输出 STEP-CHECK，抽查 3 个文件确认修改正确
4. 禁止改动 frontmatter（`---` 之间的部分）
5. 禁止改动正文中已有的 `##` 及以下级别标题
6. 如文件正文第一行本身就是 `## `，则该文件无需修改（跳过）

**具体操作**：对每个文件，将紧接 frontmatter 之后的 `# 标题文字` 行改为 `## 标题文字`。

**【固定回报模板】**
```
STEP-PLAN
- 目标文件数: 19
- 修改方式: 正文第一个 # 标题 → ## 标题
- 各文件预计操作清单（列出全部19个）:

STEP-EXECUTED
- 实际修改文件数:
- 跳过（本已为##）:

STEP-CHECK
- 校验1（抽查 0105 第一个标题行）:
- 校验2（抽查 0112 第一个标题行）:
- 校验3（抽查 0123 第一个标题行）:
- 校验4（是否有超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

## 已知陷阱

- 只改正文第一个 `# 标题` 行，如果文件中出现多个 `#` 开头的行，逐一核实是否是 h1 还是 `#` 注释
- KB-20260324-0123 的内容是"源文件待补充"的占位符，同样需要把 h1 改为 h2
- 禁止改动 frontmatter，即使发现 frontmatter 有其他问题也不要顺手改
