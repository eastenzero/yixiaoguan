# T3 任务: v8 INGEST — ChromaDB 全量重入库（修订版）

## ⚠️ 关键约束

1. **所有命令必须通过 SSH 执行**（格式：`ssh easten@10.80.3.165 "命令"`）
2. **绝对不要在本地 PowerShell 直接运行 curl、python、docker**
3. **不要检测本地服务**，ai-service 在远程 165 服务器上

## Step 1: 检查新文件是否已同步

```
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-01*.md 2>/dev/null | wc -l"
```

期望 ≥ 19。如果 < 19，等待 2 分钟再重试（Mutagen 同步延迟）。

## Step 2: 停止 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml stop ai-service 2>/dev/null || pkill -f uvicorn 2>/dev/null); echo STOPPED"
```

## Step 3: 清空 ChromaDB

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/clear_kb_collection.py && echo CLEARED"
```

## Step 4: 全量入库

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/batch_ingest_kb.py --yes 2>&1 | tail -5"
```

## Step 5: 重启 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml start ai-service 2>/dev/null || nohup /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 &); echo STARTED"
```

等待 8 秒：
```
ssh easten@10.80.3.165 "sleep 8 && echo READY"
```

## Step 6: 验证（通过 SSH 执行 curl，不是本地）

```
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats"
```

期望 entry_count ≥ 270。

## Step 7: 抽查公众号来源 KB

```
ssh easten@10.80.3.165 "curl -s -X POST http://localhost:8000/kb/search -H 'Content-Type: application/json' -d '{\"query\":\"通勤车时刻表\",\"top_k\":3}'"
```

## 输出

将结果写入 `kimi/ingest-v8-report.md`，包含各步骤执行结果和最终 entry_count。

## 验收标准
- batch_ingest 无异常
- entry_count ≥ 270
- 公众号来源抽查命中

请开始执行。
