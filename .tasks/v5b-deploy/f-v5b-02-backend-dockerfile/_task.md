---
id: "f-v5b-02-backend-dockerfile"
parent: "v5b-deploy"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"

scope:
  - "services/business-api/Dockerfile"
out_of_scope:
  - "services/business-api/ruoyi-admin/src/"
  - "services/business-api/ruoyi-common/"
  - "apps/"
  - "deploy/"

context_files:
  - ".teb/antipatterns.md"
  - "services/ai-service/Dockerfile"
  - ".tasks/v5b-deploy/_task.md"

done_criteria:
  L0: "services/business-api/Dockerfile 文件存在"
  L1: |
    在 165 服务器上执行：
    cd ~/dev/yixiaoguan/deploy && docker compose build business-api
    → 构建无 error（需先确认 jar 存在，详见已知陷阱）
  L2: |
    docker run --rm yx_business_api_test java -version 2>&1 | grep '21'
    → 确认使用 JRE 21
  L3: "T1 检查：Dockerfile 内容符合规格，无安全隐患（无硬编码密码）"

depends_on: []
created_at: "2026-04-06"
---

# F-V5B-02: Spring Boot 后端 Dockerfile

> 完成后：`services/business-api/Dockerfile` 存在，
> `docker compose build business-api` 可成功构建镜像。

## 背景

business-api（若依 Spring Boot）目前在 Tmux 中手动 `java -jar` 启动，
需要 Dockerfile 纳入 Docker Compose 编排。

## 规格

```dockerfile
FROM eclipse-temurin:21-jre-alpine
LABEL maintainer="yixiaoguan-team"

WORKDIR /app

# 使用预构建 jar（不在容器内 Maven 构建，节省资源）
COPY ruoyi-admin/target/ruoyi-admin.jar app.jar

RUN mkdir -p logs uploadPath

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
```

## 已知陷阱

- **RISK-1（关键）**: `target/` 目录被 Mutagen 排除同步。执行前先在 165 上确认 jar 存在：
  ```bash
  ls -lh ~/dev/yixiaoguan/services/business-api/ruoyi-admin/target/ruoyi-admin.jar
  ```
  若不存在：
  ```bash
  cd ~/dev/yixiaoguan/services/business-api && mvn package -DskipTests
  ```
- Docker build context 是 `services/business-api/`，COPY 路径相对于此目录
- `eclipse-temurin:21-jre-alpine` 是 JRE（非 JDK），体积更小，够用
