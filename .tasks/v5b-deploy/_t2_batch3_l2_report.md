# T2 Batch-3 L2 运行时验证报告

**验证时间**: 2026-04-06T18:35:00+08:00  
**验证类型**: L2 Runtime Verification  
**执行位置**: 192.168.100.165 服务器  

---

## 执行命令

```bash
cd ~/dev/yixiaoguan/deploy
docker compose build business-api
docker compose up -d
sleep 60
docker compose ps
docker compose logs business-api --tail=30 | grep -iE 'started|error|exception|fail'
```

---

## 验证结果

### Docker Build

| 服务 | 状态 | 镜像大小 | 说明 |
|------|------|---------|------|
| business-api | ✅ SUCCESS | ~90MB | eclipse-temurin:21-jre-alpine |
| ai-service | ✅ SUCCESS | ~500MB | python:3.11-slim, pip install ~30s |

### 服务启动状态

| 服务 | 状态 | 健康检查 | 启动时间 | 说明 |
|------|------|---------|---------|------|
| postgres | ✅ UP (healthy) | ✅ PASS | 22h uptime | 数据持久化正常 |
| redis | ✅ UP (healthy) | ✅ PASS | 22h uptime | 数据持久化正常 |
| business-api | ✅ UP (healthy) | ✅ PASS | ~9s | Spring Boot 启动成功 |
| ai-service | ⚠️ UP (unhealthy) | ❌ FAIL | ~3s | 服务运行正常，healthcheck 失败 |
| nginx | ❌ NOT STARTED | N/A | N/A | 依赖 ai-service healthy |

### business-api 日志验证

```
Started RuoYiApplication in 8.668 seconds (process running for 9.521)
Scheduler quartzScheduler_$_NON_CLUSTERED started
```

✅ 无 DB 连接错误  
✅ 无 Redis 连接错误  
✅ Spring Boot 正常启动  

### ai-service 日志验证

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
2026-04-06 10:31:36,589 - main - INFO - 🚀 医小管 AI 服务启动中...
2026-04-06 10:31:36,748 - app.core.kb_vectorize - INFO - 向量存储初始化完成
2026-04-06 10:31:36,748 - main - INFO - ✅ ChromaDB 向量存储初始化成功
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ Uvicorn 正常启动  
✅ ChromaDB 初始化成功  
✅ 服务实际运行正常  

---

## 发现的问题

### ISSUE-1: ai-service healthcheck 失败

**严重程度**: MEDIUM  
**组件**: ai-service  
**描述**: Healthcheck 使用 `curl` 但 python:3.11-slim 镜像不包含 curl  

**根本原因**:
```yaml
# docker-compose.yml line 103
healthcheck:
  test: [ "CMD", "curl", "-f", "http://localhost:8000/" ]
```

**影响**:
- ai-service 被标记为 unhealthy
- nginx 无法启动（depends_on ai-service healthy）
- 前端页面无法访问

**修复方案**:
```yaml
# 方案 A: 使用 wget（需安装）
test: ["CMD-SHELL", "wget -qO- http://localhost:8000/ || exit 1"]

# 方案 B: 使用 Python（推荐，无需额外安装）
test: ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8000/\")' || exit 1"]
```

**临时解决方案**: 服务实际运行正常，可手动启动 nginx 进行测试

---

## L2 验证结论

**结果**: ⚠️ PARTIAL_PASS

**通过项**:
- ✅ Docker 镜像构建成功
- ✅ business-api 启动成功，Spring Boot 正常运行
- ✅ 数据库和 Redis 连接正常
- ✅ ai-service 实际运行正常

**未通过项**:
- ❌ ai-service healthcheck 失败（curl 不可用）
- ❌ nginx 未启动（被 healthcheck 阻塞）

**建议**:
1. 创建 hotfix 任务修复 ai-service healthcheck
2. 修复后重新执行 `docker compose up -d`
3. 验证 nginx 正常启动
4. 验证前端页面可访问（http://192.168.100.165 和 http://192.168.100.165:81）

---

**T2 签名**: Foreman  
**下一步**: 上报 T1，建议创建 hotfix 任务或在 batch-int 中修复
