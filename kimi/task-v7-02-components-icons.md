# 任务: F-V7-02 公共组件转换 (TopAppBar + BottomNavBar + 27图标)

## 目标状态
`apps/teacher-app/src/components/` 下存在 TopAppBar.vue、BottomNavBar.vue 和 icons/ 目录下 27 个 SVG 图标组件，所有组件可被页面正常导入使用。

## 参考文件
- React TopBar: `D:\Backup_2025\下载\zip7-extracted\src\components\TopBar.tsx`
- React BottomNav: `D:\Backup_2025\下载\zip7-extracted\src\components\BottomNav.tsx`
- 设计系统: `D:\Backup_2025\下载\stitch4-extracted\stitch\ametrine_scholar\DESIGN.md`
- 色彩变量: `apps/teacher-app/src/styles/theme.scss`（已创建，直接 @import 使用）

## 关键设计规则（来自 DESIGN.md）
1. **No-Line Rule**: 禁 1px 实线边框，用背景色层级区分
2. **Tonal Stacking**: Surface 4 级层级
3. **毛玻璃**: backdrop-filter: blur(20px); background: rgba(255,255,255,0.8)
4. **禁纯黑**: 文字用 $on-surface (#2f2e32)
5. **药丸形**: 按钮/标签 border-radius: 9999px
6. **Ambient Shadow**: 阴影带 primary 色调 rgba(112,42,225,0.08)

## 执行步骤

### 步骤 1: 创建 TopAppBar.vue

文件路径: `apps/teacher-app/src/components/TopAppBar.vue`

转换规则（React TSX → Vue 3 SFC）:
- JSX → `<template>` + `<view>` / `<text>`
- `useNavigate(-1)` → `uni.navigateBack()`
- Lucide 图标 → 导入 icons/ 下对应组件
- Tailwind 类名 → SCSS（使用 theme.scss 变量）
- `className` → `class`
- `onClick` → `@click`

Props（defineProps）:
```typescript
interface Props {
  title: string
  showBack?: boolean
  action?: 'search' | 'settings' | 'add' | 'edit' | 'none'
}
```
默认值: showBack=false, action='none'

视觉规格:
- fixed 定位，top:0, z-index:50
- 高度 56px（h-14）
- 背景: rgba(255,255,255,0.8) + backdrop-filter: blur(20px) + -webkit-backdrop-filter: blur(20px)
- 标题: font-weight:700, font-size:20px, color:$on-surface
- 返回按钮: 圆形 padding:8px, hover 时 background:$surface-container-low
- action=add 时右侧按钮: background:rgba($primary, 0.1), color:$primary

Emit:
```typescript
const emit = defineEmits<{ action: [] }>()
```

### 步骤 2: 创建 BottomNavBar.vue

文件路径: `apps/teacher-app/src/components/BottomNavBar.vue`

这是 Custom TabBar 组件。

结构:
- 4 个 Tab 项: 工作台、学生提问、知识库、我的
- 对应路径: /pages/dashboard/index, /pages/questions/index, /pages/knowledge/index, /pages/profile/index
- 使用 `uni.switchTab()` 切换（注意：switchTab 只能跳 tabBar 页面）

视觉规格:
- fixed 定位，bottom:0, z-index:50
- 背景: rgba(255,255,255,0.9) + backdrop-filter: blur(20px) + -webkit-backdrop-filter: blur(20px)
- 顶部圆角: border-radius: 24px 24px 0 0 (rounded-t-3xl)
- 阴影: box-shadow: 0 -4px 20px rgba(99,14,212,0.05)
- 高度: calc(64px + env(safe-area-inset-bottom))
- padding-bottom: env(safe-area-inset-bottom)

每个 Tab 项:
- 图标 24x24
- 标签文字 font-size:10px, font-weight:500
- 未激活: color:$on-surface-variant, opacity:0.6
- 激活: color:$primary
- 激活态图标: strokeWidth 2.5, fill currentColor
- 激活态底部: 小圆点 (4x4, background:$primary, border-radius:50%)

"学生提问" Tab 需要支持红色数字徽章:
- Props: `badge?: number`
- 徽章样式: position:absolute, top:-6px, right:-8px, background:$error, color:white, font-size:10px, font-weight:700, padding:2px 6px, border-radius:9999px, ring:2px white

当前激活态判断:
- 使用一个 ref 来跟踪当前活跃的 tab index
- 由外部传入 `current` prop，或者在 onShow 生命周期中根据页面路径自动判断

**重要**: 在 UniApp 中，自定义 tabBar 的实现方式是：
1. pages.json 中声明 `"custom": true`
2. 在每个 tabBar 页面中手动引入 BottomNavBar 组件
3. 不需要 tabBar 的页面（如详情页）不引入

因此 BottomNavBar 需要接收 `current` prop（number, 0-3）表示当前选中的 tab。

```typescript
interface Props {
  current: number
  badge?: number  // 学生提问的未读数
}
```

### 步骤 3: 创建 27 个图标组件

在 `apps/teacher-app/src/components/icons/` 下创建以下 27 个 .vue 文件。

每个图标组件的统一模式:
```vue
<template>
  <svg xmlns="http://www.w3.org/2000/svg" :width="size" :height="size" viewBox="0 0 24 24" 
       fill="none" :stroke="color" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <!-- SVG path 内容 -->
  </svg>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  size?: number | string
  color?: string
}>(), {
  size: 24,
  color: 'currentColor'
})
</script>
```

以下是 27 个图标及其 SVG path（来自 Lucide 图标库）：

1. **IconDashboard.vue** (LayoutDashboard)
```svg
<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>
```

2. **IconMessage.vue** (MessageSquare)
```svg
<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
```

3. **IconBook.vue** (BookOpen)
```svg
<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
```

4. **IconUser.vue** (User)
```svg
<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
```

5. **IconBell.vue** (Bell)
```svg
<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
```

6. **IconPlus.vue** (PlusCircle)
```svg
<circle cx="12" cy="12" r="10"/><path d="M8 12h8"/><path d="M12 8v8"/>
```

7. **IconMegaphone.vue** (Megaphone)
```svg
<path d="m3 11 18-5v12L3 13v-2z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>
```

8. **IconChart.vue** (BarChart2)
```svg
<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>
```

9. **IconSettings.vue** (Settings)
```svg
<path d="M12.22 2h-.44a2 2 0 0 0-2 2v.18a2 2 0 0 1-1 1.73l-.43.25a2 2 0 0 1-2 0l-.15-.08a2 2 0 0 0-2.73.73l-.22.38a2 2 0 0 0 .73 2.73l.15.1a2 2 0 0 1 1 1.72v.51a2 2 0 0 1-1 1.74l-.15.09a2 2 0 0 0-.73 2.73l.22.38a2 2 0 0 0 2.73.73l.15-.08a2 2 0 0 1 2 0l.43.25a2 2 0 0 1 1 1.73V20a2 2 0 0 0 2 2h.44a2 2 0 0 0 2-2v-.18a2 2 0 0 1 1-1.73l.43-.25a2 2 0 0 1 2 0l.15.08a2 2 0 0 0 2.73-.73l.22-.39a2 2 0 0 0-.73-2.73l-.15-.08a2 2 0 0 1-1-1.74v-.5a2 2 0 0 1 1-1.74l.15-.09a2 2 0 0 0 .73-2.73l-.22-.38a2 2 0 0 0-2.73-.73l-.15.08a2 2 0 0 1-2 0l-.43-.25a2 2 0 0 1-1-1.73V4a2 2 0 0 0-2-2z"/><circle cx="12" cy="12" r="3"/>
```

10. **IconAlert.vue** (AlertCircle)
```svg
<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>
```

11. **IconCheck.vue** (CheckCircle2)
```svg
<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>
```

12. **IconArrowRight.vue** (ArrowRight)
```svg
<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>
```

13. **IconArrowLeft.vue** (ArrowLeft)
```svg
<path d="m12 19-7-7 7-7"/><path d="M19 12H5"/>
```

14. **IconSearch.vue** (Search)
```svg
<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>
```

15. **IconBrain.vue** (BrainCircuit)
```svg
<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>
```

16. **IconBot.vue** (Bot)
```svg
<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/><path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>
```

17. **IconLock.vue** (Lock)
```svg
<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>
```

18. **IconEye.vue** (Eye)
```svg
<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z"/><circle cx="12" cy="12" r="3"/>
```

19. **IconInfo.vue** (Info)
```svg
<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>
```

20. **IconLogout.vue** (LogOut)
```svg
<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>
```

21. **IconChevronRight.vue** (ChevronRight)
```svg
<path d="m9 18 6-6-6-6"/>
```

22. **IconEdit.vue** (Edit2)
```svg
<path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/>
```

23. **IconVolume.vue** (Volume2)
```svg
<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>
```

24. **IconGraduationCap.vue** (GraduationCap)
```svg
<path d="M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z"/><path d="M22 10v6"/><path d="M6 12.5V16a6 3 0 0 0 12 0v-3.5"/>
```

25. **IconQrCode.vue** (QrCode)
```svg
<rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/>
```

26. **IconFingerprint.vue** (Fingerprint)
```svg
<path d="M12 10a2 2 0 0 0-2 2c0 1.02-.1 2.51-.26 4"/><path d="M14 13.12c0 2.38 0 6.38-1 8.88"/><path d="M17.29 21.02c.12-.6.43-2.3.5-3.02"/><path d="M2 12a10 10 0 0 1 18-6"/><path d="M2 16h.01"/><path d="M21.8 16c.2-2 .131-5.354 0-6"/><path d="M5 19.5C5.5 18 6 15 6 12a6 6 0 0 1 .34-2"/><path d="M8.65 22c.21-.66.45-1.32.57-2"/><path d="M9 6.8a6 6 0 0 1 9 5.2v2"/>
```

27. **IconUserCheck.vue** (UserCheck)
```svg
<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><polyline points="16 11 18 13 22 9"/>
```

### 步骤 4: 创建 icons/index.ts（统一导出）

文件: `apps/teacher-app/src/components/icons/index.ts`

```typescript
export { default as IconDashboard } from './IconDashboard.vue'
export { default as IconMessage } from './IconMessage.vue'
export { default as IconBook } from './IconBook.vue'
export { default as IconUser } from './IconUser.vue'
export { default as IconBell } from './IconBell.vue'
export { default as IconPlus } from './IconPlus.vue'
export { default as IconMegaphone } from './IconMegaphone.vue'
export { default as IconChart } from './IconChart.vue'
export { default as IconSettings } from './IconSettings.vue'
export { default as IconAlert } from './IconAlert.vue'
export { default as IconCheck } from './IconCheck.vue'
export { default as IconArrowRight } from './IconArrowRight.vue'
export { default as IconArrowLeft } from './IconArrowLeft.vue'
export { default as IconSearch } from './IconSearch.vue'
export { default as IconBrain } from './IconBrain.vue'
export { default as IconBot } from './IconBot.vue'
export { default as IconLock } from './IconLock.vue'
export { default as IconEye } from './IconEye.vue'
export { default as IconInfo } from './IconInfo.vue'
export { default as IconLogout } from './IconLogout.vue'
export { default as IconChevronRight } from './IconChevronRight.vue'
export { default as IconEdit } from './IconEdit.vue'
export { default as IconVolume } from './IconVolume.vue'
export { default as IconGraduationCap } from './IconGraduationCap.vue'
export { default as IconQrCode } from './IconQrCode.vue'
export { default as IconFingerprint } from './IconFingerprint.vue'
export { default as IconUserCheck } from './IconUserCheck.vue'
```

## 允许修改的文件
- `apps/teacher-app/src/components/**`（新建）

## 禁止修改的文件
- `apps/teacher-app/src/styles/**`（已有，不改）
- `apps/teacher-app/src/stores/**`
- `apps/teacher-app/src/utils/**`
- `apps/teacher-app/src/types/**`
- `apps/teacher-app/src/api/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/vite.config.ts`
- `apps/student-app/**`
- `services/**`

## 硬约束
- 只做当前任务（组件和图标），不创建页面文件
- 每个图标组件必须支持 size 和 color props
- TopAppBar 和 BottomNavBar 必须使用 @import theme.scss 中的 SCSS 变量
- BottomNavBar 的 Tab 切换使用 uni.switchTab()
- 所有 SVG path 数据必须正确（来自 Lucide 图标库）
- 不要在组件中使用 Tailwind 类名，全部用 SCSS
- 必须添加 -webkit-backdrop-filter 前缀（兼容性）

## 完成标准
- L0: TopAppBar.vue, BottomNavBar.vue, icons/index.ts 存在
- L1: icons/ 目录下有 27 个 .vue 文件
- L2: TopAppBar 支持 title/showBack/action props; BottomNavBar 支持 current/badge props

## 报告
最终报告写入: `.tasks/v7-teacher-app/f-v7-02-components-icons/_report.md`

最终仅输出四段：
STEP-PLAN
STEP-EXECUTED
STEP-CHECK
BLOCKERS
