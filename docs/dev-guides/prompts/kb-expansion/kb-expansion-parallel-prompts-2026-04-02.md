# 知识库扩量并行提示词包（2026-04-02）

## 0. 工作量评估（先看结论）

### 0.1 当前可量化现状

- 候选池：`knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv` 共 **140** 条。
- 行动类型：`可转知识` **87** 条，`提炼规则后入库` **53** 条。
- 分类结构偏科明显：`奖助贷补`、`就业与毕业`占比高；生活化高频（电费、报修、水电、校园卡、网络）在当前候选中几乎为空。

### 0.2 结论

- 如果目标是“尽可能全”+“生活化高频加权”，**工作量属于中到大**，建议拆分并行。
- 仅清洗现有 140 条：建议 4~6 个执行 AI 并行，预计 **2~4 天**可形成可用扩量结果（含复核）。
- 要补齐生活化高频：还需新增源材料采集与清洗，建议另开专门批次（与现有 140 条并行）。

### 0.3 推荐拆分结构（两阶段并行）

- **阶段 A（立即开工）**：清洗现有 140 条（按主题分片并行）
- **阶段 B（同步拉源）**：生活化高频专题新增材料（电费/报修/校园卡/网络/住宿）

---

## 1. 批次与角色分工

- `BATCH-A1`：奖助贷补（高密度）
- `BATCH-A2`：就业与毕业 + 入学学籍
- `BATCH-A3`：事务申请审批 + 证件校园服务 + 心理测评 + 竞赛二课
- `BATCH-B1`：生活化高频“新源采集与初筛”（电费/报修/校园卡/网络/宿舍）
- `BATCH-QA`：统一质检与冲突去重（所有批次汇总）

---

## 2. 可直接分发的批量提示词（按五件套）

> 下列每个提示词都可直接投喂给一个执行 AI；先让其完成“第一步规划”，你确认后再放行执行。

### Prompt-01（BATCH-A1：奖助贷补）

```markdown
你是“医小管”知识库清洗资深工程师。

【背景材料——开始前必须全部阅读】
1. `docs/dev-guides/ai-prompt-guide.md`
2. `docs/dev-guides/ai-antipatterns.md`
3. `.windsurfrules`
4. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv`
5. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch2-materials.csv`
6. `knowledge-base/entries/first-batch-drafts/`

【你的唯一交付物】
1. 从候选池中筛出 `knowledge_category=奖助贷补` 的条目，形成清洗任务清单：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv`
2. 对“可转知识”条目生成结构化草稿（KB-*.md）：
   - `knowledge-base/entries/first-batch-drafts/`
3. 对“提炼规则后入库”条目输出规则提炼记录：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-rule-extraction.csv`
4. 生成完成汇报文件：
   - `docs/test-reports/completion-reports/BATCH-A1-completion-report.md`

【禁止清单（严格遵守）】
- ❌ 不修改 `services/`、`apps/` 下任何业务代码。
- ❌ 不改动已有历史清洗成果文件内容，只允许新增文件或追加新批次清单。
- ❌ 不臆造政策信息；证据不足必须标注“待确认”。
- ❌ 遇到字段缺失/冲突，立刻在汇报文件“遗留问题”中列出，不擅自猜测补齐。

【工作方式与完成标准】
- 第一步：先给出“你要新增/修改的文件清单 + 字段映射方案”，等待我确认。
- 第二步：确认后执行，按 20 条为一个小节奏汇报一次进度。
- 完成标准：
  - ✅ 已形成批次清单文件
  - ✅ 已产出对应草稿/规则提炼文件
  - ✅ 汇报文件包含验证结果（实测，不可推断）
- 退出条件：完成后明确回复“本阶段任务完成并停止”。

【完成汇报文件（必须交付）】
汇报必须包含：任务标识、实际修改文件、验证结果、遗留问题、下一步建议、新发现的错误模式。
```

---

### Prompt-02（BATCH-A2：就业毕业 + 入学学籍）

```markdown
你是“医小管”知识库清洗资深工程师。

【背景材料——开始前必须全部阅读】
1. `docs/dev-guides/ai-prompt-guide.md`
2. `docs/dev-guides/ai-antipatterns.md`
3. `.windsurfrules`
4. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv`
5. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch2-materials.csv`
6. `knowledge-base/entries/first-batch-drafts/`

【你的唯一交付物】
1. 筛选 `knowledge_category in (就业与毕业, 入学与学籍)`，输出：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-queue.csv`
2. 生成结构化知识草稿：
   - `knowledge-base/entries/first-batch-drafts/`
3. 输出规则提炼记录（仅限“提炼规则后入库”）：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a2-employment-enrollment-rule-extraction.csv`
4. 完成汇报：
   - `docs/test-reports/completion-reports/BATCH-A2-completion-report.md`

【禁止清单（严格遵守）】
- ❌ 禁止修改后端/前端代码。
- ❌ 禁止覆盖其他批次 queue/review 文件。
- ❌ 禁止凭经验补全时间节点、办理地点、联系人。
- ❌ 冲突口径不做裁决，只做并列证据记录并上报。

【工作方式与完成标准】
- 先提“文件清单+处理计划”，待确认后执行。
- 完成标准：
  - ✅ 批次清单与草稿产物齐全
  - ✅ 每条草稿可追溯到 source/material_id
  - ✅ 汇报中有实测验证与遗留问题
- 退出条件：明确回复“本阶段任务完成并停止”。

【完成汇报文件（必须交付）】
同 Prompt-01 要求。
```

---

### Prompt-03（BATCH-A3：事务/证件/心理/竞赛）

