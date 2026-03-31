# docs/dev-guides — 开发指引

本目录存放面向开发者的操作指引，是 AI 辅助开发时的重要上下文来源。

## 待写文档

- [ ] `local-setup.md` — **本地环境搭建**（Docker Compose、数据库初始化、环境变量）
- [ ] `ruoyi-guide.md` — **若依使用约定**（裁剪说明、代码生成器用法、命名约定）
- [ ] `uniapp-guide.md` — **uni-app 开发约定**（目录结构、组件约定、H5/小程序差异处理）
- [ ] `ai-service-guide.md` — **AI 服务开发约定**（RAG 流程、Prompt 模板规范、ChromaDB 集合约定）
- [ ] `git-workflow.md` — **Git 提交约定**（分支策略、commit 格式）

## 环境变量说明（草稿）

所有敏感配置放在 `.secrets/.env`，不提交 Git。

| 变量名 | 说明 |
|---|---|
| `DASHSCOPE_API_KEY` | 阿里云 DashScope API Key |
| `DB_HOST` | PostgreSQL 地址 |
| `DB_PORT` | PostgreSQL 端口（默认 5432） |
| `DB_NAME` | 数据库名 |
| `DB_USER` | 数据库用户名 |
| `DB_PASSWORD` | 数据库密码 |
| `REDIS_HOST` | Redis 地址 |
| `REDIS_PORT` | Redis 端口（默认 6379） |
| `JWT_SECRET` | JWT 签名密钥 |
| `COS_SECRET_ID` | 腾讯云 COS SecretId |
| `COS_SECRET_KEY` | 腾讯云 COS SecretKey |
| `COS_BUCKET` | COS Bucket 名称 |
| `COS_REGION` | COS 地域（如 ap-beijing） |
