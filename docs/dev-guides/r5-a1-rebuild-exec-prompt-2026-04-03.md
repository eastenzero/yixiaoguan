# R5-A1-REBUILD-EXEC 执行任务提示词（2026-04-03）

> **任务性质**：从源文件内容重建 7 个 A1 知识库草稿文件  
> **Cascade L2 授权状态**：✅ 已授权  
> **前置条件**：R4 已完成（A1 queue 7 行已标记 rebuild_needed，编号 0124~0130）  
> **下发方式**：指挥官将"通用前置 + 子 agent Prompt"一起投给执行 AI

---

## 通用前置（必须保留，复制时不要删）

```
【执行模式：强约束】
1) 只能做我指定的单一任务，不允许顺手修别的问题。
2) 只能修改"允许修改文件列表"中的文件，超范围立即停止。
3) 必须先输出 STEP-PLAN，等我回复"继续"后再执行。
4) 执行后必须输出 STEP-CHECK，逐项说明验收结果。
5) 遇到源文件找不到或内容不足，写 BLOCKED（单条），继续处理其余条目。
6) 禁止修改 services/、apps/ 下任何代码。
7) 禁止修改已存在的 .md 草稿文件。

【固定回报模板】
STEP-PLAN
- 预计创建文件数:
- 风险点（哪些条目可能找不到源文件）:

STEP-EXECUTED
- 实际创建文件数:
- BLOCKED 条目（若有）:

STEP-CHECK
- 校验1（创建文件数 + BLOCKED 数 == 7）:
- 校验2（每个文件 entry_id 与文件名一致）:
- 校验3（A1 queue 对应行 status 已改为 completed）:
- 校验4（未修改其他 queue CSV 或已有草稿文件）:

BLOCKERS
- 无 / 有（条目编号 + 原因）
```

---

## 可直接投喂子 agent 的 Prompt

