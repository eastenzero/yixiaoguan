# Wechat-Article-Exporter 本地缓存检查报告

**检查时间**: 2026-04-10  
**检查路径**: `C:\wechat-exporter\.data`  
**Docker 容器**: wechat-article-exporter (运行中)

---

## 检查结果

### 1. `.data/` 目录结构

```
C:\wechat-exporter\.data\
└── kv/
    └── cookie/
        └── b982b119ba0744358c1dbcd6711c06fe  (2,792 bytes)
```

### 2. SQLite 数据库

**❌ 未找到任何 SQLite 数据库文件**

搜索范围:
- 主机路径: `C:\wechat-exporter\.data\**
- 容器路径: `/app/**`

未找到以下类型的文件:
- `*.db`
- `*.sqlite`
- `*.sqlite3`

### 3. Cookie 文件内容

找到 1 个 cookie 文件，包含以下内容:
- **token**: 已设置 (1096541962)
- **cookies**: 10 个 WeChat 相关 cookie
  - rand_info, slave_bizuin, data_bizuin, bizuin
  - data_ticket, ua_id, slave_sid, slave_user
  - xid, ticket_uin
- **过期时间**: 2026-04-14 (部分cookie)

### 4. 文章数据

**❌ 本地缓存中没有文章数据**

wechat-article-exporter 的设计是:
1. 通过浏览器实时获取微信公众号文章列表
2. 文章数据存储在内存或浏览器 localStorage 中
3. 下载的文章直接导出到指定目录，不保留在本地数据库

---

## 结论

| 检查项 | 结果 | 说明 |
|--------|------|------|
| SQLite 数据库 | ❌ 无 | 应用未使用本地数据库存储文章 |
| JSON/JSONL 数据文件 | ❌ 无 | 无导出格式的缓存文件 |
| Cookie/认证信息 | ✅ 有 | 已登录，认证有效至 2026-04-14 |
| 文章缓存 | ❌ 无 | 文章数据不在本地缓存中 |

---

## 建议

由于 wechat-article-exporter **没有本地文章缓存**，要获取历史文章需要:

1. **通过 Web UI 重新获取**: 访问 http://localhost:3000 登录并重新下载文章
2. **检查现有导出目录**: 查看之前是否已导出到 `wechat-exports/` 或类似目录
3. **使用其他数据源**: 如已有 `wechat-exports/` 中的文章文件，可直接使用

---

**状态**: 完成 ✅  
**发现**: 本地缓存仅包含认证信息，无文章数据
