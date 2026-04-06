---
id: "fix-04"
parent: "v5c-ui-debt-fixes"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "low"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/knowledge/detail.vue"
out_of_scope:
  - "apps/student-app/src/pages/chat/**"
  - "apps/student-app/src/api/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/knowledge/detail.vue"

done_criteria:
  L0: "apps/student-app/src/pages/knowledge/detail.vue 存在"
  L1: "grep -c '暂不可用' apps/student-app/src/pages/knowledge/detail.vue 返回 0"
  L2: "grep '以下为该参考资料的相关摘要\\|fallback\\|summary' apps/student-app/src/pages/knowledge/detail.vue 有结果"
  L3: "知识详情页不再出现黄色「暂不可用」横幅，摘要内容正常展示"

created_at: "2026-04-06"
---

# FIX-04: 知识详情页去除"暂不可用"提示

> 知识详情页不再显示"知识详情暂不可用"字样，改为中性描述，摘要内容正常展示。

## 背景

v5a FIX-06 已将 knowledge/detail.vue 改为方案 B（直接用 URL summary 参数展示内容），但页面仍保留了旧的黄色横幅提示，给用户"功能故障"的错觉。

## 变更详情

- **文件**: `apps/student-app/src/pages/knowledge/detail.vue`
- **操作**: 找到含"知识详情暂不可用"的 `fallback-notice` 元素
- **采用方案 B**（中性替换）：
  - 将文案改为"以下为该参考资料的相关摘要"
  - 移除黄色警告样式（保留容器但改为普通提示样式，或直接移除横幅）

## 已知陷阱

- 不要修改摘要内容的渲染逻辑，只改横幅文案/样式
- 如果横幅与摘要内容是条件互斥的（v-if/v-else），确保摘要内容路径不受影响
