---
id: "fix-a-chat-markdown-penetration"
parent: "v4-chat-bugfix"
type: "bugfix"
status: "pending"
tier: "T2"
priority: "high"
risk: "high"
foundation: true

scope:
  - "apps/student-app/src/pages/chat/index.vue"

out_of_scope:
  - "apps/student-app/src/pages/chat/index.vue <script> 逻辑层（SSE/API/来源引用/快捷问题）"
  - "apps/student-app/src/pages.json"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - "apps/student-app/src/pages/chat/index.vue"
  - ".tasks/v3-student-ui/s3-hotfix-bubble-height/_report.md"

done_criteria:
  L0: "chat/index.vue 中 .markdown-body 子选择器已穿透（:deep() 或独立 unscoped style），并覆盖 p/h1-h4/ul/ol/li/code/pre/a/blockquote/hr/strong/b"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "报告给出代码级证据：v-html 分支保留，且穿透方案与 RISK-1 兜底口径一致"
  L3: "[H5] 发送多行问题后 AI 气泡高度自适应，段落/列表/加粗/链接完整显示"

depends_on: []
created_at: "2026-04-06 00:55:00"
---

# FIX-A：Chat Markdown 样式穿透修复（BUG-2）

> 完成后，AI 回复气泡不再只显示一行，`v-html` 渲染的 Markdown 在聊天页可正确套用样式。

## 背景

BUG-2 根因已定位为 `scoped` 样式对 `v-html` 注入子节点失效，历史 hotfix 修改了 flex 但未命中根因。本任务只处理样式穿透，不改聊天逻辑。

## 执行步骤

1. 在 `chat/index.vue` 保留现有 `v-html="renderMarkdown(msg.content)"` 渲染路径
2. 将 `.markdown-body` 子选择器改为穿透方案（`:deep()` 或 unscoped）
3. 覆盖段落/标题/列表/代码块/链接/引用等常见 Markdown 元素
4. 本地构建验证后给出关键片段证据

## 已知陷阱

- 禁止修改 `<script setup>` 中 SSE、来源引用、快捷问题发送逻辑
- 不得引入全局样式污染；若使用 unscoped，范围需仅限 `.markdown-body`
- 与 FIX-B 同文件，必须遵循批次门禁串行执行
