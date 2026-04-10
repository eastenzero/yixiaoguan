# T3 任务: Debug wechat API 响应格式

## 目标
找出 wechat-article-exporter API 返回的文章字段名称，特别是时间戳字段。

## ⚠️ 不要运行 curl，用 curl.exe

## Step 1: 获取教务部第一页文章（原始 JSON）

```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=5" | python -m json.tool
```

仔细查看返回的 JSON 结构，特别是：
1. 文章列表的外层键名（data? list? articles? items?）
2. 每篇文章的字段名列表
3. 时间字段的名称（create_time? update_time? publish_time? datetime? time?）
4. 时间字段的值格式（Unix 时间戳? 字符串? 毫秒?）
5. URL/链接字段的名称（link? url? article_url?）

## Step 2: 打印第一篇文章的所有字段

输出第一篇文章完整信息。

## Step 3: 验证时间范围

对一篇 2024-2026 年的文章，计算其时间戳对应的日期：
```python
from datetime import datetime
ts = <第一篇文章的时间戳值>
print(datetime.fromtimestamp(ts))  # 如果是秒级
print(datetime.fromtimestamp(ts/1000))  # 如果是毫秒级
```

## Step 4: 检查页数

```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=20" | python -c "import sys,json; d=json.load(sys.stdin); print('总条数:', d.get('total', d.get('count', '?'))); print('本页文章数:', len(d.get('data', d.get('list', d.get('articles', [])))))"
```

是否有 total 字段表示总文章数？

## 输出

输出以下信息：
1. 文章列表的外层键名
2. 时间字段名称及值格式（整数秒/毫秒/字符串）
3. 链接字段名称
4. 是否有 total 字段
5. 第一篇文章的完整字段列表

请开始执行。
