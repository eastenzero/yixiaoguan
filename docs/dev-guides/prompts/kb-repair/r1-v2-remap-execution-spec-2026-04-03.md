# R1-v2 重映射执行规范（严格版）

## 1. 目标

本规范用于修复 R1 阶段的阻塞问题：`old_kb_id` 一对多映射，导致无法安全执行批量重命名。

---

## 2. 输入与输出文件

### 2.1 输入文件

- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed.csv`
- `knowledge-base/entries/first-batch-drafts/`

### 2.2 输出文件（本轮必须产出）

- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-id-remap-plan-v2.csv`
- `knowledge-base/raw/first-batch-processing/manifests/batch-r1-kb-draft-rebuild-needed-v2.csv`

> 模板文件：
> - `batch-r1-kb-id-remap-plan-v2.template.csv`
> - `batch-r1-kb-draft-rebuild-needed-v2.template.csv`

---

## 3. 强约束规则

1. `batch-r1-kb-id-remap-plan-v2.csv` 中，`old_kb_id` 只允许出现一次（严格一对一）。
2. 若同一 `old_kb_id` 对应多个候选目标，最多保留 1 条 `action=rename`，其余必须转入 `rebuild-needed-v2`。
3. `KB-REX-*` 条目禁止进入重命名动作。
4. `status` 仅允许：
   - `can_rename`：源文件存在且一对一映射成立
   - `need_rebuild`：源文件不存在或发生一对多冲突无法直接重命名
5. 不允许修改 `services/`、`apps/` 代码。
6. 不允许删除任何历史文件。

---

## 4. 字段定义

## 4.1 `batch-r1-kb-id-remap-plan-v2.csv`

字段：
- `source_batch`
- `material_id`
- `old_kb_id`
- `new_kb_id`
- `action`（`rename` / `keep`）
- `reason`

## 4.2 `batch-r1-kb-draft-rebuild-needed-v2.csv`

字段：
- `source_batch`
- `material_id`
- `old_kb_id`
- `target_new_kb_id`
- `source_path`
- `status`（`can_rename` / `need_rebuild`）
- `decision_reason`
- `next_action`

---

## 5. 验收门槛（全部通过才算完成）

1. `remap-plan-v2` 中 `old_kb_id` 去重后数量 == 总行数。
2. 所有 `action=rename` 条目都能在草稿目录找到唯一源文件。
3. 所有无法唯一重命名的条目都在 `rebuild-needed-v2` 且 `status=need_rebuild`。
4. 文档中明确列出：
   - 可直接重命名数量
   - 必须重建数量
   - 被跳过的 `KB-REX-*` 数量

---

## 6. 建议执行顺序

1. 先生成 `remap-plan-v2`（只做映射决策，不重命名文件）。
2. 再生成 `rebuild-needed-v2`（补齐冲突与缺失处理）。
3. 最后做 dry-run 校验（仅模拟，不落盘重命名）。

---

## 7. 当前判定（供指挥官）

- 当前唯一 **P0 阻塞项**：R1 一对多映射，未满足安全重命名条件。
- 其余问题主要为 **P1 文档口径与策略语义**，不阻塞修复方案产出，但会影响后续执行一致性。
