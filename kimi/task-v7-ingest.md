# T3 任务: v7 INGEST — ChromaDB 全量重入库

## 角色
你是山东第一医科大学（医小管）系统的运维工程师。

## 任务目标
在 165 服务器上执行 ChromaDB 全量重入库，将所有 KB 条目（含 v7 新增 51 条）入库。

## 前置条件
- QA-REVIEW-V7 已通过（51 条新 KB，KB-20260410-0001~0051）
- 文件已通过 Mutagen 同步到 165 服务器

## 执行步骤

### Step 1: 确认文件同步
```bash
# 在 165 服务器上执行
ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-*.md | wc -l
# 期望: 51
```

### Step 2: 停止 ai-service
```bash
cd /home/easten/dev/yixiaoguan
sudo pkill -f uvicorn || true
sleep 3
# 确认已停止
ps aux | grep uvicorn | grep -v grep
```

### Step 3: 清空 ChromaDB 并全量入库
```bash
cd /home/easten/dev/yixiaoguan
# 使用 venv Python
PYTHON=/home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python

# 清空旧数据
$PYTHON -c "
import chromadb
client = chromadb.PersistentClient(path='services/ai-service/chroma_db')
try:
    client.delete_collection('kb_entries')
    print('Collection deleted')
except:
    print('No collection to delete')
"

# 全量入库
$PYTHON scripts/batch_ingest_kb.py --yes
```

### Step 4: 验证入库数量
```bash
$PYTHON -c "
import chromadb
client = chromadb.PersistentClient(path='services/ai-service/chroma_db')
col = client.get_collection('kb_entries')
print(f'Total entries: {col.count()}')
# 抽查 5 条 KB-20260410-* 的 metadata
results = col.get(where={'entry_id': {'\\$regex': 'KB-20260410'}}, limit=5, include=['metadatas'])
for m in results['metadatas']:
    print(f\"  {m.get('entry_id', 'N/A')} - {m.get('title', 'N/A')} - {m.get('category', 'N/A')}\")
"
```

### Step 5: 重启 ai-service
```bash
cd /home/easten/dev/yixiaoguan/services/ai-service
sudo nohup /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai-service.log 2>&1 &
sleep 5
# 确认启动
curl -s http://localhost:8000/kb/stats | python3 -m json.tool
```

### Step 6: 验证 /kb/stats
```bash
curl -s http://localhost:8000/kb/stats
# 期望: entry_count >= 260
```

## 预期结果
- 入库总量: 现有 ~210 + v7 新增 51 = **~261 条**
- chunks: **~400+**
- /kb/stats entry_count ≥ 260

## 验收标准
- AC-ING7-01: batch_ingest_kb.py 运行无异常
- AC-ING7-02: /kb/stats entry_count ≥ 260
- AC-ING7-03: 抽查 5 条 KB-20260410-* metadata 正确

## 注意事项
- 使用正确的 venv Python: `/home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python`
- ai-service 可能以 root 运行，停止时需要 sudo
- 如遇权限问题，参考 v6 的处理方式

请在 165 服务器上执行以上步骤，并报告每一步的执行结果。
