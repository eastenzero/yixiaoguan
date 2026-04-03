# 知识库修复 P1 单任务提示词包（2026-04-03）

> 用途：在 R1(P0) 修复进行中，同步处理非阻塞问题。  
> 要求：每个 Prompt 只做 1 件事，先计划后执行，固定输出。

---

## 通用前置（每个 Prompt 前都加）

```markdown
【执行模式：强约束】
1) 只能做我指定的单一任务。
2) 只能修改“允许修改文件列表”中的文件。
3) 先输出 STEP-PLAN，等我回复“继续”后再执行。
4) 执行后必须输出 STEP-CHECK（文件存在、修改条数、是否越界修改）。
5) 信息不足时写 BLOCKED，不允许猜测。
6) 禁止修改 `services/`、`apps/` 下任何代码。

【固定回报模板】
STEP-PLAN
- 目标文件:
- 预计修改:
- 风险点:

STEP-EXECUTED
- 实际修改文件:
- 实际修改条目数:

STEP-CHECK
- 校验1（文件存在）:
- 校验2（关键字段/文案）:
- 校验3（是否超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## Prompt-P1-01（修复 SUMMARY-v2 的 QA 旧状态文案）

```markdown
你是“修复文档状态口径工程师”。

【任务目标】
仅修复 `KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md` 中“QA待生成”旧文案，改为与当前实物一致的“已生成”。

【输入文件】
1. `docs/test-reports/completion-reports/KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist.csv`
3. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-manual-review-list.csv`
4. `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`

【允许修改文件列表】
1. `docs/test-reports/completion-reports/KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md`
2. `docs/test-reports/completion-reports/BATCH-P1-01-summary-v2-status-fix-report.md`

【强制修改点】
- 仅改“BATCH-QA 待补充交付物”段落状态：`待生成 -> 已生成`
- 仅改“验收结果”中的“质检收口”状态：`待完成 -> 已完成`
- 禁止改动任何统计数字

【完成标准】
- 两处状态文案修正完成
- 报告文件说明“修改前后对照”
```

---

## Prompt-P1-02（统一编号策略口径到 A3=0105 起）

```markdown
你是“编号策略口径修订工程师”。

【任务目标】
仅修订 `BATCH-QA-completion-report.md` 中与编号策略不一致的建议文案，使其与 R1 方案一致：A2 从 0082 起，A3 从 0105 起。

【输入文件】
1. `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan.csv`
3. `docs/test-reports/completion-reports/BATCH-R1-id-remap-plan-report.md`

【允许修改文件列表】
1. `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`
2. `docs/test-reports/completion-reports/BATCH-P1-02-numbering-policy-fix-report.md`

【强制修改点】
- 只改“待决策事项”里编号建议口径不一致的句子
- 统一为：A2 从 `KB-0082` 起，A3 从 `KB-0105` 起
- 不改动其他分类统计与结论

【完成标准】
- 文档内不再出现 `A3 从 KB-0100 起` 的口径
- 报告文件包含“旧文案 -> 新文案”对照
```

---

## Prompt-P1-03（明确 whitelist 语义边界）

```markdown
你是“QA清单语义规范工程师”。

【任务目标】
新增一份 whitelist 使用说明，明确它是“可入库候选清单（含已知非结构性问题）”，避免执行误读。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-manual-review-list.csv`
3. `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist-usage-note.md`
2. `docs/test-reports/completion-reports/BATCH-P1-03-whitelist-semantics-report.md`

【说明文档必须包含】
- whitelist 定义
- manual-review 定义
- 两者边界（哪些问题可进 whitelist，哪些必须进 manual）
- 执行人员注意事项（先看 manual 再入库）
- 与当前 CSV 的对应关系

【禁止事项】
- 禁止改动两个 CSV 的内容
- 禁止修改历史报告文件

【完成标准】
- usage-note 可独立给执行同学阅读并直接使用
- 报告文件说明“为何不改CSV只补语义文档”
```

---

## 推荐下发顺序（可并发）

- 并发下发：`P1-01` + `P1-02` + `P1-03`
- 前提：R1(P0) 仍按原计划推进，不受这三项影响
