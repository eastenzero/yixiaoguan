# R2-RENAME 执行任务提示词（2026-04-03）

> **任务性质**：高风险文件操作（实际重命名 `.md` 草稿文件）  
> **Cascade L2 签字状态**：✅ 已确认 v3 CSV 数据正确，授权执行  
> **下发方式**：指挥官将"通用前置 + 子 agent Prompt"一起投给执行 AI

---

## 通用前置（必须保留，复制时不要删）

```
【执行模式：强约束】
1) 只能做我指定的单一任务，不允许顺手修别的问题。
2) 只能修改"允许修改文件列表"中的文件，超范围立即停止。
3) 必须先输出 STEP-PLAN，等我回复"继续"后再执行。
4) 执行后必须输出 STEP-CHECK，逐项说明验收结果。
5) 信息不足时写 BLOCKED，不允许猜测，不允许补脑。
6) 禁止修改 services/、apps/ 下任何代码。
7) 禁止改动任何队列 CSV 文件（A1/A2/A3 queue）。
8) 禁止修改 v3 CSV 文件本身。

【固定回报模板】
STEP-PLAN
- 目标操作数:
- 读取文件:
- 预计修改清单（列出全部21行）:
- 风险点:

STEP-EXECUTED
- 实际重命名文件数:
- 实际更新 entry_id 数:
- 跳过项（如有）:

STEP-CHECK
- 校验1（重命名文件数 == 21）:
- 校验2（A3 文件的 entry_id 已更新为新编号）:
- 校验3（A2 文件无 entry_id 字段，已确认跳过 frontmatter 更新）:
- 校验4（是否有超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## 可直接投喂子 agent 的 Prompt

```
你是"知识库草稿文件重命名工程师"。

【任务目标】
按照 remap-plan-v3.csv 执行 21 条文件重命名，并同步更新 A3 文件的 frontmatter entry_id 字段。

【输入文件】
1. knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v3.csv
   （共 21 行，字段：current_file_kb_id, current_material_id, current_owner_batch,
   target_batch, target_new_kb_id, action, decision_reason）

【操作目录】
knowledge-base/entries/first-batch-drafts/

【允许修改文件列表】
1. knowledge-base/entries/first-batch-drafts/KB-20260324-0061.md → 重命名为 KB-20260324-0105.md
2. knowledge-base/entries/first-batch-drafts/KB-20260324-0062.md → 重命名为 KB-20260324-0106.md
3. knowledge-base/entries/first-batch-drafts/KB-20260324-0063.md → 重命名为 KB-20260324-0107.md
4. knowledge-base/entries/first-batch-drafts/KB-20260324-0064.md → 重命名为 KB-20260324-0108.md
5. knowledge-base/entries/first-batch-drafts/KB-20260324-0065.md → 重命名为 KB-20260324-0109.md
6. knowledge-base/entries/first-batch-drafts/KB-20260324-0066.md → 重命名为 KB-20260324-0110.md
7. knowledge-base/entries/first-batch-drafts/KB-20260324-0067.md → 重命名为 KB-20260324-0111.md
8. knowledge-base/entries/first-batch-drafts/KB-20260324-0068.md → 重命名为 KB-20260324-0112.md
9. knowledge-base/entries/first-batch-drafts/KB-20260324-0069.md → 重命名为 KB-20260324-0113.md
10. knowledge-base/entries/first-batch-drafts/KB-20260324-0070.md → 重命名为 KB-20260324-0114.md
11. knowledge-base/entries/first-batch-drafts/KB-20260324-0071.md → 重命名为 KB-20260324-0115.md
12. knowledge-base/entries/first-batch-drafts/KB-20260324-0072.md → 重命名为 KB-20260324-0116.md
13. knowledge-base/entries/first-batch-drafts/KB-20260324-0073.md → 重命名为 KB-20260324-0117.md
14. knowledge-base/entries/first-batch-drafts/KB-20260324-0074.md → 重命名为 KB-20260324-0118.md
15. knowledge-base/entries/first-batch-drafts/KB-20260324-0075.md → 重命名为 KB-20260324-0119.md
16. knowledge-base/entries/first-batch-drafts/KB-20260324-0076.md → 重命名为 KB-20260324-0120.md
17. knowledge-base/entries/first-batch-drafts/KB-20260324-0077.md → 重命名为 KB-20260324-0121.md
18. knowledge-base/entries/first-batch-drafts/KB-20260324-0078.md → 重命名为 KB-20260324-0122.md
19. knowledge-base/entries/first-batch-drafts/KB-20260324-0079.md → 重命名为 KB-20260324-0123.md
20. knowledge-base/entries/first-batch-drafts/KB-20260324-0080.md → 重命名为 KB-20260324-0101.md
21. knowledge-base/entries/first-batch-drafts/KB-20260324-0081.md → 重命名为 KB-20260324-0102.md
22. docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md（新建）

