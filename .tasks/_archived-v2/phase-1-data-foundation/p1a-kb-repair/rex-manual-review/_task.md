---
id: "rex-manual-review"
parent: "p1a-kb-repair"
type: "feature"
status: "done"
tier: "T3"
priority: "medium"
risk: "medium"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/KB-REX-0001.md"
  - "knowledge-base/entries/first-batch-drafts/KB-REX-0002.md"
  - "docs/test-reports/completion-reports/BATCH-REX-manual-review-report.md"
out_of_scope:
  - "knowledge-base/raw/first-batch-processing/manifests/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/prompts/kb-repair/r5b-rex-parallel-dispatch-prompt-2026-04-03.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v3.csv"
  - "docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md"

done_criteria:
  L0: "docs/test-reports/completion-reports/BATCH-REX-manual-review-report.md 存在"
  L1: "报告中 KB-REX-0001/0002 各有处置决定（keep-rename / archive），含 decision_reason；queue_seq 8~12 各有处置决定（skip / pending-source）"
  L2: "若 keep-rename：KB-REX 条目已重命名为正式编号（KB-20260324-XXXX）；若 archive/skip：报告注明原因"
  L3: "用户确认 KB-REX-0001/0002 的处置合理；queue_seq 8~12 的最终决定（跳过/待补全源文件）符合项目知识库方向"

depends_on: ["r5-a1-rebuild-exec"]
created_at: "2026-04-04 01:43:00"
verified_by: "human"
---

# REX：残余条目人工处置

> 所有 REX 条目及 r5 遗留的 queue_seq 8~12 条目已逐条处置，结果有据可查。

## 背景

本任务合并处置两类遗留项：

### Part A：原始 REX 条目（2 条）

| entry_id | title | 当前状态 |
|----------|-------|---------|
| KB-REX-0001 | 团员组织关系介绍信参考模板 | 有内容，entry_id 非标准格式 |
| KB-REX-0002 | 在读或预毕业证明中英文模板（外合部） | 有内容，entry_id 非标准格式 |

**决策选项**：
- `keep-rename`：内容有效，重命名为正式编号（KB-20260324-0136 起，p4a 相应后移）
- `archive`：内容与已有条目重复或不适合入库，归档不入 Chroma

### Part B：r5 遗留的 queue_seq 8~12（5 条，均源文件缺失）

| queue_seq | 源文件（原始 DOC/PDF） | 性质 |
|-----------|----------------------|------|
| 8 | 附件1：山东省高等教育资助申请表.doc | 空白申请表 |
| 9 | 附件3：个人承诺书.pdf | 承诺书表格 |
| 10 | 贫困认定弃权声明 (2).docx（路径A） | 弃权声明表格 |
| 11 | 贫困认定弃权声明 (2).docx（路径B） | 同名异路径 |
| 12 | 附件2：勤工助学申请表.doc | 空白申请表 |

**决策选项**：
- `skip`：空白表格，知识价值低，不入库
- `pending-source`：有价值但需等待源文件转换，记录待办

**执行方式**：参考 `docs/dev-guides/prompts/kb-repair/r5b-rex-parallel-dispatch-prompt-2026-04-03.md`，
由用户和 AI 协作逐条审查，决策后记录在报告文件中。

## 已知陷阱

- REX 条目的处置决定必须有 decision_reason，不能仅写 keep-rename/skip 而没有说明
- 若 KB-REX-0001/0002 选 keep-rename，需通知 T1 更新 p4a 的起始编号（当前 0136，可能需后移至 0138）
- 这是 p1a 修复管道的最后一步，也是潜在阻塞点（依赖用户参与）
