# 任务: F-V7-04 学生提问列表 + 提问详情页面

## 目标状态
`apps/teacher-app/src/pages/questions/index.vue` 和 `apps/teacher-app/src/pages/questions/detail.vue` 存在，视觉还原 React 原型。

## 参考文件（必须先读取）
- React 提问列表: `D:\Backup_2025\下载\zip7-extracted\src\pages\Questions.tsx`
- React 提问详情: `D:\Backup_2025\下载\zip7-extracted\src\pages\QuestionDetail.tsx`
- 色彩变量: `apps/teacher-app/src/styles/theme.scss`
- 公共组件: `apps/teacher-app/src/components/TopAppBar.vue`
- 公共组件: `apps/teacher-app/src/components/BottomNavBar.vue`
- 图标: `apps/teacher-app/src/components/icons/index.ts`

## 转换规则
- React JSX → Vue 3 `<template>` + UniApp 标签 (`<view>`, `<text>`, `<image>`, `<input>`)
- **禁止使用** `<div>`, `<span>`, `<img>`, `<p>`, `<h1>`~`<h6>` 等 HTML 标签
- Tailwind → SCSS（使用 theme.scss 变量）
- Lucide 图标 → icons/ Vue 组件
- 外部图片 URL → 灰色占位圆
- 动画用 global.scss 中的 `.animate-fade-up` + `.delay-N`

## 页面 1: questions/index.vue（提问列表）

### 结构
1. TopAppBar (title="学生提问", showBack=true, action="search")
2. 筛选标签横向滚动区（4个药丸标签：全部/待处理/处理中/已解决）
   - 选中态: `background: $primary; color: $on-primary; box-shadow`
   - 未选中: `background: $surface-container; color: $on-surface-variant`
3. 提问卡片列表（3张 mock 卡片）
4. BottomNavBar (current=1)

### 提问卡片结构（每张）
- 头像占位圆(48x48) + 学生姓名 + 专业·时间
- 右上状态标签（药丸形）:
  - 待处理: `background: rgba($error-container, 0.1); color: $error-dim`
  - 处理中: `background: rgba($primary-container, 0.2); color: $primary`
- 提问内容（2行截断）
- AI匹配度进度条（BrainCircuit图标 + 百分比 + 进度条）
  - 进度条颜色: >=80% 绿色, 60-79% 琥珀色, <60% 红色($error)

### 样式要点
- 卡片: `background: $surface-container-lowest; border-radius: 24px; padding: 20px`
- 卡片间距: `margin-bottom: 24px`
- 顶部留白: `padding-top: 80px`（给 TopAppBar 让位）
- 底部留白: `padding-bottom: 112px`（给 BottomNavBar 让位）

## 页面 2: questions/detail.vue（提问详情）

### 结构
1. TopAppBar (title="提问详情", showBack=true)
2. 学生信息卡（头像+姓名+状态标签+院系·年级）
3. 对话记录区:
   - 学生消息（右侧，紫色背景圆角气泡，`background: $primary; color: $on-primary`）
   - AI回复（左侧，Bot图标+白色气泡+红色左边框表示拒答）
   - 系统消息（居中，灰色药丸，"学生已呼叫老师"）
4. 底部固定操作栏（"接单处理"渐变按钮 + UserCheck图标）

### 样式要点
- 学生信息卡: `background: $surface-container-lowest; border-radius: 24px; padding: 20px`
- 学生气泡: `background: $primary; color: $on-primary; border-radius: 16px 16px 0 16px; padding: 16px`
- AI气泡: `background: white; border: 1px solid rgba($error, 0.2); border-radius: 16px 16px 16px 0; padding: 16px; position: relative`，左侧红线 `width: 4px; background: $error`
- 系统消息: `background: $surface-container; border-radius: 9999px; padding: 6px 16px`
- 底部操作栏: `background: rgba(255,255,255,0.9); backdrop-filter: blur(20px); padding: 24px`
- 接单按钮: `height: 56px; border-radius: 9999px; background: linear-gradient(135deg, $primary, $primary-container)`

### Mock 数据
所有数据 const 定义在 `<script setup>` 中。

## 允许修改的文件
- `apps/teacher-app/src/pages/questions/index.vue`（新建）
- `apps/teacher-app/src/pages/questions/detail.vue`（新建）

## 禁止修改的文件
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/dashboard/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/src/pages.json`
- `apps/student-app/**`
- `services/**`

## 完成标准
- L0: questions/index.vue 和 questions/detail.vue 存在
- L1: 列表页含筛选标签+卡片; 详情页含学生信息+对话+底部按钮
- L2: 无 Tailwind 类名，无 HTML 标签（div/span/img/p）

## 报告
写入: `.tasks/v7-teacher-app/f-v7-04-questions/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
