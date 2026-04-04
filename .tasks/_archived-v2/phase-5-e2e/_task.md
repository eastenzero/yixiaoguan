---
id: "phase-5-e2e"
parent: ""
type: "integration-test"
status: "pending"
tier: "T1"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "temp/"
  - "docs/test-reports/"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/"
  - "apps/student-app/src/pages/chat/"
out_of_scope:
  - "knowledge-base/"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/config.py"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"
  - "teb-starter-kit/guides/verification-guide.md"

done_criteria:
  L0: "p5a/p5b 子目录均存在 _report.md；截图存档于 docs/test-reports/"
  L1: "p5b 修改的 Java 文件编译通过（mvn compile 无错误）"
  L2: "≥10 个测试用例通过（应命中 / 拒答 / 意图兜底 / 来源引用 / 多轮追问）"
  L3: "全链路体感流畅：问答有来源引用可点击，意图识别后展示官网链接，追问能保持上下文"

depends_on: ["phase-3-tuning", "phase-4a-kb-expansion", "phase-1-data-foundation"]
created_at: "2026-04-04 01:43:00"

batches:
  - name: "batch-9"
    tasks: ["p5a-full-chain-test", "p5b-multiround-history"]
    parallel: true
    note: "p5a 测试当前功能；p5b 修复 history 缺失，两者可并行开发，p5a 最终验收需 p5b 完成"
---

# Phase 5：端到端验证

> ≥10 个测试用例全部通过，多轮对话历史传递正常，全链路功能可用。

## 背景

所有数据和调参工作完成后，做最终的端到端验证，覆盖：
1. **知识库问答**：应命中场景 → 结构化回答 + 来源引用可点击
2. **拒答场景**：超出知识库范围 → 友好提示，不幻觉
3. **办事意图**：识别 → 官网兜底链接（p1d 成果验收）
4. **多轮追问**：第二轮问题能引用第一轮上下文（p5b 成果验收）

p5b 修复 DEBT-04（history 始终为空）：`AiCoordinatorServiceImpl` 构造 `ChatStreamRequest` 时从数据库取最近 N 条消息传入 history，前端 `chat/index.vue` 同步传递。

## 已知陷阱

- 测试截图存入 `docs/test-reports/`（不要放 `temp/`，需要长期存档）
- p5b 修改 Java 代码后必须编译验证，不能只改不验
- 多轮 history 长度上限需评估（避免超过模型 context 窗口），建议取最近 6 条
