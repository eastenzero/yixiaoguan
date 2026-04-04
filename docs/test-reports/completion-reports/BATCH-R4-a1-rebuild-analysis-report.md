# BATCH-R4-A1-REBUILD 分析完成报告

## 任务标识

- **任务 ID**: BATCH-R4-A1-REBUILD
- **执行时间**: 2026-04-04 02:46:07
- **执行 AI 身份**: T3

## 决策映射规则

1. **7 条有 material_id 的行**（MAT-20260324-0024~0029、MAT-20260324-0055，对应 KB-20260324-0124~0130）：原规划编号被 A3 队列占用并已被重命名，当前已分配新编号，但草稿文件从未生成，决策统一为 **`rebuild_needed`**。
2. **5 条候补行**（queue_seq=8~12）：
   - 在 `batch-a1-award-aid-queue.csv` 中检索所有 `source_type=batch2-materials` 的现有条目，比对 `source_path` 与 `file_name`；
   - 若发现相同源文件或高度重复项，决策为 **`candidate_duplicate`**（无需新建）；
   - 若未找到匹配项，判定为独立知识点，决策为 **`rebuild_needed`**（需新建）。

## 12 行决策明细表

| queue_seq | material_id | kb_draft_id | decision | decision_reason |
|-----------|-------------|-------------|----------|-----------------|
| 1 | MAT-20260324-0024 | KB-20260324-0124 | rebuild_needed | 原规划编号 KB-0061 被 A3 内容占用，当前已重分配为 KB-20260324-0124，但对应草稿文件从未生成，需从源文件重建 |
| 2 | MAT-20260324-0025 | KB-20260324-0125 | rebuild_needed | 原规划编号 KB-0062 被 A3 内容占用，当前已重分配为 KB-20260324-0125，但对应草稿文件从未生成，需从源文件重建 |
| 3 | MAT-20260324-0026 | KB-20260324-0126 | rebuild_needed | 原规划编号 KB-0063 被 A3 内容占用，当前已重分配为 KB-20260324-0126，但对应草稿文件从未生成，需从源文件重建 |
| 4 | MAT-20260324-0027 | KB-20260324-0127 | rebuild_needed | 原规划编号 KB-0064 被 A3 内容占用，当前已重分配为 KB-20260324-0127，但对应草稿文件从未生成，需从源文件重建 |
| 5 | MAT-20260324-0028 | KB-20260324-0128 | rebuild_needed | 原规划编号 KB-0065 被 A3 内容占用，当前已重分配为 KB-20260324-0128，但对应草稿文件从未生成，需从源文件重建 |
| 6 | MAT-20260324-0029 | KB-20260324-0129 | rebuild_needed | 原规划编号 KB-0066 被 A3 内容占用，当前已重分配为 KB-20260324-0129，但对应草稿文件从未生成，需从源文件重建 |
| 7 | MAT-20260324-0055 | KB-20260324-0130 | rebuild_needed | 原规划编号 KB-0067 被 A3 内容占用，当前已重分配为 KB-20260324-0130，但对应草稿文件从未生成，需从源文件重建 |
| 8 |  |  | rebuild_needed | 在 A1 队列 batch2-materials 中检索 file_name="附件1：山东省高等教育资助申请表.doc" 及对应 source_path，未找到匹配的现有条目，判定为独立知识点，需新建草稿 |
| 9 |  |  | rebuild_needed | 在 A1 队列 batch2-materials 中检索 file_name="附件3：个人承诺书、社会救助家庭经济状况核对授权.pdf" 及对应 source_path，未找到匹配的现有条目，判定为独立知识点，需新建草稿 |
| 10 |  |  | rebuild_needed | 在 A1 队列 batch2-materials 中检索 file_name="贫困认定弃权声明 (2).docx"（路径：家庭经济困难认定工作通知/附件/），未找到匹配的现有条目，判定为独立知识点，需新建草稿 |
| 11 |  |  | rebuild_needed | 在 A1 队列 batch2-materials 中检索 file_name="贫困认定弃权声明 (2).docx"（路径：家庭经济困难认定+助学金评审/），未找到匹配的现有条目，判定为独立知识点，需新建草稿 |
| 12 |  |  | rebuild_needed | 在 A1 队列 batch2-materials 中检索 file_name="附件2山东第一医科大学学生勤工助学申请表.doc" 及对应 source_path，未找到匹配的现有条目，判定为独立知识点，需新建草稿 |

## 校验结果

- 12 行决策覆盖完整性：✅（共 12 行）
- decision 枚举合规性：✅（全部 12 行仅使用 `rebuild_needed` 或 `candidate_duplicate`）
- decision_reason 填写完整性：✅（12 行全部填写，无"看文件名猜归属"描述）
- A1 CSV 对齐性：✅（`batch-a1-award-aid-queue.csv` 中对应 12 行的 `status` 已统一为 `rebuild_needed`，本次实际修改 5 行）
- A2/A3 队列未被触碰：✅
- 是否有超范围修改：否

## 遗留问题

无

## 下一步建议

等待 Cascade L2 验收后，方可根据分析结果制定重建计划。