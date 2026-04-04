# R4-A1 Rebuild Analysis 自检报告

## L0 验收
- **标准**: `docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md` 存在
- **结果**: ✅ 通过
- **证据路径**: `docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md`

## L1 验收
- **标准**: A1 队列 12 行中每行均有明确处置决定（`rebuild_needed` 或 `candidate_duplicate`）
- **结果**: ✅ 通过
- **证据路径**:
  - 报告内「12 行决策明细表」中 `decision` 列全部为 `rebuild_needed`，无其他值。
  - `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv` 中 queue_seq=1~7 及 8~12 的 `status` 与报告 `decision` 一致。

## L2 验收
- **标准**: 7 行有 material_id 的条目已标记新编号（KB-20260324-0124~0130）；5 行候补条目归属已明确
- **结果**: ✅ 通过
- **证据路径**:
  - CSV 中 queue_seq=1~6 对应 `kb_draft_id`=KB-20260324-0124~0129，queue_seq=7 对应 KB-20260324-0130，`status`=`rebuild_needed`。
  - CSV 中 queue_seq=8~12 经与 A1 batch2-materials 比对无重复，决策为 `rebuild_needed`，归属已明确。

## L3 验收
- **标准**: 报告中每条决定均有 `decision_reason`，无"看文件名猜归属"描述
- **结果**: ✅ 通过
- **证据路径**: 报告内 12 行决策明细表的 `decision_reason` 均已填写，7 条 material 行依据为"原编号被 A3 占用且草稿未生成"，5 条候补行依据为"在 A1 batch2-materials 中未检索到重复源文件/文件名"，无猜测性描述。