【操作规则】
规则1：对每个文件执行重命名（原路径 → 新路径）。
规则2：仅对 target_batch == BATCH-A3 的文件（第1~19条），重命名完成后打开文件，
       将 frontmatter 中的 entry_id 字段值从旧编号改为新编号。
       例：entry_id: KB-20260324-0061 → entry_id: KB-20260324-0105
规则3：对 target_batch == BATCH-A2 的文件（第20~21条），只改文件名，
       不改 frontmatter（这两个文件无 entry_id 字段）。
规则4：如果某个源文件不存在，写入 BLOCKED，停止执行，不要跳过继续。
规则5：禁止改动 frontmatter 中的任何其他字段（material_id、title、source 等）。

【禁止事项】
1. 禁止修改任何队列 CSV（A1/A2/A3 queue）。
2. 禁止修改 remap-plan-v3.csv 或 rebuild-needed-v3.csv。
3. 禁止修改 knowledge-base/entries/ 下其他任何文件。
4. 禁止修改 services/、apps/ 下任何内容。
5. 禁止在重命名时"顺便"修改文件内容（除 entry_id 以外的字段）。

【完成报告必须包含】
路径：docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md

报告章节（缺一不可）：
1. 任务标识：任务ID=BATCH-R2-RENAME，执行时间（精确到秒），执行AI身份
2. 重命名明细表：| 旧文件名 | 新文件名 | entry_id更新 | 状态 |
   （21行，entry_id更新列：A3填"已更新"，A2填"无此字段/跳过"）
3. 校验结果：
   - 重命名文件总数（应为21）
   - A3 entry_id 更新总数（应为19）
   - A2 跳过 entry_id 更新总数（应为2）
   - 是否有超范围修改（应为否）
4. 遗留问题：发现但未处理的问题
5. 下一步建议：告知指挥官"等待 Cascade L2 验收后，方可进行队列字段更新"

完成报告写入后，回复"阶段任务完成并停止"，不要继续优化。
```

---

## 指挥官 L1 核查清单（子 agent 完成后必须做）

参考 `docs/dev-guides/commander-verification-sop.md`，重点核查：

```
□ L1-1 文件是否齐：BATCH-R2-rename-execution-report.md 是否已创建
□ L1-2 数字一致性：
     报告"重命名文件总数" == 21
     报告"A3 entry_id 更新总数" == 19
     报告"A2 跳过总数" == 2
□ L1-3 字段名核查：报告明细表中"entry_id更新"列是否区分了A3/A2两种状态
□ L1-4 禁止项核查：子 agent STEP-EXECUTED 中有无出现队列 CSV 或其他禁止文件
```

**L1 全通过后，上报 Cascade 做 L2 验收，等待放行才能进入下一步（队列字段更新）。**

---

## 执行后 Cascade L2 验收点

Cascade 收到 L1 核查报告后，将抽查：
1. 任取 3 个已重命名的 A3 文件，确认 `entry_id` 已正确更新
2. 确认 A2 文件（0101/0102）frontmatter 无 `entry_id` 字段
3. 确认旧编号文件（0061-0081）已不存在
4. 签字放行下一步：队列字段同步任务

---

## 版本记录

| 版本 | 时间 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | 基于 remap-plan-v3.csv（Cascade L2 授权）首次发布 |
