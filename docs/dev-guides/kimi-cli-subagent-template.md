# Kimi CLI 子代理下发模板（T2内部执行）

> 用途：给 Cascade/T2 自用，不面向业务汇报。
> 目标：标准化 Kimi CLI 下发、并行执行、与验收收口。

---

## 1) 单任务下发模板（非交互）

```powershell
$env:NO_COLOR='1'
kimi --print -p "
执行任务：<TASK_ID>

必须同时读取以下文件：
1) <PRIMARY_PROMPT_FILE>
2) <TASK_FILE>

规则冲突时：以 <TASK_FILE> 为准。
你已获得‘继续’授权，直接执行，不要等待交互确认。

允许修改：
- <ALLOWED_PATH_1>
- <ALLOWED_PATH_2>

禁止修改：
- services/
- apps/
- <OTHER_FORBIDDEN_PATHS>

硬约束：
- 只能做当前任务，不得顺手修复其他问题
- 遇到源缺失或目标已存在时，单条标记 BLOCKED 并继续
- 最终报告必须写入：<REPORT_PATH>

最终仅输出四段：
STEP-PLAN
STEP-EXECUTED
STEP-CHECK
BLOCKERS
"
```

---

## 2) 并行下发模板（多任务）

> 适用：任务文件范围不重叠（无共享写路径）时。

### 并行规则

1. 先做路径冲突检查：两个任务的可写文件不能重叠。
2. 每个任务使用独立 `kimi --print -p` 调用，后台执行。
3. 记录每个后台命令 ID，分别轮询状态。
4. 任一任务失败不自动重试覆盖文件，先保留现场再诊断。

### 下发示例（PowerShell）

```powershell
# 任务A
$cmdA = "kimi --print -p \"<TASK_A_PROMPT>\""
# 任务B
$cmdB = "kimi --print -p \"<TASK_B_PROMPT>\""

# 分别后台启动（在 Cascade 中以非阻塞 run_command 执行）
# 然后保存返回的 CommandId：A=<idA>, B=<idB>
# 后续轮询：command_status(idA), command_status(idB)
```

### 何时不能并行

- 任务写同一 CSV 或同一报告文件
- 任务都要改同一目录内同名文件
- 后一任务依赖前一任务输出（存在硬前置）

---

## 3) R5 专用下发模板（Batch-3）

```text
执行 Batch-3: r5-a1-rebuild-exec。
必须同时读取并严格遵循：
1) docs/dev-guides/r5-a1-rebuild-exec-prompt-2026-04-03.md
2) .tasks/phase-1-data-foundation/p1a-kb-repair/r5-a1-rebuild-exec/_task.md
冲突规则：以 _task.md 的⚠️高风险提示为准。

你已获得“继续”授权，直接执行。
硬约束：禁止修改任何已存在草稿文件；若目标文件已存在则该条记 BLOCKED 并写明原因；不得改 services/apps；不得修改 scope 之外文件。

必须产出并更新：docs/test-reports/completion-reports/BATCH-R5-a1-rebuild-exec-report.md
报告必须满足：
- 新建+BLOCKED=12
- queue_seq 1~7（0124~0130）全有结果
- queue_seq 8~12（0131~0135）全有结果
- 必须专门说明 queue_seq 10/11（同文件名异路径）是合并还是分建以及理由

任务结束时只输出：STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
```

---

## 4) T2 验收速查（执行后）

1. 报告存在：`<REPORT_PATH>`
2. 数字约束满足（如 `新建 + BLOCKED = N`）
3. 指定分组条目全部有处置结果
4. 特殊条目说明完整（例如同名异路径）
5. 无超范围修改（重点查禁止目录与已有草稿）
6. 输出结论：通过 / 不通过 + 下一步建议
