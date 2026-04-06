---
id: "f-v5a-06"
parent: "v5a-quick-fixes"
type: "bugfix"
status: "done"
tier: "T3"
priority: "medium"
risk: "medium"
foundation: false

depends_on: ["f-v5a-02", "f-v5a-03"]

scope:
  - "apps/student-app/src/pages/knowledge/detail.vue"
  - "apps/student-app/src/api/knowledge.ts"
out_of_scope:
  - "apps/student-app/src/pages/chat/index.vue"
  - "services/**"
  - "scripts/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/knowledge/detail.vue"
  - "apps/student-app/src/api/knowledge.ts"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "apps/student-app/src/pages/knowledge/detail.vue 存在"
  L1: "grep -c '知识详情暂不可用' apps/student-app/src/pages/knowledge/detail.vue 返回 0（或降级提示不再作为默认状态出现）"
  L2: "点击参考资料条目后，detail 页显示摘要内容而非"暂不可用"提示"
  L3: "知识详情页内容可读、排版正常；若采用方案C需在本报告记录 DEBT-V5A-01"

time_budget: "2h（超出则标记 DEBT-V5A-01 保持现状降级展示）"

root_cause: |
  detail.vue 调用 GET /api/v1/knowledge/entries/{id}，
  AI 回复中的 entry_id 格式为 "KB-20260323-0001-chunk-5"（ChromaDB metadata），
  后端 API 可能不存在或 ID 映射失败，导致 404，触发降级逻辑。

strategies:
  A: "修改 normalizeEntryId 适配 ChromaDB entry_id 格式（若后端 API 已实现）"
  B: "detail.vue 完全依赖 URL 参数中的 summary 展示内容，不调后端 API（推荐）"
  C: "成本 >2h 则保持现状，记录 DEBT-V5A-01"

created_at: "2026-04-06"
---

# F-V5A-06: 知识详情页不可用修复

> 点击 AI 回复中的参考资料条目后，knowledge/detail 页能展示有意义的内容（摘要），不再默认显示"暂不可用"。

## 背景

当前点击参考资料条目跳转 `knowledge/detail` 后显示降级提示。根因为后端 `GET /api/v1/knowledge/entries/{id}` 接口可能不存在，或 ChromaDB 的 entry_id 格式（如 `KB-20260323-0001-chunk-5`）与接口期望的 ID 格式不匹配。

## 执行步骤

1. **诊断**：先检查 `detail.vue` 调用逻辑和 `knowledge.ts` API 定义，确认接口是否真实存在
2. **如果后端无此接口（大概率）** → 采用**方案 B**：
   - `detail.vue` 不调 `/api/v1/knowledge/entries/{id}`
   - 改为直接读取路由参数中的 `summary`（AI 回复时已随 entry_id 一起传入 URL）
   - 用 `v-html` + markdown 渲染展示内容
3. **如果 2h 内无法完成** → 记录为 DEBT-V5A-01，维持现状（降级摘要展示已可用）

## 已知陷阱

- 方案 B 中 URL 参数的 `summary` 可能被 URL encode，需 `decodeURIComponent` 处理
- v-html 渲染 markdown 需引入 marked 或使用现有 markdown-it（检查项目已有依赖）
- 不要修改 `chat/index.vue` 中的 `normalizeEntryId`（该文件已在 batch-2 处理过）
