# 医小管（YiXiaoGuan）AI Agent 上下文文件

> 本文件面向所有 AI 助手/Agent，合并了 `.windsurfrules`、`.cursorrules`、`.globalrules` 的全部内容。  
> 请在每次对话开始时优先读取本文件，再读其他文档。

---

## 一、项目定位

校园智能服务平台，面向学生、教师、管理员三类角色，提供：
- **学生端**：AI 问答、事务导办、空教室申请、进度查询（uni-app H5/小程序）
- **教师端**：答疑处理、审批、一键转知识库、工作台统计（Vue 3 PC Web）
- **管理端**：知识审核、分类管理、权限、日志（并入教师端后台）

---

## 二、技术栈

| 层次 | 技术 |
|------|------|
| 主业务后端 | Java 21 + Spring Boot 3 + 若依（RuoYi-Vue3 3.9.2） |
| AI 能力层 | Python 3.11+ + FastAPI + ChromaDB + 阿里云 DashScope |
| 大模型 | 通义千问（DashScope API） |
| Embedding | DashScope text-embedding-v3 |
| 向量库 | **ChromaDB**（本地持久化，非 pgvector），集合：`kb_entries`、`quick_links` |
| 教师/管理 Web | Vue 3 + TypeScript + Element Plus |
| 学生端 | uni-app + TypeScript（H5 优先） |
| 数据库 | PostgreSQL 16 + Redis 7 |
| 对象存储 | 腾讯云 COS |
| 部署 | Docker Compose 单机 |
| 默认终端 | **PowerShell**（Windows，注意 PowerShell 语法） |

---

## 三、目录结构

```
yixiaoguan/
├── apps/
│   ├── student-app/        # uni-app 学生端
│   └── teacher-web/        # Vue 3 教师/管理端
├── services/
│   ├── business-api/       # Spring Boot 主业务后端（ruoyi-admin 子模块）
│   └── ai-service/         # FastAPI AI 服务
├── knowledge-base/
│   ├── entries/            # 知识条目正式文件（分类目录）
│   │   └── first-batch-drafts/   # 第一批草稿（约 81 份）
│   └── raw/                # 原始材料清洗产物
│       └── first-batch-processing/
│           ├── manifests/  # 材料总表与清洗标注 CSV
│           ├── converted/  # 格式转换结果（markdown/pdf）
│           └── logs/       # 转换日志与阻塞记录
├── docs/
│   ├── project-docs/       # 核心规划文档（00~14 编号系列）
│   ├── dev-guides/         # 开发指南、后端路线图、提示词模板
│   ├── test-reports/       # 测试与完成报告
│   ├── architecture/       # 架构文档
│   ├── database/           # 数据库 schema
│   └── legacy/             # 旧版草稿（仅参考）
├── _references/            # 原始材料（不移动、不覆盖）
├── deploy/                 # docker-compose.yml + .env
├── scripts/                # 数据处理脚本
└── temp/                   # 临时脚本/日志（执行后清理）
```

---

## 四、架构约束

- `services/business-api/`：**只处理业务逻辑**，禁止直接调用大模型
- `services/ai-service/`：**只处理 RAG/Embedding/Prompt**，不处理业务权限
- AI 服务只对 business-api 暴露接口，**不直接对前端暴露**
- WebSocket 服务在 business-api 中实现，用于教师实时插入对话和主动推送
- 数据库表名：snake_case，统一加 `yx_` 前缀（如 `yx_user`、`yx_conversation`）
- API 响应格式统一：`{ code, msg, data }`
- 时间字段统一用 ISO 8601

---

## 五、本地服务配置（真实值，禁止擅自修改）

> 密码权威来源是 `deploy/.env`，yml 中是占位符 `${POSTGRES_PASSWORD}` / `${REDIS_PASSWORD}`。

| 服务 | 配置项 | 值 |
|------|-------|-----|
| PostgreSQL | host:port/db | localhost:5432/yixiaoguan |
| PostgreSQL | username | yx_admin |
| PostgreSQL | password | Yx@Admin2026! |
| Redis | host:port | localhost:6379 |
| Redis | password | Yx@Redis2026! |
| business-api | 端口 | 8080 |
| ai-service | 端口 | 8000 |
| teacher-web (dev) | 端口 | 5173 |
| student-app (dev) | 端口 | 5174 |

