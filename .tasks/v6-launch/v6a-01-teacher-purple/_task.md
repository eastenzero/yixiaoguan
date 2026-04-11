---
id: "v6a-01-teacher-purple"
parent: "v6-launch"
type: "feature"
status: "pending"
tier: "T3"
priority: "high"
risk: "medium"
foundation: false

scope:
  - "apps/teacher-web/src/assets/main.css"
  - "apps/teacher-web/src/assets/base.css"
  - "apps/teacher-web/src/views/*.vue"
  - "apps/teacher-web/src/layouts/*.vue"
  - "apps/teacher-web/src/App.vue"

out_of_scope:
  - "apps/student-app/**"
  - "services/**"
  - "scripts/**"
  - "deploy/**"
  - "apps/teacher-web/src/api/**"
  - "apps/teacher-web/src/stores/**"
  - "apps/teacher-web/src/router/**"
  - "apps/teacher-web/src/utils/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/teacher-web/src/assets/main.css"

done_criteria:
  L0: "apps/teacher-web/src/assets/main.css 中 --primary-color 值为紫色系 (#7C3AED 或 #630ed4)"
  L1: "grep -r '#00685f' apps/teacher-web/src/ 无结果（注释除外）; grep -r '#008378' 无结果; grep -r '#0D9488' 无结果; grep -r '#004d47' 无结果; grep -r '#006a63' 无结果; grep -r 'rgba(0, 104, 95' 无结果"
  L2: "npm run build --prefix apps/teacher-web 成功无错误"
  L3: "登录页、侧边栏、导航栏、按钮、表格行悬停均呈现紫色系"

depends_on: []
created_at: "2026-04-11 16:20:00"
---

# 教师端主题色从绿色改为紫色

> 教师端 (teacher-web) 所有绿色系主题元素变为紫色系，与学生端统一品牌色。

## 背景

教师端当前使用深翠绿 (#00685f) 作为主题色。老师要求统一改为紫色系，与学生端一致。

## 目标色值

```css
--primary-color: #7C3AED      /* 主色 (violet-600) */
--primary-container: #6D28D9  /* 容器色 (violet-700) */
--primary-light: #8B5CF6      /* 浅色 (violet-500) */
--primary-dark: #5B21B6       /* 深色 (violet-800) */
--primary-bg: #F5F3FF         /* 背景色 (violet-50) */
--primary-bg-soft: #EDE9FE    /* 柔和背景 (violet-100) */
--secondary: #6D28D9          /* 次要色 */
```

## 变更要点

1. **main.css** — 修改 `:root` 下所有主色 CSS 变量
2. **所有 .vue 文件** — 搜索并替换硬编码的绿色值:
   - `#00685f` → `var(--primary-color)` 或 `#7C3AED`
   - `#008378` → `var(--primary-container)` 或 `#6D28D9`
   - `#0D9488` → `var(--primary-light)` 或 `#8B5CF6`
   - `#004d47` → `var(--primary-dark)` 或 `#5B21B6`
   - `#006a63` → `var(--primary-color)` 或 `#7C3AED`
   - `rgba(0, 104, 95, ...)` → 对应紫色 rgba
3. **card-shadow-hover** — `rgba(0, 104, 95, 0.08)` → `rgba(124, 58, 237, 0.08)`
4. **textarea focus** — `rgba(0, 104, 95, 0.1)` → `rgba(124, 58, 237, 0.1)`

## 已知硬编码位置 (42处，10个文件)

- AnalyticsView.vue: 9处
- DashboardView.vue: 8处
- main.css: 7处
- MainLayout.vue: 4处
- ProfileView.vue: 4处
- KnowledgeView.vue: 3处
- QuestionsView.vue: 3处
- ApprovalView.vue: 2处
- LoginView.vue: 1处
- NotFoundView.vue: 1处

## 已知陷阱

- Element Plus 组件通过 CSS 变量继承颜色，改 `:root` 变量即可覆盖大部分，但 `.vue` 中的内联硬编码必须逐一替换
- 注意 SVG 或 icon 中可能有绿色硬编码
- 不要改 --success 色（#10b981 是绿色但是功能色，不是主题色）
