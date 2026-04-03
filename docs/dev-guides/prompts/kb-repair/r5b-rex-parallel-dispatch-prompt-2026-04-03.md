# R5b + REX 并行派发包（2026-04-03）

> **派发模式**：指挥官同时派出两个子 agent，各自独立完成，互不干扰  
> **Cascade L2 授权状态**：✅ 已授权（REX 入库决策已由 Cascade 确认）  
> **前置条件**：R5-A1-REBUILD-EXEC 已完成（L2 已签字）

---

## 指挥官派发说明

请将以下两个 Prompt 分别投给两个独立的子 agent，**可同时下发**。

| 子 agent | 任务 | 文件影响范围 |
|----------|------|-------------|
| 子 agent 1 | R5b — A1 候补条目建档 | `batch-a1-award-aid-queue.csv` + 4 个新 .md |
| 子 agent 2 | REX — 模板类条目建档 | `batch-r1-kb-draft-rebuild-needed-v3.csv` + 2 个新 .md |

两个任务**文件不重叠**，可以并行执行。
两个子 agent 各自完成后，分别汇报 L1，指挥官汇总后一次性上报 Cascade L2 验收。

---

## 通用前置（两个子 agent 均须包含，复制时不要删）

```
【执行模式：强约束】
1) 只能做我指定的单一任务，不允许顺手修别的问题。
2) 只能修改"允许修改文件列表"中的文件，超范围立即停止。
3) 必须先输出 STEP-PLAN，等我回复"继续"后再执行。
4) 执行后必须输出 STEP-CHECK，逐项说明验收结果。
5) 信息不足时写 BLOCKED，不允许猜测，不允许补脑。
6) 禁止修改 services/、apps/ 下任何代码。
7) 禁止修改已存在的任何 .md 草稿文件。

【固定回报模板】
STEP-PLAN
- 预计创建文件数:
- 预计更新 CSV 行数:
- 风险点:

STEP-EXECUTED
- 实际创建文件数:
- 实际更新 CSV 行数:
- BLOCKED 条目（若有）:

STEP-CHECK
（各任务自行填写，见下方各自的 STEP-CHECK 要求）

BLOCKERS
- 无 / 有（条目编号 + 原因）
```

---

## 子 agent 1 Prompt — R5b：A1 候补条目建档

