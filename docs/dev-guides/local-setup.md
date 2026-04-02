# 本地开发环境搭建指南

## 环境依赖

- Java 21 (使用 VS Code Red Hat Java Extension 自带的 JRE)
- Maven 3.x (使用 IntelliJ IDEA 自带的 Maven)
- Node.js 20+
- Docker & Docker Compose

## 路径配置

### Java
```powershell
$env:JAVA_HOME="C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
```

### Maven
```powershell
"C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd"
```

## 启动步骤

### 1. 启动基础设施（PostgreSQL + Redis）

```powershell
cd deploy
docker compose up -d postgres redis
```

数据库配置在 `deploy/.env`：
- PostgreSQL: `localhost:5432`, 用户 `yx_admin`, 密码 `Yx@Admin2026!`
- Redis: `localhost:6379`, 密码 `Yx@Redis2026!`

### 2. 编译后端

```powershell
cd services/business-api
$env:JAVA_HOME="C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" clean package -DskipTests
```

### 3. 启动后端

```powershell
cd services/business-api/ruoyi-admin
$env:JAVA_HOME="C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
$env:POSTGRES_PASSWORD="Yx@Admin2026!"
$env:REDIS_PASSWORD="Yx@Redis2026!"
& "$env:JAVA_HOME\bin\java.exe" -jar target/ruoyi-admin.jar
```

后端服务将启动在 `http://localhost:8080`

### 4. 启动前端

```powershell
cd apps/teacher-web
npm install  # 首次运行
npm run dev -- --host 0.0.0.0 --port 5175
```

前端将启动在 `http://192.168.100.209:5175/`

## 环境变量说明

后端需要以下环境变量：
- `POSTGRES_PASSWORD`: PostgreSQL 数据库密码
- `REDIS_PASSWORD`: Redis 密码

前端环境变量在 `apps/teacher-web/.env.development`：
- `VITE_API_BASE_URL`: API 基础地址
- `VITE_WS_BASE_URL`: WebSocket 基础地址

## 已知问题

1. **Druid 连接池验证查询**: PostgreSQL 不支持 `SELECT 1 FROM DUAL`，已修改为 `SELECT 1`
2. **Redis 密码**: 需要在 `application.yml` 中配置 `${REDIS_PASSWORD}` 环境变量
3. **后端 Bean 注入**: `IYxRoleService` 服务需要修复

## 测试验证

启动后可以通过以下方式验证：

```bash
# 测试后端健康
curl http://localhost:8080

# 通过 agent-browser 测试前端
npx agent-browser open http://192.168.100.209:5175/
```
