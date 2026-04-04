---
id: "p5a-full-chain-test"
parent: "phase-5-e2e"
type: "integration-test"
status: "done"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "temp/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "services/"
  - "apps/"
  - "knowledge-base/"
  - "scripts/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "teb-starter-kit/guides/verification-guide.md"
  - ".tasks/_spec.yaml"
  - "docs/test-reports/eval-set-v1.yaml"

done_criteria:
  L0: "docs/test-reports/completion-reports/P5A-full-chain-test-report.md 存在；截图存入 docs/test-reports/"
  L1: "测试覆盖全部 4 类场景（知识库问答 / 拒答 / 办事意图兜底 / 来源引用可点击）"
  L2: "≥10 个测试用例通过，结果有截图存档"
  L3: "体感验收：回答有来源引用且可点击跳转；意图识别后展示官网链接；拒答措辞友好不生硬"

depends_on: ["phase-3-tuning", "phase-1-data-foundation"]
created_at: "2026-04-04 01:43:00"
---

# p5a：全链路功能验证

> ≥10 个端到端测试用例通过，四类场景均有截图存档。

## 背景

所有数据、调参、代码改动完成后，做最终的端到端功能验证。
覆盖学生端 AI 对话的核心场景，验证从前端到 RAG 管道到知识库的完整链路。

## 测试用例矩阵

| 场景类型 | 示例问题 | 预期行为 |
|---------|---------|---------|
| 知识库命中 | "奖学金怎么申请？" | 结构化回答 + 来源引用可点击 |
| 知识库命中 | "心理测评在哪做？" | 正确回答 + 来源引用 |
| 拒答 | "明天天气怎么样？" | 友好说明超出范围 |
| 拒答 | "宿舍报修怎么弄？" | 说明暂无相关信息（生活服务缺口） |
| 办事意图 | "我想预约教室" | 官网兜底链接回复 |
| 办事意图 | "帮我提交报修" | 官网兜底链接回复 |
| 来源引用 | 点击回复中的来源标签 | 跳转知识详情页或弹层摘要 |
| 边界情况 | "奖学金多少钱？"（库中有相关但无金额） | 部分回答 + 说明信息不完整 |

## 已知陷阱

- 截图存入 `docs/test-reports/`（长期存档），不要放 `temp/`
- 所有服务需同时运行：docker compose 容器（ai-service）+ business-api + student-app dev server
- 来源引用测试需要确认 ChromaDB metadata 中有 source_url 或 entry_id，前端才能生成跳转链接
