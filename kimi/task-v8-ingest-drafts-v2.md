# T3 任务: v8 INGEST — first-batch-drafts 432条全量入库（修订版）

## ⚠️ 所有命令通过 SSH 执行，禁止本地执行，禁止使用 Invoke-WebRequest

```powershell
ssh easten@10.80.3.165 "命令"
```

## Step 1: 确认草稿文件已同步到服务器

```powershell
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md 2>/dev/null | wc -l"
```

如果 < 430，等待并重试：
```powershell
Start-Sleep 120
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md 2>/dev/null | wc -l"
```

## Step 2: 将草稿复制到正式目录

```powershell
ssh easten@10.80.3.165 "cp /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md /home/easten/dev/yixiaoguan/knowledge-base/entries/ && echo COPY_DONE"
```

```powershell
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/KB-*.md | wc -l"
```

## Step 3: 查找 ingest 脚本路径

```powershell
ssh easten@10.80.3.165 "find /home/easten/dev/yixiaoguan -name '*.py' | xargs grep -l 'ingest\|chroma\|embed' 2>/dev/null | head -10"
```

## Step 4: 停止 ai-service

```powershell
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml stop ai-service 2>/dev/null; pkill -f uvicorn 2>/dev/null; echo STOPPED"
```

## Step 5: 全量重入库

根据 Step 3 找到的 ingest 脚本，执行（示例路径，按实际调整）：

```powershell
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && python scripts/ingest_kb.py --reset 2>&1 | tail -30"
```

或者：
```powershell
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && python -m scripts.ingest_kb --reset 2>&1 | tail -30"
```

## Step 6: 重启 ai-service

```powershell
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml up -d ai-service 2>/dev/null && echo STARTED"
```

## Step 7: 验证（用 curl.exe 不用 Invoke-WebRequest）

```powershell
ssh easten@10.80.3.165 "curl -s http://localhost:8000/api/kb/stats"
```

```powershell
ssh easten@10.80.3.165 "curl -s -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"图书馆暑假开馆时间\",\"session_id\":\"test\"}'"
```

## 验收标准
- entry_count ≥ 450
- 测试问题有实质回答
- ai-service 正常运行

完成后输出 stats JSON 和测试问题的回答摘要（answer 字段前100字）。
