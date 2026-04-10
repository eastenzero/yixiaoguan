#!/bin/bash
PROJ=/home/easten/dev/yixiaoguan
VENV_PY=$PROJ/services/ai-service/venv/bin/python
cd $PROJ

echo "=== Step 1: KB file count check ==="
ls $PROJ/knowledge-base/entries/first-batch-drafts/KB-20260409-*.md | wc -l

echo ""
echo "=== Step 2: Clear ChromaDB collection ==="
$VENV_PY << 'PYEOF'
try:
    import chromadb
    client = chromadb.PersistentClient(path='/home/easten/dev/yixiaoguan/services/ai-service/data/chroma_db')
    try:
        client.delete_collection('kb_entries')
        print('Collection kb_entries deleted successfully.')
    except Exception as e:
        print(f'Delete error (may not exist): {e}')
except Exception as e:
    print(f'ChromaDB error: {e}')
PYEOF

echo ""
echo "=== Step 3: Full re-ingestion ==="
$VENV_PY $PROJ/scripts/batch_ingest_kb.py --yes

echo ""
echo "=== Step 4: Verify entry count ==="
$VENV_PY << 'PYEOF'
try:
    import chromadb
    client = chromadb.PersistentClient(path='/home/easten/dev/yixiaoguan/services/ai-service/data/chroma_db')
    col = client.get_collection('kb_entries')
    count = col.count()
    print(f'Total chunks in kb_entries: {count}')
    results = col.get(limit=5, include=['metadatas'])
    print('Sample metadata (first 5):')
    for i, m in enumerate(results['metadatas']):
        print(f"  {i+1}. entry_id={m.get('entry_id','?')} category={m.get('category','?')}")
except Exception as e:
    print(f'Error: {e}')
PYEOF

echo ""
echo "=== INGEST DONE ==="
