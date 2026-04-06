# Task Report: f-v5b-02-backend-dockerfile

## 执行摘要
创建 Spring Boot 后端 Dockerfile，符合规格要求。

## 修改文件

| 文件 | 变更类型 | 摘要 |
|------|----------|------|
| `services/business-api/Dockerfile` | 新增 | 使用 eclipse-temurin:21-jre-alpine 基础镜像 |

## 自检结果

### L0: 文件存在
```powershell
Test-Path "services/business-api/Dockerfile"
# 输出: True
```
✓ 通过

### L1: Docker Compose Build
```bash
# 目标命令（需在 165 服务器执行）：
cd ~/dev/yixiaoguan/deploy && docker compose build business-api
```
⚠ 阻塞：SSH 连接 192.168.100.165 超时，无法验证

### L2: JRE 21 版本确认
```bash
# 目标命令（需在 165 服务器执行）：
docker run --rm yx_business_api_test java -version 2>&1 | grep '21'
```
⚠ 阻塞：依赖 L1 完成

## 已知陷阱处理

- **RISK-1**: 需在 165 服务器确认 jar 存在后，才能成功构建
  ```bash
  ls -lh ~/dev/yixiaoguan/services/business-api/ruoyi-admin/target/ruoyi-admin.jar
  # 若不存在：cd ~/dev/yixiaoguan/services/business-api && mvn package -DskipTests
  ```

## 遗留问题

1. SSH 连接 165 服务器超时，L1/L2 验证待补做
2. 需确认 165 上 jar 文件存在后方可构建

## 新发现的错误模式

无

## Dockerfile 内容

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
