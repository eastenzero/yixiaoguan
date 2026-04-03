# BATCH-B1 竞赛评优 Discovery 提示词（2026-04-03）

> **任务性质**：扫描源文件目录，建立 BATCH-B1（竞赛申报/评优评选/综合测评）批次队列 CSV  
> **批次编号**：BATCH-B1  
> **下发方式**：指挥官将"通用前置 + 子 agent Prompt"一起投给执行 AI  
> **前置条件**：无（独立任务，可在修复阶段并行执行）

---

## 背景说明

当前知识库（BATCH-A1/A2/A3）已覆盖奖助贷补、就业毕业、入学学籍等基础事务。
BATCH-B1 目标是新增竞赛申报、评优评选、综合测评相关的知识库条目，填补这一空白。

参考第一批已有的队列格式（`batch-a1-award-aid-queue.csv`），建立同结构的 `batch-b1-competition-eval-queue.csv`。

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
7) 禁止修改已有的 batch-a1/a2/a3 队列 CSV。
8) 禁止修改知识库 entries/ 目录下任何文件。

【固定回报模板】
STEP-PLAN
- 扫描目录:
- 预计发现文件数量范围:
- 风险点:

STEP-EXECUTED
- 实际扫描文件数:
- 纳入队列条目数:
- 排除/跳过条目数（含原因）:

STEP-CHECK
- 校验1（队列 CSV 已创建且列名与参考文件一致）:
- 校验2（material_id 无重复）:
- 校验3（knowledge_category 仅使用允许值）:
- 校验4（已有 batch-a1/a2/a3 队列未被触碰）:

BLOCKERS
- 无 / 有（具体原因）
```

---

## 可直接投喂子 agent 的 Prompt

```
你是"知识库 BATCH-B1 扫描建档工程师"。

【任务目标】
扫描源文件目录，识别竞赛申报、评优评选、综合测评相关文档，
建立 BATCH-B1 批次队列 CSV，为后续草稿生成做准备。

【参考文件（只读）】
1. knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv
   （参考队列列名格式，不允许修改）

【扫描目录（只读）】
- _references/数据库部分材料/
  重点子目录（优先扫描）：
  · 任何包含"竞赛"、"大赛"、"申报"、"评优"、"综测"、"综合素质"、"优秀学生"、"优秀毕业生"、"创新创业"、"双创"关键词的子目录或文件名

【允许修改文件列表】
1. knowledge-base/raw/first-batch-processing/manifests/batch-b1-competition-eval-queue.csv（新建）
2. docs/test-reports/completion-reports/BATCH-B1-discovery-report.md（新建）

【禁止事项】
1. 禁止修改任何已有队列 CSV（batch-a1/a2/a3）。
2. 禁止修改 knowledge-base/entries/ 下任何文件。
3. 禁止修改源文件目录（_references/）下任何文件。
4. 禁止为同一份物理文件创建重复条目。

---

### 队列 CSV 列名规范

与 batch-a1-award-aid-queue.csv 保持完全一致：
batch_id, queue_seq, source_type, material_id, source_path, file_name,
extension, knowledge_category, processing_action, value_level, timeliness,
title_guess, audience, kb_draft_id, rule_task_id, status

字段填写规则：
- batch_id: "BATCH-B1"
- queue_seq: 从 1 开始递增（规则类用 R1、R2...）
- source_type: 暂统一填 "b1-materials"
- material_id: "MAT-B1-<四位序号>"，例如 MAT-B1-0001
- source_path: 相对于 _references/ 的路径
- knowledge_category: 从以下值中选一个：
  竞赛申报 / 评优评选 / 综合测评 / 创新创业 / 学籍管理 / 奖助贷补 / 就业与毕业
  （若不确定，填"待分类"）
- processing_action: "可转知识" 或 "提炼规则后入库"
  判断标准：面向学生的说明/指南/表格→"可转知识"；评审细则/条件文件→"提炼规则后入库"
- value_level: A（核心高频）/ B（常用参考）/ C（低频/过期参考）/ D（明确过期）
- timeliness: "长期有效" / "阶段性" / "待确认"
- title_guess: 从文件名中提取，不要加扩展名
- audience: 从文件内容/路径推断；不确定填 "全体学生"
- kb_draft_id: 留空（后续草稿生成时分配，从 KB-20260324-0200 起，按序递增）
- rule_task_id: 留空（规则类条目后续分配 RULE-B1-xxx）
- status: "queued"

### 排除规则（不入队列）

1. 纯表格模板（空白表、签到表）→ 排除，在报告中注明
2. 文件名含"公示结果"且无指导性内容 → 排除
3. 已在 batch-a1/a2/a3 中覆盖的材料（通过 source_path 交叉核查）→ 排除
4. 扩展名为 .jpg/.png/.mp4 等非文档格式 → 排除

---

### 完成报告要求

路径：docs/test-reports/completion-reports/BATCH-B1-discovery-report.md

报告章节（缺一不可）：
1. **任务标识**：任务ID=BATCH-B1-DISCOVERY，执行时间，执行AI身份
2. **扫描摘要**：
   - 扫描目录列表
   - 发现文件总数 / 纳入队列数 / 排除数
3. **按 knowledge_category 分布表**：
   | 类别 | 条目数 |
4. **排除条目列表**（含排除原因）
5. **转换需求评估**：
   - 已有转换 Markdown 的文件数
   - 需要新运行 MinerU 转换的文件数（列出文件名）
6. **下一步建议**：
   - 若需要新转换：提示"需先补充 MinerU 转换后，方可进入草稿生成阶段"
   - 若转换已齐：提示"等待 Cascade L2 验收后，可直接进入 BATCH-B1-DRAFT-GEN 阶段"

完成报告写入后，回复"阶段任务完成并停止"，不要继续优化。
```

---

## 指挥官 L1 核查清单

```
□ L1-1 文件是否齐：batch-b1-competition-eval-queue.csv 已创建
□ L1-2 列名核查：与 batch-a1 列名完全一致（可用 head -1 对比）
□ L1-3 material_id 格式：全部为 MAT-B1-XXXX，无重复
□ L1-4 禁止项核查：已有 batch-a1/a2/a3 CSV 未被触碰
□ L1-5 数量合理性：纳入条目数 > 0（若为 0 则说明扫描路径有问题）
```

**L1 全通过后，上报 Cascade 做 L2 验收。**

---

## Cascade L2 验收点

1. 抽查 5 条队列条目，确认 knowledge_category / processing_action 分类合理
2. 确认 material_id 格式正确（MAT-B1-XXXX）且无重复
3. 审阅排除条目列表，确认没有误排（高价值文件被排掉）
4. 确认转换需求评估准确
5. 签字放行：进入 BATCH-B1-DRAFT-GEN 阶段

---

## 版本记录

| 版本 | 时间 | 说明 |
|------|------|------|
| v1.0 | 2026-04-03 | 初版，竞赛评优新批次 Discovery 阶段 |
