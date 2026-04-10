# T3 任务: v8 SYNC-ARTICLES — 同步 A/B 类公众号文章列表

## 角色
你是医小管知识库自动化工程师。

## 认证信息
auth-key: b982b119ba0744358c1dbcd6711c06fe
Base URL: http://localhost:3000
⚠️ 所有 HTTP 请求用 curl.exe（不是 curl）

## 已确认账号 fakeid

### A 类（高价值，必须全量同步）
| 公众号 | fakeid |
|--------|--------|
| 山东第一医科大学教务部 | Mzg3ODMyNjg1Nw== |
| 山东第一医科大学研究生处 | Mzg5MTY0Njg2NA== |
| 山一大学工 | Mzg5MDc2MDMwNA== |
| 山一大后勤 | Mzg5NTQyMzg4NQ== |
| 山一大 心理健康教育中心 | MzkxNzU2NTQxMg== |
| 山东第一医科大学图书馆 | MzU1OTI5MzIwNA== |
| 山东第一医科大学就业 | MzkwMDQxNDA2Nw== |
| 山东第一医科大学科研部 | MzkzOTE5OTI5Mg== |

### B 类（中价值，全量同步）
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

## 任务目标

对以上 16 个账号，通过 API 获取文章列表（分页翻页直到末页），统计各账号文章总数。

## 执行方法

### 方法：API 分页获取

每次请求 20 条，begin 递增，直到返回数量 < 20：

```powershell
# 示例：获取教务部第1页
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=20"

# 第2页
curl.exe -s -H "X-Auth-Key: b982b119ba0744358c1dbcd6711c06fe" "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=20&count=20"
```

API 返回的每条文章包含：
- `title`: 文章标题
- `link`: 原始链接
- `create_time` 或 `update_time`: 发布时间（Unix 时间戳）

### 注意事项
- 微信接口有频率限制，每次翻页之间 sleep 1-2 秒
- 工具会缓存文章列表，后续重复调用不消耗配额
- 文章总数可能达数百甚至数千，要耐心翻页
- 如果某个账号获取失败（如接口限流），记录并跳过，继续下一个

## 输出

生成 `kimi/wechat-sync-stats.md`：

```markdown
# 公众号文章同步统计

同步时间: YYYY-MM-DD
auth-key: b982b119ba0744358c1dbcd6711c06fe

## A 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
| 教务部 | ... | ... | ... | ... | ✅ |

## B 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
```

## 验收标准
- AC-SYN-01: A 类 8 个账号文章列表全部同步（或注明失败原因）
- AC-SYN-02: B 类至少 5 个账号同步完成
- AC-SYN-03: 统计表已生成，含文章总数

请开始执行。
