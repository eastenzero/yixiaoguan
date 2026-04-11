# F-V7-02 公共组件+图标 任务报告

## STEP-PLAN
1. 创建 TopAppBar.vue - 顶部导航栏组件（支持 title/showBack/action props）
2. 创建 BottomNavBar.vue - 底部导航栏组件（支持 current/badge props）
3. 创建 27 个图标组件（SVG 图标，支持 size/color props）
4. 创建 icons/index.ts - 统一导出所有图标

## STEP-EXECUTED

### ✅ 步骤 1: TopAppBar.vue
- 路径: `apps/teacher-app/src/components/TopAppBar.vue`
- Props: title, showBack, action
- 特性:
  - 固定定位，z-index: 50，高度 56px
  - 毛玻璃效果: backdrop-filter: blur(20px) + -webkit-backdrop-filter
  - 背景: rgba(255,255,255,0.8)
  - 返回按钮使用 IconArrowLeft
  - action 支持: search/settings/add/edit/none
  - add 按钮使用 primary 色背景
  - 导入 theme.scss 使用 SCSS 变量

### ✅ 步骤 2: BottomNavBar.vue
- 路径: `apps/teacher-app/src/components/BottomNavBar.vue`
- Props: current, badge
- 特性:
  - 4 个 Tab: 工作台/学生提问/知识库/我的
  - 固定底部，z-index: 50
  - 毛玻璃效果 + 顶部圆角 24px
  - 阴影: box-shadow: 0 -4px 20px rgba(99,14,212,0.05)
  - 安全区适配: env(safe-area-inset-bottom)
  - 激活态: primary 色 + 底部小圆点
  - 学生提问 Tab 支持红色数字徽章
  - 使用 uni.switchTab() 切换页面

### ✅ 步骤 3: 27 个图标组件
全部创建于 `apps/teacher-app/src/components/icons/`:

| 序号 | 组件名 | Lucide 对应 |
|------|--------|-------------|
| 1 | IconDashboard | LayoutDashboard |
| 2 | IconMessage | MessageSquare |
| 3 | IconBook | BookOpen |
| 4 | IconUser | User |
| 5 | IconBell | Bell |
| 6 | IconPlus | PlusCircle |
| 7 | IconMegaphone | Megaphone |
| 8 | IconChart | BarChart2 |
| 9 | IconSettings | Settings |
| 10 | IconAlert | AlertCircle |
| 11 | IconCheck | CheckCircle2 |
| 12 | IconArrowRight | ArrowRight |
| 13 | IconArrowLeft | ArrowLeft |
| 14 | IconSearch | Search |
| 15 | IconBrain | BrainCircuit |
| 16 | IconBot | Bot |
| 17 | IconLock | Lock |
| 18 | IconEye | Eye |
| 19 | IconInfo | Info |
| 20 | IconLogout | LogOut |
| 21 | IconChevronRight | ChevronRight |
| 22 | IconEdit | Edit2 |
| 23 | IconVolume | Volume2 |
| 24 | IconGraduationCap | GraduationCap |
| 25 | IconQrCode | QrCode |
| 26 | IconFingerprint | Fingerprint |
| 27 | IconUserCheck | UserCheck |

每个图标组件:
- 支持 size 和 color props（默认 size=24, color='currentColor'）
- 使用 Lucide 标准 SVG path
- stroke-width="2", stroke-linecap="round", stroke-linejoin="round"

### ✅ 步骤 4: icons/index.ts
- 路径: `apps/teacher-app/src/components/icons/index.ts`
- 统一导出全部 27 个图标组件
- 支持批量导入: `import { IconDashboard, IconUser } from '@/components/icons'`

## STEP-CHECK

### L0 检查 - 文件存在性
| 文件 | 状态 |
|------|------|
| TopAppBar.vue | ✅ 3089 bytes |
| BottomNavBar.vue | ✅ 3254 bytes |
| icons/index.ts | ✅ 1592 bytes |
| icons/*.vue (27个) | ✅ 全部存在 |

### L1 检查 - 图标数量
```
icons 目录文件数: 28 (27个 .vue + 1个 index.ts)
```

### L2 检查 - Props 支持
| 组件 | Props | 默认值 |
|------|-------|--------|
| TopAppBar | title, showBack, action | showBack=false, action='none' |
| BottomNavBar | current, badge | current=0, badge=0 |
| 图标组件 | size, color | size=24, color='currentColor' |

### 设计规则遵守
- ✅ No-Line Rule: 无 1px 实线边框
- ✅ Tonal Stacking: 使用 $surface-container-low 等层级
- ✅ 毛玻璃: backdrop-filter + -webkit-backdrop-filter
- ✅ 禁纯黑: 使用 $on-surface (#2f2e32)
- ✅ 药丸形: border-radius: 9999px (徽章)
- ✅ Ambient Shadow: rgba(99,14,212,0.05)
- ✅ 全部使用 SCSS，无 Tailwind 类名

## BLOCKERS
无阻塞问题，任务完成。
