---
id: "fix-c-knowledge-markdown-fallback"
parent: "v4-chat-bugfix"
type: "bugfix"
status: "pending"
tier: "T2"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "apps/student-app/src/pages/knowledge/detail.vue"

out_of_scope:
  - "apps/student-app/src/api/knowledge.ts"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - "apps/student-app/src/pages/knowledge/detail.vue"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "knowledge/detail.vue 的 fallback 分支使用 v-html 渲染 Markdown；.markdown-body 子选择器已穿透（:deep() 或独立 unscoped style），与 FIX-A 方案一致"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "报告含代码证据：API 失败路径仍可渲染 fallbackSummary 的标题/列表/段落"
  L3: "[H5] 点击来源引用进入参考资料页，Markdown 展示正常，不再裸露原始标记"

depends_on: ["fix-b-chat-navbar-custom"]
created_at: "2026-04-06 00:55:00"
---

# FIX-C：知识详情 fallback Markdown 渲染修复（BUG-3 + BUG-4）

> 完成后，知识详情接口失败时仍能展示可读的 Markdown 摘要，不再出现纯文本裸露与内容不可读问题。

## 背景

BUG-3 与 BUG-4 同源：接口失败后 fallback 分支走纯 `<text>` 输出，且 `.markdown-body` 在 scoped 下对子节点样式失效。

## 执行步骤

1. 修改 `knowledge/detail.vue` fallback 分支，改为 `md.render(...)` + `v-html` 渲染
2. 将 `.markdown-body` 子选择器改为与 FIX-A 一致的穿透方案
3. 保持现有加载失败提示逻辑，仅做可读性修复
4. 构建验证后进行来源引用跳转链路人工验收

## 已知陷阱

- 不修改后端 API，不新增后端依赖
- 穿透方案必须与 FIX-A 统一，避免两个页面表现不一致
- 如提示文案需弱化，仅在 fallback 内容可读前提下做最小改动
