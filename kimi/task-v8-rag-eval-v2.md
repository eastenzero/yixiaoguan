# T3 任务: v8 RAG-EVAL — 回归测试

## ⚠️ 严格约束
- **不要在本地执行任何 curl 命令**
- **不要检测本地服务**
- 远程命令全部用 `ssh easten@192.168.100.165 "..."` 执行

## Step 1: 追加测试题到本地 eval-set 文件

直接追加到本地文件 `scripts/eval/eval-set-v3.yaml` 末尾（**用 WriteFile/AppendFile 工具，不要用 curl**）：

```yaml

# ==================== v8 公众号来源内容 (7题) ====================

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
  question: "学校有没有去加拿大或英国的暑期项目？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0113", "KB-20260410-0114"]
  category: "grounding-verify-in"

- id: "v8-006"
  question: "山东省大学生就业服务平台网址是什么？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0115"]
  category: "grounding-verify-in"

- id: "v8-007"
  question: "个人所得税怎么做年度汇算清缴？"
  expected_behavior: "hit"
  expected_entry_ids: ["KB-20260410-0118", "KB-20260410-0119"]
  category: "grounding-verify-in"
```

## Step 2: 通过 SSH 运行评测脚本（等待 Mutagen 同步，约 30 秒）

```
ssh easten@192.168.100.165 "sleep 30 && cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v3.py"
```

## Step 3: 通过 SSH 读取报告

```
ssh easten@192.168.100.165 "cat /home/easten/dev/yixiaoguan/scripts/eval/eval-report-v3.md"
```

## Step 4: 将报告写入本地

将 Step 3 输出写入 `kimi/rag-eval-v8-report.md`。

输出 Recall@5 和拒答准确率的最终结果（PASS/FAIL）。

请开始执行。
