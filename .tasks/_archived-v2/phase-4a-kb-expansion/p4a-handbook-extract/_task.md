---
id: "p4a-handbook-extract"
parent: "phase-4a-kb-expansion"
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
  - "knowledge-base/raw/student-handbook-mineru/full.md"
  - "services/"
  - "apps/"
  - "scripts/batch_ingest_kb.py"
  - "knowledge-base/raw/first-batch-processing/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "knowledge-base/templates/knowledge-entry-template.md"
  - "knowledge-base/raw/student-handbook-mineru/full.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-b1-life-services-gap-analysis.csv"

done_criteria:
  L0: "≥10 个新建草稿文件存在于 first-batch-drafts/，编号从 KB-20260324-0138 起连续（r5 占用 0131~0135，REX keep-rename 占用 0136~0137）"
  L1: "每个新建文件 frontmatter 包含 entry_id、material_id、category='生活服务'、source 字段"
  L2: "新条目覆盖 ≥3 个生活服务主题（如缴费流程、校园卡补办、学生证补办）；docs/test-reports/completion-reports/P4A-handbook-extract-report.md 存在"
  L3: "抽查 3 条新条目，内容忠实于 full.md 对应章节，无 AI 补脑内容；source 字段指向具体章节"

depends_on: ["phase-2-vectorize"]
created_at: "2026-04-04 01:43:00"
note: "新建条目需要在 Phase 2 之后再次运行 batch_ingest_kb.py 才能进入 ChromaDB，本任务只负责创建 .md 文件"
---

# p4a：从学生手册提取生活服务条目

> 从 `full.md` 提取 ≥10 条生活服务类知识条目（编号 KB-20260324-0138 起），覆盖缴费流程、校园卡补办、学生证补办等学生手册已有章节。

## 背景

生活服务类当前 0 条（7 个 P0 缺口）。`full.md`（2148 行）已覆盖部分缺口：
- **八.学工办事流程**：校园卡补办、学生证补办、银行卡使用说明
- **十.学校各职能部门**：缴费流程事项、图书馆说明等

这些主题无需等待学校部门提供材料，可直接从手册提取。

Phase 4b（报修/水电/网络/宿舍）仍需学校部门材料，不在本任务范围内。

## 执行步骤

1. 阅读 `full.md`，定位相关章节
2. 对每个主题，提取关键信息，生成符合模板格式的条目
3. 新条目编号从 **KB-20260324-0138** 起续排（r5 占用 0124~0135，REX keep-rename 占用 0136~0137），不要跳号或重复
4. frontmatter 示例：
   ```yaml
   entry_id: KB-20260324-0138
   material_id: HANDBOOK-2026-001
   category: 生活服务
   title: 校园卡补办流程
   source: knowledge-base/raw/student-handbook-mineru/full.md § 八.学工办事流程-校园卡补办
   ```
5. 将新建条目清单写入 `docs/test-reports/completion-reports/P4A-handbook-extract-report.md`

## 已知陷阱

- **禁止 AI 补脑**：条目内容必须严格来自 full.md，不得推断或补充手册未提及的信息
- 新条目只写 .md 文件，不执行入库（入库在 Phase 2 完成后再运行 batch_ingest_kb.py）
- source 字段必须精确到章节，方便后续来源引用溯源
- 注意确认当前 first-batch-drafts/ 中最大编号，续排时不要跳号或重复
