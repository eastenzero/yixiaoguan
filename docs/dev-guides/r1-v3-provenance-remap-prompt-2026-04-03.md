# R1-v3 Provenance Remap 单任务提示词（2026-04-03）

> 用途：修复 `R1-v2` 在 dry-run 中暴露出的“编号正确但内容归属错误”问题。  
> 目标：生成一版**真正可执行**的 `remap-plan-v3` / `rebuild-needed-v3`，供正式落地前再次验收。

---

## 通用前置（复制给执行 AI 前必须保留）

```markdown
【执行模式：强约束】
1) 你只能做我指定的单一任务，不允许顺手修别的问题。
2) 你只能修改“允许修改文件列表”中的文件，超范围立即停止。
3) 你必须先输出 STEP-PLAN，等我回复“继续”后再执行。
4) 执行后必须输出 STEP-CHECK，逐项说明验收结果。
5) 信息不足时写 BLOCKED，不允许猜测，不允许补脑。
6) 禁止修改 `services/`、`apps/` 下任何代码。
7) 禁止直接重命名任何 `.md` 草稿文件；本任务只生成 v3 方案，不做正式执行。
8) 禁止仅凭 `old_kb_id` 推断归属，必须以草稿 frontmatter 的 `material_id` 为准。

【固定回报模板】
STEP-PLAN
- 目标文件:
- 读取文件:
- 预计输出:
- 风险点:

STEP-EXECUTED
- 实际修改文件:
- 实际生成文件:
- 统计摘要:

STEP-CHECK
- 校验1（old_kb_id 是否一对一）:
- 校验2（rename 条目 material_id 是否与目标批次队列一致）:
- 校验3（need_rebuild 条目是否覆盖剩余冲突/缺失项）:
- 校验4（是否存在超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## 可直接投喂 Subagent 的 Prompt

```markdown
你是“知识库 provenance 重映射工程师”。

【任务目标】
仅处理 R1-v3：基于现有草稿 frontmatter 的 `material_id`，重建一版真正可执行的编号重映射方案。

你要解决的问题不是“old_kb_id 重复”，而是：
- 当前 `KB-20260324-0061.md ~ 0081.md` 的**实物内容归属**，与 `batch-r1-kb-id-remap-plan-v2.csv` 的假设不一致；
- 已知 dry-run 发现：`0061~0079` 多数草稿实际更接近 A3，`0080~0081` 对应 A2；
- 因此，禁止继续沿用“保留 A2、重建 A3”的先验，必须重新按 `material_id` 归属做 v3 方案。

【输入文件】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v2.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v2.csv`
3. `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv`
4. `knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv`
5. `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv`
6. `knowledge-base/entries/first-batch-drafts/KB-20260324-0061.md`
7. `knowledge-base/entries/first-batch-drafts/KB-20260324-0062.md`
8. `knowledge-base/entries/first-batch-drafts/KB-20260324-0063.md`
9. `knowledge-base/entries/first-batch-drafts/KB-20260324-0064.md`
10. `knowledge-base/entries/first-batch-drafts/KB-20260324-0065.md`
11. `knowledge-base/entries/first-batch-drafts/KB-20260324-0066.md`
12. `knowledge-base/entries/first-batch-drafts/KB-20260324-0067.md`
13. `knowledge-base/entries/first-batch-drafts/KB-20260324-0068.md`
14. `knowledge-base/entries/first-batch-drafts/KB-20260324-0069.md`
15. `knowledge-base/entries/first-batch-drafts/KB-20260324-0070.md`
16. `knowledge-base/entries/first-batch-drafts/KB-20260324-0071.md`
17. `knowledge-base/entries/first-batch-drafts/KB-20260324-0072.md`
18. `knowledge-base/entries/first-batch-drafts/KB-20260324-0073.md`
19. `knowledge-base/entries/first-batch-drafts/KB-20260324-0074.md`
20. `knowledge-base/entries/first-batch-drafts/KB-20260324-0075.md`
21. `knowledge-base/entries/first-batch-drafts/KB-20260324-0076.md`
22. `knowledge-base/entries/first-batch-drafts/KB-20260324-0077.md`
23. `knowledge-base/entries/first-batch-drafts/KB-20260324-0078.md`
24. `knowledge-base/entries/first-batch-drafts/KB-20260324-0079.md`
25. `knowledge-base/entries/first-batch-drafts/KB-20260324-0080.md`
26. `knowledge-base/entries/first-batch-drafts/KB-20260324-0081.md`
27. `docs/test-reports/completion-reports/KB-R1-DRY-RUN-2026-04-03.md`

【允许修改文件列表】
1. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v3.csv`
2. `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v3.csv`
3. `docs/test-reports/completion-reports/BATCH-R1-v3-provenance-remap-report.md`

