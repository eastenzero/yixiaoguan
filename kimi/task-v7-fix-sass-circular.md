# 任务: 修复 Sass 循环导入错误

## 问题
所有页面白屏，控制台报错:
```
[plugin:vite:css] [sass] This file is already being loaded.
@import '@/styles/theme.scss';
```

## 根因
`uni.scss` 已经 `@import '@/styles/theme.scss'`。UniApp 框架会自动将 uni.scss 注入到每个 .vue 组件的 `<style>` 块中。因此各 .vue 文件不应再手动 `@import theme.scss`，否则造成循环导入。

同理，`global.scss` 也 `@import './theme.scss'`，如果 `App.vue` 引用了 global.scss，也不应再单独引入 theme.scss。

## 修复方案

**删除以下文件中 `<style>` 块里的 `@import ...theme.scss` 行：**

1. `apps/teacher-app/src/pages/login/index.vue` — 删除 `@import '../../styles/theme.scss';`
2. `apps/teacher-app/src/pages/dashboard/index.vue` — 删除 `@import '../../styles/theme.scss';`
3. `apps/teacher-app/src/pages/questions/index.vue` — 删除 `@import '../../styles/theme.scss';`
4. `apps/teacher-app/src/pages/questions/detail.vue` — 删除 `@import '../../styles/theme.scss';`
5. `apps/teacher-app/src/pages/knowledge/index.vue` — 删除 `@import '../../styles/theme.scss';`
6. `apps/teacher-app/src/pages/knowledge/detail.vue` — 删除 `@import '../../styles/theme.scss';`
7. `apps/teacher-app/src/pages/profile/index.vue` — 删除 `@import '../../styles/theme.scss';`
8. `apps/teacher-app/src/components/TopAppBar.vue` — 删除 `@import '../styles/theme.scss';`
9. `apps/teacher-app/src/components/BottomNavBar.vue` — 删除 `@import '../styles/theme.scss';`
10. `apps/teacher-app/src/App.vue` — 删除 `@import '@/styles/theme.scss';`
11. `apps/teacher-app/src/styles/global.scss` — 删除 `@import './theme.scss';`

**注意**:
- 只删除 `@import` 那一行，不删除其他任何内容
- 不要删除 `uni.scss` 中的 `@import '@/styles/theme.scss';`，那是唯一正确的入口
- 删除后，$primary 等变量仍然可用，因为 uni.scss 全局注入
- 如果 `global.scss` 中使用了 theme.scss 的变量（如 $primary），在删除 import 后需要确认 global.scss 是如何被引入的。如果 global.scss 被 App.vue 的 `<style>` 引用，则 uni.scss 注入的变量在该作用域中已可用

## 允许修改的文件
上述 11 个文件（仅删除 @import 行）

## 禁止修改的文件
- `apps/teacher-app/src/uni.scss`（不改！这是正确的全局入口）
- `apps/teacher-app/src/styles/theme.scss`（不改）
- `apps/teacher-app/package.json`
- `apps/teacher-app/vite.config.ts`

## 完成标准
- L0: 所有 11 个文件中的 `@import ...theme.scss` 行已删除
- L1: 项目无 Sass 编译错误

## 报告
最终输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
不需要写报告文件。
