import requests
import re

REJECT_SCORE_THRESHOLD = 0.60

def normalize_entry_id(entry_id):
    if not entry_id:
        return ""
    return re.sub(r'__chunk_\d+$', '', entry_id)

def search_with_scores(question, top_k=5):
    try:
        payload = {"query": question, "top_k": top_k}
        r = requests.post('http://localhost:8000/kb/search', json=payload, timeout=15)
        data = r.json()
        results = data.get("data", [])
        if isinstance(results, list):
            ids = []
            max_score = 0
            for item in results:
                raw_id = item.get("entry_id", item.get("id", ""))
                score = item.get("score", 0) or 0
                if score > max_score:
                    max_score = score
                normalized = normalize_entry_id(raw_id)
                if normalized and normalized not in ids:
                    ids.append(normalized)
            return ids, max_score
        return [], 0
    except Exception as e:
        return [f"ERROR: {e}"], 0

# 测试几个边界情况的 hit 题
hit_tests = [
    ("如何申请空教室？", ["KB-20260324-0014"]),
    ("图书馆开放时间？", ["KB-20260324-0011"]),
    ("电费怎么交？", ["KB-20260324-LIFE-001"]),
]

print("=== Hit 题 Score 分布 (阈值 0.60) ===")
for q, expected in hit_tests:
    ids, max_score = search_with_scores(q)
    matched = any(eid in ids for eid in expected)
    hit_status = "YES" if matched else "NO"
    status = "PASS" if matched else "FAIL"
    print(f"{status} {q}: score={max_score:.3f}, hit={hit_status}")

print("\n=== Reject 题 Score 分布 (阈值 0.60) ===")
reject_tests = [
    "北京大学图书馆几点开门？",
    "山东大学图书馆几点开门？",
    "热水供应时间是几点到几点？",
]

for q in reject_tests:
    ids, max_score = search_with_scores(q)
    is_rejected = max_score < REJECT_SCORE_THRESHOLD
    rej_status = "REJECT" if is_rejected else "RETURN"
    status = "PASS" if is_rejected else "FAIL"
    print(f"{status} {q}: score={max_score:.3f} -> {rej_status}")
