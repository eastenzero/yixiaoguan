# T3 任务: 重启 ai-service 并验证入库结果

## 服务器: 192.168.100.165
## ⚠️ 所有命令通过 SSH 执行

## Step 1: 强制杀掉旧进程（运行在 root，需要 sudo）

```
ssh easten@192.168.100.165 "sudo pkill -f uvicorn; sudo pkill -f 'ai.service\|ai_service\|main:app'; echo KILLED"
```

等待 3 秒确认进程退出：
```
ssh easten@192.168.100.165 "sleep 3 && pgrep -f uvicorn | wc -l"
```
期望返回 0。

## Step 2: 重新启动 ai-service

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan/services/ai-service && nohup /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai-service.log 2>&1 & echo STARTED PID:$!"
```

## Step 3: 等待启动完成并验证

```
ssh easten@192.168.100.165 "sleep 8 && curl -s http://localhost:8000/kb/stats"
```

期望 entry_count = 279（v7 的 259 + v8 新增 19 = 278，实际入库 279）。

## Step 4: 功能验证

```
ssh easten@192.168.100.165 "curl -s -X POST http://localhost:8000/kb/search -H 'Content-Type: application/json' -d '{\"query\":\"通勤车时刻表\",\"top_k\":3}' | python3 -c 'import sys,json; d=json.load(sys.stdin); print([(r.get(\"entry_id\",\"\"),r.get(\"score\",0)) for r in d.get(\"data\",d.get(\"results\",[]))[:3]])'"
```

期望命中 KB-20260410-0101（通勤车时刻表）。

## 输出

追加到 `kimi/ingest-v8-report.md` 末尾：

```markdown
## 重启验证

| 项目 | 结果 |
|------|------|
| 进程重启 | ✅/❌ |
| entry_count | 279 ✅/❌ |
| 通勤车查询命中 | ✅/❌ |

结论: PASS / FAIL
```

请开始执行。
