# 知识库问题修复并行任务 - 严格验收报告（v2）

> 验收对象：BATCH-R1 / BATCH-R2 / BATCH-R3 / BATCH-R4 / BATCH-R5 交付物  
> 验收时间：2026-04-03  
> 验收原则：以仓库实物文件为准，不以口头汇总为准

---

## 一、验收范围与方法

### 1.1 实物验收文件

- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-rule-extraction-v2-dedup.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-r2-dedup-mapping.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-qa-ingestion-whitelist.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-qa-manual-review-list.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-r5-missing-source-request.csv`
- `docs/test-reports/completion-reports/KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md`
- `docs/test-reports/completion-reports/KB-REPAIR-PARALLEL-2026-04-02-FINAL-SUMMARY.md`
- `docs/test-reports/completion-reports/BATCH-R1-id-remap-plan-report.md`
- `docs/test-reports/completion-reports/BATCH-R2-rule-dedup-report.md`
- `docs/test-reports/completion-reports/BATCH-QA-completion-report.md`
- `docs/test-reports/completion-reports/BATCH-R5-missing-source-report.md`

### 1.2 数据级校验项

- CSV 行数（不含表头）
- ID 映射唯一性（R1）
- 去重映射一致性（R2）
- 白名单与复核清单字段完整性（R3）
- 缺源任务单时限与优先级一致性（R5）
- 汇总文档口径一致性（R4）

---

## 二、验收结果总览

| 批次 | 结论 | 说明 |
|------|------|------|
| R1 编号重映射 | ⚠️ 有条件通过 | 产物齐全，但映射方案存在落地风险 |
| R2 规则去重 | ✅ 通过 | 行数、mapping 与 canonical 关系一致 |
| R3 QA收口 | ⚠️ 有条件通过 | 文件齐全，但清单策略存在口径争议 |
| R4 统计回填 | ⚠️ 有条件通过 | 核心数字已修正，但文档仍有旧状态残留 |
| R5 缺源追补 | ✅ 通过 | 任务单字段完整且时限一致 |

---

## 三、通过项（已严格核对）

### 3.1 行数与交付一致

- `batch-r1-kb-id-remap-plan.csv`：42 条
- `batch-r1-kb-draft-rebuild-needed.csv`：21 条
- `batch-a1-award-aid-rule-extraction-v2-dedup.csv`：23 条
- `batch-r2-dedup-mapping.csv`：6 条
- `batch-qa-ingestion-whitelist.csv`：26 条
- `batch-qa-manual-review-list.csv`：34 条
- `batch-r5-missing-source-request.csv`：9 条

### 3.2 R2 去重一致性通过

- mapping 中 6 条 duplicate 均已从 v2 文件移除
- mapping 中 canonical 均在 v2 文件中可找到
- 原始 `batch-a1-award-aid-rule-extraction.csv` 未被覆盖

### 3.3 R5 任务单规范通过

- `priority` 全部为 `P1`
- `due_date` 全部为 `2026-04-15`
- 9 条缺源任务可直接派发

---

## 四、严格发现的问题（需整改）

## P0（阻塞执行）

### P0-1：R1 映射方案存在“一对多”冲突，不能直接批量重命名

**证据：**
- `batch-r1-kb-id-remap-plan.csv` 中 `action=remap` 共 40 条
- 其中 `old_kb_id` 出现重复 19 个（如 `KB-20260324-0061` 同时映射到 A2 和 A3）

**影响：**
- 单个旧文件无法一次重命名成两个新文件
- 若直接执行自动重命名，会导致覆盖或丢失

**整改要求（必须先完成）：**
1. 生成 `batch-r1-kb-id-remap-plan-v2.csv`，保证 `old_kb_id -> new_kb_id` 一对一（仅针对现存文件）。
2. 将无法一对一重命名的条目转入“重建清单”（`need_rebuild`），不得标 `can_rename`。
3. 在执行脚本层面强制校验：发现重复 `old_kb_id` 即中止。

---

## P1（高优先级修订）

### P1-1：R1 重建清单只覆盖 A2，未覆盖 A3

**证据：**
- `batch-r1-kb-draft-rebuild-needed.csv` 仅 21 条，均为 A2；无 A3 条目
- 但 remap 方案中 A3 有 19 条 remap

**建议：**
- 补充 A3 的重建/重命名判定，输出 `batch-r1-kb-draft-rebuild-needed-v2.csv`。

### P1-2：`SUMMARY-v2` 仍残留“QA待生成”旧文案

**证据：**
- `KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md` 仍写 `batch-qa-ingestion-whitelist.csv`、`batch-qa-manual-review-list.csv`、`BATCH-QA-completion-report.md` 为“待生成”
- 实际上述文件已存在

**建议：**
- 更新该段状态为“已生成”，避免误导后续执行。

### P1-3：编号策略文档口径不一致（A3 起始号）

**证据：**
- `BATCH-R1-id-remap-plan-report.md` 与 remap 方案采用 A3 从 `KB-0105` 起
- `BATCH-QA-completion-report.md` 建议 A3 从 `KB-0100` 起

**建议：**
- 统一全项目口径为一个版本（推荐沿用 R1 的 `0105` 起）。

### P1-4：Whitelist 包含“规则重复”类条目，策略语义需明确

**证据：**
- `batch-qa-ingestion-whitelist.csv` 中包含 10 条 `规则条目重复`

**风险：**
- 若“whitelist”被理解为“可直接入库且无冲突”，将产生执行歧义

**建议：**
- 二选一：
  1) 调整命名为 `ingestion-candidate-with-known-issues.csv`；或
  2) 将“规则重复”迁至 manual-review-list，whitelist 仅保留“无结构冲突”条目。

---

## 五、可执行整改顺序（严格版）

1. **先修 R1（阻塞项）**
   - 输出 `batch-r1-kb-id-remap-plan-v2.csv`
   - 输出 `batch-r1-kb-draft-rebuild-needed-v2.csv`
   - 完成“一对一映射”校验

2. **再修文档口径（R4 / QA）**
   - 修订 `KB-EXPANSION-PARALLEL-2026-04-02-SUMMARY-v2.md` 旧状态段
   - 统一 `BATCH-QA-completion-report.md` 与 R1 的编号策略

3. **最后执行落地动作**
   - 按 R1-v2 执行重命名（先 dry-run）
   - 替换 R2 v2 去重文件
   - 按 R5 派发缺源任务

---

## 六、最终验收结论

当前修复任务属于：**交付完成，但未达到“可无风险直接执行”标准**。

- **可直接采纳：** R2、R5
- **需先整改后执行：** R1、R4、R3（策略语义）

在完成本报告“P0 + P1”整改后，可进入下一阶段：
- 执行重命名落地
- 更新队列字段
- 按白名单推进入库

---

**报告状态：** 严格验收完成（v2）  
**建议动作：** 先修 R1-v2，再做批量执行