```
你是"知识库 A1 草稿重建工程师"。

【任务目标】
为 7 个从未生成过草稿的奖助贷补类知识库条目，
从已转换的 Markdown 源文件中提取内容，创建标准知识库草稿文件。

【输入文件】
1. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
   （用于读取 material_id、source_path、knowledge_category、title_guess、audience 等字段）
2. knowledge-base/raw/first-batch-processing/converted/markdown/
   （存放源文件已转换的 Markdown 内容，按文件名匹配）

【允许修改文件列表】
1~7. knowledge-base/entries/first-batch-drafts/KB-20260324-0124.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0125.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0126.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0127.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0128.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0129.md（新建）
       knowledge-base/entries/first-batch-drafts/KB-20260324-0130.md（新建）
8. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
   （仅允许将 7 个目标行的 status 从 rebuild_needed 改为 completed）
9. docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md（新建）

【禁止事项】
1. 禁止修改已存在的任何 .md 草稿文件。
2. 禁止修改 A2/A3 队列 CSV。
3. 禁止修改 A1 queue 中除 status 字段以外的任何字段，也不允许改非目标行。
4. 禁止使用 knowledge-base/templates/knowledge-entry-template.md 的格式——
   必须使用下方指定的"草稿格式"。

---

### 七条目信息清单

| 序号 | material_id | 新 kb_entry_id | queue 中 title_guess |
|------|-------------|---------------|----------------------|
| 1 | MAT-20260324-0024 | KB-20260324-0124 | 附件3：（学院）国家助学金申请表 |
| 2 | MAT-20260324-0025 | KB-20260324-0125 | 附件4：本专科生国家助学金实施细则 |
| 3 | MAT-20260324-0026 | KB-20260324-0126 | 关于做好2024-2025学年本科生国家助学金评选工作的通知 |
| 4 | MAT-20260324-0027 | KB-20260324-0127 | 附件2：一网通办系统学生申请操作说明 |
| 5 | MAT-20260324-0028 | KB-20260324-0128 | 关于开展2025-2026学年家庭经济困难认定的通知 |
| 6 | MAT-20260324-0029 | KB-20260324-0129 | 学院、班级一网通办操作说明 |
| 7 | MAT-20260324-0055 | KB-20260324-0130 | 通知（院级优秀评选） |

---

### 操作步骤（每条目重复以下流程）

步骤1：在 batch-a1-award-aid-queue.csv 中找到该 material_id 对应行，
       读取 source_path（源文件路径）、file_name、knowledge_category、audience。

步骤2：根据 file_name，在以下路径寻找对应 Markdown 文件：
       knowledge-base/raw/first-batch-processing/converted/markdown/
       文件名通常为 <原文件名（去掉扩展名）>.md 或类似形式。
       若找不到 → 在报告中标注 BLOCKED，继续下一条目，不中止整个任务。

步骤3：读取 Markdown 内容，理解文档主要信息（适用对象、核心内容、流程等）。

步骤4：按以下格式创建草稿文件：

----- 草稿文件格式 -----
---
entry_id: KB-20260324-XXXX
material_id: MAT-20260324-XXXX
title: "（从内容中提炼，优先使用文档标题，而不是文件名）"
category: （从 queue 的 knowledge_category 字段取值）
audience: （从 queue 的 audience 字段取值；若为空则写 "全体学生"）
source: （queue 中 file_name 字段的值）
created_at: 2026-04-03
status: 草稿
---

## 问题概述

（用 2~4 句话概括这份文件解决什么问题，适合什么场景）

## 标准答复

（核心内容摘要，包含主要规定、条件、流程要点，200~400 字）

## 办理流程

（如有明确流程步骤，列出 1、2、3……；无则写"见来源文件"）

## 注意事项

（列出文件中的关键注意点；无则省略本节）

## 来源说明

- 来源文件：（file_name 值）
- material_id：（该条目的 material_id）
----- 格式结束 -----

步骤5：文件创建成功后，在 batch-a1-award-aid-queue.csv 中将该 material_id 对应行
       的 status 字段从 rebuild_needed 改为 completed。

---

### 完成报告要求

路径：docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md

报告章节（缺一不可）：
1. **任务标识**：任务ID=BATCH-R5-A1-REBUILD-EXEC，执行时间，执行AI身份
2. **创建明细表**：
   | 序号 | material_id | 新文件名 | 标题 | 状态 |
   （7 行，BLOCKED 条目在状态列标注原因）
3. **A1 queue 更新明细**：哪些行的 status 从 rebuild_needed → completed
4. **校验结果**：
   - 实际创建文件数
   - BLOCKED 条目数（预期为 0，若 >0 列出原因）
   - A1 queue 更新行数（应 == 实际创建文件数）
   - 是否有超范围修改
5. **遗留问题**：BLOCKED 条目列表 + 找不到源文件的具体路径
6. **下一步建议**：告知指挥官"等待 Cascade L2 验收后，方可进入候补条目重建（R5b）"

完成报告写入后，回复"阶段任务完成并停止"，不要继续优化。
```

---

## 指挥官 L1 核查清单

```
□ L1-1 文件是否齐：BATCH-R5-a1-rebuild-exec-report.md 已创建
□ L1-2 数字一致性：
     报告"创建文件数 + BLOCKED 数 == 7"
□ L1-3 文件存在性：
     ls knowledge-base/entries/first-batch-drafts/ | grep "KB-20260324-012[4-9]\|KB-20260324-0130"
     应出现 6+ 个文件（BLOCKED 的除外）
□ L1-4 禁止项核查：是否有已有草稿被修改（FAIL 条件）
□ L1-5 A1 queue status 已更新：抽查 1~2 行，确认 status == completed
```

**L1 全通过后，上报 Cascade 做 L2 验收。**

---

## Cascade L2 验收点

1. 抽查 3 个新文件，确认 frontmatter 中 entry_id、material_id、title 正确
2. 确认 entry_id 与文件名一致（KB-20260324-0124 → entry_id: KB-20260324-0124）
3. 确认正文内容非空且与源文件主题相符
4. 确认 A1 queue 对应 status 已由 rebuild_needed → completed
5. 签字放行：进入 R5b（候补条目建档）

---

## 版本记录

| 版本 | 时间 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | R4 验收通过后首次发布，seq=10/11 合并决策已确认 |
