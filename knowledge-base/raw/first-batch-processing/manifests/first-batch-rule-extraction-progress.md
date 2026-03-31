# 首批规则抽取推进进展（P0）

## 当前状态

- 材料索引规模：62 份（原22 + 本轮扩量40）
- 转换日志：62 条（本轮新增40条，成功40，失败0）
- 规则抽取草案：63 条任务（`first-batch-rule-extraction-draft.csv`）
- 抽取主表：63 条（`first-batch-rule-extraction-master.csv`）
- 含复核主表：63 条（`first-batch-rule-extraction-master-with-review.csv`）
- 可入库规则：60 条（`first-batch-rule-extraction-ready.csv`）
- 复核队列：6 条（`first-batch-rule-extraction-review-queue.csv`）
- 条目草稿队列：60 条（`first-batch-entry-draft-queue.csv`）
- 条目草稿填充：60 条（`first-batch-entry-draft-fill-progress.csv`）
- 草稿文件：`knowledge-base/entries/first-batch-drafts/`（`KB-20260324-0001`~`0060` 共60份）

## 本轮扩量（B2/B3）

- 新增选材：40 份（优先覆盖入学与学籍、奖助贷补、就业与毕业、心理与测评、证件与校园服务、竞赛与第二课堂、事务申请与审批）
- 新增抽取：40 条（P1新增23条，P2新增17条）
- 新增 ready：38 条
- 新增人工复核：2 条（`P2-REX-0018`、`P2-REX-0019`）
- `P0-REX-0014` 继续维持 `manual_review`，未并入 ready 主链路

## 本轮新增产物

- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-p0-worksheet.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-progress.md`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-p1-worksheet.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-p2-worksheet.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-master.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-review-queue.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-review-result.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-ready.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-master-with-review.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-queue.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-drafting-next-steps.md`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-fill-progress.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch2-materials.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch2-rule-rows.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-new-ready.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-new-queue.csv`
- `knowledge-base/entries/first-batch-drafts/KB-20260324-0001.md`

## 抽取执行顺序建议

1. 入学与学籍（0001/0002/0003/0004）
2. 奖助贷补（0005/0006/0008）
3. 心理与测评（0009/0010/0011）
4. 证件与校园服务（0012）
5. 竞赛与第二课堂（0013/0014）
6. 就业与毕业（0015/0020）

## 人工复核重点

- `MAT-20260323-0014`：时效为“待确认”，抽取后需二次复核。
- 学生手册拆分出的 5 条问题：抽取时需分别引用对应章节证据，避免合并成大条目。
- 模板类材料（P2）：后续仅提炼稳定规则，不直接作为最终FAQ正文。

## 下一步

- 优先完成人工复核与放行决策：
  - `P0-REX-0014`（时效待确认，维持manual_review）
  - `P2-REX-0018`、`P2-REX-0019`（申请/承诺文书口径复核）
- 第4批继续扩量建议：再增 20~30 条，以 `A/B` 级通知与操作说明为主，优先补齐入学与学籍、就业与毕业的流程细则材料。
