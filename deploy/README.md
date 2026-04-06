# 医小管 - 生产环境部署指南

> 一键部署脚本：`./start-prod.sh`

---

## 1. 快速部署（一行命令）

```bash
cd ~/dev/yixiaoguan/deploy
./start-prod.sh
```

部署完成后访问：
- 学生端：http://服务器IP
- 教师端：http://服务器IP:81

---

## 2. 服务架构

```
┌─────────────────────────────────────────────────────────────┐
│                         用户浏览器                           │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
     端口 80          端口 81         端口 8080
     (学生端)        (教师端)        (API)
          │               │               │
┌─────────▼───────────────┴───────────────▼─────────────────┐
│                      Nginx (yx_nginx)                      │
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │ student-app/dist│  │ teacher-web/dist│                  │
│  └─────────────────┘  └─────────────────┘                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   ┌────▼────┐      ┌────▼────┐      ┌────▼────┐
   │business │◄────►│   AI    │      │  Redis  │
   │  -api   │      │ service │      │   7.x   │
   │(若依)   │      │(FastAPI)│      │         │
   │:8080    │      │ :8000   │      │ :6379   │
   └────┬────┘      └─────────┘      └─────────┘
        │
   ┌────▼────┐
   │PostgreSQL│
   │  16.x   │
   │ :5432   │
   └─────────┘
```

---

## 3. 前置条件

### 3.1 必需软件

| 软件 | 版本要求 | 检查命令 |
|------|----------|----------|
| Docker | >= 24.0 | `docker --version` |
| Docker Compose | >= 2.0 | `docker compose version` |
| Node.js | >= 20.19.0 | `node --version` |
| JDK | >= 17 | `java -version` |
| Maven | >= 3.8 | `mvn -version` |

### 3.2 Node 版本切换（重要）

165 服务器默认 Node 18.19.1，但 teacher-web 需要 Node >= 20.19.0：

```bash
# 安装 nvm（如未安装）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 安装 Node 24
nvm install 24

# 脚本会自动切换，或在 shell 中手动切换：
source ~/.nvm/nvm.sh && nvm use 24
```

### 3.3 环境变量配置

```bash
cd ~/dev/yixiaoguan/deploy

# 复制模板
cp .env.example .env

# 编辑 .env，填入真实值
vim .env
```

必需的环境变量：

```bash
# 数据库
POSTGRES_DB=yixiaoguan
POSTGRES_USER=yx_admin
POSTGRES_PASSWORD=your_secure_password_here

# Redis
REDIS_PASSWORD=your_redis_password_here

# AI 服务（可选，不填则 AI 功能不可用）
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_CHAT_MODEL=qwen-plus
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v3
```

---

## 4. 手动步骤（分步说明）

如果一键脚本失败，可手动执行以下步骤：

### 4.1 构建前端

```bash
# student-app（uni-app H5）
cd ~/dev/yixiaoguan/apps/student-app
npm install --silent
npx uni build -p h5

# teacher-web（Vue3 + Vite）
cd ~/dev/yixiaoguan/apps/teacher-web
source ~/.nvm/nvm.sh && nvm use 24
npm install --silent
npm run build-only
```

### 4.2 构建后端 jar

```bash
cd ~/dev/yixiaoguan/services/business-api
mvn package -DskipTests -q
```

### 4.3 启动 Docker Compose

```bash
cd ~/dev/yixiaoguan/deploy
docker compose build business-api
docker compose up -d
```

---

## 5. 服务管理命令

| 命令 | 说明 |
|------|------|
| `docker compose up -d` | 启动所有服务（后台） |
| `docker compose down` | 停止并删除所有服务 |
| `docker compose ps` | 查看服务运行状态 |
| `docker compose logs -f` | 查看所有服务日志（实时） |
| `docker compose logs -f business-api` | 查看指定服务日志 |
| `docker compose restart business-api` | 重启指定服务 |
| `docker compose build --no-cache business-api` | 强制重新构建后端镜像 |

### 常用排查命令

```bash
# 检查容器状态
docker compose ps

# 查看服务日志
docker compose logs -f --tail=100 business-api

# 进入容器调试
docker exec -it yx_business_api /bin/sh

# 检查数据库连接
docker exec -it yx_postgres psql -U yx_admin -d yixiaoguan

# 查看网络
docker network ls
docker network inspect deploy_default
```

---

## 6. 访问地址

| 服务 | URL | 说明 |
|------|-----|------|
| 学生端 | http://服务器IP | 学生小程序 H5 版本 |
| 教师端 | http://服务器IP:81 | 教师管理后台 |
| API 接口 | http://服务器IP:8080 | 后端 API 地址 |
| PostgreSQL | 服务器IP:5432 | 数据库（仅内部访问） |
| Redis | 服务器IP:6379 | 缓存（仅内部访问） |

### 服务器 165 具体地址

- 学生端：http://192.168.100.165
- 教师端：http://192.168.100.165:81
- API 接口：http://192.168.100.165:8080

---

## 7. 故障排查

### 7.1 前端构建失败

**现象**：`npm install` 或 `npx uni build` 报错  
**解决**：
```bash
# 检查 Node 版本
node --version  # 应为 20+ 或 24

# 清除缓存重试
rm -rf node_modules package-lock.json
npm install --silent
```

### 7.2 jar 文件不存在

**现象**：提示 `ruoyi-admin.jar` 未找到  
**解决**：
```bash
cd ~/dev/yixiaoguan/services/business-api
mvn package -DskipTests -q
```

### 7.3 数据库连接失败

**现象**：business-api 健康检查失败，日志显示数据库连接超时  
**解决**：
```bash
# 检查 .env 配置
cat ~/dev/yixiaoguan/deploy/.env

# 检查 Postgres 是否启动
docker compose ps postgres
docker compose logs postgres
```

### 7.4 端口被占用

**现象**：`docker compose up` 报错端口冲突  
**解决**：
```bash
# 检查端口占用
sudo netstat -tlnp | grep -E ':80|:81|:8080|:5432|:6379'

# 停止占用服务或修改 docker-compose.yml 端口映射
```

---

## 8. 目录结构

```
deploy/
├── start-prod.sh          # 一键部署脚本
├── docker-compose.yml     # Docker Compose 配置
├── .env                   # 环境变量（不提交 Git）
├── .env.example           # 环境变量模板
├── README.md              # 本文档
└── nginx/
    ├── nginx.conf         # Nginx 主配置
    └── conf.d/
        ├── student.conf   # 学生端配置（端口 80）
        └── teacher.conf   # 教师端配置（端口 81）
```
