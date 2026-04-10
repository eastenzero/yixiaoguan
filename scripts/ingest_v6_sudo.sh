#!/bin/bash
set -e
PROJ=/home/easten/dev/yixiaoguan
cd $PROJ

echo "=== [INGEST-V6] Step 1: Current KB stats ==="
curl -s http://localhost:8000/kb/stats

echo ""
echo "=== [INGEST-V6] Step 2: Stop ai-service ==="
echo "ZhaYeFan05.07.14" | sudo -S pkill -f "uvicorn" || echo "pkill returned non-zero (may be ok)"
sleep 3

echo ""
echo "=== [INGEST-V6] Step 3: Clear ChromaDB collection ==="
python3 -c "
import sys
sys.path.insert(0, '$PROJ/services/ai-service')
try:
    import chromadb
    client = chromadb.PersistentClient(path='$PROJ/services/ai-service/data/chroma_db')
    client.delete_collection('kb_entries')
    print('Collection kb_entries deleted.')
except Exception as e:
    print(f'Note: {e}')
"

echo ""
echo "=== [INGEST-V6] Step 4: Full re-ingestion ==="
python3 $PROJ/scripts/batch_ingest_kb.py --yes

echo ""
echo "=== [INGEST-V6] Step 5: Restart ai-service ==="
cd $PROJ/services/ai-service
echo "ZhaYeFan05.07.14" | sudo -S bash -c "nohup /usr/local/bin/python3.11 /usr/local/bin/uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/ai-service-v6.log 2>&1 &"
echo "ai-service restart issued"
sleep 6

echo ""
echo "=== [INGEST-V6] Step 6: Verify /kb/stats ==="
curl -s http://localhost:8000/kb/stats

echo ""
echo "=== [INGEST-V6] DONE ==="
