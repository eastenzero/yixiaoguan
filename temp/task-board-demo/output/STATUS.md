# 任务状态板 (Task Evidence Board)

> 🕐 自动生成于 **2026-04-03 17:36**
> ⚠️  本文件由脚本派生，请勿手动编辑。修改任务请编辑 `tasks/` 目录下对应文件。

## 总体进度

```
  kb-repair             ███████████████░  74/81 (91%)
  kb-expansion          ░░░░░░░░░░░░░░░░  0/1 (0%)
  ────────────────────  ────────────────  ──────────────
  全局合计                  ██████████████░░  74/82 (90%)
```

## 任务明细

### 🔄 `KB-REPAIR` — 知识库修复阶段（第一批次遗留问题）

进度：`██████████████████░░` **74/81 (91%)**

| task_id | 任务名称 | 状态 | 进度 | 优先级 | 依赖 | 执行者 | 报告 |
|:--------|:--------|:-----|:-----|:------:|:-----|:-------|:----:|
| `R1` | [来源溯源重映射方案（v3）](docs/dev-guides/prompts/kb-repair/r1-v3-provenance-remap-prompt-2026-04-03.md) | ✅ `L2-pass` | `████████` 1/1 (100%) | 🔴 | — | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-R1-v3-provenance-remap-report.md) |
| `R2` | [文件重命名 + frontmatter 同步（21 文件）](docs/dev-guides/prompts/kb-repair/r2-rename-execution-prompt-2026-04-03.md) | ✅ `L2-pass` | `████████` 21/21 (100%) | 🔴 | `R1` | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-R2-rename-execution-report.md) |
| `R3` | [队列字段同步（A3×19 + A2×21）](docs/dev-guides/prompts/kb-repair/r3-queue-sync-prompt-2026-04-03.md) | ✅ `L2-pass` | `████████` 40/40 (100%) | 🔴 | `R2` | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-R3-queue-sync-report.md) |
| `R4` | [A1 队列修复 + 候补条目分析](docs/dev-guides/prompts/kb-repair/r4-a1-rebuild-analysis-prompt-2026-04-03.md) | ✅ `L2-pass` | `████████` 12/12 (100%) | 🔴 | `R2` | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-R4-a1-rebuild-analysis-report.md) |
| `R5` | [A1 草稿重建（7 个 MAT 条目）](docs/dev-guides/prompts/kb-repair/r5-a1-rebuild-exec-prompt-2026-04-03.md) | 🔄 `in_progress` | `░░░░░░░░` 0/7 (0%) | 🔴 | `R4` | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md) |

### ⏳ `KB-EXPANSION` — 知识库扩量阶段（新批次 B1+）

进度：`░░░░░░░░░░░░░░░░░░░░` **0/1 (0%)**

| task_id | 任务名称 | 状态 | 进度 | 优先级 | 依赖 | 执行者 | 报告 |
|:--------|:--------|:-----|:-----|:------:|:-----|:-------|:----:|
| `B1-DISC` | [竞赛/评优新批次文件扫描建档](docs/dev-guides/prompts/kb-expansion/batch-b1-competition-eval-discovery-prompt-2026-04-03.md) | ⏳ `pending` | `░░░░░░░░` 0/1 (0%) | 🟡 | `KB-REPAIR` | sub-agent | [📄](docs/test-reports/completion-reports/BATCH-B1-discovery-report.md) |

## 待处理任务 & 完成标准

### ⏳ `B1-DISC` — 竞赛/评优新批次文件扫描建档  `0/1 (0%)`

- [ ] batch-b1-competition-eval-queue.csv 已创建，列名与 batch-a1 一致
- [ ] material_id 格式为 MAT-B1-XXXX，无重复
- [ ] 排除条目列表已记录（含排除原因）
- [ ] 转换需求评估已完成（是否需要补充 MinerU 转换）
- [ ] Cascade L2 抽查 5 条分类通过

### 🔄 `R5` — A1 草稿重建（7 个 MAT 条目）  `0/7 (0%)`

- [ ] KB-0124.md 存在，entry_id=KB-20260324-0124，material_id=MAT-20260324-0024
- [ ] KB-0125.md 存在，entry_id=KB-20260324-0125，material_id=MAT-20260324-0025
- [ ] KB-0126.md 存在，entry_id=KB-20260324-0126，material_id=MAT-20260324-0026
- [ ] KB-0127.md 存在，entry_id=KB-20260324-0127，material_id=MAT-20260324-0027
- [ ] KB-0128.md 存在，entry_id=KB-20260324-0128，material_id=MAT-20260324-0028
- [ ] KB-0129.md 存在，entry_id=KB-20260324-0129，material_id=MAT-20260324-0029
- [ ] KB-0130.md 存在，entry_id=KB-20260324-0130，material_id=MAT-20260324-0055
- [ ] A1 queue 对应 7 行 status 已从 rebuild_needed 改为 completed

---

## 图例

- ⏳ `pending`
- 🔄 `in_progress`
- 🚫 `blocked`
- 🔵 `L1-pass`
- ✅ `L2-pass`
- ⏭️ `skipped`

*由 [`generate_status.py`](../generate_status.py) 生成 · 数据源: `tasks/`*