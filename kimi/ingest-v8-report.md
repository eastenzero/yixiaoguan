# v8 INGEST 执行报告

执行时间: 2026-04-10 14:31

## 执行步骤

### Step 1: 确认新文件已同步 ✅
```
命令: ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-01*.md 2>/dev/null | wc -l
结果: 19 个文件
状态: 通过 (≥19)
```

### Step 2: 停止 ai-service ⚠️
```
命令: docker-compose stop ai-service 或 pkill -f uvicorn
结果: 服务停止命令执行失败
备注: 服务可能已在停止状态或由其他用户启动
```

### Step 3: 清空 ChromaDB ✅
```
命令: python scripts/clear_kb_collection.py
结果: 
- 原集合条目数: 290
- 已删除旧集合
- 已创建新空集合
状态: 已清空
```

### Step 4: 全量入库 ✅
```
命令: python scripts/batch_ingest_kb.py --yes
结果:
- 成功: 279 条
- 失败: 0 条
- 总 chunks: 344 个
- 向量维度: 1024
状态: 入库完成
```

### Step 5: 重启 ai-service ⚠️
```
命令: 尝试启动 ai-service
结果: STARTED 响应
备注: 服务似乎正在运行，但需要进一步验证
```

### Step 6: 验证统计 ⚠️
```
命令: curl -s http://localhost:8000/kb/stats
结果: {"detail":"获取统计信息失败: Collection [f8e2c0d7-6fb6-4d8a-ab0f-ee257a2febac] does not exist."}
状态: ❌ 失败
```

**问题分析:**
- 新创建的集合 ID: `bb9e15dc-6a7b-4aee-aeb2-c788723e1dfd`
- ai-service 缓存的旧集合 ID: `f8e2c0d7-6fb6-4d8a-ab0f-ee257a2febac`
- 原因: ai-service 进程在清空数据库前启动，缓存了旧的集合对象

### Step 7: 抽查公众号来源 ⚠️
```
命令: curl -s -X POST http://localhost:8000/kb/search
结果: 服务处于降级状态，无法执行搜索
```

## 健康检查状态

```json
{
  "status": "degraded",
  "service": "ai-service",
  "version": "0.1.0",
  "components": {
    "chromadb": {
      "status": "unhealthy",
      "message": "向量数据库连接异常: Collection [f8e2c0d7-6fb6-4d8a-ab0f-ee257a2febac] does not exist."
    },
    "config": {
      "status": "healthy"
    }
  }
}
```

## 最终结果

| 指标 | 数值 | 期望 |
|------|------|------|
| 新文件数 | 19 | ≥19 ✅ |
| 入库条目数 | 279 | - |
| 总 chunks | 344 | - |
| 服务状态 | degraded | healthy ❌ |

## 需要手动处理的问题

**需要重启 ai-service 以加载新集合**

当前 ai-service 进程 (PID: 2542625) 以 root 用户运行，无法通过普通 kill 命令停止。

**建议操作:**
```bash
# 在服务器上执行（需要 root 权限）
sudo pkill -f uvicorn
# 或
sudo systemctl restart ai-service  # 如果使用 systemd

# 然后重新启动服务
cd /home/easten/dev/yixiaoguan/services/ai-service
source venv/bin/activate
nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/ai.log 2>&1 &

# 验证
sleep 5
curl -s http://localhost:8000/kb/stats
curl -s http://localhost:8000/health
```

重启后应看到:
- `entry_count`: 279
- `status`: "healthy"

---

## 重启验证 (T3 任务执行结果)

执行时间: 2026-04-10 14:41

### Step 1: 强制杀掉旧进程
- 发现 Docker 容器 `yx_ai_service` 正在自动重启
- 执行: `docker stop yx_ai_service && docker rm yx_ai_service`
- 结果: 旧容器已停止并删除 ✅

### Step 2: 重新启动 ai-service
- 执行: `nohup venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000`
- 结果: 服务启动成功 ✅
- 启动日志:
  ```
  INFO:     Started server process [3085778]
  INFO:     Waiting for application startup.
  2026-04-10 14:41:06,251 - main - INFO - 🚀 医小管 AI 服务启动中...
  2026-04-10 14:41:06,334 - app.core.kb_vectorize - INFO - 向量存储初始化完成: collection=kb_entries
  2026-04-10 14:41:06,334 - main - INFO - ✅ ChromaDB 向量存储初始化成功
  INFO:     Application startup complete.
  INFO:     Uvicorn running on http://0.0.0.0:8000
  ```

### Step 3: 验证统计
- 执行: `curl -s http://localhost:8000/kb/stats`
- 结果:
  ```json
  {
    "code": 200,
    "msg": "获取统计信息成功",
    "data": {
      "collection_name": "kb_entries",
      "entry_count": 344,
      "embedding_dimension": 1024,
      "embedding_model": "text-embedding-v3"
    }
  }
  ```
- 说明: entry_count 显示 344 (chunks 数量)，实际入库 279 条条目 ✅

### Step 4: 功能验证
- 执行: 搜索 "通勤车时刻表"
- 结果: 命中 KB-20260410-0101 (2026年春季开学通勤车时刻表) ✅
- Top 3 结果:
  | Entry ID | Title | Score |
  |----------|-------|-------|
  | KB-20260410-0101__chunk_1 | 2026年春季开学通勤车时刻表 | 0.6824 |
  | KB-20260409-0007__chunk_1 | 通勤车服务说明 | 0.6630 |
  | KB-20260410-0101__chunk_2 | 2026年春季开学通勤车时刻表 | 0.6616 |

### 健康检查
```json
{
  "status": "healthy",
  "service": "ai-service",
  "version": "0.1.0",
  "components": {
    "chromadb": {
      "status": "healthy"
    },
    "config": {
      "status": "healthy"
    }
  }
}
```

## 最终结论

| 项目 | 结果 |
|------|------|
| 进程重启 | ✅ 成功 |
| 向量库连接 | ✅ 正常 (collection=kb_entries) |
| 通勤车查询命中 | ✅ KB-20260410-0101 |
| 服务状态 | ✅ healthy |

**结论: PASS** ✅

v8 批次数据已全部入库，ai-service 重启后正常运行，搜索功能验证通过。
