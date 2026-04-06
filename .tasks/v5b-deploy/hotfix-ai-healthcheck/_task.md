---
id: "hotfix-ai-healthcheck"
parent: "v5b-deploy"
type: "hotfix"
status: "done"
tier: "T3"
priority: "high"
risk: "low"

scope:
  - "deploy/docker-compose.yml"
out_of_scope:
  - "services/ai-service/Dockerfile"
  - "services/ai-service/app/"
  - "apps/"

context_files:
  - ".teb/antipatterns.md"
  - "deploy/docker-compose.yml"

done_criteria:
  L0: |
    docker-compose.yml 第 103 行 healthcheck test 不再包含 "curl"，
    改为 python -c 'import urllib.request...' 形式
  L1: |
    在 165 服务器上执行：
    cd ~/dev/yixiaoguan/deploy && docker compose config --quiet
    → 无错误输出（YAML 语法正确）
  L2: |
    在 165 服务器上执行：
    docker compose up -d
    sleep 30
    docker compose ps | grep ai-service
    → ai-service 状态为 healthy（不再是 unhealthy 或 starting）
    docker compose ps | grep nginx
    → nginx 状态为 Up（不再因依赖 ai-service 而阻塞）
  L3: "T1 检查：healthcheck test 命令在 python:3.11-slim 容器内有效"

depends_on: ["f-v5b-04-compose-integration"]
created_at: "2026-04-06"
---

# hotfix-ai-healthcheck: 修复 ai-service healthcheck

> 完成后：ai-service 状态变为 healthy，nginx 正常启动，全栈 5 个服务全部 Up。

## 根因

`docker-compose.yml` 的 ai-service healthcheck 使用 `curl`，但 `python:3.11-slim`
基础镜像不包含 `curl`（Debian slim 版本，极简安装），每次健康检查都 exit 1，
导致 ai-service 永远 unhealthy，nginx 因 `depends_on: ai-service: condition: service_healthy`
而无法启动。

## 精确修改

**文件**：`deploy/docker-compose.yml`

**当前内容（约第 103 行）**：
```yaml
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8000/" ]
```

**修改为**：
```yaml
    healthcheck:
      test: ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8000/\")' || exit 1"]
```

其余字段（interval/timeout/retries）保持不变。

## 验证步骤（在 165 服务器上）

```bash
cd ~/dev/yixiaoguan/deploy

# 1. 语法检查
docker compose config --quiet

# 2. 重启 ai-service（不需要重建镜像）
docker compose up -d ai-service

# 3. 等待健康检查通过（约 30s）
sleep 30
docker compose ps

# 4. 如果 ai-service 已 healthy，nginx 会自动启动
# 若 nginx 未启动：
docker compose up -d nginx
```

## 预期结果

```
NAME               STATUS           PORTS
yx_postgres        Up (healthy)     0.0.0.0:5432->5432/tcp
yx_redis           Up (healthy)     0.0.0.0:6379->6379/tcp
yx_business_api    Up (healthy)     0.0.0.0:8080->8080/tcp
yx_ai_service      Up (healthy)     0.0.0.0:8000->8000/tcp
yx_nginx           Up               0.0.0.0:80->80/tcp, 0.0.0.0:81->81/tcp
```

## 已知陷阱

- 修改 docker-compose.yml 后无需重建镜像，直接 `docker compose up -d` 即可生效
- `python:3.11-slim` 中 Python 可执行文件名为 `python3`，但 slim 镜像通常也有 `python` 软链接，
  如报错 `python: not found`，改用 `python3`
- healthcheck 用双引号和转义需注意：`"http://localhost:8000/"` 的内部引号需转义为 `\"`
