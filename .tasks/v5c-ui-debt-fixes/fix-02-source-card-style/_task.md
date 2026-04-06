---
id: "fix-02"
parent: "v5c-ui-debt-fixes"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "low"
risk: "low"
foundation: false

depends_on: ["fix-01", "fix-04"]

scope:
  - "apps/student-app/src/pages/chat/index.vue"
out_of_scope:
  - "apps/student-app/src/styles/**"
  - "apps/student-app/src/api/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "apps/student-app/src/pages/chat/index.vue 存在"
  L1: "所有参考资料条目位置（内嵌列表 + 弹层）的背景色均为 rgba(0,106,100,0.06)"
  L2: "grep -c 'surface-container' apps/student-app/src/pages/chat/index.vue 在参考资料相关 selector 内返回 0"
  L3: "聊天页参考资料条目（内嵌和弹层）样式视觉一致，均为浅绿背景+边框"

created_at: "2026-04-06"
---

# FIX-02: 参考资料卡片样式统一

> 聊天页所有参考资料条目（消息内嵌 + 弹层）样式统一使用浅主题色背景，无视觉不一致。

## 背景

v5a FIX-03 已将 `.source-item` 改为方案 B（rgba 背景），但弹层中的参考资料列表可能未同步更新，导致内嵌与弹层样式不一致。

## 变更详情

检查 `chat/index.vue` 中所有参考资料相关 selector（`.source-item`、弹层内条目等），统一为：
```scss
background: rgba(0, 106, 100, 0.06);
border: 1px solid rgba(0, 106, 100, 0.15);
```

## 已知陷阱

- **fix-03 必须在本任务之后执行**（同文件 chat/index.vue）
- 只改样式，不改点击逻辑和数据渲染
