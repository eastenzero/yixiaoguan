# 任务: F-V7-03 登录页 + 工作台页面

## 目标状态
`apps/teacher-app/src/pages/login/index.vue` 和 `apps/teacher-app/src/pages/dashboard/index.vue` 存在，视觉还原 React 原型，使用 SCSS 变量和已有公共组件。

## 参考文件（必须先读取）
- React 登录页: `D:\Backup_2025\下载\zip7-extracted\src\pages\Login.tsx`
- React 工作台: `D:\Backup_2025\下载\zip7-extracted\src\pages\Dashboard.tsx`
- 色彩变量: `apps/teacher-app/src/styles/theme.scss`
- 公共组件: `apps/teacher-app/src/components/TopAppBar.vue`
- 公共组件: `apps/teacher-app/src/components/BottomNavBar.vue`
- 图标组件: `apps/teacher-app/src/components/icons/index.ts`

## 转换规则
- React JSX → Vue 3 `<template>` + UniApp 标签 (`<view>`, `<text>`, `<image>`, `<input>`)
- **禁止使用** `<div>`, `<span>`, `<img>`, `<p>`, `<h1>`~`<h6>` 等 HTML 标签，全部用 UniApp 标签
- Tailwind 类名 → SCSS（使用 theme.scss 变量）
- `className` → `class`
- `onClick` → `@click`
- `useNavigate` → `uni.navigateTo` / `uni.switchTab` / `uni.reLaunch`
- Lucide 图标 → 导入 icons/ 下对应 Vue 组件
- 外部图片 URL → 用灰色占位圆（avatar 用 `background: $surface-container-high; border-radius: 50%`）
- `Link to=` → `@click="uni.navigateTo({url: ...})"`
- 动画 `animate-[fadeUp...]` → 使用 global.scss 中已有的 `.animate-fade-up` + `.delay-N`

## 页面 1: login/index.vue

创建 `apps/teacher-app/src/pages/login/index.vue`

### 结构
1. 全屏渐变背景 (from-primary via-primary-dim to-primary-container 方向)
2. 装饰光晕圆（2个，absolute，blur，半透明）
3. 居中登录卡片（白色/95%透明 + 毛玻璃 + 圆角24px + 阴影）
4. Logo区域（渐变方块 + GraduationCap图标 + 标题"医小管" + 副标题"教师工作台"）
5. 表单区域:
   - 工号输入框（ghost风格，icon在左，$surface-container-low背景，圆角12px）
   - 密码输入框（同上 + 右侧Eye切换按钮）
   - 记住我复选框 + 忘记密码链接
   - 登录按钮（药丸形，渐变背景 primary→primary-container，白色文字+箭头图标）
6. 底部其他登录方式（QrCode + Fingerprint 图标按钮）
7. Footer（学校名称 + 版权信息）

### 交互
- 密码显示/隐藏切换（ref: showPassword）
- 登录按钮点击 → `uni.switchTab({ url: '/pages/dashboard/index' })`
- 表单数据用 ref 管理（username, password, rememberMe）

### 样式要点
- 背景渐变: `background: linear-gradient(135deg, $primary-fixed-dim, $primary, $primary-dim)`
- 卡片: `background: rgba(255,255,255,0.95); backdrop-filter: blur(40px); border-radius: 16px; padding: 40px; box-shadow: 0 32px 64px -12px rgba(0,0,0,0.15)`
- 输入框: `height: 56px; padding-left: 48px; background: $surface-container-low; border-radius: 12px; border: none; outline: none`
- 登录按钮: `height: 56px; border-radius: 9999px; background: linear-gradient(to right, $primary, $primary-container)`

## 页面 2: dashboard/index.vue

创建 `apps/teacher-app/src/pages/dashboard/index.vue`

### 结构
1. 自定义顶栏（不用 TopAppBar，Dashboard有独特的左侧 icon+标题 + 右侧通知铃铛）
2. 欢迎横幅（渐变卡片，圆角24px，"早上好，梁老师" + 待处理数 + 头像占位圆）
3. 快捷操作横向滚动区（4个药丸按钮：新建知识、发布通知、数据报告、系统设置）
4. 统计网格（2×2 grid，每格一个图标+数字+标签）
5. 待处理提问列表（标题+查看全部链接 + 3张提问卡片）
6. BottomNavBar（current=0）

### 提问卡片结构
- 学生姓名 + 院系标签 + 时间
- 提问内容（单行截断）
- 状态指示点 + 状态文字 + 箭头

### 样式要点
- 欢迎横幅: `background: linear-gradient(135deg, $primary, $primary-container); border-radius: 24px; padding: 24px; box-shadow: 0 12px 32px -4px rgba(112,42,225,0.15)`
- 快捷按钮: `background: $surface-container-low; border-radius: 9999px; padding: 12px 16px`
- 统计卡片: `border-radius: 16px; padding: 16px`，4个分别用不同背景色
- 提问卡片: `background: $surface-container-low; border-radius: 16px; padding: 16px`

### Mock 数据
所有数据使用 `<script setup>` 中的 const 定义，不调用 API。

## 允许修改的文件
- `apps/teacher-app/src/pages/login/index.vue`（新建）
- `apps/teacher-app/src/pages/dashboard/index.vue`（新建）

## 禁止修改的文件
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/stores/**`
- `apps/teacher-app/src/utils/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/vite.config.ts`
- `apps/teacher-app/src/pages.json`（路由配置由后续任务统一处理）
- `apps/student-app/**`
- `services/**`

## 硬约束
- 不使用 HTML 标签（div/span/img/p/h1），用 UniApp 的 view/text/image
- 不使用 Tailwind 类名
- 所有色彩必须用 theme.scss 变量
- 图标用 icons/ 下的 Vue 组件
- 不修改任何已有文件
- 外部图片 URL 全部替换为灰色占位

## 完成标准
- L0: login/index.vue 和 dashboard/index.vue 文件存在
- L1: Login 包含表单（用户名+密码+登录按钮）; Dashboard 包含欢迎横幅+统计网格+提问列表
- L2: 两个页面均使用 `@import theme.scss` 且无 Tailwind 类名

## 报告
最终报告写入: `.tasks/v7-teacher-app/f-v7-03-login-dashboard/_report.md`

最终仅输出四段：STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
