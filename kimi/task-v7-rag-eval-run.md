# T3 任务: v7 RAG-EVAL 实际执行 — 在 165 服务器上运行评测

## 角色
你是山东第一医科大学（医小管）RAG 系统的评测专家。

## ⚠️ 重要：所有命令必须通过 SSH 在远程服务器上执行

**所有 curl 和 python 命令都必须通过 SSH 在 165 服务器上执行，不要在本地 PowerShell 执行！**

使用以下方式执行每条命令：
```
ssh easten@10.80.3.165 "命令内容"
```

## 背景
- INGEST-V7 已完成，ai-service 已启动（entry_count=290）
- 评测集和评测脚本已在上一步创建
- 本任务需要在 165 服务器上实际运行评测

## 任务目标
在 165 服务器上执行实际的 RAG 评测，验证 v7 新增 KB 的检索和回答质量。

## 执行步骤

### Step 1: 确认 ai-service 在线
```bash
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats | python3 -m json.tool"
# 期望 entry_count >= 260
```

### Step 2: 手动测试 v7 关键问题（逐一调用 /chat 接口）

请依次测试以下 20 个问题，记录每个问题的回答：

**院系与专业类（10 题）**
```bash
# 问题 1
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "眼科学院有哪些本科专业？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 2
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "药学院的硕博点有哪些？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 3
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "实验动物学院是做什么的？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 4
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "护理学院在哪个校区？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 5
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "运动医学与康复学院有几个本科专业？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 6
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "医学信息与人工智能学院是什么时候成立的？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 7
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "外国语学院有哪些语种专业？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 8
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "继续教育学院怎么报名？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 9
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "国际教育学院招收留学生吗？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 10
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "通识教育部是干什么的？", "user_id": "eval-v7"}' | python3 -m json.tool
```

**科研与研究生类（5 题）**
```bash
# 问题 11
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "科研部的联系电话是多少？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 12
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "博士研究生怎么报考？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 13
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "研究生有哪些奖学金？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 14
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "推免保研需要什么条件？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 15
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "学位论文有什么要求？", "user_id": "eval-v7"}' | python3 -m json.tool
```

**联系方式类（2 题）**
```bash
# 问题 16
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "济南校区各学院的电话是多少？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 17
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "泰安校区各学院的联系方式？", "user_id": "eval-v7"}' | python3 -m json.tool
```

**拒答类（3 题）**
```bash
# 问题 18
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "山东第一医科大学的股票代码是多少？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 19
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "校长家住哪里？", "user_id": "eval-v7"}' | python3 -m json.tool

# 问题 20
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "帮我写一篇论文", "user_id": "eval-v7"}' | python3 -m json.tool
```

### Step 3: 回归测试（5 题）
```bash
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "图书馆怎么借书？", "user_id": "eval-v7"}' | python3 -m json.tool
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "怎么查成绩？", "user_id": "eval-v7"}' | python3 -m json.tool
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "校园卡丢了怎么办？", "user_id": "eval-v7"}' | python3 -m json.tool
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "怎么申请奖学金？", "user_id": "eval-v7"}' | python3 -m json.tool
curl -s -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"message": "心理咨询预约方式？", "user_id": "eval-v7"}' | python3 -m json.tool
```

### Step 4: 生成评测报告

将实际测试结果写入 `kimi/rag-eval-v7-report.md`（覆盖之前的占位报告），格式：

```markdown
# RAG Evaluation V7 Report (实际评测)

评测时间: YYYY-MM-DD HH:MM
入库条目: 290 (含 v7 新增 51 条)

## 评测总结

| 指标 | 目标 | 实际 | 状态 |
|------|------|------|------|
| v7新题命中率 (17题) | ≥ 80% | XX% | ✅/❌ |
| 拒答准确率 (3题) | 100% | XX% | ✅/❌ |
| 回归测试 (5题) | 100% | XX% | ✅/❌ |

## 详细结果

### v7 新增问题 (17题)
| # | 问题 | 回答摘要(前100字) | 命中 | 质量(1-5) |
|---|------|-----------------|------|---------|

### 拒答测试 (3题)
| # | 问题 | 回答摘要 | 正确拒答 |
|---|------|---------|---------|

### 回归测试 (5题)
| # | 问题 | 回答摘要 | 通过 |
|---|------|---------|------|

## 结论
PASS / FAIL
```

请开始执行。
