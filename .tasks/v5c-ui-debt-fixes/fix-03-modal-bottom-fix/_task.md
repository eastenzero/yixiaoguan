---
id: "fix-03"
parent: "v5c-ui-debt-fixes"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

depends_on: ["fix-02"]

scope:
  - "apps/student-app/src/pages/chat/index.vue"
out_of_scope:
  - "apps/student-app/src/styles/**"
  - "apps/student-app/src/api/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "apps/student-app/src/pages/chat/index.vue 存在"
  L1: "grep 'safe-area-inset-bottom\\|padding-bottom.*60' apps/student-app/src/pages/chat/index.vue 有结果（底部安全区已处理）"
  L2: "弹层 overlay 使用 fixed 定位，z-index 覆盖导航栏"
  L3: "手机屏幕上弹层底部按钮完全可见可点击，不与底部导航栏重叠"

created_at: "2026-04-06"
---

# FIX-03: 参考摘要弹层底部按钮防遮挡

> 参考资料摘要弹层底部"查看详细资料"和"知道了"按钮完全可见，不被底部导航栏遮挡。

## 背景

点击参考资料后弹出的摘要弹层，底部按钮在有导航栏的手机屏幕上被遮挡，用户无法点击。

## 变更详情

- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: 参考资料摘要弹层的 overlay/container 样式
- **修复方案**：
  1. 弹层 overlay 使用 `position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 9999`，确保覆盖导航栏
  2. 弹层内容区底部增加安全距离：
     ```scss
     padding-bottom: calc(env(safe-area-inset-bottom) + 60rpx);
     ```
  3. 或将按钮区域固定在弹层底部，内容区独立滚动

## 已知陷阱

- **必须在 fix-02 完成后执行**（同文件 chat/index.vue）
- uni-app H5 中 `env(safe-area-inset-bottom)` 支持 iOS 刘海屏，兼容性良好
- z-index 需足够高（>= 9999）以覆盖 CustomTabBar
- 只改弹层样式，不改弹层的显示/隐藏逻辑和数据
