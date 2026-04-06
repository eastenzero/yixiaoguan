---
id: "hotfix-port-conflict"
parent: "v4-kb-deploy"
type: "hotfix"
status: "pending"
tier: "T3"
priority: "high"
risk: "low"

scope:
  - "165服务器进程管理（无代码文件改动）"
out_of_scope:
  - "apps/"
  - "services/"
  - "vite.config.ts"

done_criteria:
  L0: "GET http://localhost:8000/health 或 /kb/stats 返回 {code:200} 且由 ai-service(uvicorn) 响应"
  L1: "ss -tlnp 确认 8000 端口由 uvicorn 占用，非 python run_api.py"
  L2: "curl http://localhost:8000/kb/stats 返回 entry_count >= 1059"

depends_on: []
created_at: "2026-04-06 13:30:00"
---

# Hotfix：恢复 ai-service 到 8000 端口

> ai-collab-control-plane 进程（pid=322326）占用了 8000 端口，导致 ai-service 被迫跑在 8001，前端 /api/chat 代理全部打到错误服务（返回 "Invalid API key"）。

## 根因

```
Port 8000 → python /home/easten/ai-collab-control-plane/phase2/src/scripts/run_api.py (pid=322326)
Port 8001 → uvicorn ai-service (pid=322903)  ← 应该在 8000
```

`vite.config.ts:35` 硬编码代理到 `localhost:8000`，无法改端口（影响所有学生）。

## 执行步骤

### Step 1：停止 ai-service (8001)

```bash
kill 322903
sleep 2
```

或通过 tmux：
```bash
tmux send-keys -t ai-service C-c
sleep 2
```

### Step 2：释放端口 8000（停止 ai-collab-control-plane）

```bash
kill 322326
sleep 2
```

验证端口已释放：
```bash
ss -tlnp | grep 8000
```
预期：无输出

### Step 3：重启 ai-service 到 8000

```bash
tmux send-keys -t ai-service "cd ~/dev/yixiaoguan/services/ai-service && source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" Enter
sleep 5
```

### Step 4：验证

```bash
curl -s http://localhost:8000/kb/stats
```
预期：`{"code":200, ..., "entry_count": ...}` 且非 `{"detail":"Invalid API key"}`

## 已知陷阱

- pid 可能在执行时已变（进程重启），用 `ss -tlnp | grep 8000` 重新确认实际 pid
- ai-collab-control-plane 可能有 supervisor/systemd 守护，杀掉后复活 → 若如此，用 `systemctl stop` 或直接告知 T1 处理