【禁止事项】
1. 禁止修改任何现有 `.md` 草稿文件。
2. 禁止修改 A1/A2/A3 原队列 CSV。
3. 禁止修改 v2 文件，只能新建 v3 文件。
4. 禁止仅凭文件名编号判断归属。
5. 禁止把 `KB-REX-*` 放进 rename 清单。

【核心判定规则】
1. 先读取 `KB-20260324-0061.md ~ 0081.md` frontmatter 中的 `material_id`。
2. 再分别对照 A1/A2/A3 队列中的：
   - A1：`kb_draft_id`
   - A2：`target_kb_id`
   - A3：`kb_entry_id`
   以及各自对应的 `material_id`。
3. 只有当“当前草稿文件的 material_id == 目标批次队列中的 material_id”时，才能进入 `remap-plan-v3` 的 `action=rename`。
4. 若当前草稿文件存在，但 `material_id` 不属于目标批次，则该条不得 rename，必须转入 `rebuild-needed-v3`。
5. 若某批次理论应有条目，但当前草稿目录不存在相应实物内容，也必须转入 `rebuild-needed-v3`。
6. `KB-REX-*` 一律进 `rebuild-needed-v3`，`next_action=manual_review`。

【你必须输出的 v3 文件字段】

### 文件1：`batch-r1-kb-id-remap-plan-v3.csv`
字段固定为：
- `current_file_kb_id`
- `current_material_id`
- `current_owner_batch`
- `target_batch`
- `target_new_kb_id`
- `action`
- `decision_reason`

说明：
- `action` 只允许 `rename`
- 此表中每一行都必须证明“当前文件内容归属”和“目标批次”一致

### 文件2：`batch-r1-kb-draft-rebuild-needed-v3.csv`
字段固定为：
- `expected_batch`
- `expected_material_id`
- `old_conflict_kb_id`
- `target_new_kb_id`
- `current_file_kb_id`
- `current_material_id`
- `status`
- `decision_reason`
- `next_action`

说明：
- `status` 只允许 `need_rebuild`
- `next_action` 只允许：`rebuild_from_source` / `manual_review`

【报告文件必须包含】
1. `0061~0081` 每个现有草稿的实际归属表（按 material_id 判定）
2. 可直接 rename 的数量
3. 必须重建的数量
4. `KB-REX-*` 数量
5. 为什么 v2 不能直接执行
6. v3 相比 v2 的核心修正点

【完成标准】
1. `remap-plan-v3` 中每条 rename 都能说明：
   - 当前文件是谁
   - 当前 material_id 是谁
   - 它为什么属于目标批次
2. `rebuild-needed-v3` 覆盖所有剩余冲突项、缺失项、REX项。
3. 报告中明确写出：
   - 哪些文件可以直接改名
   - 哪些必须重建
   - 哪些不能自动处理
4. 不允许出现“看文件名猜归属”的描述。
```

---

## 推荐使用方式

- 第一步：把“通用前置”+“可直接投喂 Subagent 的 Prompt”一起发给执行 AI。
- 第二步：先只收 `STEP-PLAN`，确认它真正理解了 `material_id` 归属逻辑。
- 第三步：确认后再让它执行并产出 v3 三个文件。

---

## 本 Prompt 解决的核心风险

它专门防止下面这类错误再次出现：

- 只看旧编号，把 `KB-20260324-0061.md` 直接改成 `KB-20260324-0082.md`
- 结果编号变对了，但内容其实还是 A3，不是 A2
- 后续队列字段同步后形成“编号正确、内容错误”的隐性污染
