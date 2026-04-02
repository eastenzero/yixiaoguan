<template>
  <div class="login-container">
    <div class="login-wrapper">
      <!-- 左侧品牌区 -->
      <div class="login-brand">
        <div class="brand-content">
          <div class="brand-logo">
            <el-icon :size="64" color="#fff"><School /></el-icon>
          </div>
          <h1 class="brand-title">学术智治系统</h1>
          <p class="brand-subtitle">Faculty Intelligence Platform</p>
          <div class="brand-features">
            <div class="feature-item">
              <el-icon><Check /></el-icon>
              <span>智能问答</span>
            </div>
            <div class="feature-item">
              <el-icon><Check /></el-icon>
              <span>高效审批</span>
            </div>
            <div class="feature-item">
              <el-icon><Check /></el-icon>
              <span>数据驱动</span>
            </div>
          </div>
        </div>
        <div class="brand-pattern"></div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="login-form-wrapper">
        <div class="login-form-content">
          <div class="form-header">
            <h2 class="form-title">欢迎登录</h2>
            <p class="form-subtitle">请使用您的账号密码登录系统</p>
          </div>

          <el-form
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            class="login-form"
            @keyup.enter="handleLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="loginForm.username"
                placeholder="请输入用户名"
                :prefix-icon="User"
                size="large"
                clearable
              />
            </el-form-item>

            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="请输入密码"
                :prefix-icon="Lock"
                size="large"
                show-password
                clearable
              />
            </el-form-item>

            <!-- 验证码 -->
            <el-form-item prop="captcha" v-if="captchaEnabled">
              <div class="captcha-row">
                <el-input
                  v-model="loginForm.captcha"
                  placeholder="请输入验证码"
                  :prefix-icon="CircleCheck"
                  size="large"
                  maxlength="4"
                  class="captcha-input"
                />
                <div class="captcha-img" @click="getCaptchaImage">
                  <img v-if="captchaUrl" :src="captchaUrl" alt="验证码" />
                  <el-icon v-else class="captcha-loading"><Loading /></el-icon>
                </div>
              </div>
            </el-form-item>

            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a class="forgot-link" @click="handleForgot">忘记密码？</a>
            </div>

            <el-button
              type="primary"
              size="large"
              class="login-btn"
              :loading="loading"
              @click="handleLogin"
            >
              登 录
            </el-button>
          </el-form>

          <div class="login-footer">
            <p>© 2024 学术智治系统 · 高等教育教务管理中台</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { User, Lock, CircleCheck, Loading, School, Check } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { login, getCaptcha } from '@/api/auth'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(false)
const captchaEnabled = ref(false)
const captchaUrl = ref('')
const uuid = ref('')

const loginForm = reactive({
  username: '',
  password: '',
  captcha: ''
})

const loginRules: FormRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 5, message: '密码长度不能少于5位', trigger: 'blur' }
  ],
  captcha: [{ required: true, message: '请输入验证码', trigger: 'blur' }]
}

const getCaptchaImage = async () => {
  try {
    const res = await getCaptcha()
    // 联调调试：把结果挂到 window 方便排查
    if (import.meta.env.DEV) {
      (window as any).__captchaResult = res
    }
    if (res.captchaEnabled) {
      captchaEnabled.value = true
      captchaUrl.value = 'data:image/gif;base64,' + (res.img ?? '')
      uuid.value = res.uuid ?? ''
    } else {
      captchaEnabled.value = false
    }
  } catch (error: any) {
    console.error('获取验证码失败', error)
    if (import.meta.env.DEV) {
      window.__captchaErrorDetail = {
        message: error?.message,
        name: error?.name,
        stack: error?.stack,
        string: String(error),
        json: JSON.stringify(error)
      }
    }
  }
}

