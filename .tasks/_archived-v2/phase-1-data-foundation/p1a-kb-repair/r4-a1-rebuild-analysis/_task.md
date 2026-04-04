---
id: "r4-a1-rebuild-analysis"
parent: "p1a-kb-repair"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv"
  - "docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md"
out_of_scope:
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv"
  - "knowledge-base/entries/"
  - "services/"
  - "apps/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/r4-a1-rebuild-analysis-prompt-2026-04-03.md"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv"
  - "knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v3.csv"

done_criteria:
  L0: "docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md 存在"
  L1: "A1 队列 12 行中每行均有明确处置决定（rebuild_needed 或 candidate_duplicate）"
  L2: "7 行有 material_id 的条目已标记新编号（KB-20260324-0124~0130）；5 行候补条目归属已明确"
  L3: "报告中每条决定均有 decision_reason，无'看文件名猜归属'描述"

depends_on: ["r2-file-rename"]
created_at: "2026-04-04 01:43:00"
---

# R4：A1 队列重建分析

> A1 队列 12 行的处置方案已明确：7 行需重建（编号 0124~0130），5 行候补条目归属已分析。

## 背景

A1 队列（奖助贷）中共 12 行 `kb_draft_id` 指向了已被占用的旧编号：
- **7 行有 material_id**（MAT-0024~0029, MAT-0055）：草稿从未生成，需从源文件重建（R5 执行）
- **5 行无 material_id**（候补池，queue_seq=8~12）：原编号被 A3 占用，需分析是否与现有条目重复

**执行方式**：将 `docs/dev-guides/r4-a1-rebuild-analysis-prompt-2026-04-03.md` 提示词投给子 agent。
R4 与 R3 可并行执行（操作文件不重叠）。

## 已知陷阱

- 5 行候补条目分析结果影响是否需要重建，不能跳过分析直接进 R5
- 禁止修改 A2/A3 队列
- 分析结果输出为报告文件，不直接重建草稿（重建由 R5 执行）
