---
task_id: s3-hotfix-bubble-height
parent: s3-chat-redesign
priority: high
status: open
scope_files:
  - apps/student-app/src/pages/chat/index.vue   # 仅 <style> 块，禁改 <script>
forbidden_files: []
---

# s3-hotfix-bubble-height · AI 气泡高度截断修复

## 背景

AI 对话页（`chat/index.vue`）存在多行回复被截断的问题：内容超过一行时，气泡仅显示末行，其余内容不可见。

T1 已尝试两次修复（`align-items: flex-start` / `flex-shrink: 0`），均未生效。T0 指派 T3 通过浏览器 DevTools 实测定位根因，再作最小化修复。

---

## 当前相关 CSS（已确认在源码中）

```scss
.message-item {
  display: flex;
  align-items: flex-start;
  flex-shrink: 0;           // T1 修复1
  margin-bottom: 20px;
}

.message-content {
  display: flex;
  flex-direction: column;
  max-width: 75%;
}

.message-bubble {
  padding: 12px 16px;
  word-break: break-word;
  flex-shrink: 0;           // T1 修复2
}

.message-text {
  font: $text-body-medium;
  line-height: 1.6;
  min-height: 0;
}
```

消息列表使用 `<scroll-view scroll-y>` 组件，编译为 H5 后内部会产生额外 div 容器。

---

## T3 任务要求

### 步骤一：实测 DevTools

1. 启动 student-app dev server（`npm run dev:h5`，`apps/student-app/`）
2. 打开浏览器，登录，进入"智能问答"页，发送一条会产生多行回复的问题
3. 右键 AI 气泡 → Inspect
4. **逐层检查以下元素的 computed height**，记录实测值：
   - `.message-item`
   - `.message-content`
   - `.message-bubble`
   - `.message-text.markdown-body`
   - `scroll-view` 编译后的内部 div（`uni-scroll-view-content` 或类似）

### 步骤二：定位根因

根据实测，确认以下哪层导致截断（记录在报告中）：

- [ ] `uni-scroll-view-content` 有 `display: flex` + 固定 `height` → 压缩子项
- [ ] `message-content` 被赋予 `overflow: hidden` + 约束高度
- [ ] `message-bubble` 或 `message-text` 的 `height` 被继承/覆盖为固定值
- [ ] 其他（描述）

### 步骤三：最小化修复

- **仅修改** `apps/student-app/src/pages/chat/index.vue` 的 `<style>` 块
- 禁止修改 `<template>` 和 `<script>`
- 修复后截图对比（修复前 vs 修复后）

---

## done_criteria

- [ ] 报告中含各层 computed height 实测值
- [ ] 明确写出根因所在层及具体 CSS 属性
- [ ] 修复后多行 AI 回复完整展示（无截断）
- [ ] `npm run build:h5` 无新增 Error
- [ ] 产出 `_report.md`（含截图路径或 base64）

---

## 禁止事项

- 禁止修改 `<script>` 块（消息逻辑、SSE、导航等）
- 禁止修改 `<template>` 结构
- 禁止修改 `theme.scss` 或其他共享样式文件
- 禁止新增第三方依赖
