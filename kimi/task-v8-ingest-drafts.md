# T3 任务: v8 INGEST — first-batch-drafts 432条全量入库

## ⚠️ 所有命令通过 SSH 执行
```
ssh easten@10.80.3.165 "命令"
```

## 背景
- 现有正式 KB: knowledge-base/entries/ 下已有 KB-20260410-0101~0119（19条）
- 新增草稿: first-batch-drafts/ 下 KB-20260410-0120~0449（432条），格式已全部通过 QA
- 目标：将 432 条草稿移入正式目录，全量重新入库 ChromaDB

## Step 1: 确认草稿文件已同步到服务器

```
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md 2>/dev/null | wc -l"
```

期望 ≥ 430。如果 < 430，等待 Mutagen 同步（最多 3 分钟）：
```
ssh easten@10.80.3.165 "sleep 180 && ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md | wc -l"
```

## Step 2: 将草稿移入正式目录

```
ssh easten@10.80.3.165 "cp /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md /home/easten/dev/yixiaoguan/knowledge-base/entries/ && echo COPY_DONE && ls /home/easten/dev/yixiaoguan/knowledge-base/entries/KB-*.md | wc -l"
```

期望正式目录文件数 ≥ 450。

## Step 3: 停止 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml stop ai-service 2>/dev/null || pkill -f uvicorn 2>/dev/null || true); echo STOPPED"
```

## Step 4: 清空 ChromaDB 并全量重入库

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && python scripts/ingest_kb.py --reset --dir knowledge-base/entries/ 2>&1 | tail -20"
```

如果 ingest 脚本路径不对，先查找：
```
ssh easten@10.80.3.165 "find /home/easten/dev/yixiaoguan -name 'ingest*.py' -o -name '*ingest*.py' 2>/dev/null"
```

## Step 5: 重启 ai-service

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && (docker-compose -f deploy/docker-compose.yml up -d ai-service 2>/dev/null || nohup python -m uvicorn ai_service.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 &); echo STARTED"
```

## Step 6: 验证入库结果

```
ssh easten@10.80.3.165 "curl -s http://localhost:8000/api/kb/stats 2>/dev/null || curl -s http://localhost:8001/api/kb/stats 2>/dev/null"
```

期望 entry_count ≥ 450，chunk_count ≥ 600。

## Step 7: 快速冒烟测试

```
ssh easten@10.80.3.165 "curl -s -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"通勤车时刻表怎么查\",\"session_id\":\"test\"}' 2>/dev/null | python3 -m json.tool"
```

```
ssh easten@10.80.3.165 "curl -s -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"图书馆暑假开馆时间\",\"session_id\":\"test\"}' 2>/dev/null | python3 -m json.tool"
```

## 验收标准
- entry_count ≥ 450
- 冒烟测试两题均有实质答案（非"我不知道"）
- 无报错

完成后输出完整的 stats 和两道测试题的回答摘要。