```
你是"知识库 A1 候补条目建档工程师"。

【任务目标】
为 A1 队列中 4 个无 material_id 的候补条目：
1. 在 batch-a1-award-aid-queue.csv 中分配 material_id 和新 kb_draft_id
2. 从已转换 Markdown 创建对应草稿文件
3. 将 seq=11 行标记为已合并（不创建单独草稿）

【参考文件（只读）】
- knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
- knowledge-base/raw/first-batch-processing/converted/markdown/（源文件转换后的 Markdown）

【允许修改文件列表】
1. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
   （仅允许修改 4 个候补条目的 material_id、kb_draft_id、status 字段，以及 seq=11 的 status 字段）
2. knowledge-base/entries/first-batch-drafts/KB-20260324-0131.md（新建）
3. knowledge-base/entries/first-batch-drafts/KB-20260324-0132.md（新建）
4. knowledge-base/entries/first-batch-drafts/KB-20260324-0133.md（新建）
5. knowledge-base/entries/first-batch-drafts/KB-20260324-0134.md（新建）
6. docs/test-reports/completion-reports/BATCH-R5b-candidate-pool-report.md（新建）

【禁止事项】
1. 禁止修改 seq=1~7（已有 material_id 的条目）。
2. 禁止修改 A2/A3 队列 CSV。
3. 禁止修改 batch-a1-award-aid-queue.csv 中除指定字段以外的任何字段。
4. 禁止修改已有草稿文件。

---

### 4 个候补条目分配清单

| queue_seq | 现有 kb_draft_id | 新 material_id | 新 kb_draft_id | 操作 |
|-----------|-----------------|----------------|----------------|------|
| 8 | KB-20260324-0068（旧，废弃）| MAT-20260324-0128 | KB-20260324-0131 | 建档 |
| 9 | KB-20260324-0069（旧，废弃）| MAT-20260324-0129 | KB-20260324-0132 | 建档 |
| 10 | KB-20260324-0070（旧，废弃）| MAT-20260324-0130 | KB-20260324-0133 | 建档（合并 seq=11）|
| 11 | KB-20260324-0071（旧，废弃）| 不分配 | 不分配 | 标记合并，status = skip_merged |
| 12 | KB-20260324-0072（旧，废弃）| MAT-20260324-0131 | KB-20260324-0134 | 建档 |

seq=10 合并说明：seq=10 和 seq=11 的文件名相同（贫困认定弃权声明 (2).docx），
路径不同但内容一致，视为同一表格的两个副本，合并为一个 KB 条目。
- seq=10 为主条目（保留，建档）
- seq=11 的 status 更新为 "skip_merged"，kb_draft_id 字段清空，不新建文件

### 草稿文件格式

（与 R5 任务相同格式）

---
entry_id: KB-20260324-XXXX
material_id: MAT-20260324-XXXX
title: "（从内容中提炼）"
category: 奖助贷补
audience: （从源文件判断；不确定填 "全体学生"）
source: （队列中 file_name 字段值）
created_at: 2026-04-03
status: 草稿
---

## 问题概述

（2~3 句，概括文件解决什么问题）

## 标准答复

（核心内容摘要，150~300 字）

## 办理流程

（有则列出；无则省略本节）

## 注意事项

（有则列出；无则省略本节）

## 来源说明

- 来源文件：（file_name 值）
- material_id：（该条目的 material_id）

### 源文件查找方法

在 knowledge-base/raw/first-batch-processing/converted/markdown/ 中，
用 file_name（去掉扩展名）模糊匹配对应 .md 文件。
找不到时标注 BLOCKED，继续处理其余条目。

---

### STEP-CHECK 要求

- 校验1（新建文件数 + BLOCKED 数 = 4）:
- 校验2（seq=11 status = skip_merged，kb_draft_id 字段已清空）:
- 校验3（entry_id 与文件名一致）:
- 校验4（A1 queue 中新 material_id 无重复，格式 MAT-20260324-XXXX）:
- 校验5（未触碰 seq=1~7 及 A2/A3 队列）:

完成报告写入后，回复"子 agent 1 任务完成并停止"。
```

---

## 子 agent 2 Prompt — REX：模板类条目建档

