# 任务: F-V7-06 个人中心页面

## 目标状态
`apps/teacher-app/src/pages/profile/index.vue` 存在，视觉还原 React 原型。

## 参考文件（必须先读取）
- React 个人中心: `D:\Backup_2025\下载\zip7-extracted\src\pages\Profile.tsx`
- 色彩变量: `apps/teacher-app/src/styles/theme.scss`
- 公共组件: `apps/teacher-app/src/components/TopAppBar.vue`
- 公共组件: `apps/teacher-app/src/components/BottomNavBar.vue`
- 图标: `apps/teacher-app/src/components/icons/index.ts`

## 转换规则
- React JSX → Vue 3 `<template>` + UniApp 标签 (`<view>`, `<text>`, `<image>`)
- **禁止使用** `<div>`, `<span>`, `<img>`, `<p>`, `<h1>`~`<h6>` 等 HTML 标签
- Tailwind → SCSS（theme.scss 变量）
- Lucide 图标 → icons/ Vue 组件
- 外部图片 URL → 灰色占位圆
- 动画用 global.scss 的 `.animate-fade-up` + `.delay-N`

## 页面结构

### 1. TopAppBar (title="我的", showBack=true, action="settings")

### 2. 个人信息卡（渐变 Hero）
- 渐变背景: `linear-gradient(135deg, $primary, $primary-container)`
- 圆角24px，padding 32px
- 装饰光晕（2个 absolute 半透明圆 + blur）
- 头像占位圆（96x96，灰色，border: 4px solid rgba(255,255,255,0.2)）
- 姓名（24px, 粗体, 白色）
- 职称/院系（14px, 白色90%透明度）
- 工号标签（药丸形，`background: rgba(255,255,255,0.2); backdrop-filter: blur(10px)`）
- 阴影: `box-shadow: 0 12px 32px -4px rgba(112,42,225,0.15)`

### 3. 统计网格（3列）
- 累计处理: 156
- 本月审批: 42
- 知识入库: 28
- 每格: `background: $surface-container-low; border-radius: 16px; padding: 16px; text-align: center`
- 数字: `font-size: 20px; font-weight: 800; color: $primary`
- 标签: `font-size: 10px; color: $on-surface-variant`

### 4. 系统设置列表
标题: "系统设置"（`font-size: 12px; font-weight: 700; color: $on-surface-variant; text-transform: uppercase; letter-spacing: 0.1em`）

第一组（开关项，`background: $surface-container-low; border-radius: 16px`）:
- 通知提醒（Bell图标，开关=ON）
- 声音提示（Volume图标，开关=ON）
- AI 自动回复（Bot图标，开关=OFF）

每项结构:
- 左: 图标圆（40x40, `background: white; border-radius: 50%`）+ 项目名称
- 右: 模拟开关
  - ON: `width: 48px; height: 24px; background: $primary; border-radius: 9999px`，圆点靠右
  - OFF: `background: $surface-container-highest`，圆点靠左
  - 圆点: `width: 16px; height: 16px; background: white; border-radius: 50%`

第二组（导航项）:
- 修改密码（Lock图标 + ChevronRight箭头）
- 关于我们（Info图标 + ChevronRight箭头）

### 5. 退出登录按钮
- `background: rgba($error-container, 0.1); color: $error; border-radius: 16px; padding: 20px; font-weight: 700`
- LogOut图标 + "退出登录"文字
- 点击 → `uni.reLaunch({ url: '/pages/login/index' })`

### 6. BottomNavBar (current=3)

## 交互
- 开关用 ref 管理（notificationOn, soundOn, aiReplyOn）
- 点击开关切换 boolean 值
- 退出登录 → reLaunch 到 login

## Mock 数据
const 定义在 `<script setup>` 中。

## 允许修改的文件
- `apps/teacher-app/src/pages/profile/index.vue`（新建）

## 禁止修改的文件
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/dashboard/**`
- `apps/teacher-app/src/pages/questions/**`
- `apps/teacher-app/src/pages/knowledge/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/src/pages.json`
- `apps/student-app/**`
- `services/**`

## 完成标准
- L0: profile/index.vue 存在
- L1: 含渐变Hero+统计网格+设置列表+退出按钮
- L2: 无 Tailwind 类名，无 HTML 标签，开关可交互

## 报告
写入: `.tasks/v7-teacher-app/f-v7-06-profile/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
