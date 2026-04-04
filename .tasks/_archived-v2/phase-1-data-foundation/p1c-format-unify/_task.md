---
id: "p1c-format-unify"
parent: "phase-1-data-foundation"
type: "bugfix"
status: "done"
tier: "T3"
priority: "high"
risk: "low"
foundation: true

scope:
  - "knowledge-base/templates/knowledge-entry-template.md"
  - "temp/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "knowledge-base/entries/first-batch-drafts/"
  - "scripts/batch_ingest_kb.py"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "knowledge-base/templates/knowledge-entry-template.md"
  - "scripts/batch_ingest_kb.py"

done_criteria:
  L0: "knowledge-base/templates/knowledge-entry-template.md 使用 ## 标题格式；docs/test-reports/completion-reports/P1C-format-unify-report.md 存在"
  L1: "格式校验脚本 python -m py_compile 无错误"
  L2: "校验脚本扫描所有 first-batch-drafts/*.md，输出格式异常文件数=0（或列出异常文件清单）"
  L3: "batch_ingest_kb.py 的 extract_section 逻辑与 ## 格式匹配确认（代码审查）"

root_cause: "knowledge-entry-template.md 使用 h1(#) 标题，而实际 90 条草稿均使用 h2(##)；batch_ingest_kb.py 按 ## 提取，模板不一致造成新建条目格式混乱"
affected_modules:
  - "knowledge-base/templates/"
  - "scripts/batch_ingest_kb.py（间接影响）"

depends_on: []
created_at: "2026-04-04 01:43:00"
---

# p1c：条目格式统一

> `knowledge-entry-template.md` 已更新为 `##` 格式，格式校验脚本确认全部 90 条草稿格式一致。

## 背景

技术债 DEBT-02：`knowledge-entry-template.md` 使用 `#`（h1），实际 90 条草稿全部使用 `##`（h2）。
`batch_ingest_kb.py` 的 `extract_section` 逻辑按 `##` 提取，若新建条目用模板则会出现格式不匹配。

用户已确认：**以实际条目格式（`##`）为准**，更新模板。

## 执行步骤

1. 打开 `knowledge-base/templates/knowledge-entry-template.md`，将所有 `# ` 开头的标题改为 `## `
2. 写格式校验脚本 `temp/format_check.py`，扫描 `first-batch-drafts/`，检测使用 `# ` 而非 `## ` 的文件
3. 运行校验，输出结果到 `docs/test-reports/completion-reports/P1C-format-unify-report.md`
4. 若有异常文件，列出清单供后续处理（本任务不改草稿内容）

## 已知陷阱

- 只改模板文件，不改 90 条草稿（草稿格式已正确，不需要改）
- 校验脚本检测 frontmatter 之后的正文标题格式，注意跳过 frontmatter 的 `---` 块
- `batch_ingest_kb.py` 不在本任务改动范围（Phase 2 的 p2a 负责）
