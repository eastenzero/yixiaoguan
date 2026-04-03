# docs/dev-guides — 开发指引

本目录存放面向开发者的操作指引，是 AI 辅助开发时的重要上下文来源。

---

## 目录地图

### 永久参考文档（根目录）

| 文件 | 用途 |
|------|------|
| `ai-antipatterns.md` | AI 错题本，记录反复出现的错误模式，下发任务前必读 |
| `ai-prompt-guide.md` | Prompt 工程指南，定义五件套结构和最佳实践 |
| `commander-verification-sop.md` | 指挥官 L1 验收 SOP 模板 |
| `AGENT_AUTH_GUIDE.md` / `AGENT_LOGIN_GUIDE.md` | Agent 登录与认证说明 |
| `backend-roadmap.md` | 后端开发路线图 |
| `local-setup.md` | 本地环境搭建说明 |

### prompts/ — 任务执行提示词（按阶段分类）

```
prompts/
├── (PROMPT-A ~ PROMPT-R2)   前端/后端开发提示词（历史存档）
├── kb-repair/               知识库修复阶段提示词（R1~R5，2026-04 执行完毕）
└── kb-expansion/            知识库扩量阶段提示词（新批次 B1+）
```

**命名约定**：`<阶段编号>-<任务简述>-prompt-<日期>.md`  
例：`r3-queue-sync-prompt-2026-04-03.md`、`batch-b1-competition-eval-discovery-prompt-2026-04-03.md`

---

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