---

## 六、⚠️ Java/Maven 非标准路径（执行构建命令前必读）

本机 `java`/`mvn` **不在系统 PATH** 中，必须用以下完整路径：

```powershell
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
$mvn = "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd"
```

执行示例：
```powershell
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f "C:\Users\Administrator\Documents\code\yixiaoguan\services\business-api\pom.xml" `
  spring-boot:run -pl ruoyi-admin
```

---

## 七、服务启动命令

### 基础设施（PostgreSQL + Redis + AI Service）
```powershell
# 在 deploy/ 目录，.env 已存在，直接启动
cd C:\Users\Administrator\Documents\code\yixiaoguan\deploy
docker compose up -d
```

### business-api（每次新开 PowerShell 都需设置环境变量）
```powershell
$env:POSTGRES_PASSWORD = "Yx@Admin2026!"
$env:REDIS_PASSWORD    = "Yx@Redis2026!"
$env:JAVA_HOME         = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f "C:\Users\Administrator\Documents\code\yixiaoguan\services\business-api\pom.xml" `
  spring-boot:run -pl ruoyi-admin
```

### teacher-web
```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\teacher-web
npm run dev    # http://localhost:5173
```

### student-app
```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app
npm run dev:h5    # http://localhost:5174
```

---

## 八、当前开发状态（截至 2026-04-03）

### ✅ 已完成
- business-api 全部 5 个模块（认证/会话/知识库/审批/通知）
- Dashboard API（DashboardController，含 6 个统计接口）
- teacher-web 全部页面（Dashboard、Questions、Approval、Knowledge、Analytics、Profile）+ WebSocket 引擎 + 真实 API 绑定
- student-app 全部页面（Login、Home、Chat、Apply、Status、Profile）+ SSE 流式 AI 对话 + 来源引用混合跳转策略
- ai-service RAG 管道 + 防幻觉检索门控阈值 + 流式输出

### 🔴 主要阻塞（按优先级）
1. **知识库实物入库**：81 份草稿尚未正式归类入库，8 个分类目录全部为空
   - 阻塞原因：R1-v3（provenance-aware 重映射）刚完成只读验收，正式 rename 尚未执行
   - 执行提示词：`docs/dev-guides/r1-v3-provenance-remap-prompt-2026-04-03.md`
2. **Teacher Web 联调复测**：Questions/Approval 页面的 `/api/v1/` 路径问题需最终确认
3. **Knowledge Detail 页面**：路由存在，内容渲染待验证

---

## 九、当前迭代规则（务必遵守）

- 学生端 AI 对话来源引用策略：**优先跳知识详情页 → 失败降级摘要弹层 → 有外链则外链兜底**
- AI 防幻觉优先于 UI 美化
- 知识库当前阶段：**不开放新扩量**，优先修复遗留问题（编号冲突、缺源、重复）
- 知识库编号重映射执行前：**必须先按 frontmatter `material_id` 校验内容归属**，禁止仅凭旧编号直接重命名
- 并行子代理提示词模板：单任务 + 固定输出格式 + 先计划后执行 + 超范围即停止
- 较长或复杂命令：**先写脚本到 `temp/`，执行后删除**

---

## 十、代码规范

- 注释语言：**中文**
- 函数/方法：camelCase
- 类名：PascalCase
- 数据库表名：snake_case + `yx_` 前缀
- 禁止在 `services/business-api/` 中直接调用 DashScope 或任何大模型 API
- 禁止创建测试文件（`test_*`、`*.test.*`、`*.spec.*`）；如需临时脚本放 `temp/`，用完即删
- 修改代码后自动执行编译验证

---

## 十一、知识库材料路径规则

- 原始材料：`_references/数据库部分材料/`，**清洗阶段不移动、不改名、不覆盖**
- 清洗产出：`knowledge-base/raw/first-batch-processing/`
  - `manifests/`：材料总表 CSV、清洗标注、whitelist、manual-review 清单
  - `converted/markdown/`：文本转换结果
  - `logs/`：转换日志
- 草稿文件：`knowledge-base/entries/first-batch-drafts/`（KB-20260324-XXXX.md 格式）
- 正式条目目录：`knowledge-base/entries/` 下的 8 个分类子目录（当前均为空，等待入库）
