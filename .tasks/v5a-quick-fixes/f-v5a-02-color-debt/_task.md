---
id: "f-v5a-02"
parent: "v5a-quick-fixes"
type: "bugfix"
status: "done"
tier: "T3"
priority: "low"
risk: "low"
foundation: false

depends_on: ["f-v5a-01", "f-v5a-04", "f-v5a-05"]

scope:
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/apply/status.vue"
  - "apps/student-app/src/pages/apply/detail.vue"
  - "apps/student-app/src/components/CustomTabBar.vue"
  - "apps/student-app/src/pages.json"
out_of_scope:
  - "apps/student-app/src/styles/theme.scss"
  - "services/**"
  - "scripts/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/apply/status.vue"
  - "apps/student-app/src/pages/apply/detail.vue"
  - "apps/student-app/src/components/CustomTabBar.vue"
  - "apps/student-app/src/pages.json"

done_criteria:
  L0: "上述 5 个文件均存在"
  L1: "grep -r '#006a64' apps/student-app/src/pages/chat/index.vue apps/student-app/src/pages/apply/ apps/student-app/src/components/CustomTabBar.vue 返回 0 行（template/JS 中无裸写）"
  L2: "grep 'pages.json' -A2 中含注释标注同步来源（pages.json 允许保留字面量但须有注释）"
  L3: "视觉效果与修改前完全一致，主题色未偏移"

created_at: "2026-04-06"
---

# F-V5A-02: DEBT-V4-01 硬编码颜色清理

> template 和 JS 中不再有裸写 `#006a64`（pages.json 因 uni-app 限制保留字面量但添加注释）。

## 背景

spec-v4 遗留 DEBT-V4-01：5 处 `#006a64` 硬编码在 JS/template/JSON 中，无法直接受 SCSS 变量管控。

## 变更详情

**注意：`theme.scss` 中 `$primary-40: #006a64` 是定义源，不修改。**

| 文件 | 位置 | 当前 | 目标 |
|------|------|------|------|
| `pages/chat/index.vue` | line 38 | `color="#006a64"` | `color="var(--color-primary, #006a64)"` 或 SCSS `$primary` |
| `pages/apply/status.vue` | line 291 | `confirmColor: '#006a64'` | `confirmColor: 'var(--color-primary, #006a64)'` |
| `pages/apply/detail.vue` | line 321 | `confirmColor: '#006a64'` | `confirmColor: 'var(--color-primary, #006a64)'` |
| `components/CustomTabBar.vue` | line 11 | `color="#006a64"` | `color="var(--color-primary, #006a64)"` |
| `pages.json` | tabBar.selectedColor | `#006a64` | **保留字面量**，在 JSON 注释（若支持）或上方说明中标注"同步 theme.scss \$primary-40" |

**推荐策略**：在 `App.vue` 的 `<style>` 中声明 `:root { --color-primary: #006a64; }`，然后各处使用 `var(--color-primary, #006a64)`（带 fallback 保证兼容性）。

## 已知陷阱

- `pages.json` 是纯 JSON，不支持注释，直接保留字面量即可，不做修改
- uni-app 的 template 属性绑定需注意 CSS 变量在 rpx/px 场景下的兼容性
- **不要改 theme.scss**，那是变量定义源
- 本任务执行完后，f-v5a-03 才能执行（同文件 chat/index.vue）
