---
id: "p3c-manual-qa"
parent: "phase-3-tuning"
type: "feature"
status: "done"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "knowledge-base/entries/first-batch-drafts/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "services/"
  - "apps/"
  - "scripts/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - ".tasks/_spec.yaml"
  - "knowledge-base/templates/knowledge-entry-template.md"

done_criteria:
  L0: "docs/test-reports/completion-reports/P3C-manual-qa-report.md 存在"
  L1: "报告中抽查条目数 ≥ 15，覆盖每个有条目的分类 ≥ 2 条"
  L2: "报告列出每条抽查的核对结论（正确 / 有误 / 待确认）"
  L3: "发现有误的条目已标记 status=needs_review 或直接修正，报告中有记录"

depends_on: ["phase-2-vectorize"]
created_at: "2026-04-04 01:43:00"
verified_by: "human"
owner: "用户（需人工参与，AI 无法判断学校政策正确性）"
---

# p3c：知识条目内容人工抽查

> 随机抽查 ≥15 条知识条目，与原始材料核对，发现错误的条目已修正或标记。

## 背景

90 条知识条目全部由 AI 从学校原始材料自动生成，内容可能存在：
- 政策细节过时或错误
- 关键步骤缺失
- 截止日期、联系方式等具体信息不准确

这类错误 AI 无法自行发现，必须由熟悉学校政策的人员对照原始材料核查。

**本任务 owner 是用户**，不阻塞 p3a/p3b 的 AI 执行，可并行进行。

## 执行步骤（用户操作）

1. 从 `knowledge-base/entries/first-batch-drafts/` 随机抽取 ≥15 条，覆盖每个分类 ≥2 条
2. 对照原始材料（`_references/数据库部分材料/` 或转换后的 markdown）逐条核对
3. 将核对结果记录在 `docs/test-reports/completion-reports/P3C-manual-qa-report.md`
4. 发现内容错误的条目：
   - 直接修正（若错误明确）
   - 或在 frontmatter 添加 `status: needs_review` + 备注（若不确定正确答案）

## 已知陷阱

- 重点关注：奖助贷金额/截止日期、审批流程步骤数、联系部门名称
- AI 生成的条目倾向于"听起来合理但细节有偏差"，不要因为语句通顺就认为内容正确
- 这是 RISK-01（知识库内容准确性）的直接缓解措施
