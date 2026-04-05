---
id: "fix-d-login-userinfo-mapping"
parent: "v4-chat-bugfix"
type: "bugfix"
status: "pending"
tier: "T2"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "apps/student-app/src/pages/login/index.vue"
  - "apps/student-app/src/api/auth.ts"

out_of_scope:
  - "apps/student-app/src/pages/apply/**"
  - "apps/student-app/src/utils/request.ts"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - "apps/student-app/src/pages/login/index.vue"
  - "apps/student-app/src/api/auth.ts"
  - "apps/student-app/src/pages/apply/status.vue"
  - "apps/student-app/src/utils/request.ts"

done_criteria:
  L0: "login/index.vue setUserInfo 使用兼容映射（id/username/realName 双字段兜底）；auth.ts 的 UserInfoResult 类型同步兼容"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "报告含运行时证据：登录后 userStore.userInfo.id 有值，不为 undefined"
  L3: "[H5] 登录后进入事务导办 -> 我的申请，不出现‘登录已过期’回跳"

depends_on: []
created_at: "2026-04-06 00:55:00"
---

# FIX-D：登录用户信息映射兼容修复（BUG-5）

> 完成后，登录态用户进入“我的申请”页面不再被误判未登录，申请查询链路使用有效 `applicantId`。

## 背景

当前登录映射仍按 RuoYi 旧字段读取 `userId/userName`，而 yx_user 版本返回 `id/username`，导致 `userStore.userInfo.id` 为空，后续接口触发 401 处理器回跳登录。

## 执行步骤

1. `auth.ts` 更新 `UserInfoResult` 接口，兼容 `id/userId`、`username/userName`、`realName/nickName`
2. `login/index.vue` 更新 `setUserInfo` 映射为兼容写法
3. 验证登录后 `userStore.userInfo.id` 为有效数值
4. 验证进入“我的申请”页面不触发 401 回跳

## 已知陷阱

- 仅修复字段映射，不在本任务扩展后端接口或权限配置
- 保持验证码开关逻辑不变
- 若映射修复后仍 401，按 RISK-2 记录并上报，不擅自跨 scope 处理
