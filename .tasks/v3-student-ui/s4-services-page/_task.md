---
id: "s4-services-page"
parent: "v3-student-ui"
type: "feature"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/services/index.vue"
  - "apps/student-app/src/components/icons/"

out_of_scope:
  - "apps/student-app/src/pages/apply/classroom.vue"
  - "apps/student-app/src/pages/apply/status.vue"
  - "apps/student-app/src/pages/apply/detail.vue"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages.json"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages.json"
  - "_references/前端参考/stitch_ (1)/学生移动端/_5/screen.png"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"
  - "apps/student-app/src/pages/apply/status.vue"

done_criteria:
  L0: "pages/services/index.vue 存在且非占位内容（含服务矩阵 grid）"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无"
  L3: |
    H5 preview 中：
    1. TabBar 点击"事务导办"进入服务大厅页面
    2. 页面标题"服务大厅"可见
    3. 服务矩阵 grid 展示至少 6 个入口图标+文字
    4. 点击"空教室申请"成功跳转到 /pages/apply/classroom
    5. 点击"我的申请"成功跳转到 /pages/apply/status
    6. 点击 placeholder 入口弹出"功能开发中，敬请期待"提示

depends_on: ["s1-theme-unification", "s2-tabbar-routing"]
created_at: "2026-04-04"
---

# s4: 事务导办页面（Services Page）

> `pages/services/index.vue` 从占位文件升级为完整的服务大厅页面：展示校园事务入口矩阵，已实现的功能跳转对应页面，未实现的显示"功能开发中，敬请期待"提示。参考 Screen _5 设计稿风格。

## 背景

当前第 3 个 Tab（由 s2 任务建立路由）指向此页面。需要将占位文件替换为真实内容，作为"事务导办"功能的门户页面。不新增任何后端接口，所有 placeholder 功能前端拦截提示即可。

## 执行步骤

### 步骤 0：探查现有图标可用性

```powershell
ls apps/student-app/src/components/icons/
```

需要的图标：`IconDoorOpen`、`IconClipboardList`、`IconFileSignature`、`IconGraduationCap`、`IconFileText`、`IconHelpCircle`、`IconCalendar`、`IconLayoutGrid`。

- 已存在 → 直接使用
- 不存在 → 在 `components/icons/` 中新建对应 SVG 组件（参考已有图标的实现格式，使用 1.5px stroke 线性风格，与设计原则一致）

**允许在 scope 内新建图标文件**。

### 步骤 1：页面结构设计

完全重写 `pages/services/index.vue`，包含以下区块：

```
页面布局：
├── 毛玻璃 NavBar（标题"服务大厅"，Glass Header: 85% opacity + backdrop-blur:20px）
├── Header 区（品牌副标题："高效处理您的校园行政事务"）
├── 服务矩阵 Grid（3列或4列，每格含 icon + 文字）
└── （可选）最近动态区（从现有申请 API 获取或留空）
```

### 步骤 2：服务矩阵内容

| 名称 | 图标 | 状态 | 跳转 |
|---|---|---|---|
| 空教室申请 | IconDoorOpen | active | `/pages/apply/classroom` |
| 我的申请 | IconClipboardList | active | `/pages/apply/status` |
| 请假销假 | IconFileSignature | placeholder | 弹窗提示 |
| 学籍管理 | IconGraduationCap | placeholder | 弹窗提示 |
| 证明开具 | IconFileText | placeholder | 弹窗提示 |
| 心理服务 | IconHelpCircle | placeholder | 弹窗提示 |
| 缓考申请 | IconCalendar | placeholder | 弹窗提示 |
| 更多 | IconLayoutGrid | placeholder | 弹窗提示 |

### 步骤 3：样式要求

遵循设计系统规则（DESIGN.md）：
- **No-Line Rule**：不用 1px solid 分割线，用 `$md-sys-color-surface-container-low` 背景区分层级
- **Corner Radius**：服务卡片使用 `$radius-xl`（20px）或 `$radius-2xl`（24px）
- **Color**：使用 `$primary`（来自 theme.scss，不内联 #006a64）
- active 入口：正常颜色 + 可点击阴影；placeholder 入口：灰色调 + 轻透明度
- 整体背景：`$md-sys-color-background`（#F5F5F9）

### 步骤 4：placeholder 提示实现

点击 placeholder 入口时：
```typescript
uni.showToast({
  title: '功能开发中，敬请期待',
  icon: 'none',
  duration: 2000
})
```

### 步骤 5：清理占位文件

将 s2 任务创建的最小占位内容完全替换为本任务完整实现。

## 已知陷阱

- `pages/apply/status` 已降级为非 tabBar 页面，跳转须用 `uni.navigateTo`（非 `switchTab`）
- `pages/apply/classroom` 仍是普通页面，用 `uni.navigateTo`
- 不修改 apply 目录下任何现有文件
- 使用 theme.scss 的 `$primary`，**不内联** `#006a64`