const handleLogin = async () => {
  if (!loginFormRef.value) return

  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const loginData = {
          username: loginForm.username,
          password: loginForm.password,
          ...(captchaEnabled.value ? { code: loginForm.captcha, uuid: uuid.value } : {})
        }

        // 开发环境日志：打印请求体以便联调排查
        if (import.meta.env.DEV) {
          console.log('[LoginView] login payload:', JSON.stringify(loginData))
        }

        const res = await login(loginData)
        
        if (res.code === 200) {
          userStore.setToken(res.token)
          ElMessage.success('登录成功')
          router.push('/dashboard')
        } else {
          ElMessage.error(res.msg || '登录失败')
          if (captchaEnabled.value) getCaptchaImage()
        }
      } catch (error: any) {
        ElMessage.error(error.message || '登录失败，请稍后重试')
        if (captchaEnabled.value) getCaptchaImage()
      } finally {
        loading.value = false
      }
    }
  })
}

const handleForgot = () => {
  ElMessage.info('请联系管理员重置密码')
}

onMounted(() => {
  getCaptchaImage()
})
</script>

<style scoped lang="scss">
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 50%, #99F6E4 100%);
  padding: 20px;
}

.login-wrapper {
  display: flex;
  width: 100%;
  max-width: 1000px;
  min-height: 620px;
  background: #fff;
  border-radius: 24px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

// 左侧品牌区
.login-brand {
  flex: 1;
  background: linear-gradient(135deg, #0F766E 0%, #0D9488 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  padding: 60px 40px;
  color: #fff;

  .brand-content {
    text-align: center;
    z-index: 1;
  }

  .brand-logo {
    width: 100px;
    height: 100px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 28px;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .brand-title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 8px;
    letter-spacing: 2px;
  }

  .brand-subtitle {
    font-size: 14px;
    opacity: 0.85;
    margin-bottom: 40px;
    font-weight: 400;
    letter-spacing: 1px;
  }

  .brand-features {
    display: flex;
    flex-direction: column;
    gap: 16px;
    text-align: left;
    max-width: 200px;
    margin: 0 auto;

    .feature-item {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 15px;
      opacity: 0.9;

      .el-icon {
        width: 22px;
        height: 22px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
      }
    }
  }

  .brand-pattern {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 200px;
    background: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.06'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  }
}

// 右侧登录表单
.login-form-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 50px;
  background: #fff;
}

.login-form-content {
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
}

.form-header {
  margin-bottom: 32px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.form-subtitle {
  font-size: 14px;
  color: var(--text-secondary);
}

.login-form {
  :deep(.el-input__wrapper) {
    border-radius: 12px;
    box-shadow: 0 0 0 1px #E2E8F0 inset;
    padding: 4px 16px;
    height: 52px;

    &.is-focus {
      box-shadow: 0 0 0 1px var(--primary-color) inset !important;
    }
  }

  :deep(.el-input__inner) {
    font-size: 15px;
  }

  :deep(.el-input__icon) {
    color: var(--text-tertiary);
    font-size: 18px;
  }

  :deep(.el-form-item) {
    margin-bottom: 20px;
  }
}

.captcha-row {
  display: flex;
  gap: 12px;

  .captcha-input {
    flex: 1;
  }

  .captcha-img {
    width: 120px;
    height: 52px;
    border-radius: 12px;
    overflow: hidden;
    cursor: pointer;
    background: #F8FAFC;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #E2E8F0;

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .captcha-loading {
      color: var(--text-tertiary);
      animation: rotate 1s linear infinite;
    }
  }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.form-options {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 8px 0 24px;

  :deep(.el-checkbox__label) {
    font-size: 14px;
    color: var(--text-secondary);
  }

  .forgot-link {
    font-size: 14px;
    color: var(--primary-color);
    cursor: pointer;
    transition: color 0.2s;
    font-weight: 500;

    &:hover {
      color: var(--primary-dark);
    }
  }
}

.login-btn {
  width: 100%;
  height: 52px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border: none;
  box-shadow: 0 4px 16px rgba(13, 148, 136, 0.35);
  transition: all 0.3s;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(13, 148, 136, 0.45);
  }
}

.login-footer {
  margin-top: 48px;
  text-align: center;
  font-size: 12px;
  color: var(--text-tertiary);
}

// 响应式
@media (max-width: 768px) {
  .login-brand {
    display: none;
  }

  .login-form-wrapper {
    padding: 40px 30px;
  }
}
</style>
