# R4-A1-REBUILD 分析任务提示词（2026-04-03）

> **任务性质**：A1 队列修复（7 行 kb_draft_id 重分配 + 5 行候补条目归属分析）  
> **Cascade L2 授权状态**：✅ 已授权  
> **前置条件**：R2-RENAME 已完成  
> **下发方式**：指挥官将"通用前置 + 子 agent Prompt"一起投给执行 AI

---

## 背景说明（给子 agent 的上下文）

A1 队列（奖助贷）中共有 12 行的 `kb_draft_id` 字段指向了已被占用或已不存在的旧编号：
- **7 行有正式 material_id**（MAT-0024~0029, MAT-0055）：原来规划用 KB-0061~0067，但这些编号已被 A3 内容占用并重命名为 KB-0105~0111。这 7 份 A1 材料的草稿文件从未实际生成过。
- **5 行无 material_id**（candidate-pool，queue_seq=8~12）：原来规划用 KB-0068~0072，但这些编号也已被 A3 内容占用。需要分析这 5 条是否与现有条目重复，再决定处置方式。

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
7) 禁止修改 A2/A3 队列 CSV。
8) 禁止修改任何草稿 .md 文件。

【固定回报模板】
STEP-PLAN
- 任务一预计修改行数:
- 任务二分析条目数:
- 风险点:

STEP-EXECUTED
- 任务一实际修改行数:
- 任务二分析完成条目数:

STEP-CHECK
- 校验1（任务一修改行数 == 7）:
- 校验2（每行新 kb_draft_id 与映射表一致）:
- 校验3（任务二每条候补条目均有明确分类）:
- 校验4（A2/A3 队列未被触碰）:
- 校验5（是否有超范围修改）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## 可直接投喂子 agent 的 Prompt

```
你是"知识库 A1 队列修复与分析工程师"。

【输入文件】
1. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv

【允许修改文件列表】
1. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
2. docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md（新建）

【禁止事项】
1. 禁止修改 A2/A3 队列 CSV。
2. 禁止修改任何 .md 草稿文件。
3. 禁止修改 5 个候补条目（queue_seq=8~12）的 CSV 字段（只分析，不改）。
4. 禁止修改任务一范围以外的任何行。

---

### 任务一：更新 7 个 MAT 条目的 kb_draft_id 和 status

在 batch-a1-award-aid-queue.csv 中，找到以下 7 行（通过 material_id 定位），
按映射表修改其 kb_draft_id 和 status 字段：

| material_id | 旧 kb_draft_id | 新 kb_draft_id | status 改为 |
|-------------|---------------|---------------|------------|
| MAT-20260324-0024 | KB-20260324-0061 | KB-20260324-0124 | rebuild_needed |
| MAT-20260324-0025 | KB-20260324-0062 | KB-20260324-0125 | rebuild_needed |
| MAT-20260324-0026 | KB-20260324-0063 | KB-20260324-0126 | rebuild_needed |
| MAT-20260324-0027 | KB-20260324-0064 | KB-20260324-0127 | rebuild_needed |
| MAT-20260324-0028 | KB-20260324-0065 | KB-20260324-0128 | rebuild_needed |
| MAT-20260324-0029 | KB-20260324-0066 | KB-20260324-0129 | rebuild_needed |
| MAT-20260324-0055 | KB-20260324-0067 | KB-20260324-0130 | rebuild_needed |

核查规则：修改完成后，逐行确认 material_id 与新 kb_draft_id 一一对应，共 7 行。

---

### 任务二：分析 5 个候补条目（只分析，不改 CSV）

在 batch-a1-award-aid-queue.csv 中，找到以下 5 行：
- queue_seq = 8、9、10、11、12（source_type = candidate-pool，material_id 字段为空）

对每一行，执行以下分析：

**步骤 1**：读取该行的 source_path（源文件路径）。

**步骤 2**：在 batch-a1-award-aid-queue.csv 中，搜索所有 source_type = batch2-materials 的行，
          检查是否存在 source_path 完全相同或高度相似（同一文件名、不同路径前缀）的条目。

**步骤 3**：根据结果给出分类：
- **DUPLICATE**：与 batch2-materials 中某行 source_path 相同 → 建议：从候补列表移除，由已有条目覆盖
- **UNIQUE**：未发现重复 → 建议：分配新 material_id 和 kb_draft_id，加入重建队列
- **UNCERTAIN**：文件名相同但路径前缀不同，无法确定 → 标注具体疑似匹配行，等待人工确认

在报告中输出分类表，不要修改 CSV。

---

### 完成报告要求

路径：docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md

报告章节（缺一不可）：
1. **任务标识**：任务ID=BATCH-R4-A1-REBUILD，执行时间（精确到秒），执行AI身份
2. **任务一明细表**：
   | material_id | 旧 kb_draft_id | 新 kb_draft_id | status | 操作结果 |
   （7 行）
3. **任务二分析表**：
   | queue_seq | source_path（文件名部分） | 分类 | 疑似匹配行（若有） | 建议 |
   （5 行）
4. **校验结果**：
   - 任务一修改行数（应为 7）
   - 任务二分析条目数（应为 5，覆盖 queue_seq=8~12）
   - A2/A3 队列未被触碰（✅/❌）
   - 是否有超范围修改（应为否）
5. **遗留问题**：UNCERTAIN 条目列表（如有），或"无"
6. **下一步建议**：告知指挥官"等待 Cascade L2 验收后，方可根据分析结果制定重建计划"

完成报告写入后，回复"阶段任务完成并停止"，不要继续优化。
```

---

## 指挥官 L1 核查清单（子 agent 完成后必须做）

参考 `docs/dev-guides/commander-verification-sop.md`，重点核查：

```
□ L1-1 文件是否齐：BATCH-R4-a1-rebuild-analysis-report.md 是否已创建
□ L1-2 数字一致性：
     报告"任务一修改行数" == 7
     报告"任务二分析条目数" == 5
□ L1-3 字段名核查：
     任务一改的是 kb_draft_id 和 status（不是其他字段）
□ L1-4 禁止项核查：
     报告中是否出现 A2/A3 队列被修改（出现则 FAIL）
     5 个候补条目的 CSV 字段是否有改动（有则 FAIL）
```

**L1 全通过后，上报 Cascade 做 L2 验收。**

---

## Cascade L2 验收点（收到 L1 报告后执行）

1. 检查 A1 queue 中 7 行 kb_draft_id 已更新为 0124~0130，status = rebuild_needed
2. 检查 5 行候补条目的 CSV 字段未变动
3. 审阅分类表：UNCERTAIN 条目需要人工确认，DUPLICATE 建议直接接受，UNIQUE 纳入重建队列
4. 签字放行：根据分类结果，授权后续 A1 草稿重建任务

---

## 版本记录

| 版本 | 时间 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | Cascade L2 授权发布，基于 R2-RENAME 完成后的 A1 队列状态 |
