# 任务: F-V7-05 知识库列表 + 知识详情页面

## 目标状态
`apps/teacher-app/src/pages/knowledge/index.vue` 和 `apps/teacher-app/src/pages/knowledge/detail.vue` 存在，视觉还原 React 原型。

## 参考文件（必须先读取）
- React 知识列表: `D:\Backup_2025\下载\zip7-extracted\src\pages\Knowledge.tsx`
- React 知识详情: `D:\Backup_2025\下载\zip7-extracted\src\pages\KnowledgeDetail.tsx`
- 色彩变量: `apps/teacher-app/src/styles/theme.scss`
- 公共组件: `apps/teacher-app/src/components/TopAppBar.vue`
- 公共组件: `apps/teacher-app/src/components/BottomNavBar.vue`
- 图标: `apps/teacher-app/src/components/icons/index.ts`

## 转换规则
- React JSX → Vue 3 `<template>` + UniApp 标签 (`<view>`, `<text>`, `<image>`, `<input>`)
- **禁止使用** `<div>`, `<span>`, `<img>`, `<p>`, `<h1>`~`<h6>` 等 HTML 标签
- Tailwind → SCSS（theme.scss 变量）
- Lucide 图标 → icons/ Vue 组件
- 外部图片 URL → 灰色占位区域
- 动画用 global.scss 的 `.animate-fade-up` + `.delay-N`

## 页面 1: knowledge/index.vue（知识库列表）

### 结构
1. TopAppBar (title="知识库", showBack=true, action="add")
2. 搜索栏（ghost风格，左侧搜索图标，$surface-container背景，圆角16px）
3. 分类标签横向滚动区（全部/教务管理/学生服务/生活指南）
   - 选中: `background: $primary; color: $on-primary; border-radius: 9999px; box-shadow`
   - 未选中: `background: $surface-container-low; color: $on-surface-variant; border-radius: 9999px`
4. 知识卡片列表（3张 mock 卡片）
5. BottomNavBar (current=2)

### 知识卡片结构（每张）
- 顶部: 分类药丸标签 + 状态（已发布/草稿）
  - 教务管理: `background: $secondary-container; color: $on-secondary-container`
  - 生活指南: `background: $tertiary-container; color: $on-tertiary-container`
  - 学生服务: `background: $secondary-container; color: $on-secondary-container`
  - 已发布: 绿点 + `color: $primary`
  - 草稿: 灰点 + `color: $on-surface-variant`
- 标题（粗体，18px）
- 摘要（2行截断，$on-surface-variant）
- 底部: 作者头像占位圆+作者名 + 时间

### 样式
- 卡片: `background: $surface-container-lowest; border-radius: 24px; padding: 24px`
- 卡片间距: `margin-bottom: 24px`
- 搜索框: `height: 56px; padding-left: 48px; background: $surface-container; border-radius: 16px; border: none`
- 底部分割线: `border-top: 1px solid rgba($outline-variant, 0.1); padding-top: 16px; margin-top: 16px`

## 页面 2: knowledge/detail.vue（知识详情）

### 结构
1. TopAppBar (title="知识详情", showBack=true, action="edit")
2. Hero区域:
   - 分类标签 + 状态标签
   - 大标题（30px, font-weight:800）
   - 作者信息（头像圆+姓名+更新时间）
3. 文章正文区:
   - 封面图占位（灰色矩形，圆角16px，宽高比16:9）
   - 小标题（20px, font-weight:700）
   - 段落文字
   - 有序步骤列表（每步: 编号圆+标题+描述，$surface-container-low背景，圆角16px）
   - 引用块（左边4px $primary边框 + `background: rgba($primary, 0.05); border-radius: 0 16px 16px 0`）
4. 底部固定操作栏:
   - "下线"按钮（描边，`border: 1px solid $outline-variant; border-radius: 9999px`）
   - "编辑"按钮（渐变填充，flex:2，Edit图标）

### 样式
- 正文段落: `color: $on-surface-variant; line-height: 1.7; font-size: 14px`
- 步骤编号圆: `width: 24px; height: 24px; background: $primary; color: $on-primary; border-radius: 50%; font-size: 12px; font-weight: 700`
- 底部栏: `background: rgba(255,255,255,0.9); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); padding: 16px 20px; box-shadow: 0 -8px 30px rgba(0,0,0,0.04)`

### Mock 数据
const 定义在 `<script setup>` 中。

## 允许修改的文件
- `apps/teacher-app/src/pages/knowledge/index.vue`（新建）
- `apps/teacher-app/src/pages/knowledge/detail.vue`（新建）

## 禁止修改的文件
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/dashboard/**`
- `apps/teacher-app/src/pages/questions/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/src/pages.json`
- `apps/student-app/**`
- `services/**`

## 完成标准
- L0: knowledge/index.vue 和 knowledge/detail.vue 存在
- L1: 列表页含搜索+分类标签+卡片; 详情页含Hero+正文+底部操作栏
- L2: 无 Tailwind 类名，无 HTML 标签

## 报告
写入: `.tasks/v7-teacher-app/f-v7-05-knowledge/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
