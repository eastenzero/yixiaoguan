import requests

queries = [
    ("校园卡充值的机器在哪，能现金充值吗？", "eval-032"),
    ("综合素质测评成绩是怎么算的，德育占多少分？", "eval-011"),
]

for q, eid in queries:
    print(f"\n=== {eid}: {q} ===")
    resp = requests.post('http://localhost:8000/kb/search', json={'query': q, 'top_k': 5}, timeout=30)
    data = resp.json().get('data', [])
    for d in data:
        print(f"  {d['entry_id']}: {d['score']}")
