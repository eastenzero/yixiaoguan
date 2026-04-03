# 知识库问题修复并行提示词包（V2｜弱执行代理专用）

> 适用场景：当前不开放新扩量，先修复已交付产物中的冲突、重复、缺证据与统计不一致。

---

## 0. 固定事实（先读，不允许改写）

以下为当前仓库实物基线，执行 AI 必须以此为准，不得用旧报告数字覆盖：

- `batch-a1-award-aid-queue.csv`：41 条
- `batch-a2-employment-enrollment-queue.csv`：23 条
- `batch-a3-service-admin-queue.csv`：19 条
- `batch-a1-award-aid-rule-extraction.csv`：29 条
- `batch-a2-employment-enrollment-rule-extraction.csv`：2 条
- `batch-a3-service-admin-rule-extraction.csv`：37 条
- `batch-qa-conflict-and-dup-report.csv`：61 条问题记录（含 SUMMARY 行）
- `knowledge-base/entries/first-batch-drafts/KB-20260324-0061.md ~ 0081.md` 仅 21 个文件
- `docs/test-reports/completion-reports/BATCH-QA-completion-report.md` 当前不存在

---

## 1. 通用硬约束（所有 Prompt 必须带）

复制给任意执行 AI 前，先附加下面固定规则：

```markdown
【执行模式：强约束】
1) 你只能做我指定的单一任务，不允许顺手做其他优化。
2) 你只能修改“允许修改文件列表”中的文件；超出范围立即停止并汇报。
3) 先输出“STEP-PLAN”（将改哪些文件、改几处、为什么），等待我回复“继续”后才可动手。
4) 改完后必须输出“STEP-CHECK”（逐条自检结果），格式固定，不得省略。
5) 如遇信息不足，必须写“BLOCKED: 原因”，禁止猜测、禁止编造。
6) 不允许修改 `services/`、`apps/` 下任何代码。
7) 不允许删除文件；若需替换，先生成 `-v2` 文件供人工确认。

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
- 校验2（行数/条数）:
- 校验3（字段完整）:
- 校验4（是否超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## 2. 并行修复任务（建议 4 并发 + 1 收口）

## Prompt-R1（编号冲突修复方案，不直接重写草稿）

```markdown
你是“知识库编号冲突修复工程师”。

