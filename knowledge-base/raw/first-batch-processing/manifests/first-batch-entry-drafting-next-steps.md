# 首批知识条目草稿阶段执行说明

## 输入清单

- 规则主表：`first-batch-rule-extraction-master-with-review.csv`
- 可入库规则：`first-batch-rule-extraction-ready.csv`（22条）
- 草稿队列：`first-batch-entry-draft-queue.csv`（22条，`draft_status=pending_draft`）
- 复核结论：`first-batch-rule-extraction-review-result.csv`

## 起稿原则

- 仅以 `ready` 清单进入知识条目草稿阶段。
- `需持续复核` 项（当前为 `P0-REX-0014`）不进入正式答复正文。
- 模板平行版本（P2）作为规则补充证据，不单独扩写重复FAQ。
- 政策时效项需保留“按年度公告为准”口径。

## 建议执行顺序

1. 入学与学籍（高频流程型）
2. 奖助贷补（系统操作型）
3. 心理与测评（问题处理型）
4. 就业与毕业（时点政策型）
5. 证件与校园服务、第二课堂（补充型）

## 每条草稿建议结构

- 问题
- 适用对象
- 办理条件
- 所需材料
- 办理流程
- 时间节点
- 注意事项
- 依据与证据

## 当前状态

- 规则抽取：完成
- 复核分流：完成
- 草稿队列：已生成，可直接按队列起稿
