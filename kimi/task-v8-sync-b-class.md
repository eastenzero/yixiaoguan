# T3 任务: v8 SYNC B类账号 + 补完就业账号

## 认证信息
auth-key: b982b119ba0744358c1dbcd6711c06fe
Base URL: http://localhost:3000
⚠️ 所有 HTTP 请求用 curl.exe

## 背景
A 类账号已同步完成（就业账号已获取 515+ 篇，wechat-sync-stats.md 已存在）。
本任务继续同步 B 类 8 个账号，并将就业账号标记为完成。

## Step 1: 标记就业账号同步完成

就业账号（MzkwMDQxNDA2Nw==）已获取 515+ 篇文章，可认为同步完成。
在 `kimi/wechat-sync-stats.md` 中更新就业账号状态为 ✅。

## Step 2: 同步 B 类 8 个账号

依次对以下 8 个账号获取文章列表，每页 20 条，翻页直到末页：

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
# 示例：获取官方主号第1页
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=MjM5NjA2NjcyMg==&begin=0&count=20"
```

每次翻页后 Sleep 1 秒，直到返回数量 < 20。

## Step 3: 更新统计文件

在 `kimi/wechat-sync-stats.md` 的 B 类账号表格中填入：文章总数、最新文章日期、状态。

## 输出

更新后的 `kimi/wechat-sync-stats.md`，B 类表格完整填写。

最后输出一行汇总：
- A 类: 8/8 ✅ 共 XX 篇
- B 类: X/8 ✅ 共 XX 篇
- 合计: XX 篇

## 验收标准
- B 类至少 5 个账号同步完成
- 统计表已更新