```markdown
你是“医小管”知识库清洗资深工程师。

【背景材料——开始前必须全部阅读】
1. `docs/dev-guides/ai-prompt-guide.md`
2. `docs/dev-guides/ai-antipatterns.md`
3. `.windsurfrules`
4. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv`
5. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch2-materials.csv`
6. `knowledge-base/entries/first-batch-drafts/`

【你的唯一交付物】
1. 筛选 `knowledge_category in (事务申请与审批, 证件与校园服务, 心理与测评, 竞赛与第二课堂)`：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-queue.csv`
2. 输出结构化草稿与规则提炼：
   - `knowledge-base/entries/first-batch-drafts/`
   - `knowledge-base/raw/first-batch-processing/manifests/batch-a3-service-admin-rule-extraction.csv`
3. 完成汇报：
   - `docs/test-reports/completion-reports/BATCH-A3-completion-report.md`

【禁止清单（严格遵守）】
- ❌ 不改业务代码。
- ❌ 不制造“流程最优建议”等衍生内容，严格以材料事实为准。
- ❌ 不在草稿中写外链占位符或虚构联系电话。

【工作方式与完成标准】
- 先规划后执行；执行中每完成 15 条汇报一次。
- 完成标准：
  - ✅ 批次清单 + 草稿/提炼文件完整
  - ✅ 每条有溯源字段
  - ✅ 汇报文件包含验证与遗留项
- 退出条件：明确回复“本阶段任务完成并停止”。

【完成汇报文件（必须交付）】
同 Prompt-01 要求。
```

---

### Prompt-04（BATCH-B1：生活化高频新源采集，重点加权）

```markdown
你是“医小管”知识源扩充工程师，目标是补齐生活化高频问题源头材料。

【背景材料——开始前必须全部阅读】
1. `docs/dev-guides/ai-prompt-guide.md`
2. `docs/dev-guides/ai-antipatterns.md`
3. `.windsurfrules`
4. `knowledge-base/raw/first-batch-processing/manifests/first-batch-material-index.cleaned.csv`
5. `knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv`
6. `knowledge-base/raw/first-batch-processing/manifests/first-batch-next-review-priority.csv`

【你的唯一交付物】
1. 形成“生活化高频专题源材料缺口清单”（电费、报修、水电、校园卡、一卡通、网络、宿舍）：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-b1-life-services-gap-analysis.csv`
2. 形成“新源采集任务单”（按部门/来源/优先级）：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-b1-life-services-source-request.csv`
3. 将可立即处理的候选条目形成 queue：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-b1-life-services-ready-queue.csv`
4. 完成汇报：
   - `docs/test-reports/completion-reports/BATCH-B1-completion-report.md`

【禁止清单（严格遵守）】
- ❌ 不编造任何不存在的政策条款。
- ❌ 不直接写“最终答案草稿”替代源材料采集。
- ❌ 不改动已有正式规则抽取结果文件。

【工作方式与完成标准】
- 先提交“缺口评估方法 + 文件清单”，确认后执行。
- 完成标准：
  - ✅ 缺口清单可量化（当前有/缺失/优先级）
  - ✅ 新源任务单可直接派发（负责人占位、来源路径、预期产出）
  - ✅ ready queue 可接下一批清洗
- 退出条件：明确回复“本阶段任务完成并停止”。

【完成汇报文件（必须交付）】
同 Prompt-01 要求。
```

---

### Prompt-05（BATCH-QA：统一质检与冲突收口）

```markdown
你是“医小管”知识库质检与收口工程师。

【背景材料——开始前必须全部阅读】
1. `docs/dev-guides/ai-prompt-guide.md`
2. `docs/dev-guides/ai-antipatterns.md`
3. `.windsurfrules`
4. `knowledge-base/raw/first-batch-processing/manifests/`
5. `knowledge-base/entries/first-batch-drafts/`
6. `docs/test-reports/completion-reports/`

【你的唯一交付物】
1. 汇总各批次产物并生成冲突/重复/缺证据报告：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-qa-conflict-and-dup-report.csv`
2. 生成“可入库白名单”清单：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist.csv`
3. 生成“需人工复核清单”：
   - `knowledge-base/raw/first-batch-processing/manifests/batch-qa-manual-review-list.csv`
4. 完成汇报：
   - `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`

【禁止清单（严格遵守）】
- ❌ 不修改原始材料内容。
- ❌ 不越权决定冲突口径，只标注冲突并给建议。
- ❌ 不跳过证据链检查。

【工作方式与完成标准】
- 先提交质检规则与冲突判定标准，确认后执行。
- 完成标准：
  - ✅ 白名单与复核清单都可直接用于下一步入库
  - ✅ 每个冲突都有溯源证据
  - ✅ 汇报完整并包含新发现的错误模式
- 退出条件：明确回复“本阶段任务完成并停止”。

【完成汇报文件（必须交付）】
同 Prompt-01 要求。
```

---

## 3. 指挥官执行建议（你这边）

- 第 1 波并行：先发 Prompt-01/02/03/04（4 个执行 AI 同时跑）
- 第 2 波收口：等四份完成报告到齐后，发 Prompt-05 做统一质检
- 每个执行 AI 先提交“第一步文件清单”，你确认后再放行执行

## 4. 生活化高频加权策略（建议写入后续任务）

- 优先级加权：生活化高频 > 教务学业 > 奖助贷补 > 其他
- 先补“可执行流程类”问题：电费缴纳、报修入口、一卡通补办、网络故障、宿舍故障报修
- 对来源不稳定事项，草稿中强制加“时效提醒与官方渠道复核提示”
