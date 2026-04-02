<template>
  <view class="login-page">
    <view class="login-header">
      <text class="app-title">医小管</text>
      <text class="app-subtitle">智慧校园服务平台</text>
    </view>
    
    <view class="login-form">
      <view class="form-item">
        <text class="label">学号</text>
        <input 
          class="input" 
          type="text" 
          v-model="form.username" 
          placeholder="请输入学号"
          maxlength="20"
        />
      </view>
      
      <view class="form-item">
        <text class="label">密码</text>
        <input 
          class="input" 
          type="password" 
          v-model="form.password" 
          placeholder="请输入密码"
          maxlength="20"
        />
      </view>
      
      <!-- 验证码区域：只在后端开启验证码时显示 -->
      <view v-if="captchaEnabled" class="form-item captcha-item">
        <text class="label">验证码</text>
        <view class="captcha-wrap">
          <input 
            class="input captcha-input" 
            type="text" 
            v-model="form.code" 
            placeholder="请输入验证码"
            maxlength="4"
          />
          <image 
            v-if="captchaUrl" 
            class="captcha-img" 
            :src="captchaUrl" 
            mode="aspectFit"
            @click="refreshCaptcha"
          />
          <view v-else class="captcha-placeholder" @click="refreshCaptcha">
            <text>点击刷新</text>
          </view>
        </view>
      </view>
      
      <button 
        class="login-btn" 
        :class="{ loading: isLoading }"
        :disabled="isLoading"
        @click="handleLogin"
      >
        {{ isLoading ? '登录中...' : '登录' }}
      </button>
    </view>
    
    <view class="login-footer">
      <text class="hint">首次登录请使用默认密码，登录后请修改</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getCaptcha, login, getUserInfo } from '@/api/auth'

const userStore = useUserStore()

// 表单数据
const form = reactive({
  username: '',
  password: '',
  code: '',
  uuid: ''
})

// 验证码图片 URL
const captchaUrl = ref('')
const captchaEnabled = ref(true)  // 后端可能关闭验证码
const isLoading = ref(false)

// 刷新验证码
const refreshCaptcha = async () => {
  try {
    const res = await getCaptcha()
    captchaEnabled.value = res.captchaEnabled !== false  // 明确关闭才为 false
    if (captchaEnabled.value) {
      form.uuid = res.uuid || ''
      // RuoYi 返回的 img 可能包含也可能不包含 data: 前缀
      const imgData = res.img || ''
      captchaUrl.value = imgData.startsWith('data:') ? imgData : `data:image/png;base64,${imgData}`
    }
  } catch (error) {
    console.error('获取验证码失败', error)
    // 接口失败时让用户能看到占位，点击重试
    captchaEnabled.value = true
    captchaUrl.value = ''
  }
}

// 表单验证
const validateForm = (): boolean => {
  if (!form.username.trim()) {
    uni.showToast({ title: '请输入学号', icon: 'none' })
    return false
  }
  if (!form.password) {
    uni.showToast({ title: '请输入密码', icon: 'none' })
    return false
  }
  if (captchaEnabled.value && !form.code.trim()) {
    uni.showToast({ title: '请输入验证码', icon: 'none' })
    return false
  }
  return true
}

// 登录处理
const handleLogin = async () => {
  if (!validateForm()) return
  
  isLoading.value = true
  try {
    // 1. 登录获取 token
    const loginRes = await login({
      username: form.username.trim(),
      password: form.password,
      code: form.code.trim(),
      uuid: form.uuid
    })
    
    // 2. 保存 token
    userStore.setToken(loginRes.token)
    
    // 3. 获取用户信息，将 RuoYi 字段映射为项目 UserInfo 格式
    const userInfoRes = await getUserInfo(loginRes.token)
    const ruoyiUser = userInfoRes.user
    userStore.setUserInfo({
      id: ruoyiUser.userId,
      username: ruoyiUser.userName,
      realName: ruoyiUser.nickName || ruoyiUser.userName,
      nickName: ruoyiUser.nickName,
      avatarUrl: ruoyiUser.avatar,
      email: ruoyiUser.email,
      phone: ruoyiUser.phonenumber,
      roles: userInfoRes.roles,
      permissions: userInfoRes.permissions
    })
    
    // 4. 登录成功提示
    uni.showToast({
      title: '登录成功',
      icon: 'success',
      duration: 1500
    })
    
    // 5. 跳转到首页
    setTimeout(() => {
      uni.switchTab({ url: '/pages/home/index' })
    }, 1500)
    
  } catch (error) {
    console.error('登录失败', error)
    // 刷新验证码
    refreshCaptcha()
    form.code = ''
  } finally {
    isLoading.value = false
  }
}

// 页面加载时获取验证码
onMounted(() => {
  refreshCaptcha()
})
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #00685f 0%, #008c7f 100%);
  padding: 80rpx 40rpx;
  box-sizing: border-box;
}

.login-header {
  text-align: center;
  margin-bottom: 80rpx;
  
  .app-title {
    display: block;
    font-size: 56rpx;
    font-weight: bold;
    color: #ffffff;
    margin-bottom: 16rpx;
  }
  
  .app-subtitle {
    display: block;
    font-size: 28rpx;
    color: rgba(255, 255, 255, 0.8);
  }
}

.login-form {
  background: #ffffff;
  border-radius: 36rpx;
  padding: 60rpx 40rpx;
  box-shadow: 0 8rpx 40rpx rgba(0, 0, 0, 0.12);
}

.form-item {
  margin-bottom: 40rpx;
  
  &:last-child {
    margin-bottom: 0;
  }
  
  .label {
    display: block;
    font-size: 28rpx;
    color: #333333;
    margin-bottom: 16rpx;
    font-weight: 500;
  }
  
  .input {
    width: 100%;
    height: 88rpx;
    background: rgba(0,106,100,0.06);
    border-radius: 12rpx;
    padding: 0 24rpx;
    font-size: 28rpx;
    color: #333333;
    box-sizing: border-box;
    border: none;
    outline: none;
    transition: box-shadow 0.2s ease;
    
    &::placeholder {
      color: #999999;
    }

    &:focus {
      box-shadow: 0 0 0 2px rgba(0,168,150,0.2);
    }
  }
}

.captcha-item {
  .captcha-wrap {
    display: flex;
    align-items: center;
    gap: 20rpx;
  }
  
  .captcha-input {
    flex: 1;
  }
  
  .captcha-img {
    width: 200rpx;
    height: 88rpx;
    border-radius: 12rpx;
    background: #f5f5f5;
  }
  
  .captcha-placeholder {
    width: 200rpx;
    height: 88rpx;
    border-radius: 12rpx;
    background: #f5f5f5;
    display: flex;
    align-items: center;
    justify-content: center;
    
    text {
      font-size: 24rpx;
      color: #666666;
    }
  }
}

.login-btn {
  width: 100%;
  height: 96rpx;
  background: #006a64;
  color: #ffffff;
  font-size: 32rpx;
  font-weight: 500;
  border-radius: 48rpx;
  margin-top: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  
  &:active {
    opacity: 0.9;
  }
  
  &.loading {
    opacity: 0.7;
  }
  
  &[disabled] {
    background: #cccccc;
  }
}

.login-footer {
  margin-top: 40rpx;
  text-align: center;
  
  .hint {
    font-size: 24rpx;
    color: rgba(255, 255, 255, 0.7);
  }
}
</style>
