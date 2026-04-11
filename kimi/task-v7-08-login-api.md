# 任务: F-V7-08 登录 API 对接

## 目标状态
教师端登录页可通过真实 API 完成：获取验证码 → 输入凭据 → 登录 → 跳转工作台 → 用户信息持久化。工作台页面显示真实用户名。

## 背景
- `apps/teacher-app/src/api/auth.ts` 已从 student-app 复制，包含 getCaptcha / login / getUserInfo / logout 函数
- `apps/teacher-app/src/utils/request.ts` 已包含统一请求封装（JWT Token 注入）
- `apps/teacher-app/src/stores/user.ts` 已包含 token/userInfo 管理
- 后端 API 在 `http://192.168.100.165:8080`，vite proxy 已配置
- 若依认证流程: getCaptchaImage → login(username, password, code, uuid) → getInfo

## 执行步骤

### 步骤 1: 修改 login/index.vue — 接入真实登录流程

读取现有文件: `apps/teacher-app/src/pages/login/index.vue`
读取参考: `apps/teacher-app/src/api/auth.ts`
读取参考: `apps/teacher-app/src/stores/user.ts`

在 `<script setup>` 中增加:

1. 导入:
```typescript
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getCaptcha, login as loginApi, getUserInfo } from '@/api/auth'
import { useUserStore } from '@/stores/user'
```

2. 状态变量:
```typescript
const userStore = useUserStore()
const username = ref('')
const password = ref('')
const captchaCode = ref('')
const captchaImg = ref('')
const captchaUuid = ref('')
const loading = ref(false)
const showPassword = ref(false)
```

3. 获取验证码函数:
```typescript
const refreshCaptcha = async () => {
  try {
    const res = await getCaptcha()
    captchaImg.value = 'data:image/png;base64,' + res.img
    captchaUuid.value = res.uuid
  } catch (e) {
    console.error('获取验证码失败', e)
  }
}
```

4. 登录函数:
```typescript
const handleLogin = async () => {
  if (!username.value || !password.value) {
    uni.showToast({ title: '请输入账号和密码', icon: 'none' })
    return
  }
  if (!captchaCode.value) {
    uni.showToast({ title: '请输入验证码', icon: 'none' })
    return
  }
  loading.value = true
  try {
    const loginRes = await loginApi({
      username: username.value,
      password: password.value,
      code: captchaCode.value,
      uuid: captchaUuid.value
    })
    userStore.setToken(loginRes.token)
    
    // 获取用户信息
    const userInfoRes = await getUserInfo()
    userStore.setUserInfo(userInfoRes.user)
    
    uni.switchTab({ url: '/pages/dashboard/index' })
  } catch (e: any) {
    uni.showToast({ title: e?.message || '登录失败', icon: 'none' })
    refreshCaptcha()
  } finally {
    loading.value = false
  }
}
```

5. 生命周期:
```typescript
onMounted(() => {
  refreshCaptcha()
})
onShow(() => {
  refreshCaptcha()
})
```

6. 在模板中:
- 在密码输入框下方，添加验证码区域:
  - 左侧: 验证码输入框（和用户名/密码同样的 ghost 风格）
  - 右侧: 验证码图片（`<image :src="captchaImg" mode="aspectFit" />`），点击刷新
- 登录按钮: 绑定 `@click="handleLogin"`，loading 时显示"登录中..."
- 移除原有的 `form @submit.prevent`（UniApp 不支持），改用 `@click`

7. 验证码区域样式:
```scss
.captcha-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.captcha-input {
  flex: 1;
}
.captcha-image {
  width: 120px;
  height: 56px;
  border-radius: 12px;
  background: $surface-container-low;
}
```

### 步骤 2: 修改 dashboard/index.vue — 显示真实用户名

读取现有文件: `apps/teacher-app/src/pages/dashboard/index.vue`

在 `<script setup>` 中增加:
```typescript
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const userStore = useUserStore()
const displayName = computed(() => {
  const info = userStore.userInfo
  if (info) {
    return info.nickName || info.realName || info.username || '老师'
  }
  return '老师'
})
```

在模板中:
- 将欢迎语中硬编码的 "梁老师" 替换为 `{{ displayName }}`
- 例如: `早上好，{{ displayName }} 👋`

### 步骤 3: 修改 profile/index.vue — 显示真实用户信息

读取现有文件: `apps/teacher-app/src/pages/profile/index.vue`

在 `<script setup>` 中增加:
```typescript
import { useUserStore } from '@/stores/user'
import { computed } from 'vue'

const userStore = useUserStore()
const userName = computed(() => userStore.userInfo?.nickName || userStore.userInfo?.realName || '教师')
const department = computed(() => userStore.userInfo?.department || '未知院系')
const userId = computed(() => userStore.userInfo?.username || 'N/A')
```

在模板中:
- 姓名处替换为 `{{ userName }}`
- 院系处替换为 `{{ department }}`
- 工号处替换为 `ID: {{ userId }}`

退出登录函数增加清除逻辑:
```typescript
const handleLogout = () => {
  userStore.clearAuth()
  uni.reLaunch({ url: '/pages/login/index' })
}
```

## 允许修改的文件
- `apps/teacher-app/src/pages/login/index.vue`（修改 - 增加 API 调用）
- `apps/teacher-app/src/pages/dashboard/index.vue`（修改 - 显示真实用户名）
- `apps/teacher-app/src/pages/profile/index.vue`（修改 - 显示真实用户信息+退出逻辑）

## 禁止修改的文件
- `apps/teacher-app/src/api/auth.ts`（已从 student-app 复制，不改）
- `apps/teacher-app/src/utils/request.ts`（不改）
- `apps/teacher-app/src/stores/user.ts`（不改）
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages.json`
- `apps/teacher-app/package.json`
- `apps/teacher-app/vite.config.ts`
- `apps/student-app/**`
- `services/**`

## 硬约束
- 不改已有的 auth.ts / request.ts / user.ts
- 验证码图片使用 base64 `data:image/png;base64,` 前缀
- 登录成功后必须同时存储 token 和 userInfo
- 退出登录必须清除 auth 再 reLaunch 到 login
- UniApp 中 form submit 不支持 prevent，用 @click 代替

## 完成标准
- L0: login/index.vue 导入了 auth.ts 的 getCaptcha 和 login 函数
- L1: login 页面包含验证码输入框和验证码图片区域
- L2: dashboard 和 profile 使用 userStore 显示动态用户名（非硬编码）

## 报告
写入: `.tasks/v7-teacher-app/f-v7-08-login-api/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