【任务目标】
仅生成“编号重映射方案”与“待重建草稿清单”，不直接改 KB 草稿正文。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv`
3. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-conflict-and-dup-report.csv`
4. `knowledge-base/entries/first-batch-drafts/`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed.csv`
3. `docs/test-reports/completion-reports/BATCH-R1-id-remap-plan-report.md`

【产出要求】
1) 生成 `batch-r1-kb-id-remap-plan.csv`，字段固定：
`source_batch,material_id,old_kb_id,new_kb_id,action,reason`

2) 编号策略固定：
- A1 保持不动（0061~0072）
- A2 改为 0082 起连续编号
- A3 改为 0105 起连续编号

3) 生成 `batch-r1-kb-draft-rebuild-needed.csv`，字段固定：
`kb_id,source_batch,material_id,reason,source_path,status`

4) 若发现某旧编号在草稿目录中无可对应内容，标记 `status=need_rebuild`。

【禁止事项】
- 禁止直接重命名 `knowledge-base/entries/first-batch-drafts/*.md`
- 禁止修改 A1/A2/A3 原 queue 文件
- 禁止改写 QA 冲突报告

【完成标准】
- 两个 CSV + 1 个报告都生成
- 报告中明确“可自动重命名数量 / 必须重建数量”
```

---

## Prompt-R2（规则去重修复，输出 v2 文件）

```markdown
你是“规则去重修复工程师”。

【任务目标】
对 A1 规则提炼文件做去重，输出 v2 文件，不覆盖原始文件。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-rule-extraction.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-conflict-and-dup-report.csv`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-rule-extraction-v2-dedup.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-r2-dedup-mapping.csv`
3. `docs/test-reports/completion-reports/BATCH-R2-rule-dedup-report.md`

【去重规则（固定）】
1) QA 报告中标记为 `DUP-*` 的条目必须处理。
2) 同组重复只保留 1 条 canonical 记录，优先级：
   - `evidence_status=完整` 优先
   - 若相同，保留 `material_id` 非空者
   - 若仍相同，保留 `rule_task_id` 编号更小者

【CSV字段要求】
- `batch-r2-dedup-mapping.csv` 字段固定：
`duplicate_rule_id,canonical_rule_id,decision_reason`

【禁止事项】
- 禁止改原文件 `batch-a1-award-aid-rule-extraction.csv`
- 禁止修改 A2/A3 规则文件

【完成标准】
- v2 去重文件可直接替换使用
- mapping 文件能追溯每条被删除规则的去向
```

---

## Prompt-R3（生成 QA 白名单 + 人工复核清单）

```markdown
你是“QA 收口工程师”。

【任务目标】
基于现有冲突报告，补齐 QA 缺失交付物。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-conflict-and-dup-report.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv`
3. `knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv`
4. `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-manual-review-list.csv`
3. `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`

【判定规则（固定）】
1) 任一条目命中以下类型之一，进入 `manual-review-list`：
   - `severity` 包含 `P0`
   - `issue_type` 属于：KB编号冲突 / 源文件缺失 / 版本冲突
2) 不命中上面条件，且无重复冲突的条目可进入 `ingestion-whitelist`。
3) 对 `SUMMARY` 行只做统计，不写入两份清单。

【CSV字段要求】
- whitelist 字段：`kb_id,material_id,source_batch,reason,ready_for_ingest`
- manual-review 字段：`kb_id,material_id,source_batch,issue_type,severity,required_action`

【完成标准】
- 两个 CSV 均生成且字段完整
- 完成报告包含三段：统计口径、分类结果、待决策事项
```

---

## Prompt-R4（统计口径回填修复）

```markdown
你是“统计一致性修复工程师”。

【任务目标】
修复最终汇总报告中的数字与实物不一致问题，仅改统计和状态，不改结论框架。

【输入文件】
1. `docs/test-reports/completion-reports/KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY.md`
2. manifests 下相关 CSV（A1/A2/A3/QA）

【允许修改文件列表】
1. `docs/test-reports/completion-reports/KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md`

【修复规则】
1) 不覆盖原报告，输出 `-v2`。
2) 所有计数以 CSV 实际行数（不含表头）为准。
3) 明确标注“旧值 -> 新值”的修订说明段。

【完成标准】
- v2 报告可独立阅读
- 至少修复以下统计：A2条数、A3条数、A3规则数、QA问题总数
```

---

## Prompt-R5（缺失源文件追补任务单）

```markdown
你是“缺失源文件追补工程师”。

【任务目标】
把“源文件缺失”问题转成可派发工单，不做内容补写。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-qa-conflict-and-dup-report.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-r5-missing-source-request.csv`
2. `docs/test-reports/completion-reports/BATCH-R5-missing-source-report.md`

【输出字段（固定）】
`kb_id,material_id,source_path,missing_reason,owner_placeholder,due_date,priority,next_action`

【规则】
1) 仅提取 QA 报告中 `issue_type=源文件缺失` 条目。
2) `priority` 统一先标 `P1`。
3) `owner_placeholder` 统一填 `待指派`。
4) `due_date` 统一填 `2026-04-15`。

【完成标准】
- 追补任务单可直接发给资料管理员
- 报告里给出“按学院/主题”分组统计
```

---

## 3. 推荐发包顺序（你作为指挥官）

先并行发 4 个：`R1 + R2 + R3 + R5`，都完成后再发 `R4`。

- R1 解决“编号策略与重建边界”
- R2 解决“规则重复可追溯去重”
- R3 解决“QA 缺交付物”
- R5 解决“缺源材料派单”
- R4 最后统一更新汇总报告口径

---

## 4. 给弱执行代理的额外提示（建议每次都附）

```markdown
你不是来做“优化”，你是来做“对账修复”。
先对齐文件事实，再写结果；不做猜测，不做扩展，不做越界改动。
如果你发现输入文件与我给你的数字不一致，立即停止并回报差异，不要继续执行。
```
