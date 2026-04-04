---
id: "s2-tabbar-routing"
parent: "v3-student-ui"
type: "feature"
status: "pending"
tier: "T2"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/components/CustomTabBar.vue"
  - "apps/student-app/src/pages/home/index.vue"
  - "apps/student-app/src/pages/profile/index.vue"
  - "apps/student-app/src/pages/apply/status.vue"

out_of_scope:
  - "apps/student-app/src/pages/apply/classroom.vue"
  - "apps/student-app/src/pages/apply/detail.vue"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/services/index.vue"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/components/CustomTabBar.vue"
  - "apps/student-app/src/pages/home/index.vue"
  - "apps/student-app/src/pages/profile/index.vue"

done_criteria:
  L0: "pages.json 中第 3 个 tab pagePath 为 pages/services/index；pages/services/index 已在 pages 数组中注册"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无"
  L3: "H5 preview 中 TabBar 四项文字为 首页/智能问答/事务导办/我的；点击事务导办进入 services 页面（即使是空页面）；apply/status 仍可从其他入口导航进入"

depends_on: []
created_at: "2026-04-04"
---

# s2: TabBar 路由重构

> `pages.json` 第 3 个 Tab 从 `pages/apply/status` 改为 `pages/services/index`，四个 Tab 文字全部改为中文；`CustomTabBar.vue` 标签同步中文化；全局搜索并迁移 `switchTab apply/status` 为 `navigateTo`。

## 背景

当前 Tab 2 text="咨询"，Tab 3 text="申请"（指向 apply/status）。需改为"智能问答"和"事务导办"（指向新建的 services/index）。apply/status 降级为普通页面，不再是 tabBar 页面。CustomTabBar.vue 当前英文标签需汉化（DEBT-V3-02）。

## 执行步骤

### 步骤 0：探查 CustomTabBar 渲染机制（RISK-V3-01）

**先执行，再动代码：**

```powershell
grep -r "CustomTabBar" apps/student-app/src/pages/ --include="*.vue" -l
```

- 若输出了文件列表 → 各页面手动引入，修改 `CustomTabBar.vue` labels 即可生效
- 若无输出 → 组件未被页面使用，需排查是否走 uni-app 标准 custom-tab-bar 机制（检查 `apps/student-app/src/custom-tab-bar/` 是否存在）
- **无论哪种情况**，都要确保最终 TabBar 显示正确中文标签，不允许只改 pages.json 文字了事（原生 tabBar 优先级低于 custom）

记录探查结果在 `_report.md` 中。

### 步骤 1：修改 pages.json

1. Tab 2（index=1）：`"text": "咨询"` → `"text": "智能问答"`
2. Tab 3（index=2）：`"pagePath": "pages/apply/status"` → `"pagePath": "pages/services/index"`，`"text": "申请"` → `"text": "事务导办"`
3. 在 `pages` 数组中新增 services/index 注册（暂时指向空白页，由 s4 任务填充内容）：
   ```json
   {
     "path": "pages/services/index",
     "style": {
       "navigationBarTitleText": "事务导办",
       "navigationStyle": "custom"
     }
   }
   ```

### 步骤 2：修改 CustomTabBar.vue 标签（DEBT-V3-02）

将 `tabs` 数组的 `label` 字段改为中文：

```typescript
const tabs = [
  { key: 'home' as const, label: '首页', icon: IconHome },
  { key: 'assistant' as const, label: '智能问答', icon: IconBot },
  { key: 'services' as const, label: '事务导办', icon: IconLayoutGrid },
  { key: 'profile' as const, label: '我的', icon: IconUser }
]
```

### 步骤 3：全局迁移 switchTab apply/status（RISK-V3-03）

先搜索所有引用位置：
```powershell
grep -r "switchTab.*apply" apps/student-app/src/ --include="*.vue" -n
grep -r "apply/status" apps/student-app/src/ --include="*.vue" -n
```

预计涉及文件：
- `pages/home/index.vue`：`goToServices()` 方法中的 `switchTab` 调用 → 改为 `uni.switchTab({ url: '/pages/services/index' })`（注意：跳转目标也要改，从 apply/status 改为 services/index）
- `pages/profile/index.vue`：`goToApplyStatus()` 中的 `switchTab` → 改为 `uni.navigateTo({ url: '/pages/apply/status' })`

**规则**：
- 所有 `switchTab` 指向 `apply/status` 的 → 改为 `navigateTo`（因为它不再是 tabBar 页面）
- 如果原意是"跳转到事务导办 Tab" → 改为 `switchTab` 指向 `services/index`

### 步骤 4：pages/services/index.vue 占位文件

创建最小化占位页面（s4 任务会重写，这里只是让路由不报错）：

```vue
<template>
  <view class="services-placeholder">
    <text>事务导办（加载中...）</text>
  </view>
</template>
<script setup lang="ts"></script>
```

> ⚠️ 此占位文件由 s4 任务完全重写，不必精心设计。

## 已知陷阱

- RISK-V3-01：custom tabBar 渲染机制必须先探查，禁止跳过步骤 0
- RISK-V3-03：全局 grep 搜索不能漏，包括 home、profile、questions 等所有页面
- `apply/status` 的 `navigationBarTitleText` 在 pages.json 中已是"我的申请"，保持不变
- **不要修改** apply/classroom.vue、apply/detail.vue、chat/index.vue 等 out_of_scope 文件
