---
id: "p1a-kb-repair"
parent: "phase-1-data-foundation"
type: "feature"
status: "pending"
tier: "T2"
priority: "high"
risk: "high"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/"
  - "knowledge-base/raw/first-batch-processing/manifests/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "services/"
  - "apps/"
  - "knowledge-base/entries/奖助贷补/"
  - "knowledge-base/entries/心理与测评/"
  - "knowledge-base/entries/就业与毕业/"
  - "knowledge-base/entries/事务申请与审批/"
  - "knowledge-base/entries/竞赛与第二课堂/"
  - "knowledge-base/entries/入学与学籍/"
  - "knowledge-base/entries/证件与校园服务/"
  - "knowledge-base/entries/生活服务/"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"
  - "docs/dev-guides/r2-rename-execution-prompt-2026-04-03.md"
  - "docs/dev-guides/r3-queue-sync-prompt-2026-04-03.md"
  - "docs/dev-guides/r4-a1-rebuild-analysis-prompt-2026-04-03.md"
  - "docs/dev-guides/r5-a1-rebuild-exec-prompt-2026-04-03.md"
  - "docs/dev-guides/prompts/kb-repair/r5b-rex-parallel-dispatch-prompt-2026-04-03.md"

done_criteria:
  L0: "r2/r3/r4/r5/rex 五个子目录均存在 _report.md"
  L1: "r2 _report.md 记录重命名总数=21，A3 entry_id 更新=19，A2 跳过=2"
  L2: "r3 队列字段同步完成；r5 新建草稿文件数=7（KB-20260324-0124~0130）；知识库草稿目录无 0061~0100 编号文件"
  L3: "所有草稿 frontmatter material_id 归属与对应批次队列一致（Cascade L2 抽查 3 条确认）"

depends_on: []
created_at: "2026-04-04 01:43:00"

batches:
  - name: "batch-1"
    tasks: ["r2-file-rename"]
    parallel: false
    note: "高风险，单独执行。必须先收 STEP-PLAN 确认再放行"
  - name: "batch-2"
    tasks: ["r3-queue-sync", "r4-a1-rebuild-analysis"]
    parallel: true
    depends_on: "batch-1"
    note: "两者均只依赖 r2 完成，可并行发给不同子 agent"
  - name: "batch-3"
    tasks: ["r5-a1-rebuild-exec"]
    depends_on: "batch-2（仅 r4）"
  - name: "batch-4"
    tasks: ["rex-manual-review"]
    depends_on: "batch-3"
    note: "需人工判定，可能是阻塞点"
---

# p1a：知识库修复管道

> R2 → R3/R4 → R5 → REX 修复链执行完毕后，`first-batch-drafts/` 中的 90 条草稿编号正确、无冲突、material_id 归属清晰。

## 背景

R1-v3 provenance 分析已完成（只读验收通过）。现有执行提示词已就绪，覆盖完整修复链：
- **R2**：21 个文件重命名（0061~0081 → 新编号），同步 A3 文件 entry_id 字段
- **R3**：A3/A2 队列 CSV 字段同步（target_kb_id / kb_entry_id 更新）
- **R4**：A1 队列 12 行重分析（7 行 material_id 确认 + 5 行候补条目归属）
- **R5**：A1 队列 7 个草稿文件从源文件内容重建（编号 0124~0130）
- **REX**：剩余无法自动处理的条目，人工判定后处置

## 已知陷阱

- 每个子任务的执行提示词已在 `context_files` 中列出，执行时直接引用，不要重复写步骤
- R3 和 R4 可以并行给两个子 agent，但各自的 out_of_scope 不能交叉
- REX 条目中可能包含内容不足无法自动重建的项，需用户决策
- 整个修复链是 Phase 2 入库的前置条件，不能跳过
