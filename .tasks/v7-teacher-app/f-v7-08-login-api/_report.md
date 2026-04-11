# F-V7-08 登录API对接 - 执行报告

## STEP-PLAN
1. 修改 `login/index.vue` — 接入真实登录流程
   - 导入必要的API函数和store
   - 添加验证码状态变量
   - 实现获取验证码和登录逻辑
   - 添加验证码UI区域
   
2. 修改 `dashboard/index.vue` — 显示真实用户名
   - 导入 userStore
   - 使用 computed 计算显示名称
   - 替换硬编码的"梁老师"

3. 修改 `profile/index.vue` — 显示真实用户信息
   - 导入 userStore
   - 使用 computed 计算用户名/院系/工号
   - 更新退出登录逻辑，添加 clearAuth

## STEP-EXECUTED

### Step 1: login/index.vue 修改完成
- ✅ 导入: `getCaptcha`, `login as loginApi`, `getUserInfo`, `useUserStore`
- ✅ 状态变量: `userStore`, `captchaCode`, `captchaImg`, `captchaUuid`, `loading`
- ✅ 函数: `refreshCaptcha()` - 获取验证码并设置 base64 图片
- ✅ 函数: `handleLogin()` - 完整登录流程（验证→登录→获取用户信息→跳转）
- ✅ 生命周期: `onMounted`, `onShow` 均调用 `refreshCaptcha()`
- ✅ 模板: 添加验证码输入框和图片区域，支持点击刷新
- ✅ 样式: 添加 `.captcha-row`, `.captcha-input`, `.captcha-image` 样式
- ✅ 移除原有的 `form @submit.prevent`，改用 `@click`

### Step 2: dashboard/index.vue 修改完成
- ✅ 导入: `useUserStore`, `computed`
- ✅ 创建 `displayName` computed，优先使用 nickName > realName > username > '老师'
- ✅ 替换欢迎语: `早上好，{{ displayName }} 👋`

### Step 3: profile/index.vue 修改完成
- ✅ 导入: `useUserStore`, `computed`
- ✅ 创建 `userName`, `department`, `userId` computed
- ✅ 模板替换: 姓名/院系/工号均使用动态数据
- ✅ 退出登录: 添加 `userStore.clearAuth()` 清除认证状态

## STEP-CHECK

### L0 - 导入检查
- ✅ `login/index.vue` 正确导入了 `getCaptcha` 和 `login` 函数
```typescript
import { getCaptcha, login as loginApi, getUserInfo } from '@/api/auth'
```

### L1 - 验证码区域
- ✅ 登录页面包含验证码输入框和验证码图片区域
- ✅ 验证码图片使用 base64 `data:image/png;base64,` 前缀
- ✅ 点击验证码图片可刷新

### L2 - 动态用户名
- ✅ dashboard 页面显示动态用户名（从 userStore.userInfo 获取）
- ✅ profile 页面显示动态用户信息（用户名、院系、工号）
- ✅ 退出登录后清除认证状态并跳转到登录页

### 硬约束验证
- ✅ 未修改 `auth.ts` / `request.ts` / `user.ts`
- ✅ 登录成功后同时存储 token 和 userInfo
- ✅ 退出登录使用 `clearAuth()` 清除状态后 `reLaunch` 到 login

## BLOCKERS
无

---
执行时间: 2026-04-11
