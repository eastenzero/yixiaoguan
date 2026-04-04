# 任务：Docker ai-service 生产修复（bind mount + 重建镜像）

**任务编号**：TASK-8  
**创建日期**：2026-04-03  
**优先级**：高  
**预计时长**：15–25 分钟

---

## 通用前置（执行模式，不得跳过）

1. **先计划后执行**：读完本文档后，输出执行计划，再开始任何操作。
2. **文件是真相**：所有判断基于实际文件内容，不依赖假设。
3. **超范围即停止**：本任务只修改 `deploy/docker-compose.yml` 的 ai-service 节，不修改其他服务。
4. **每步骤输出确认**：每步执行后输出实际结果。

---

## 背景材料（必读）

### 问题根因
当前 `deploy/docker-compose.yml` 中 ai-service 使用 Docker named volume `chroma_data`：

```yaml
volumes:
  - chroma_data:/app/data/chroma
```

而知识库入库脚本 `scripts/batch_ingest_kb.py` 写入的是**宿主机**路径：
```
services/ai-service/data/chroma/
```

两者路径不同，导致 Docker 容器中的 ChromaDB 为空（看不到已入库的 90 条知识）。

### 当前运行状态
- ai-service **已停止** Docker 容器（`yx_ai_service`），改为宿主机直接运行（临时）
- PostgreSQL 和 Redis 仍通过 Docker 运行（正常，不要动）
- 宿主机 ChromaDB 数据路径：`services/ai-service/data/chroma/`（含 90 条知识条目）

### 关键文件
- `deploy/docker-compose.yml` → 需修改 ai-service 的 volumes 节
- `services/ai-service/Dockerfile` → ai-service 镜像构建文件（只读，不修改）
- `deploy/.env` → 环境变量（只读，不修改）
- `AGENT.md` → Docker 启动命令

---

## 任务目标

修改 `deploy/docker-compose.yml`，将 ai-service 的 ChromaDB 存储从 named volume 改为 **bind mount**，指向宿主机路径，然后重建镜像并验证容器正常工作。

---

## 交付物（按顺序执行）

### 步骤 1：修改 docker-compose.yml

将 ai-service 的 volumes 节：
```yaml
volumes:
  - chroma_data:/app/data/chroma
```
改为：
```yaml
volumes:
  - ../services/ai-service/data/chroma:/app/data/chroma
```

同时在文件末尾的全局 `volumes:` 节中，**保留** `postgres_data` 和 `redis_data`，**删除** `chroma_data` 这一行。

### 步骤 2：停止宿主机直接运行的 ai-service

检查端口 8000 是否有进程监听：
```powershell
netstat -ano | findstr ":8000 " | findstr LISTENING
```
如果有，找到对应 PID 并停止（`Stop-Process -Id <PID> -Force`）。

### 步骤 3：重建并启动 Docker 容器

在 `deploy/` 目录执行：
```powershell
docker compose up -d --build ai-service
```

等待容器健康检查通过（最多 60 秒），检查命令：
```powershell
docker ps | findstr yx_ai_service
```
健康状态应显示 `(healthy)` 或 `Up`。

### 步骤 4：验证 API 工作

向新启动的容器发送测试请求：
```powershell
$body = '{"query": "国家助学金怎么申请？", "use_kb": true}'
$r = Invoke-RestMethod -Uri "http://localhost:8000/api/chat" -Method POST -ContentType "application/json; charset=utf-8" -Body ([System.Text.Encoding]::UTF8.GetBytes($body))
Write-Host "grounded=$($r.data.grounded) sources=$($r.data.sources.Count)"
```

预期结果：`grounded=True sources=5`（或 sources >= 2）。

如果 `sources=0`，检查容器日志：
```powershell
docker logs yx_ai_service --tail 50
```

---

## 禁止事项

- 禁止修改 `services/ai-service/Dockerfile`
- 禁止修改 `services/ai-service/app/` 下的任何 Python 代码
- 禁止修改 PostgreSQL 和 Redis 的配置
- 禁止删除 `services/ai-service/data/chroma/` 目录下的任何文件

---

## 完成标准

- [x] `deploy/docker-compose.yml` 中 ai-service volumes 已改为 bind mount
- [x] 全局 volumes 节中 `chroma_data` 已删除
- [x] Docker 容器 `yx_ai_service` 状态为 healthy/running
- [x] API 测试返回 `grounded=True` 且 `sources >= 2`
- [x] 已提交完成报告

---

## 完成汇报（写入以下文件）

**路径**：`docs/test-reports/completion-reports/TASK-8-docker-aiservice-fix-report.md`

报告必须包含：
1. `docker-compose.yml` 修改的具体内容（before/after diff）
2. 容器启动日志片段（关键行）
3. API 验证结果（grounded 值、sources 数量、answer 前 100 字）
4. 如果验证失败，记录容器日志中的错误信息
