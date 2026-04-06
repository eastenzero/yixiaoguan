---
id: "task2-e2e-verify"
parent: "v4-kb-deploy"
type: "integration-test"
status: "pending"
tier: "T3"
priority: "high"
risk: "medium"
foundation: false

scope:
  - ".tasks/v4-kb-deploy/task2-e2e-verify/_report.md"
out_of_scope:
  - "apps/"
  - "services/"
  - "scripts/"
  - "knowledge-base/"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/v4-kb-deploy/task1-kb-ingest/_report.md"

done_criteria:
  L0: "_report.md 存在且包含5条问题的实测结果"
  L1: "5条问题中至少4条 AI 返回有效答案（非拒答、非幻觉）"
  L2: "curl 测试命令无网络错误，ai-service 返回 HTTP 200"
  L3: "电费问题返回完美校园APP步骤；报修返回后勤流程；校园卡返回充值/办理方式"

depends_on: ["task1-kb-ingest"]
created_at: "2026-04-06 13:15:00"
---

# 端到端验证：AI回答新KB内容

> 入库22条新KB后，AI能正确回答电费/报修/校园卡/奖学金/请假等生活服务问题，证明入库生效。

## 背景

task1-kb-ingest 完成后，ChromaDB 包含新22条KB。本任务通过调用 ai-service API 验证 AI 能检索到新内容。

## 执行步骤

### Step 1：确认 ai-service 运行

```bash
curl -s http://192.168.100.165:8000/health
```
预期返回 `{"status":"ok"}` 或类似响应。

### Step 2：逐条测试（在165服务器上执行）

用 curl 调用 `/chat/stream` 或 `/kb/search` 端点，逐条测试以下5个问题：

```bash
# 测试1：电费
curl -s -X POST http://localhost:8000/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "怎么交电费", "top_k": 3}'

# 测试2：报修
curl -s -X POST http://localhost:8000/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "东西坏了怎么报修", "top_k": 3}'

# 测试3：校园卡
curl -s -X POST http://localhost:8000/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "校园卡怎么办理", "top_k": 3}'

# 测试4：奖学金
curl -s -X POST http://localhost:8000/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "怎么申请奖学金", "top_k": 3}'

# 测试5：请假
curl -s -X POST http://localhost:8000/kb/search \
  -H "Content-Type: application/json" \
  -d '{"query": "请假流程是什么", "top_k": 3}'
```

**注意**：若 `/kb/search` 端点不存在，改用 `/kb/query`。先用 `curl http://localhost:8000/docs` 确认端点名称。

### Step 3：记录结果

在 `_report.md` 中记录每条问题的：
- 返回的 top-1 entry_id 和 title
- score（相关性分数）
- 是否命中新KB（KB-0150~KB-0171）

## 验收标准

| 问题 | 预期命中 KB | 预期 title |
|------|------------|-----------|
| 怎么交电费 | KB-0150 | 电费缴纳指南 |
| 东西坏了怎么报修 | KB-0151 | 宿舍报修流程 |
| 校园卡怎么办理 | KB-0152 | 校园卡办理与使用 |
| 怎么申请奖学金 | KB-0156 | 奖学金评定指南 |
| 请假流程是什么 | KB-0155 | 请假销假制度 |

## 已知陷阱

- KB 检索使用向量相似度，结果不精确匹配，关注 score > 0.5 即可认为命中
- 若分数过低（< 0.4），说明入库未生效，检查 task1 是否正确执行
