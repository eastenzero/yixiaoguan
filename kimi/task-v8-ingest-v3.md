# T3 任务 [REVISED 192.168.100.165]: v8 INGEST — ChromaDB 全量重入库

## ⚠️ 服务器 IP: 192.168.100.165（不是 10.80.3.165）
## ⚠️ 所有命令通过 SSH 执行，不要本地运行 curl/python

## Step 1: 确认新文件已同步

```
ssh easten@192.168.100.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-01*.md 2>/dev/null | wc -l"
```
期望 ≥ 19。

## Step 2: 停止 ai-service

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml stop ai-service 2>/dev/null || pkill -f uvicorn 2>/dev/null); echo STOPPED"
```

## Step 3: 清空 ChromaDB

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/clear_kb_collection.py && echo CLEARED"
```

## Step 4: 全量入库

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/batch_ingest_kb.py --yes 2>&1 | tail -5"
```

## Step 5: 重启 ai-service

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml start ai-service 2>/dev/null || nohup /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 &); echo STARTED"
```

## Step 6: 验证（SSH 内执行 curl，不是本地）

```
ssh easten@192.168.100.165 "sleep 8 && curl -s http://localhost:8000/kb/stats"
```

期望 entry_count ≥ 270。

## Step 7: 抽查公众号来源

```
ssh easten@192.168.100.165 "curl -s -X POST http://localhost:8000/kb/search -H 'Content-Type: application/json' -d '{\"query\":\"通勤车时刻表\",\"top_k\":3}'"
```

## 输出

写入 `kimi/ingest-v8-report.md`，记录各步执行结果和最终 entry_count。

请开始执行。
