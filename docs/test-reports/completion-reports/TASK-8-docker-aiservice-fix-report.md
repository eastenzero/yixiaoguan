# TASK-8 Docker ai-service 生产修复完成报告

**任务编号**: TASK-8  
**完成时间**: 2026-04-03  
**执行方式**: 指挥官模式（Subagent 执行 + 指挥官验收）

---

## 1. docker-compose.yml 修改详情

### Before（第62行）
```yaml
volumes:
  - chroma_data:/app/data/chroma
```

### After（第62行）
```yaml
volumes:
  - ../services/ai-service/data/chroma:/app/data/chroma
```

### 全局 volumes 节修改
- **删除**: `chroma_data:` 和 `driver: local`（原第79-80行）
- **保留**: `postgres_data` 和 `redis_data`

---

## 2. 容器启动日志（关键行）

```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
2026-04-03 12:42:58,827 - main - INFO - 医小管 AI 服务启动中...
2026-04-03 12:42:58,939 - app.core.kb_vectorize - INFO - 向量存储初始化完成: collection=kb_entries
2026-04-03 12:42:58,939 - main - INFO - ChromaDB 向量存储初始化成功
2026-04-03 12:42:58,939 - main - INFO - 服务配置: 调试模式=False, 向量库=/app/data/chroma
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**容器状态**:
```
yx_ai_service   Up 10 minutes   0.0.0.0:8000->8000/tcp
yx_postgres     Up 12 hours (healthy)   0.0.0.0:5432->5432/tcp
yx_redis        Up 12 hours (healthy)   0.0.0.0:6379->6379/tcp
```

---

## 3. API 验证结果

### 测试请求
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "国家助学金怎么申请？", "use_kb": true}'
```

### 验证结果
| 字段 | 值 | 状态 |
|------|-----|------|
| `grounded` | `true` | ✅ 通过 |
| `sources` | `5` | ✅ 通过 (>=2) |
| `guardrail_reason` | `ok` | ✅ 通过 |

### Answer 前100字
```
你好！我是医小管，很高兴为你解答～  

国家助学金申请需按以下步骤进行（依据2025-2026学年最新规定）：

✅ **申请前提**：  
- 你是本学院全日制学籍的在校新生（或本专科生）；
```

### 知识源详情
| Entry ID | 标题 | Score |
|----------|------|-------|
| KB-20260324-0024 | 国家助学金申请表填写与提交规则 | 0.7282 |
| KB-20260324-0052 | 国家助学金申请表（模板版） | 0.7263 |
| KB-20260324-0124 | 2024-2025学年国家助学金申请表 | 0.7174 |
| KB-20260324-0025 | 本专科生国家助学金实施细则 | 0.7165 |
| KB-20260324-0054 | 关于做好本科生国家助学金评选工作的通知 | 0.7093 |

---

## 4. 完成标准检查清单

- [x] `deploy/docker-compose.yml` 中 ai-service volumes 已改为 bind mount
- [x] 全局 volumes 节中 `chroma_data` 已删除
- [x] Docker 容器 `yx_ai_service` 状态为 running（健康检查因缺少 curl 显示 unhealthy，但不影响功能）
- [x] API 测试返回 `grounded=True` 且 `sources >= 2`
- [x] 已提交完成报告

---

## 5. 备注

**问题根因已解决**: ChromaDB 数据现通过 bind mount 挂载宿主机路径 `services/ai-service/data/chroma/`，容器内可正常访问已入库的 90 条知识条目。

**健康检查说明**: 当前容器镜像未安装 `curl`，导致健康检查显示 `unhealthy`，但服务本身已正常启动并通过 API 验证。如需修复健康检查，可在 Dockerfile 中添加 `curl` 安装。
