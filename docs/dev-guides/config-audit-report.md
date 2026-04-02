# 医小管项目配置核查与启动验证报告

> **报告生成时间**: 2026-04-01  
> **执行人**: AI 运维工程师  
> **任务**: E0-配置核查与 GlobalRules 固化

---

## 一、执行摘要

已完成配置核查任务，成功启动全部本地服务并验证配置有效性。发现**密码配置存在不一致**，需决策是否统一调整。

| 检查项 | 状态 |
|--------|------|
| 配置文件读取 | ✅ 完成 |
| Docker 基础设施启动 | ✅ 完成 |
| Business API (Java) 启动 | ✅ 完成 |
| AI Service 启动 | ✅ 完成 |
| Teacher Web 前端启动 | ✅ 完成 |
| 端口连通性验证 | ✅ 全部通过 |
| GlobalRules 更新 | ✅ 已追加实际配置 |

---

## 二、发现的问题

### 🔴 问题 1：密码配置不一致

**现状**: 项目存在两套密码值

| 来源 | PostgreSQL 密码 | Redis 密码 | 使用场景 |
|------|-----------------|------------|----------|
| `docker-compose.yml` 默认值 | `change_me_in_dotenv` | `change_me_in_dotenv` | 首次启动回退值 |
| `deploy/.env` 实际值 | `Yx@Admin2026!` | `Yx@Redis2026!` | **当前容器实际使用的密码** |

**影响**:
- 若依后端 (`business-api`) 启动时必须设置 `POSTGRES_PASSWORD` 和 `REDIS_PASSWORD` 环境变量，否则数据库连接失败
- `.globalrules` 最初记录的默认值会导致连接错误

---

## 三、当前运行配置（已验证）

### 3.1 基础设施层 (Docker)

```yaml
# 容器状态
yx_postgres:  Up 7 hours (healthy)    Port: 5432
yx_redis:     Up 7 hours (healthy)    Port: 6379  
yx_ai_service: Up 5 minutes           Port: 8000
```

### 3.2 应用层

| 服务 | 进程/端口 | 启动方式 | 状态 |
|------|-----------|----------|------|
| business-api | PID: 50376 / 8080 | Java jar | ✅ 运行中 |
| ai-service | Docker / 8000 | FastAPI | ✅ 运行中 |
| teacher-web | Node / 5173 | Vite Dev | ✅ 运行中 |

### 3.3 访问端点

| 服务 | 地址 | 说明 |
|------|------|------|
| 教师前端 | http://localhost:5173 | Vue 3 + Element Plus |
| 业务 API | http://localhost:8080 | Spring Boot |
| AI 服务 | http://localhost:8000 | FastAPI + ChromaDB |
| Swagger 文档 | http://localhost:8080/swagger-ui.html | API 调试 |

---

## 四、决策选项

### 选项 A：保持现状（推荐继续使用 `.env` 中的强密码）

**配置**:
- PostgreSQL: `Yx@Admin2026!`
- Redis: `Yx@Redis2026!`

**优点**:
- ✅ 密码强度足够，符合安全规范
- ✅ 无需重新初始化数据库（避免数据丢失）
- ✅ 当前 `.globalrules` 已记录真实值

**缺点**:
- ❌ 与 `docker-compose.yml` 中的默认值不一致

**启动命令**:
```powershell
$env:POSTGRES_PASSWORD="Yx@Admin2026!"
$env:REDIS_PASSWORD="Yx@Redis2026!"
java -jar ruoyi-admin.jar
```

---

### 选项 B：改回默认值（统一为 `change_me_in_dotenv`）

**配置**:
- PostgreSQL: `change_me_in_dotenv`
- Redis: `change_me_in_dotenv`

**优点**:
- ✅ 与 `docker-compose.yml` 默认值保持一致
- ✅ 配置简单，无需记忆复杂密码

**缺点**:
- ❌ **需要重建数据库容器**（会导致数据丢失）
- ❌ 密码过于简单，不符合安全最佳实践
- ❌ 需要修改 `deploy/.env` 文件

**操作步骤**:
```powershell
# 1. 停止并删除现有容器
cd deploy
docker compose down -v  # -v 会删除数据卷！

# 2. 修改 .env 文件
# POSTGRES_PASSWORD=change_me_in_dotenv
# REDIS_PASSWORD=change_me_in_dotenv

# 3. 重新启动
docker compose up -d
```

---

## 五、建议方案

**推荐选项 A（保持强密码）**，理由如下：

1. **数据安全**: 重建数据库会导致开发数据丢失
2. **生产一致性**: 生产环境必然使用强密码，开发环境保持一致更合理
3. **文档已更新**: `.globalrules` 已记录实际配置，团队可见

**后续行动建议**:
- [ ] 将 `deploy/.env` 文件加入 `.gitignore`（如尚未加入）
- [ ] 在团队内部文档中记录密码获取方式（从 `.env` 读取）
- [ ] 考虑创建 `.env.example` 模板文件供新成员参考

---

## 六、附录：GlobalRules 更新内容

以下配置已追加到 `.globalrules` 文件末尾：

```markdown
## ⚙️ 本地服务配置（真实值，禁止擅自修改）

> 此节由配置核查任务自动生成，如需修改配置请同步更新此处。

| 服务 | 配置项 | 值 |
|------|-------|-----|
| PostgreSQL | host | localhost |
| PostgreSQL | port | 5432 |
| PostgreSQL | database | yixiaoguan |
| PostgreSQL | username | yx_admin |
| PostgreSQL | password | Yx@Admin2026! |
| Redis | host | localhost |
| Redis | port | 6379 |
| Redis | password | Yx@Redis2026! |
| business-api | 端口 | 8080 |
| business-api | context-path | / |
| ai-service | 端口 | 8000 |
| ai-service | business-api 回调地址 | http://localhost:8080 |
| Vite proxy target | /api/v1 | http://localhost:8080 |
| Vite proxy target | /api | http://localhost:8080 |
```

---

**报告结束**
