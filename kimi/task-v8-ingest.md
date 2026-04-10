# T3 任务: v8 INGEST — ChromaDB 全量重入库

## 重要：所有命令必须通过 SSH 在远程服务器执行

```
ssh easten@10.80.3.165 "命令"
```

**不要在本地直接执行 curl 或 python！**

## 背景
- v7 已入库 259条 / 290 chunks
- v8 新增 19 条 KB（KB-20260410-0101~0119），QA PASS
- 本任务将全量重入库，预期 entry_count ≥ 270

## Step 1: 确认新文件已同步到服务器

```
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-01*.md 2>/dev/null | wc -l"
```
期望 ≥ 19。如果少于 19，等待 Mutagen 同步（1-2 分钟后重试）。

## Step 2: 停止 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml stop ai-service 2>/dev/null || sudo systemctl stop ai-service 2>/dev/null || pkill -f 'uvicorn\|gunicorn' 2>/dev/null; echo 'stop done'"
```

## Step 3: 清空 ChromaDB 并全量入库

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/clear_kb_collection.py && echo 'clear done'"
```

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/batch_ingest_kb.py --yes 2>&1 | tail -20"
```

## Step 4: 重启 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml start ai-service 2>/dev/null || sudo systemctl start ai-service 2>/dev/null || nohup /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python -m uvicorn services.ai-service.app.main:app --host 0.0.0.0 --port 8000 &; echo 'start done'"
```

等待 5 秒再验证：
```
ssh easten@10.80.3.165 "sleep 5 && curl -s http://localhost:8000/kb/stats"
```

## Step 5: 验证入库结果

```
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats | python3 -m json.tool"
```
期望 entry_count ≥ 270。

抽查 5 条新入库的公众号来源 KB：
```
ssh easten@10.80.3.165 "curl -s -X POST http://localhost:8000/kb/search -H 'Content-Type: application/json' -d '{\"query\":\"通勤车\",\"top_k\":3}' | python3 -m json.tool"
```

## 输出

将结果写入 `kimi/ingest-v8-report.md`:

```markdown
# INGEST V8 Report

时间: YYYY-MM-DD
新增: 19 条 KB（KB-20260410-0101~0119）

## 验收

| 项目 | 预期 | 实际 | 状态 |
|------|------|------|------|
| 新文件同步数 | ≥19 | | |
| batch_ingest 无异常 | ✅ | | |
| entry_count | ≥270 | | |
| 公众号来源抽查 | 命中 | | |

## 结论: PASS / FAIL
```

请开始执行。
