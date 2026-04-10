# T3 任务: v8 RAG-EVAL — 回归测试 + 新增评测题

## 服务器: 192.168.100.165
## ⚠️ 所有命令通过 SSH 执行

## 背景
- v7 基线: Recall@5=86.0%, 拒答=92.9%
- v8 新增 19 条公众号来源 KB（KB-20260410-0101~0119）
- 当前入库: 279 条 / 344 chunks

## Step 1: 确认服务在线

```
ssh easten@192.168.100.165 "curl -s http://localhost:8000/kb/stats"
```

## Step 2: 新增 5-8 个测试题（基于 v8 新 KB 内容）

在 `scripts/eval/eval-set-v3.yaml` 末尾追加以下测试题：

```yaml
# ==================== v8 公众号来源内容新增 (7题) ====================

- id: "v8-001"
  question: "开学通勤车几点发车，在哪坐？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0101", "KB-20260410-0102"]
  category: "grounding-verify-in"

- id: "v8-002"
  question: "假期水管坏了报修电话是多少？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0105"]
  category: "grounding-verify-in"

- id: "v8-003"
  question: "假期食堂还开着吗？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0106"]
  category: "grounding-verify-in"

- id: "v8-004"
  question: "2026年硕士研究生调剂怎么申请？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0109", "KB-20260410-0110"]
  category: "grounding-verify-in"

- id: "v8-005"
  question: "有没有去加拿大或者英国的暑期项目？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0113", "KB-20260410-0114"]
  category: "grounding-verify-in"

- id: "v8-006"
  question: "就业服务平台的网址是什么？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0115"]
  category: "grounding-verify-in"

- id: "v8-007"
  question: "个人所得税怎么做年度汇算？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0118", "KB-20260410-0119"]
  category: "grounding-verify-in"
```

## Step 3: 运行评测脚本

```
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v3.py"
```

## Step 4: 查看报告

```
ssh easten@192.168.100.165 "cat /home/easten/dev/yixiaoguan/scripts/eval/eval-report-v3.md"
```

## Step 5: 写入本地报告

将 Step 4 的报告内容写入 `kimi/rag-eval-v8-report.md`。

## 验收标准
- AC-EVAL8-01: 新增 7 题
- AC-EVAL8-02: Recall@5 ≥ 85%
- AC-EVAL8-03: 原有题目 Recall 不退化
- AC-EVAL8-04: 拒答准确率 ≥ 90%

请开始执行。
