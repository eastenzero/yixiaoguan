#!/bin/bash
set -e
cd ~/dev/yixiaoguan

echo "=== [INGEST-V6] Step 1: Check current KB stats ==="
curl -s http://localhost:8000/kb/stats || echo "ai-service may be stopped"

echo ""
echo "=== [INGEST-V6] Step 2: Stop ai-service ==="
pkill -f "uvicorn" || echo "No uvicorn process found"
sleep 2

echo ""
echo "=== [INGEST-V6] Step 3: Clear existing ChromaDB data ==="
python services/ai-service/app/scripts/clear_kb.py 2>/dev/null || \
  python -c "
import chromadb
client = chromadb.PersistentClient(path='services/ai-service/data/chroma_db')
try:
    client.delete_collection('kb_entries')
    print('Collection kb_entries deleted.')
except Exception as e:
    print(f'Delete collection: {e}')
"

echo ""
echo "=== [INGEST-V6] Step 4: Full re-ingestion ==="
python scripts/batch_ingest_kb.py --yes

echo ""
echo "=== [INGEST-V6] Step 5: Restart ai-service ==="
cd services/ai-service
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1 > /tmp/ai-service.log 2>&1 &
echo "ai-service PID: $!"
sleep 5
cd ~/dev/yixiaoguan

echo ""
echo "=== [INGEST-V6] Step 6: Verify /kb/stats ==="
curl -s http://localhost:8000/kb/stats

echo ""
echo "=== [INGEST-V6] Step 7: Sample 5 new entries metadata ==="
python -c "
import chromadb
client = chromadb.PersistentClient(path='services/ai-service/data/chroma_db')
col = client.get_collection('kb_entries')
results = col.get(
    where={'\$or': [
        {'entry_id': {'\\$contains': 'KB-20260409-0001'}},
        {'entry_id': {'\\$contains': 'KB-20260409-0010'}},
        {'entry_id': {'\\$contains': 'KB-20260409-0050'}},
        {'entry_id': {'\\$contains': 'KB-20260409-0070'}},
        {'entry_id': {'\\$contains': 'KB-20260409-0084'}},
    ]},
    limit=10,
    include=['metadatas']
)
for m in results['metadatas'][:5]:
    print(m)
" 2>/dev/null || echo "Metadata sample check - see /kb/stats above"

echo ""
echo "=== [INGEST-V6] DONE ==="
