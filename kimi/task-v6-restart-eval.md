# T3 任务: 重启 ai-service + 重跑 RAG-EVAL

## 背景
Scope Guard 已在本地实现，需要：
1. 确认 165 服务器上文件已同步（通过 Mutagen 自动同步）
2. 重启 ai-service 使新代码生效
3. 重跑 eval 验证指标达标

## 执行步骤

### Step 1: 确认服务器文件已同步

在 165 服务器（easten@192.168.100.165）上验证：
```bash
# 检查 scope_guard.py 是否存在
ls -la /home/easten/dev/yixiaoguan/services/ai-service/app/core/scope_guard.py

# 检查 kb.py 是否包含 scope_guard 导入
grep -n "scope_guard\|is_out_of_scope" /home/easten/dev/yixiaoguan/services/ai-service/app/api/kb.py | head -5
```

### Step 2: 检查 ai-service 管理方式

```bash
# 方法1: 查找 systemd 服务
ls /etc/systemd/system/ 2>/dev/null | grep -i ai
systemctl list-units --type=service 2>/dev/null | grep -i ai

# 方法2: 查找启动脚本
ls /home/easten/dev/yixiaoguan/*.sh 2>/dev/null
ls /home/easten/dev/yixiaoguan/scripts/*.sh 2>/dev/null | grep -i start
```

### Step 3: 重启 ai-service

根据 Step 2 的发现选择重启方式：

**如果有 systemd 服务**：
```bash
echo "ZhaYeFan05.07.14" | sudo -S systemctl restart <service-name>
sleep 5
systemctl status <service-name>
```

**如果没有 systemd 服务**（直接 kill + 重启）：
ai-service 目前以 root 身份运行在 /usr/local/bin/uvicorn，PID 为 1656619（或其替代进程）。

尝试以下方式发送 SIGHUP 信号触发热重载（如果 uvicorn 支持）：
```bash
# 获取当前 PID
UVPID=$(pgrep -f "uvicorn main:app" | head -1)
echo "Current uvicorn PID: $UVPID"

# 发送 SIGHUP 触发热重载
echo "ZhaYeFan05.07.14" | sudo -S kill -HUP $UVPID
sleep 5
echo "Hot reload signal sent"
```

如果 SIGHUP 不支持，记录"需要手动重启，请联系 T1"，并跳过 Step 4。

### Step 4: 验证 ai-service 正常运行

```bash
curl -s http://localhost:8000/kb/stats
```

期望返回：`{"code":200,...,"entry_count":239,...}`

### Step 5: 快速验证 Scope Guard 生效

```bash
# 测试：北京大学图书馆应该被拦截（返回空结果）
curl -s "http://localhost:8000/kb/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"北京大学图书馆几点开门","top_k":3}' | python3 -c "import sys,json; d=json.load(sys.stdin); print('results count:', len(d.get('data',{}).get('results',d.get('data',[]))))"

# 测试：山一大图书馆应该正常返回
curl -s "http://localhost:8000/kb/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"山一大图书馆几点开门","top_k":3}' | python3 -c "import sys,json; d=json.load(sys.stdin); print('results count:', len(d.get('data',{}).get('results',d.get('data',[]))))"
```

期望：北京大学查询返回 0 条结果，山一大查询返回 ≥ 1 条结果。

### Step 6: 重跑完整 RAG-EVAL

```bash
cd /home/easten/dev/yixiaoguan
/home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v2.py
```

### Step 7: 输出报告内容

读取 `scripts/eval/eval-report-v2.md` 并完整输出其内容。

## 期望结果
- Recall@5 ≥ 80% ✅
- 拒答准确率 ≥ 90% ✅（修复了北京大学/山东大学图书馆误命中问题后应可达到）

## 注意
- 如果 ai-service 无法自动重启，请在报告中明确说明，T1 将另行安排
- 不要修改任何 KB 文件或 ChromaDB 数据
