---
id: "v4-chat-bugfix"
parent: ""
type: "bugfix"
status: "pending"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

scope:
  - "apps/student-app/src/**"
  - ".tasks/v4-chat-bugfix/**"

out_of_scope:
  - "services/**"
  - "apps/teacher-web/**"
  - "knowledge-base/**"
  - "scripts/**"
  - "docs/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/knowledge/detail.vue"
  - "apps/student-app/src/pages/login/index.vue"
  - "apps/student-app/src/api/auth.ts"
  - "apps/student-app/src/pages.json"

done_criteria:
  L0: "fix-a/fix-b/fix-c/fix-d/int-v4-chat-bugfix 五个子任务目录均产出 _report.md"
  L1: "apps/student-app 执行 npm run build:h5 编译零错误"
  L2: "集成验收报告包含自动化检查证据（navigationStyle custom、样式穿透、userinfo 映射）"
  L3: "H5 手工验收 AC-1~AC-7 全部通过，5 个 bug 均闭环"

depends_on: []
created_at: "2026-04-06 00:55:00"

batches:
  - name: "batch-1"
    tasks: ["fix-a-chat-markdown-penetration", "fix-d-login-userinfo-mapping"]
    parallel: true
  - name: "batch-2"
    tasks: ["fix-b-chat-navbar-custom"]
    depends_on: "batch-1"
  - name: "batch-3"
    tasks: ["fix-c-knowledge-markdown-fallback"]
    depends_on: "batch-2"
  - name: "batch-int"
    tasks: ["int-v4-chat-bugfix"]
    depends_on: "batch-3"
---

# spec-v4 聊天链路问题修复（总任务）

> 完成后，学生端智能问答页面恢复正确的布局与多行渲染，知识详情页在后端缺失接口时仍能可读展示 Markdown，登录后的“我的申请”不再被误判未登录，且相关路径无回归。

## 背景

T0 规格已定位 5 个前端侧 bug，集中在样式穿透、页面导航栏叠加、fallback 渲染策略和用户信息字段映射四类问题。

- BUG-1：chat 双层 header 挤压首屏
- BUG-2：AI 气泡仅一行（v-html + scoped 样式失效）
- BUG-3/BUG-4：知识详情 fallback 未 markdown 渲染
- BUG-5：/getInfo 字段映射不兼容导致申请页 401 回跳登录

## 批次门禁

| Batch | 任务 | 并行 | 门禁条件 |
|---|---|---|---|
| batch-1 | fix-a-chat-markdown-penetration + fix-d-login-userinfo-mapping | 是 | 无 |
| batch-2 | fix-b-chat-navbar-custom | 否 | batch-1 全部 PASS |
| batch-3 | fix-c-knowledge-markdown-fallback | 否 | batch-2 PASS |
| batch-int | int-v4-chat-bugfix | 否 | batch-3 PASS |

## 已知陷阱

- `v-html` 注入节点不带 scoped 标识，`.markdown-body` 子选择器必须穿透
- FIX-A 与 FIX-B 均涉及 `chat/index.vue`，禁止并行开发
- BUG-5 修复后若仍 401，需按规格上报后端接口/权限问题，不得在本批次扩 scope
