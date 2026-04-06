---
id: "f-v5b-04-compose-integration"
parent: "v5b-deploy"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "high"

scope:
  - "deploy/docker-compose.yml"
  - "deploy/.env.example"
out_of_scope:
  - "services/business-api/ruoyi-admin/src/"
  - "apps/"
  - "deploy/nginx/"

context_files:
  - ".teb/antipatterns.md"
  - "deploy/docker-compose.yml"
  - "deploy/.env"
  - "deploy/.env.example"
  - "services/business-api/ruoyi-admin/src/main/resources/application.yml"
  - "services/business-api/ruoyi-admin/src/main/resources/application-druid.yml"
  - ".tasks/v5b-deploy/_task.md"
  - ".tasks/v5b-deploy/f-v5b-02-backend-dockerfile/_task.md"
  - ".tasks/v5b-deploy/f-v5b-03-nginx-config/_task.md"

done_criteria:
  L0: "deploy/docker-compose.yml 包含 business-api 和 nginx 两个服务定义"
  L1: |
    在 165 服务器上执行：
    cd ~/dev/yixiaoguan/deploy && docker compose config --quiet
    → 无错误输出（验证 YAML 语法和变量引用正确）
  L2: |
    cd ~/dev/yixiaoguan/deploy && docker compose up -d
    sleep 60
    docker compose ps
    → 所有服务状态为 Up 或 healthy（business-api 启动约 30-60s）
    docker compose logs business-api --tail=20 | grep -i 'started\|error'
    → 日志显示 Spring Boot 启动成功，无 DB 连接错误
  L3: |
    T1 检查：
    - business-api 环境变量覆盖了 application-druid.yml 的 localhost
    - ai-service 的 BUSINESS_API_BASE_URL 改为 http://business-api:8080
    - 新增 volumes: backend_logs, backend_upload

depends_on: ["f-v5b-02-backend-dockerfile", "f-v5b-03-nginx-config"]
created_at: "2026-04-06"
---

# F-V5B-04: Docker Compose 全栈编排

> 完成后：`deploy/docker-compose.yml` 包含全部 5 个服务，
> `docker compose up -d` 可一键启动，`docker compose ps` 全部 healthy。

## 背景

当前 docker-compose.yml 只有 postgres、redis、ai-service。需要新增 business-api 和 nginx。

## 变更规格

### 1. 修改 ai-service 的 BUSINESS_API_BASE_URL

```yaml
# 原值（host.docker.internal 仅 Docker Desktop 生效，Linux 无效）
BUSINESS_API_BASE_URL: http://host.docker.internal:8080
# 改为 Docker 内部服务名
BUSINESS_API_BASE_URL: http://business-api:8080
```

同时为 ai-service 添加 depends_on：
```yaml
depends_on:
  postgres:
    condition: service_healthy
  redis:
    condition: service_healthy
  business-api:
    condition: service_healthy
```

### 2. 新增 business-api 服务

```yaml
business-api:
  build:
    context: ../services/business-api
    dockerfile: Dockerfile
  container_name: yx_business_api
  restart: unless-stopped
  environment:
    # 覆盖 application-druid.yml 中的 localhost（RISK-2）
    SPRING_DATASOURCE_DRUID_MASTER_URL: jdbc:postgresql://postgres:5432/${POSTGRES_DB:-yixiaoguan}
    SPRING_DATASOURCE_DRUID_MASTER_USERNAME: ${POSTGRES_USER:-yx_admin}
    SPRING_DATASOURCE_DRUID_MASTER_PASSWORD: ${POSTGRES_PASSWORD}
    # 覆盖 application.yml 中的 spring.data.redis.host: localhost
    SPRING_DATA_REDIS_HOST: redis
    SPRING_DATA_REDIS_PORT: 6379
    SPRING_DATA_REDIS_PASSWORD: ${REDIS_PASSWORD}
  ports:
    - "8080:8080"
  volumes:
    - backend_logs:/app/logs
    - backend_upload:/app/uploadPath
  depends_on:
    postgres:
      condition: service_healthy
    redis:
      condition: service_healthy
  healthcheck:
    test: ["CMD-SHELL", "wget -qO- http://localhost:8080/captchaImage || exit 1"]
    interval: 15s
    timeout: 10s
    retries: 10
    start_period: 60s
```

### 3. 新增 nginx 服务

```yaml
nginx:
  image: nginx:1.25-alpine
  container_name: yx_nginx
  restart: unless-stopped
  ports:
    - "80:80"
    - "81:81"
  volumes:
    - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    - ./nginx/conf.d:/etc/nginx/conf.d:ro
    - ../apps/student-app/dist/build/h5:/usr/share/nginx/html/student:ro
    - ../apps/teacher-web/dist:/usr/share/nginx/html/teacher:ro
  depends_on:
    business-api:
      condition: service_healthy
    ai-service:
      condition: service_healthy
```

### 4. volumes 区块新增

```yaml
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  backend_logs:
    driver: local
  backend_upload:
    driver: local
```

### 5. 更新 .env.example 顶部注释

将旧说明从"本地开发"改为"全栈部署"。

## 已知陷阱

- **RISK-2（关键）**: Spring Boot 的 Druid 数据源用的是 `spring.datasource.druid.master.url`，不是标准的 `spring.datasource.url`。对应的环境变量是 `SPRING_DATASOURCE_DRUID_MASTER_URL`。注意大写和下划线
- business-api healthcheck 使用 `wget`（alpine 镜像有，`curl` 不一定有）
- ai-service 原本依赖 host.docker.internal，在 Linux 上不生效，必须改为服务名
- `version: "3.9"` 已 obsolete，会有 warning，不影响功能，保留即可
