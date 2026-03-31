# 首批规则抽取与草稿阶段交付索引

## 1) 规则抽取主链路

- 草案源：`first-batch-rule-extraction-draft.csv`
- P0工作表：`first-batch-rule-extraction-p0-worksheet.csv`
- P1工作表：`first-batch-rule-extraction-p1-worksheet.csv`
- P2工作表：`first-batch-rule-extraction-p2-worksheet.csv`
- 主表：`first-batch-rule-extraction-master.csv`
- 含复核结果主表：`first-batch-rule-extraction-master-with-review.csv`
- 可入库清单：`first-batch-rule-extraction-ready.csv`

## 2) 复核链路

- 复核队列：`first-batch-rule-extraction-review-queue.csv`
- 复核结论：`first-batch-rule-extraction-review-result.csv`
- 下一轮复核优先级：`first-batch-next-review-priority.csv`
- P0-0014问询包：`p0-rex-0014-review-question-pack.md`

## 3) 知识条目草稿链路

- 草稿队列：`first-batch-entry-draft-queue.csv`
- 草稿执行说明：`first-batch-entry-drafting-next-steps.md`
- 草稿填充进展：`first-batch-entry-draft-fill-progress.csv`
- 草稿目录：`knowledge-base/entries/first-batch-drafts/`

## 4) 当前完成度

- 规则抽取：23/23 完成
- 复核分流：完成（重点复核4项）
- 可入库规则：22/23
- 草稿骨架：22/22 已创建
- 草稿填充：22/22 已填充

## 5) 下一步建议

1. 发出 `p0-rex-0014-review-question-pack.md` 做业务确认。
2. 复核 `first-batch-next-review-priority.csv` 的 4 项并回写结论。
3. 复核通过后将 P0-0014 补入 `ready` 与草稿队列。
4. 进入知识条目润色（统一语气、统一证据引用格式）。
