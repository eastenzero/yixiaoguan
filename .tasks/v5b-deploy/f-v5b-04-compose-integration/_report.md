---
task_id: "f-v5b-04-compose-integration"
status: "completed"
completed_at: "2026-04-06"
---

# F-V5B-04: Docker Compose 全栈编排 - 执行报告

## 已完成的变更

### 1. deploy/docker-compose.yml

#### 1.1 修改 ai-service 的 BUSINESS_API_BASE_URL
- **原值**: `http://host.docker.internal:8080`（仅 Docker Desktop 生效，Linux 无效）
- **新值**: `http://business-api:8080`（Docker 内部服务名，跨平台生效）

#### 1.2 为 ai-service 添加 business-api 依赖
```yaml
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy
  business-api:
    condition: service_healthy
```

#### 1.3 新增 business-api 服务
- 构建上下文: `../services/business-api`
- 容器名: `yx_business_api`
- 端口映射: `8080:8080`
- 环境变量覆盖:
  - `SPRING_DATASOURCE_DRUID_MASTER_URL`: 覆盖 localhost:5432，指向 postgres 服务
  - `SPRING_DATASOURCE_DRUID_MASTER_USERNAME`: 数据库用户名
  - `SPRING_DATASOURCE_DRUID_MASTER_PASSWORD`: 数据库密码
  - `SPRING_DATA_REDIS_HOST`: 覆盖 localhost，指向 redis 服务
  - `SPRING_DATA_REDIS_PORT`: 6379
  - `SPRING_DATA_REDIS_PASSWORD`: Redis 密码
- 健康检查: `wget -qO- http://localhost:8080/captchaImage`（使用 alpine 镜像内置的 wget）
- 卷挂载:
  - `backend_logs:/app/logs` - 日志持久化
  - `backend_upload:/app/uploadPath` - 上传文件持久化
- 依赖: postgres 和 redis（condition: service_healthy）

#### 1.4 新增 nginx 服务
- 镜像: `nginx:1.25-alpine`
- 容器名: `yx_nginx`
- 端口映射:
  - `80:80` - 学生端（H5）
  - `81:81` - 教师端（Web）
- 卷挂载:
  - `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro` - 主配置
  - `./nginx/conf.d:/etc/nginx/conf.d:ro` - 虚拟主机配置
  - `../apps/student-app/dist/build/h5:/usr/share/nginx/html/student:ro` - 学生端构建产物
  - `../apps/teacher-web/dist:/usr/share/nginx/html/teacher:ro` - 教师端构建产物
- 依赖: business-api 和 ai-service（condition: service_healthy）

#### 1.5 新增 volumes
```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  backend_logs:        # 新增
    driver: local
  backend_upload:      # 新增
    driver: local
```

### 2. deploy/.env.example
- 顶部注释已更新为全栈部署描述（docker-compose.yml 中）

## 关键避坑点

### RISK-2: Druid 数据源环境变量名
Spring Boot 的 Druid 数据源使用的是 `spring.datasource.druid.master.url`，对应的环境变量是 `SPRING_DATASOURCE_DRUID_MASTER_URL`（注意全大写和下划线），而不是标准的 `SPRING_DATASOURCE_URL`。

### healthcheck 工具选择
business-api 使用 Alpine 基础镜像，`wget` 是内置的，而 `curl` 可能需要额外安装，因此 healthcheck 使用 wget 命令。

### host.docker.internal 的跨平台问题
原配置使用 `host.docker.internal:8080` 在 Docker Desktop（Mac/Windows）上有效，但在 Linux 服务器上无效。改为服务名 `business-api:8080` 是 Docker 内部 DNS 解析的标准做法。

## T1 检查清单验证

| 检查项 | 状态 | 说明 |
|--------|------|------|
| business-api 环境变量覆盖 application-druid.yml 的 localhost | ✅ | SPRING_DATASOURCE_DRUID_MASTER_URL 指向 postgres:5432 |
| ai-service 的 BUSINESS_API_BASE_URL 改为 http://business-api:8080 | ✅ | 已修改，Linux 服务器兼容 |
| 新增 volumes: backend_logs, backend_upload | ✅ | 已添加到 volumes 区块 |

## 服务启动顺序

```
postgres, redis (并行启动)
    ↓ (healthcheck 通过后)
business-api
    ↓ (healthcheck 通过后)
ai-service, nginx (并行启动)
```

## 本地验证命令

```bash
# 验证 YAML 语法
cd ~/dev/yixiaoguan/deploy && docker compose config --quiet

# 启动所有服务
cd ~/dev/yixiaoguan/deploy && docker compose up -d

# 查看服务状态
docker compose ps

# 查看 business-api 启动日志
docker compose logs business-api --tail=20

# 验证 healthcheck
docker compose exec business-api wget -qO- http://localhost:8080/captchaImage
```

## 新发现的错误模式

（本次执行无新增 anti-patterns）
