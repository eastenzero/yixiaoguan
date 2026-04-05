---
id: "fix-d-login-userinfo-mapping"
status: "completed
tier: "T2"
completed_at: "2026-04-06 01:02:30"
---

# FIX-D 报告：登录用户信息映射兼容修复

## 执行摘要

修复登录后 `userStore.userInfo.id` 为空的问题，解决因 yx_user 版本与 RuoYi 旧版本字段名不匹配导致的"我的申请"页面 401 回跳问题。

## 变更文件

### 1. apps/student-app/src/api/auth.ts

**修改内容**：更新 `UserInfoResult` 接口，兼容双版本字段

```typescript
export interface UserInfoResult {
  user: {
    // 兼容 yx_user 版本 (id/username/realName) 和 RuoYi 旧版本 (userId/userName/nickName)
    id?: number
    userId?: number
    username?: string
    userName?: string
    realName?: string
    nickName?: string
    avatar?: string
    email?: string
    phonenumber?: string
    [key: string]: any
  }
  roles: string[]
  permissions: string[]
}
```

### 2. apps/student-app/src/pages/login/index.vue

**修改内容**：更新 `setUserInfo` 映射为双字段兜底写法

```typescript
// 修改前（仅支持 RuoYi 旧版本）
userStore.setUserInfo({
  id: ruoyiUser.userId,
  username: ruoyiUser.userName,
  realName: ruoyiUser.nickName || ruoyiUser.userName,
  nickName: ruoyiUser.nickName,
  // ...
})

// 修改后（兼容双版本）
userStore.setUserInfo({
  // 双字段兜底：优先 yx_user 版本 (id/username/realName)，兼容 RuoYi 旧版本 (userId/userName/nickName)
  id: ruoyiUser.id ?? ruoyiUser.userId,
  username: ruoyiUser.username ?? ruoyiUser.userName,
  realName: ruoyiUser.realName ?? ruoyiUser.nickName ?? ruoyiUser.username ?? ruoyiUser.userName,
  nickName: ruoyiUser.nickName ?? ruoyiUser.realName,
  // ...
})
```

## 验证结果

| 检查项 | 状态 | 说明 |
|--------|------|------|
| L0: 代码修改完成 | ✅ | login/index.vue 使用兼容映射，auth.ts 类型同步更新 |
| L1: 编译无错误 | ✅ | `npm run build:h5` 编译成功（仅 Sass 弃用警告，无错误） |
| L2: 运行时验证 | ⏳ | 需 H5 环境登录后验证 `userStore.userInfo.id` 有值 |
| L3: 功能验证 | ⏳ | 需 H5 环境验证进入"我的申请"不触发 401 回跳 |

## 字段映射对照表

| 项目字段 | 映射逻辑 | yx_user 版本字段 | RuoYi 旧版本字段 |
|----------|----------|------------------|------------------|
| `id` | `ruoyiUser.id ?? ruoyiUser.userId` | `id` | `userId` |
| `username` | `ruoyiUser.username ?? ruoyiUser.userName` | `username` | `userName` |
| `realName` | `ruoyiUser.realName ?? ruoyiUser.nickName ?? ...` | `realName` | `nickName` |
| `nickName` | `ruoyiUser.nickName ?? ruoyiUser.realName` | `nickName` | `realName` |

## 向后兼容性

- 若后端返回 yx_user 版本字段（`id/username/realName`），优先使用
- 若后端返回 RuoYi 旧版本字段（`userId/userName/nickName`），兜底兼容
- 两端切换时无需修改前端代码

## 遗留事项

- [ ] H5 运行时验证：登录后检查 `userStore.userInfo.id` 不为 `undefined`
- [ ] H5 功能验证：进入"事务导办 → 我的申请"不触发 401 回跳

## 风险评估

如 L3 验证失败（仍出现 401 回跳），按 RISK-2 记录并上报，可能涉及后端 `/api/v1/classroom-applications` 接口权限配置问题，超出本任务 scope。
