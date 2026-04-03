# prompts/kb-repair — 知识库修复阶段提示词

**阶段状态**：✅ 2026-04 执行完毕，归档存放。

## 文件列表

| 文件 | 任务 | 状态 |
|------|------|------|
| `r1-v2-remap-execution-spec-2026-04-03.md` | R1-v2 重映射规格说明（已被 v3 取代） | 已归档 |
| `r1-v3-provenance-remap-prompt-2026-04-03.md` | R1-v3 来源溯源重映射（子 agent 执行） | ✅ 完成 |
| `kb-repair-p1-single-task-prompts-2026-04-03.md` | P1 单任务提示词包（三项修复） | ✅ 完成 |
| `r2-rename-execution-prompt-2026-04-03.md` | R2-RENAME 21 文件重命名 + frontmatter 同步 | ✅ 完成 |
| `r3-queue-sync-prompt-2026-04-03.md` | R3-QUEUE-SYNC 队列字段同步（A3×19 + A2×21） | ✅ 完成 |
| `r4-a1-rebuild-analysis-prompt-2026-04-03.md` | R4-A1 队列修复 + 候补条目分析 | ✅ 完成 |
| `r5-a1-rebuild-exec-prompt-2026-04-03.md` | R5-A1 7 个草稿文件重建 | 执行中 |

## 执行顺序

R1-v3 → R2-RENAME → R3-QUEUE-SYNC → R4-A1-REBUILD → R5-A1-REBUILD-EXEC → R5b（候补条目）
