import requests, json

queries = [
    ("毕业生档案去向核对了发现有错误咋改？", "eval-006", "KB-20260324-0016"),
]

for q, eid, target in queries:
    print(f"\n=== {eid}: {q} ===")
    resp = requests.post('http://localhost:8000/kb/search', json={'query': q, 'top_k': 20}, timeout=30)
    data = resp.json().get('data', [])
    found = False
    for d in data:
        marker = " <-- TARGET" if target in d['entry_id'] else ""
        print(f"  {d['entry_id']}: {d['score']}{marker}")
        if target in d['entry_id']:
            found = True
    if not found:
        print("  TARGET NOT FOUND in top 20")
