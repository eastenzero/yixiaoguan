# T3 任务: v8 SYNC B类账号 (重试)

## 认证信息
auth-key: b982b119ba0744358c1dbcd6711c06fe
Base URL: http://localhost:3000
⚠️ 所有 HTTP 请求用 curl.exe（不是 curl）

## Step 1: 先验证 auth-key 是否真的过期

```powershell
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/authkey"
```

**如果返回 code:0** → auth-key 有效，继续 Step 2  
**如果返回错误** → 停止，报告具体错误内容

注意：auth-key 有效期是 4 天，刚生成不到 30 分钟，不应该过期。如果上次失败，可能是接口限流或网络抖动，不是真正过期。

## Step 2: 同步 B 类 8 个账号（每账号之间 sleep 3 秒）

依次对以下 8 个账号，每页 20 条，翻页直到末页：

| 公众号 | fakeid |
|--------|--------|
| 山东第一医科大学 山东省医学科学院 | MjM5NjA2NjcyMg== |
| 山一大招生办 | MzAxNzYyMzM1OA== |
| 青春山一大 | MzIyMTA3MDc4OA== |
| 山东第一医科大学医药管理学院 | Mzg2NTY5ODAwNA== |
| 山东第一医科大学科创中心 | Mzg3NDcwOTc0Mw== |
| 山一大饮食 | MzkxOTU2MTMyNg== |
| 山东第一医科大学对外合作交流部 | Mzg2MzYwNDM0MQ== |
| 山东第一医科大学计划财务处 | Mzg4NDUxNDU1OA== |

```powershell
# 获取文章列表（每账号从 begin=0 开始翻页）
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=MjM5NjA2NjcyMg==&begin=0&count=20"
```

每页翻页后 Sleep 2 秒。如果某个账号连续3次返回错误，跳过并记录。

## Step 3: 更新统计文件

在 `kimi/wechat-sync-stats.md` 的 B 类表格填入文章总数和日期范围。

## 输出

最终输出：
- A 类: 8/8 共 XX 篇
- B 类: X/8 共 XX 篇
- 合计: XX 篇

请开始执行。
