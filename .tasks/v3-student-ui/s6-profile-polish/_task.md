---
id: "s6-profile-polish"
parent: "v3-student-ui"
type: "feature"
status: "pending"
tier: "T2"
priority: "low"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/profile/index.vue"

out_of_scope:
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/home/index.vue"
  - "apps/student-app/src/pages/services/index.vue"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages/profile/index.vue"
  - "_references/前端参考/stitch_ (1)/学生移动端/_7/screen.png"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"

done_criteria:
  L0: "profile/index.vue 中不含 hardcoded mock AI 历史数据数组（grep 验证）"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无"
  L3: |
    H5 preview 中：
    1. 个人中心页面正常显示，退出登录功能正常
    2. "常用服务"入口名称与事务导办模块保持一致
    3. 跳转 apply/status 使用 navigateTo（非 switchTab）
    4. 无 hardcoded mock 数据显示（AI 助手历史区域为空状态或从 API 获取）

depends_on: ["s1-theme-unification", "s2-tabbar-routing"]
created_at: "2026-04-04"
---

# s6: 个人中心微调（Profile Polish）

> `profile/index.vue` 修正路由跳转（apply/status 从 switchTab → navigateTo）、清理 hardcoded mock AI 历史数据、将"常用服务"入口名称与事务导办模块对齐。不做大幅样式重写，现有样式已基本符合参考设计 Screen _7。

## 背景

个人中心有两个已知问题：
1. `goToApplyStatus()` 使用 switchTab 跳转 apply/status，但 s2 任务完成后 apply/status 不再是 tabBar 页面
2. 页面可能存在 hardcoded mock 数据（AI 助手历史等），展示时容易误导

## 执行步骤

### 步骤 1：修正路由跳转

搜索 profile/index.vue 中所有 `switchTab.*apply` 引用：
```powershell
Select-String -Path "apps/student-app/src/pages/profile/index.vue" -Pattern "switchTab.*apply"
```

将 `goToApplyStatus()` 或类似方法改为：
```typescript
uni.navigateTo({ url: '/pages/apply/status' })
```

### 步骤 2：清理 hardcoded mock 数据

搜索页面中的 mock 数据：
```powershell
Select-String -Path "apps/student-app/src/pages/profile/index.vue" -Pattern "mock|history.*\[|historyList"
```

找到 AI 助手历史的 hardcoded 数组 → 替换为：
- 空数组（`[]`）+ 空状态提示文案"暂无历史记录"，或
- 从现有 API 接口获取（若接口存在）

**优先选空状态**，不要为此新建接口。

### 步骤 3：常用服务入口名称对齐

检查个人中心的"常用服务"快捷入口：
- "申请"或"空教室申请"相关入口 → 确认命名与 s4 事务导办一致
- 跳转目标确认：空教室申请 → navigateTo apply/classroom；我的申请 → navigateTo apply/status

### 步骤 4：样式微检查（按需）

仅检查以下项，不做大幅改动：
- 是否有内联 `#00639B`（旧蓝色）→ 替换为 `$primary`
- 是否有 `1px solid` 分割线 → 酌情改为背景色层级（No-Line Rule，低优先级）

## 已知陷阱

- "关于医小管"字样已正确，保持不变
- 不修改登录/退出逻辑
- 不修改样式主体结构（现有样式已基本符合设计稿）
- 改动范围控制在最小，P2 优先级，不影响核心功能
