# Kiro CLI 子代理使用指南（T2 Foreman 角色）

> **用途**: T1 (Cascade) 下发任务后，T2 (Kiro CLI) 接收并分发给 T3 (Kimi Code) 执行。  
> **原则**: T2 只做任务分发 + L0-L2 验收，不直接修改业务代码。

---

## 角色定义

| 层级 | 工具 | 职责 |
|------|------|------|
| T1 | Cascade (Windows) | 任务分解、编排、最终 L3 验收 |
| **T2** | **Kiro CLI (165 服务器)** | 接收 T1 任务包、分发给 T3、做 L0-L2 机器验收 |
| T3 | Kimi Code (165 服务器) | 实际执行：写代码、操作文件、运行命令 |

---

## 1) 从 T1 接收任务

T1 (Cascade) 会在 Windows 端创建任务文件，通过 Mutagen 同步到 165 的 `~/dev/yixiaoguan/`。  
T2 (Kiro) 收到 T1 下发通知后，读取对应 `_task.md` 文件开始分发。

**在 165 上确认任务文件已同步**:
```bash
ls -lh ~/dev/yixiaoguan/.tasks/<task-dir>/
cat ~/dev/yixiaoguan/.tasks/<task-dir>/<task-id>/_task.md
```

---

## 2) 单任务下发到 T3（Kimi Code）

Kiro CLI (T2) 在 165 上使用以下模板把任务子包发给 Kimi Code (T3) 执行。

### 实际验证过的调用语法

**Kiro CLI (T2) 非交互模式**（已验证 @ 165）：
```bash
~/.local/bin/kiro-cli chat --no-interactive --trust-all-tools "INPUT"
```

**Kimi (T3) 非交互模式**（已验证 @ 165）：
```bash
~/.local/bin/kimi --print -p "PROMPT"
```

### T2 (Kiro) 下发 T3 (Kimi) 的完整模板
```bash
# 在 165 服务器上，T2 (Kiro) 调用 T3 (Kimi)
cd ~/dev/yixiaoguan

~/.local/bin/kiro-cli chat --no-interactive --trust-all-tools "
你是 T2 Foreman，当前任务：<TASK_ID>。

步骤1: 读取任务文件
  cat .tasks/<task-dir>/<task-id>/_task.md

步骤2: 调用 T3 (Kimi Code) 执行任务
  运行以下命令（使用完整路径）：
  NO_COLOR=1 ~/.local/bin/kimi --print -p \"<T3_PROMPT>\" \
    > /tmp/kimi-<task-id>.log 2>&1
  等待完成后输出 /tmp/kimi-<task-id>.log

步骤3: 验收 L0/L1/L2（按 _task.md 的 done_criteria 执行）
  L0: 检查 _report.md 存在性
  L1: 静态检查（JSON/grep 等）
  L2: 运行时检查（curl 等）

步骤4: 输出验收结论给 T1
"
```

---

## 3) 并行下发多个 T3 子任务

> **前提**: 两个任务的 `scope` 可写路径不重叠。

```bash
# 任务 A（后台执行）
~/.local/bin/kiro-cli chat --no-interactive --trust-all-tools "<TASK_A_PROMPT>" \
  > /tmp/kiro-taskA.log 2>&1 &
PID_A=$!

# 任务 B（后台执行）
~/.local/bin/kiro-cli chat --no-interactive --trust-all-tools "<TASK_B_PROMPT>" \
  > /tmp/kiro-taskB.log 2>&1 &
PID_B=$!

# 等待并检查
wait $PID_A && echo "Task A done" || echo "Task A FAILED"
wait $PID_B && echo "Task B done" || echo "Task B FAILED"

# 查看输出
cat /tmp/kiro-taskA.log
cat /tmp/kiro-taskB.log
```

### 何时不能并行

- 两个任务都要写同一个文件（如同一个 `.conf` 或 `.json`）
- 后一任务依赖前一任务的产出（存在硬前置 `depends_on`）
- 任务都涉及重启同一 Docker 容器

---

## 4) T2 向 T3 (Kimi Code) 嵌套调用（已验证语法）

```bash
# T2 (Kiro) 在 165 上调用 T3 (Kimi Code)，使用完整路径
cd ~/dev/yixiaoguan

NO_COLOR=1 ~/.local/bin/kimi --print -p "
你是 T3 执行器，当前任务：<TASK_ID>。

必须同时读取：
1) .teb/antipatterns.md
2) .tasks/<task-dir>/<task-id>/_task.md

规则冲突时以 _task.md 为准。
你已获得继续授权，直接执行。

允许修改路径（scope）：<ALLOWED_PATHS>
禁止修改：apps/ services/ <OTHER_FORBIDDEN>

报告写入：.tasks/<task-dir>/<task-id>/_report.md

仅输出：STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
" > /tmp/kimi-<task-id>.log 2>&1

cat /tmp/kimi-<task-id>.log
```

---

## 5) T2 验收速查（L0-L2，机器可执行）

T3 执行完后，T2 (Kiro) 按以下步骤做本地验收，**有一项不通过就标记为 FAIL 并上报 T1**：

```bash
# L0: 报告文件存在
test -f ~/dev/yixiaoguan/.tasks/<task-dir>/<task-id>/_report.md && echo "L0 PASS" || echo "L0 FAIL"

# L1: 静态检查（根据任务 done_criteria.L1 执行）
# 示例：JSON 格式验证
python3 -m json.tool ~/dev/yixiaoguan/deploy/materials/material-index.json > /dev/null && echo "L1 PASS" || echo "L1 FAIL"

# L2: 运行时检查（根据任务 done_criteria.L2 执行）
# 示例：HTTP 访问
curl -s -o /dev/null -w "%{http_code}" http://192.168.100.165/materials/student-handbook.pdf
```

---

## 6) 上报 T1 的标准格式

T2 完成所有子任务验收后，向 T1 汇报：

```
T2 Batch-<N> 验收报告

任务 <TASK_ID>:
  L0: PASS / FAIL — <说明>
  L1: PASS / FAIL — <说明>
  L2: PASS / FAIL — <说明>
  _report.md: 已存在 / 缺失

结论: PASS（可发布下一 batch） / BLOCKED（见 BLOCKERS 说明）

BLOCKERS:
- <具体阻塞原因与建议>
```

---

## 7) 常见问题排查

| 问题 | 排查命令 | 解决 |
|------|----------|------|
| Kiro CLI 命令未找到 | `which kiro-cli` 或直接用全路径 `~/.local/bin/kiro-cli` | 安装在 `~/.local/bin/`，不在系统 PATH 需用全路径 |
| Kimi CLI 命令未找到 | `which kimi` 或直接用全路径 `~/.local/bin/kimi` | 同上 |
| Nginx 容器无法读取新文件 | `docker exec yx_nginx ls /usr/share/nginx/html/materials/` | 检查 volume 映射 + 文件权限 chmod 644 |
| curl 返回 403 | `docker exec yx_nginx ls -la /usr/share/nginx/html/materials/` | chmod 644 文件 |
| curl 返回 404 | `grep 'location /materials/' ~/dev/yixiaoguan/deploy/nginx/conf.d/student.conf` | 检查 conf 是否正确，重建容器 |
