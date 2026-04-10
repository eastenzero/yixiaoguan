<template>
  <view class="login-page">
    <view class="login-card">
      <view class="header">
        <image class="logo" src="/static/logo.png" mode="aspectFit" />
        <text class="title">医小管</text>
        <text class="subtitle">智慧校园服务平台</text>
      </view>

      <view class="form">
        <view class="input-group">
          <input class="input" v-model="form.username" placeholder="请输入学号" />
        </view>
        <view class="input-group">
          <input class="input" v-model="form.password" type="password" placeholder="请输入密码" />
        </view>
        <view class="input-group captcha-group">
          <input class="input" v-model="form.code" placeholder="请输入验证码" />
          <image class="captcha-img" :src="captchaUrl" @click="refreshCaptcha" mode="aspectFit" />
        </view>

        <button class="login-btn" @click="handleLogin">登录</button>
      </view>

      <view class="footer">
        <text class="hint">初始密码与学号相同</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { login, getCaptcha, getUserInfo } from '@/api/auth'

const userStore = useUserStore()

const form = ref({
  username: '',
  password: '',
  code: '',
  uuid: ''
})

const captchaUrl = ref('')

const refreshCaptcha = async () => {
  try {
    const res = await getCaptcha()
    captchaUrl.value = 'data:image/gif;base64,' + res.img
    form.value.uuid = res.uuid
  } catch (error) {
    console.error('Failed to get captcha', error)
  }
}

onMounted(() => {
  refreshCaptcha()
})

// ⚠️ 不可修改 - 登录流程
const handleLogin = async () => {
  // 1. 登录获取 token
  const loginRes = await login({
    username: form.value.username.trim(),
    password: form.value.password,
    code: form.value.code.trim(),
    uuid: form.value.uuid
  })
  
  // 2. 保存 token
  userStore.setToken(loginRes.token)
  
  // 3. 获取用户信息（兼容字段映射）
  const userInfoRes = await getUserInfo(loginRes.token)
  const ruoyiUser = userInfoRes.user
  userStore.setUserInfo({
    id: ruoyiUser.id ?? ruoyiUser.userId,
    username: ruoyiUser.username ?? ruoyiUser.userName,
    realName: ruoyiUser.realName ?? ruoyiUser.nickName ?? ruoyiUser.username ?? ruoyiUser.userName,
    nickName: ruoyiUser.nickName ?? ruoyiUser.realName,
    avatarUrl: ruoyiUser.avatar,
    email: ruoyiUser.email,
    phone: ruoyiUser.phonenumber,
    roles: userInfoRes.roles,
    permissions: userInfoRes.permissions
  })
  
  // 4. 跳转首页
  uni.switchTab({ url: '/pages/home/index' })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  padding: $spacing-md;
}

.login-card {
  width: 100%;
  max-width: 600rpx;
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-xl $spacing-lg;
  box-shadow: $elevation-3;
  animation: $animation-fade-in-up;
}

.header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: $spacing-xl;

  .logo {
    width: 120rpx;
    height: 120rpx;
    margin-bottom: $spacing-sm;
  }

  .title {
    font-size: 48rpx;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: $spacing-xs;
  }

  .subtitle {
    font-size: 28rpx;
    color: $text-secondary;
  }
}

.form {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;

  .input-group {
    width: 100%;
  }

  .input {
    width: 100%;
    height: 88rpx;
    background: $bg-secondary;
    border-radius: $radius-md;
    padding: 0 $spacing-md;
    font-size: 28rpx;
    color: $text-primary;
    box-sizing: border-box;
  }

  .captcha-group {
    display: flex;
    gap: $spacing-sm;

    .input {
      flex: 1;
    }

    .captcha-img {
      width: 200rpx;
      height: 88rpx;
      border-radius: $radius-md;
      background: $bg-secondary;
    }
  }

  .login-btn {
    width: 100%;
    height: 88rpx;
    border-radius: $radius-pill;
    background: linear-gradient(90deg, $primary-40 0%, $primary-50 100%);
    color: $text-inverse;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: $spacing-md;
    box-shadow: $elevation-2;
    transition: $transition-base;

    &:active {
      transform: scale(0.96);
    }
  }
}

.footer {
  margin-top: $spacing-lg;
  text-align: center;

  .hint {
    font-size: 24rpx;
    color: $text-tertiary;
  }
}
</style>
