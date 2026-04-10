# T3 任务: v8 FILTER-DOWNLOAD — 筛选并下载有价值文章

## 认证信息
auth-key: b982b119ba0744358c1dbcd6711c06fe
Base URL: http://localhost:3000
⚠️ 所有 HTTP 请求用 curl.exe

## 背景
已同步 1837 篇文章（A类 1793 篇 + B类 44 篇）。
原始数据存于 `kimi/wechat-sync-data.json`。
本任务从已同步的文章列表中筛选有价值文章，逐篇下载为 Markdown。

## 筛选条件

**时间范围**: Unix 时间戳对应 2024-04-01 ~ 2026-04-10
（2024-04-01 = 1711900800, 2026-04-10 = 1744214400）

**纳入关键词**（标题含任一即纳入）:
通知, 公告, 安排, 须知, 指南, 攻略, 流程, 办理, 报名, 缴费, 政策, 规定,
奖学金, 助学金, 选课, 考试, 成绩, 宿舍, 校园卡, 图书馆, 网络, VPN,
毕业, 就业, 考研, 保研, 实习, 社团, 竞赛, 志愿, 心理, 讲座

**排除关键词**（标题含任一则跳过）:
招聘, 聘用, 人才引进, 论文发表, SCI, 学术会议,
领导调研, 视察, 座谈, 转发, 转载

## 执行步骤

### Step 1: 编写筛选脚本并执行

创建并执行 Python 脚本 `scripts/wechat/filter_articles.py`：

```python
import json
import re
from datetime import datetime

# 加载原始数据
with open('kimi/wechat-sync-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 筛选条件
start_ts = 1711900800  # 2024-04-01
end_ts = 1744214400    # 2026-04-10

include_keywords = [
    '通知','公告','安排','须知','指南','攻略','流程','办理','报名','缴费',
    '政策','规定','奖学金','助学金','选课','考试','成绩','宿舍','校园卡',
    '图书馆','网络','VPN','毕业','就业','考研','保研','实习','社团',
    '竞赛','志愿','心理','讲座'
]

exclude_keywords = [
    '招聘','聘用','人才引进','论文发表','SCI','学术会议',
    '领导调研','视察','座谈','转发','转载'
]

results = []
for account_name, articles in data.items():
    for article in articles:
        title = article.get('title', '')
        create_time = article.get('create_time', article.get('update_time', 0))
        url = article.get('link', article.get('url', ''))
        
        # 时间过滤
        if not (start_ts <= create_time <= end_ts):
            continue
        
        # 排除关键词
        if any(kw in title for kw in exclude_keywords):
            continue
        
        # 纳入关键词
        if any(kw in title for kw in include_keywords):
            results.append({
                'account': account_name,
                'title': title,
                'url': url,
                'date': datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
            })

print(f"筛选结果: {len(results)} 篇文章")
with open('kimi/filtered-articles.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
```

### Step 2: 查看筛选结果

```powershell
python scripts/wechat/filter_articles.py
```
输出筛选后的文章总数，并查看 `kimi/filtered-articles.json`。

### Step 3: 批量下载筛选出的文章

对 `kimi/filtered-articles.json` 中每篇文章，调用下载 API：

```powershell
# 下载单篇文章为 Markdown（article_url 需 URL 编码）
curl.exe -s -o "wechat-exports/{account}/{date}-{title}.md" `
  -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" `
  "http://localhost:3000/api/public/v1/download?url={encoded_url}&format=markdown"
```

创建 Python 脚本 `scripts/wechat/download_articles.py` 自动化执行：

```python
import json, os, time
import urllib.parse, requests

with open('kimi/filtered-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

auth_key = 'b982b119ba0744358c1dbcd6711c06fe'
headers = {'X-Auth-Key': auth_key}

downloaded = 0
failed = 0

for article in articles:
    account = article['account']
    title = article['title'][:50]  # 截断过长标题
    date = article['date']
    url = article['url']
    
    # 创建输出目录
    out_dir = f"wechat-exports/{account}"
    os.makedirs(out_dir, exist_ok=True)
    
    # 安全文件名（去除特殊字符）
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)
    out_file = f"{out_dir}/{date}-{safe_title}.md"
    
    if os.path.exists(out_file):
        continue  # 跳过已下载
    
    # 下载
    try:
        encoded_url = urllib.parse.quote(url, safe='')
        resp = requests.get(
            f"http://localhost:3000/api/public/v1/download?url={encoded_url}&format=markdown",
            headers=headers,
            timeout=30
        )
        if resp.status_code == 200:
            with open(out_file, 'w', encoding='utf-8') as f:
                f.write(resp.text)
            downloaded += 1
        else:
            failed += 1
            print(f"FAIL [{resp.status_code}]: {title}")
    except Exception as e:
        failed += 1
        print(f"ERROR: {title} - {e}")
    
    time.sleep(1)  # 频率限制

print(f"完成: 下载 {downloaded} 篇, 失败 {failed} 篇")
```

运行：
```powershell
python scripts/wechat/download_articles.py
```

### Step 4: 统计下载结果

```powershell
Get-ChildItem -Recurse -Filter "*.md" wechat-exports | Measure-Object | Select-Object Count
```

生成 `kimi/wechat-download-stats.md`:

| 公众号 | 文章总数(同步) | 时间内文章 | 关键词命中 | 已下载 |
|--------|-------------|----------|----------|--------|

## 验收标准
- AC-FDL-01: 筛选脚本执行成功，输出 filtered-articles.json
- AC-FDL-02: A 类公众号符合条件文章全部下载
- AC-FDL-03: wechat-exports/ 目录按账号分类存储
- AC-FDL-04: 下载统计文件已生成，总下载量 ≥ 50 篇

请开始执行。