```
你是"知识库 REX 模板条目建档工程师"。

【任务目标】
为两个已在 A2 队列中但尚未建档的模板类条目创建知识库草稿文件，
并更新 rebuild-needed-v3.csv 中的状态。

【背景说明】
KB-REX-0001 和 KB-REX-0002 是因为属于"模板类"而被标记为 manual_review 的条目。
Cascade 已确认：两个条目均应正式入库。

【参考文件（只读）】
- knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv
  （读取 source_path、file_name、knowledge_category 等字段）
- knowledge-base/raw/first-batch-processing/converted/markdown/
- knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v3.csv

【允许修改文件列表】
1. knowledge-base/entries/first-batch-drafts/KB-REX-0001.md（新建）
2. knowledge-base/entries/first-batch-drafts/KB-REX-0002.md（新建）
3. knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v3.csv
   （仅将 KB-REX-0001、KB-REX-0002 对应行的 status 从 manual_review 改为 completed）
4. docs/test-reports/completion-reports/BATCH-REX-entry-report.md（新建）

【禁止事项】
1. 禁止修改 batch-a2-employment-enrollment-queue.csv（A2 队列中 target_kb_id 已正确指向 KB-REX-0001/0002，无需修改）。
2. 禁止修改 A1/A3 队列 CSV。
3. 禁止修改已有草稿文件。
4. 禁止修改 rebuild-needed-v3.csv 中除 status 字段以外的任何字段。

---

### 两个条目信息

**条目 1：KB-REX-0001**
- material_id：MAT-20260324-0116（已在 A2 队列中）
- file_name：团员组织关系介绍信参考模板.doc
- source_path：数据库部分材料/.../2025级毕业生团关系转出/团员组织关系介绍信参考模板.doc
- knowledge_category：就业与毕业
- 建档文件：KB-REX-0001.md

**条目 2：KB-REX-0002**
- material_id：MAT-20260324-0118（已在 A2 队列中）
- file_name：9在读或预毕业证明中英文模板（外合部）.docx
- source_path：数据库部分材料/.../出国留学英文证明模板终稿/9在读或预毕业证明中英文模板（外合部）.docx
- knowledge_category：就业与毕业
- 建档文件：KB-REX-0002.md

### 草稿文件格式

---
entry_id: KB-REX-0001        （或 KB-REX-0002）
material_id: MAT-20260324-XXXX
title: "（从内容提炼）"
category: 就业与毕业
audience: （推断；不确定填 "毕业生"）
source: （file_name 值）
created_at: 2026-04-03
status: 草稿
---

## 问题概述

（说明这份模板用于什么场景、什么时候需要用到）

## 标准答复

（模板主要内容说明，填写要点或注意事项，150~300 字）

## 注意事项

（有则列出；无则省略）

## 来源说明

- 来源文件：（file_name 值）
- material_id：（该条目的 material_id）

### 源文件查找方法

在 knowledge-base/raw/first-batch-processing/converted/markdown/ 中，
用 file_name（去掉扩展名）模糊匹配对应 .md 文件。
找不到时标注 BLOCKED，继续处理另一条目。

---

### STEP-CHECK 要求

- 校验1（新建文件数 + BLOCKED 数 = 2）:
- 校验2（entry_id 与文件名一致：KB-REX-0001 → entry_id: KB-REX-0001）:
- 校验3（rebuild-needed-v3.csv 中 KB-REX-0001/0002 的 status = completed）:
- 校验4（A2 队列 target_kb_id 未被修改）:

完成报告写入后，回复"子 agent 2 任务完成并停止"。
```

---

## 指挥官汇总 L1 核查清单

两个子 agent 均完成后，执行以下核查，通过后一次性上报 Cascade：

```
【R5b 核查】
□ L1-1 BATCH-R5b-candidate-pool-report.md 已创建
□ L1-2 实际新建文件数 + BLOCKED 数 = 4
□ L1-3 存在性：ls first-batch-drafts/ | grep "KB-20260324-013[1-4]" 应见 3~4 个
□ L1-4 seq=11 在 A1 queue 中 status = skip_merged
□ L1-5 seq=8/9/10/12 的 material_id 已填入（格式 MAT-20260324-XXXX）

【REX 核查】
□ L1-6 BATCH-REX-entry-report.md 已创建
□ L1-7 KB-REX-0001.md 和 KB-REX-0002.md 均已创建
□ L1-8 rebuild-needed-v3.csv 中 KB-REX-0001/0002 的 status = completed
□ L1-9 A2 队列 target_kb_id 字段未被改动
```

**全部通过后，上报 Cascade 做 L2 验收。**

---

## Cascade L2 验收点

**R5b：**
1. 抽查 2 个新文件（如 KB-0132、KB-0134），确认 frontmatter 正确、内容非空
2. 确认 seq=10 entry_id = KB-20260324-0133，seq=11 status = skip_merged
3. 确认新 material_id 无重复，格式正确

**REX：**
4. 读取 KB-REX-0001.md 和 KB-REX-0002.md，确认 entry_id、内容主题相符
5. 确认 rebuild-needed-v3.csv 状态已更新
6. 签字放行：**修复阶段全部收口，进入入库阶段（ChromaDB 全量入库）**

---

## 版本记录

| 版本 | 时间 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | 并行派发包，R5b + REX，修复阶段收尾 |
