# T3 任务: v8 DISCOVER — 确认公众号 fakeid 并补充搜索

## 角色
你是医小管知识库自动化工程师。

## 背景
wechat-article-exporter 已部署在本地 localhost:3000。
学生已整理 25 个公众号清单（见 kimi/wechat-accounts-list.md）。
现需通过 API 确认每个账号的 fakeid，并补充搜索遗漏的账号。

## 认证信息
auth-key: b982b119ba0744358c1dbcd6711c06fe
Base URL: http://localhost:3000

## ⚠️ HTTP 请求方式
PowerShell 中 curl 是别名，必须用 curl.exe：
```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/authkey"
```

## Step 1: 验证 auth-key 有效
```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/authkey"
```
期望返回 `{"code":0,...}`。如果失败，停止并报告。

## Step 2: 搜索 A 类账号 fakeid（8个）

依次搜索以下账号，记录 fakeid（返回 JSON 中的 `fakeid` 字段）：

```powershell
# A01 教务部
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E6%95%99%E5%8A%A1%E9%83%A8"

# A02 研究生处
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E7%A0%94%E7%A9%B6%E7%94%9F%E5%A4%84"

# A03 学工
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E5%AD%A6%E5%B7%A5"

# A04 后勤
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E5%90%8E%E5%8B%A4"

# A05 心理健康教育中心
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E5%BF%83%E7%90%86"

# A06 图书馆
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E5%9B%BE%E4%B9%A6%E9%A6%86"

# A07 就业
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E5%B0%B1%E4%B8%9A"

# A08 科研部
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E7%A7%91%E7%A0%94%E9%83%A8"
```

## Step 3: 搜索 B 类账号 fakeid（8个）

```powershell
# B01 官方主号
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6+%E5%B1%B1%E4%B8%9C%E7%9C%81%E5%8C%BB%E5%AD%A6%E7%A7%91%E5%AD%A6%E9%99%A2"

# B02 招生办
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E6%8B%9B%E7%94%9F%E5%8A%9E"

# B03 团委/青春山一大
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E9%9D%92%E6%98%A5%E5%B1%B1%E4%B8%80%E5%A4%A7"

# B04 医药管理学院
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E5%8C%BB%E8%8D%AF%E7%AE%A1%E7%90%86%E5%AD%A6%E9%99%A2"

# B05 科创中心
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E7%A7%91%E5%88%9B%E4%B8%AD%E5%BF%83"

# B06 饮食
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7%E9%A5%AE%E9%A3%9F"

# B07 对外合作交流部
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E5%AF%B9%E5%A4%96%E5%90%88%E4%BD%9C"

# B08 计划财务处
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6%E8%AE%A1%E5%88%92%E8%B4%A2%E5%8A%A1"
```

## Step 4: 补充关键词搜索（发现遗漏账号）

```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%9C%E7%AC%AC%E4%B8%80%E5%8C%BB%E7%A7%91%E5%A4%A7%E5%AD%A6"
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/account?keyword=%E5%B1%B1%E4%B8%80%E5%A4%A7"
```

对新发现的账号（不在已知25个中的），判断 KB 价值并分类。

## Step 5: 更新账号清单

读取 `kimi/wechat-accounts-list.md`，将所有找到的 fakeid 填入对应行（替换"待确认"）。
新发现的账号追加到对应分类末尾。

写回 `kimi/wechat-accounts-list.md`。

## 输出

1. 更新后的 `kimi/wechat-accounts-list.md`（含真实 fakeid）
2. 输出确认摘要：A 类确认几个 / B 类确认几个 / 新发现几个

## 验收标准
- AC-DIS-01: A 类 8 个账号 fakeid 全部确认（或注明"搜不到"）
- AC-DIS-02: B 类至少 5 个账号 fakeid 确认
- AC-DIS-03: 清单已更新并保存

请开始执行。
