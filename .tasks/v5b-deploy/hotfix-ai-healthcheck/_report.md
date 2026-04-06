# hotfix-ai-healthcheck 执行报告

## 任务概述
将 ai-service healthcheck 从 `curl` 改为 Python `urllib.request`，解决 `python:3.11-slim` 镜像中无 curl 导致的 unhealthy 问题。

## 执行时间
2026-04-06

## 修改内容

**文件**: `deploy/docker-compose.yml` 第 103 行

**变更前**:
```yaml
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8000/" ]
```

**变更后**:
```yaml
    healthcheck:
      test: ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8000/\")' || exit 1"]
```

## 验证结果

- [x] L0: healthcheck test 不再包含 "curl"，已改为 python -c 形式
- [ ] L1: YAML 语法验证需在 165 服务器执行 `docker compose config --quiet`
- [ ] L2: 服务健康状态需在 165 服务器验证 `docker compose ps`
- [ ] L3: T1 检查 healthcheck 在 python:3.11-slim 容器内有效

## 新发现的错误模式

无

## 备注

- 修改采用 CMD-SHELL 格式，与 business-api 的 healthcheck 保持一致
- 使用 `|| exit 1` 确保 urllib 异常时返回非零退出码
- 引号转义：`"http://localhost:8000/"` 已正确转义为 `\"`
