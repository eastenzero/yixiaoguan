# 任务: F-V7-07 路由配置 + 冒烟测试

## 目标状态
`apps/teacher-app/src/pages.json` 正确配置所有页面路由和自定义 tabBar，项目 `npx uni -p h5` 启动后所有页面可访问、tabBar 切换正常。

## 背景
当前 pages.json 只有一个临时首页 `pages/index/index`。需要替换为完整的路由配置，包含 tabBar 页面和子页面。

## 执行步骤

### 步骤 1: 修改 src/pages.json

**完全替换**现有 `apps/teacher-app/src/pages.json` 内容为以下内容：

```json
{
  "pages": [
    {
      "path": "pages/login/index",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "登录"
      }
    },
    {
      "path": "pages/dashboard/index",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "工作台"
      }
    },
    {
      "path": "pages/questions/index",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "学生提问"
      }
    },
    {
      "path": "pages/knowledge/index",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "知识库"
      }
    },
    {
      "path": "pages/profile/index",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "我的"
      }
    },
    {
      "path": "pages/questions/detail",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "提问详情"
      }
    },
    {
      "path": "pages/knowledge/detail",
      "style": {
        "navigationStyle": "custom",
        "navigationBarTitleText": "知识详情"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "医小管教师端",
    "navigationBarBackgroundColor": "#faf5fb",
    "backgroundColor": "#faf5fb"
  },
  "tabBar": {
    "custom": true,
    "color": "#5d5b5f",
    "selectedColor": "#702ae1",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/dashboard/index",
        "text": "工作台"
      },
      {
        "pagePath": "pages/questions/index",
        "text": "学生提问"
      },
      {
        "pagePath": "pages/knowledge/index",
        "text": "知识库"
      },
      {
        "pagePath": "pages/profile/index",
        "text": "我的"
      }
    ]
  }
}
```

**关键配置说明：**
- `pages` 数组的第一项是应用启动首页 → 设为 `pages/login/index`（登录页）
- 所有页面使用 `"navigationStyle": "custom"` 因为已有自定义 TopAppBar
- `tabBar.custom = true` 启用自定义 tabBar（使用 BottomNavBar 组件）
- tabBar `list` 必须包含 4 个 tab 页面，路径不带前导 `/`
- 子页面（detail）不在 tabBar 中，通过 `uni.navigateTo` 访问

### 步骤 2: 删除临时首页

删除 `apps/teacher-app/src/pages/index/index.vue` 文件（已被 login 和 dashboard 替代）。

如果无法删除文件，则将其内容替换为：
```vue
<template>
  <view></view>
</template>
<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
onLoad(() => {
  uni.reLaunch({ url: '/pages/login/index' })
})
</script>
```

### 步骤 3: 验证项目启动

在 `apps/teacher-app` 目录下执行：
```bash
npx uni -p h5
```

等待输出包含 `ready in` 字样，确认端口为 5175。

如果有编译错误，检查并修复：
- 检查 pages.json 中的路径是否与实际文件路径一致
- 检查所有被引用的组件是否存在
- 检查 SCSS import 路径是否正确

### 步骤 4: 冒烟验证

启动后，在浏览器中验证以下路由可访问（不报白屏或 404）：
1. `http://localhost:5175/#/pages/login/index` — 登录页
2. `http://localhost:5175/#/pages/dashboard/index` — 工作台
3. `http://localhost:5175/#/pages/questions/index` — 提问列表
4. `http://localhost:5175/#/pages/knowledge/index` — 知识库
5. `http://localhost:5175/#/pages/profile/index` — 个人中心
6. `http://localhost:5175/#/pages/questions/detail` — 提问详情
7. `http://localhost:5175/#/pages/knowledge/detail` — 知识详情

**注意：** 只需确认页面可渲染（不是白屏），不要求功能完整。如果有编译告警但页面可渲染，记录告警但不算失败。

## 允许修改的文件
- `apps/teacher-app/src/pages.json`（修改）
- `apps/teacher-app/src/pages/index/index.vue`（删除或替换）

## 禁止修改的文件
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/dashboard/**`
- `apps/teacher-app/src/pages/questions/**`
- `apps/teacher-app/src/pages/knowledge/**`
- `apps/teacher-app/src/pages/profile/**`
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/package.json`
- `apps/teacher-app/vite.config.ts`
- `apps/student-app/**`
- `services/**`

## 硬约束
- pages.json 第一项必须是 login/index
- tabBar.custom 必须为 true
- 所有页面 navigationStyle 必须为 custom
- 冒烟测试端口必须是 5175
- 如果有编译错误，只允许修复 pages.json 或 index/index.vue，不改其他页面

## 完成标准
- L0: pages.json 包含 7 个页面路由 + tabBar 配置
- L1: `npx uni -p h5` 启动成功（输出 `ready in`）
- L2: 至少 login 和 dashboard 两个页面可在浏览器渲染（非白屏）

## 报告
写入: `.tasks/v7-teacher-app/f-v7-07-routing-smoke/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS

**重要：冒烟测试完成后，必须停止 dev server（Ctrl+C 或关闭进程），不要让它持续运行。**
