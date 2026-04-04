---
id: "s5-home-polish"
parent: "v3-student-ui"
type: "feature"
status: "pending"
tier: "T2"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/home/index.vue"
  - "apps/student-app/src/components/BentoCard.vue"
  - "apps/student-app/src/components/LinkCard.vue"

out_of_scope:
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/services/index.vue"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages/home/index.vue"
  - "_references/前端参考/stitch_ (1)/学生移动端/_8/screen.png"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"

done_criteria:
  L0: "home/index.vue 中不含字符串 'AI学术助教'（grep 验证零结果）"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无"
  L3: |
    H5 preview 中：
    1. 首页顶部显示"医小管AI助手"或"医小管"品牌名
    2. 点击 AI 输入框/入口跳转到智能问答页面（pages/chat/index）
    3. 事务导办入口跳转到 pages/services/index（非 apply/status）
    4. 已有 Bento Grid、通知横幅正常显示
    5. 无编译告警

depends_on: ["s1-theme-unification", "s2-tabbar-routing"]
created_at: "2026-04-04"
---

# s5: 首页样式升级（Home Polish）

> `home/index.vue` 品牌名统一为"医小管"，事务导办路由从 apply/status 更新为 services/index，整体色调和细节样式按参考设计 Screen _8 方向微调。保持现有结构（欢迎区+AI输入+快捷标签+Bento Grid+链接+通知）不变。

## 背景

首页当前使用"AI学术助教"等旧品牌名，并且 `goToServices()` 方法可能仍指向 apply/status。需要在 s2 完成路由重构后，对应更新首页的品牌文字和跳转逻辑。

## 执行步骤

### 步骤 1：品牌名替换

全局替换首页中的旧品牌文字：
- `"AI学术助教"` → `"医小管AI助手"`
- 其他含"学术助手"/"学术亭"的文字 → 替换为"医小管"相关表述

### 步骤 2：路由更新

在 `<script>` 中找到所有跳转逻辑，确认：
- 跳转到"事务导办"的方法（`goToServices()` 或类似）：改为 `uni.switchTab({ url: '/pages/services/index' })`
- 跳转到"智能问答"的方法：确认已指向 `/pages/chat/index`
- 任何残留的 `switchTab apply/status` → 改为 `navigateTo apply/status`

### 步骤 3：样式微调（参考 Screen _8）

按参考设计方向做以下调整（不做大幅重写）：

- **Bento 卡片**：确认使用 `$radius-xl`（0.75rem+）圆角，若有硬编码 pixel 值改为 token
- **通知横幅**：内容更新为更通用的提示，或改为动态获取（若当前是 hardcoded 字符串）
- **色调**：确认首页主色调 teal，不内联 `#006a64`，改用 `$primary`
- **分割线**：检查是否有 `1px solid` 分割线，若有改为背景色层级区分（No-Line Rule）

### 步骤 4：BentoCard.vue / LinkCard.vue（按需）

仅在以下情况才修改：
- 内联了 `#00639B`（旧蓝色）→ 替换为 `$primary` 或移除内联
- 内联了非 token 的 border-radius → 改为 `$radius-*` token

**若无需修改则不动这两个文件。**

## 已知陷阱

- 不修改 chat/index.vue 和 services/index.vue（有专属任务处理）
- 不修改 theme.scss（s1 已完成）
- 样式调整以"微调"为准，不做大幅重写，控制改动范围
