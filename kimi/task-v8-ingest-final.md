# T3 任务: v8 INGEST FINAL — 432条草稿全量入库

## ⚠️ 铁律：所有命令只能写成 `ssh easten@192.168.100.165 "..."` 形式
## ⚠️ 禁止在本地 PowerShell 调用 curl / python / Invoke-WebRequest

---

## Step 1: 确认 first-batch-drafts 已同步

```powershell
ssh easten@192.168.100.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md 2>/dev/null | wc -l"
```

如果 < 430，等待 2 分钟：
```powershell
Start-Sleep -Seconds 120
ssh easten@192.168.100.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md 2>/dev/null | wc -l"
```

## Step 2: 将草稿复制到正式目录

```powershell
ssh easten@192.168.100.165 "cp /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-*.md /home/easten/dev/yixiaoguan/knowledge-base/entries/ && echo COPY_DONE"
```

```powershell
ssh easten@192.168.100.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/KB-*.md | wc -l"
```

## Step 3: 停止 ai-service

```powershell
ssh easten@192.168.100.165 "pkill -f uvicorn 2>/dev/null; pkill -f gunicorn 2>/dev/null; echo STOPPED"
```

## Step 4: 找到 ingest 脚本

```powershell
ssh easten@192.168.100.165 "find /home/easten/dev/yixiaoguan -name '*.py' 2>/dev/null | xargs grep -l 'chroma\|embed\|ingest' 2>/dev/null | grep -v __pycache__ | head -10"
```

## Step 5: 全量重入库（根据 Step 4 找到的脚本调整路径）

```powershell
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && find . -name 'venv' -type d | head -1 | xargs -I{} {}/bin/python scripts/batch_ingest_kb.py --yes 2>&1 | tail -20"
```

如果上面失败，尝试：
```powershell
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && python3 scripts/batch_ingest_kb.py --yes 2>&1 | tail -20"
```

## Step 6: 重启 ai-service

```powershell
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 & sleep 10 && echo STARTED"
```

如果服务在 services/ 子目录：
```powershell
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan/services/ai-service && nohup ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 & sleep 10 && echo STARTED"
```

## Step 7: 验证 (在 SSH 内用 curl，不是本地)

```powershell
ssh easten@192.168.100.165 "curl -s http://localhost:8000/kb/stats"
```

```powershell
ssh easten@192.168.100.165 "curl -s http://localhost:8000/api/kb/stats"
```

## Step 8: 冒烟测试

```powershell
ssh easten@192.168.100.165 "curl -s -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d '{\"message\":\"通勤车时刻表\",\"session_id\":\"t1\"}' | python3 -c 'import sys,json; d=json.load(sys.stdin); print(d.get(\"answer\",d)[:200])'"
```

## 验收标准
- entry_count ≥ 450
- 冒烟测试有实质答案

完成后输出 stats 结果和冒烟测试摘要。
