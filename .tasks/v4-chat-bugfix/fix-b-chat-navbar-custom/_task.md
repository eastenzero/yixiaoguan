---
id: "fix-b-chat-navbar-custom"
parent: "v4-chat-bugfix"
type: "bugfix"
status: "pending"
tier: "T2"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/pages/chat/index.vue"

out_of_scope:
  - "apps/student-app/src/pages/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "pages.json 中 chat 页面已配置 navigationStyle=custom，且 chat 页面仅保留一套导航栏"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "报告含自动化证据：grep/navigationStyle 命中 chat 页面配置"
  L3: "[H5] 智能问答空状态首屏仅单层 header，输入框首屏可见"

depends_on: ["fix-a-chat-markdown-penetration", "fix-d-login-userinfo-mapping"]
created_at: "2026-04-06 00:55:00"
---

# FIX-B：Chat 双层导航栏修复（BUG-1）

> 完成后，智能问答页不再出现原生导航栏与自定义 navbar 叠加，首屏布局恢复正常。

## 背景

BUG-1 根因为 `pages.json` 原生导航栏与 `chat/index.vue` 自定义 `.navbar` 并存。该问题会直接影响空状态输入区域可见性。

## 执行步骤

1. 在 `pages.json` 的 chat 页面配置 `navigationStyle: "custom"`
2. 检查 `chat/index.vue` navbar 结构与样式，确保仅一层导航可见
3. 构建验证并记录配置命中证据
4. H5 实机确认输入框首屏可见

## 已知陷阱

- 本任务与 FIX-A 同文件，但本批次是串行执行，禁止并行改动
- 不得修改 chat 页核心逻辑（消息发送、来源引用、SSE）
- 标题文案是否从“医小管”改“智能问答”按现有页面一致性处理，不做额外需求扩展
