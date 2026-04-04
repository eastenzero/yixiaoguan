---
id: "p3a-eval-set"
parent: "phase-3-tuning"
type: "feature"
status: "done"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "docs/test-reports/"
  - "temp/"
out_of_scope:
  - "services/ai-service/app/core/config.py"
  - "scripts/batch_ingest_kb.py"
  - "knowledge-base/"
  - "apps/"
  - "services/business-api/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - ".tasks/_spec.yaml"
  - "services/ai-service/app/core/llm_chat.py"
  - "services/ai-service/app/core/config.py"

done_criteria:
  L0: "docs/test-reports/eval-set-v1.yaml（或 .json）文件存在"
  L1: "评测集文件 YAML/JSON 格式合法，可被 Python yaml.safe_load / json.load 解析"
  L2: "≥30 对问答，分布满足：应命中 ≥12 / 应拒答 ≥8 / 边界情况 ≥5 / 生活服务（应拒答）≥5；每对包含 question、expected_entry_ids、expected_behavior 字段"
  L3: "抽查 5 对：问题措辞贴近真实学生提问（非教科书式），expected_entry_ids 与知识库内容对应正确"

depends_on: ["phase-2-vectorize"]
created_at: "2026-04-04 01:43:00"
---

# p3a：构建检索质量评测集

> 包含 ≥30 对 `(question, expected_entry_ids, expected_behavior)` 的黄金评测集已就绪，可被自动化脚本读取执行。

## 背景

评测集是调参的基础。没有评测集，阈值调整只能靠感觉，结果不可信。

四类问题分布：
1. **应命中**（≥12 对）：知识库有答案，RAG 应检索到对应条目
2. **应拒答**（≥8 对）：完全无关问题（天气、外校事务），应拒绝作答
3. **边界情况**（≥5 对）：主题相关但知识库信息不足，应友好说明无法完整回答
4. **生活服务类（应拒答）**（≥5 对）：当前库无覆盖（报修/水电等），应拒答不幻觉

## 执行步骤

1. 阅读 `first-batch-drafts/` 中各分类条目，为"应命中"类生成问题
2. 构造"应拒答"和"边界情况"问题
3. 输出 `docs/test-reports/eval-set-v1.yaml`，格式：
   ```yaml
   - id: "eval-001"
     question: "奖学金怎么申请？"
     expected_behavior: "hit"
     expected_entry_ids: ["KB-20260324-0001", "KB-20260324-0002"]
   - id: "eval-002"
     question: "明天天气怎么样？"
     expected_behavior: "reject"
     expected_entry_ids: []
   ```
4. 同时写自动化评测脚本 `temp/run_eval.py`，调用 ai-service 的 `/chat` 或 `/search` 接口，计算 Recall@5 和拒答准确率

## 已知陷阱

- 问题措辞要贴近真实学生提问，避免直接复制知识条目标题作为问题
- 生活服务类问题（LIFE-01~07）均应标记 `expected_behavior: reject`，当前库无覆盖
- expected_entry_ids 的精确填写依赖你对知识库内容的实际阅读，不能凭印象填
