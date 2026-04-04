---
id: "phase-4a-kb-expansion"
parent: ""
type: "feature"
status: "pending"
tier: "T1"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "knowledge-base/entries/first-batch-drafts/"
  - "knowledge-base/raw/student-handbook-mineru/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "services/"
  - "apps/"
  - "knowledge-base/raw/first-batch-processing/"
  - "scripts/batch_ingest_kb.py"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"
  - "knowledge-base/templates/knowledge-entry-template.md"
  - "knowledge-base/raw/student-handbook-mineru/full.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-b1-life-services-gap-analysis.csv"

done_criteria:
  L0: "p4a-handbook-extract/_report.md 存在；新建条目文件存在于 first-batch-drafts/"
  L1: "新建条目 frontmatter 包含 material_id、category、source 字段"
  L2: "新增生活服务类条目 ≥10 条（覆盖缴费流程、校园卡补办、学生证补办等学生手册已有章节）"
  L3: "抽查 3 条新条目，内容与 full.md 对应章节一致，无幻觉补脑"

depends_on: ["phase-2-vectorize"]
created_at: "2026-04-04 01:43:00"
note: "phase-4b（需学校部门材料的主题）单独阻塞等待，不在本任务树内"

batches:
  - name: "batch-7"
    tasks: ["p4a-handbook-extract"]
    parallel: true
    note: "可与 phase-3-tuning batch-7 同步并行，内容独立互不影响"
---

# Phase 4a：知识库扩量（学生手册）

> 从 `full.md` 提取生活服务类知识条目 ≥10 条，填补当前 0 条生活服务的关键缺口（LIFE-04 校园卡、缴费流程、学生证补办等）。

## 背景

生活服务类 7 个 P0 缺口中，部分已被学生手册覆盖（不依赖学校部门材料）：
- 缴费流程（十.学校各职能部门 — 缴费流程事项）
- 校园卡补办（八.学工办事流程 — 校园卡补办）
- 学生证补办（八.学工办事流程 — 学生证补办）
- 银行卡使用说明（十.学校各职能部门）

`full.md` 共 2148 行，已在 `knowledge-base/raw/student-handbook-mineru/` 就绪。

Phase 4b（报修/水电/网络/宿舍管理）依赖学校部门提供原始材料，暂不执行，单独阻塞等待。

## 已知陷阱

- 新条目编号从当前最大值（KB-20260324-0130）之后续排，不要复用已有编号
- 格式必须与现有条目一致（`##` 标题，frontmatter 含 material_id/category/source）
- source 字段填写 `knowledge-base/raw/student-handbook-mineru/full.md` + 对应章节标题
- 条目内容必须忠实于 full.md 原文，禁止 AI 补脑补充未提及的内容
