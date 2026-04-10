#!/bin/bash
PROJ=/home/easten/dev/yixiaoguan
VENV_PY=$PROJ/services/ai-service/venv/bin/python

echo "=== /kb/stats ==="
curl -s http://localhost:8000/kb/stats

echo ""
echo "=== Sample 5 new KB-20260409-* entries ==="
$VENV_PY << 'PYEOF'
try:
    import chromadb
    client = chromadb.PersistentClient(path='/home/easten/dev/yixiaoguan/services/ai-service/data/chroma')
    col = client.get_collection('kb_entries')
    results = col.get(
        where={"entry_id": {"$gt": "KB-20260409-0000"}},
        limit=5,
        include=['metadatas']
    )
    print(f"Found {len(results['metadatas'])} results")
    for m in results['metadatas']:
        print(f"  entry_id={m.get('entry_id','?')} | category={m.get('category','?')} | title={m.get('title','?')}")
except Exception as e:
    print(f'Error: {e}')
PYEOF

echo ""
echo "=== Check specific entry KB-20260409-0001 ==="
$VENV_PY << 'PYEOF'
try:
    import chromadb
    client = chromadb.PersistentClient(path='/home/easten/dev/yixiaoguan/services/ai-service/data/chroma')
    col = client.get_collection('kb_entries')
    results = col.get(
        ids=['KB-20260409-0001__chunk_0'],
        include=['metadatas', 'documents']
    )
    if results['metadatas']:
        m = results['metadatas'][0]
        print(f"entry_id: {m.get('entry_id')}")
        print(f"title: {m.get('title')}")
        print(f"category: {m.get('category')}")
        print(f"campus: {m.get('campus','N/A')}")
        print(f"doc_preview: {results['documents'][0][:100]}...")
    else:
        print("Entry not found - trying alternate ID format")
        r2 = col.get(limit=5, include=['metadatas'])
        print("Sample IDs:", [m.get('entry_id') for m in r2['metadatas'][:5]])
except Exception as e:
    print(f'Error: {e}')
PYEOF
