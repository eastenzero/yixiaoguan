import requests, json

reject_queries = [
    "明天天气怎么样？",
    "北京大学图书馆几点开门？",
    "帮我写一份Java简历",
    "清华大学今年的考研分数线是多少？",
    "马斯克最近又发了什么推特？",
    "推荐几部最近好看的电影",
    "怎么制作红烧肉？",
    "iPhone 16多少钱？",
    "学校附近有什么好吃的？",
    "辅导员办公室在哪栋楼？",
    "图书馆能借几本书，借多久？",
    "校医院上班时间是什么时候？",
    "学校食堂有哪些档口？",
    "宿舍水管坏了，怎么报修？",
    "电费在哪交，怎么充值？",
    "宿舍WiFi密码是多少，网连不上找谁？",
    "热水供应时间是几点到几点？",
    "校园卡充值的机器在哪，能现金充值吗？",
]

for q in reject_queries:
    resp = requests.post('http://localhost:8000/kb/search', json={'query': q, 'top_k': 5}, timeout=30)
    data = resp.json().get('data', [])
    if data:
        best = max(d['score'] for d in data)
        print(f"{best:.4f} - {q[:30]}")
    else:
        print(f"0.0000 - {q[:30]} (no results)")
