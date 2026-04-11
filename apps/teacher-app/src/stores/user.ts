import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/types/api'

// Token 存储键名（与若依后端保持一致）
const TOKEN_KEY = 'Admin-Token'
const USER_INFO_KEY = 'User-Info'

export const useUserStore = defineStore('user', () => {
  // ===== State =====
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  
  // ===== Getters =====
  const isLoggedIn = computed(() => !!token.value)
  
  // ===== Actions =====
  
  /**
   * 初始化（从 Storage 读取）
   */
  const init = () => {
    try {
      const storedToken = uni.getStorageSync(TOKEN_KEY)
      const storedUserInfo = uni.getStorageSync(USER_INFO_KEY)
      
      if (storedToken) {
        token.value = storedToken
      }
      if (storedUserInfo) {
        userInfo.value = JSON.parse(storedUserInfo)
      }
    } catch (error) {
      console.error('[UserStore] 初始化失败', error)
    }
  }
  
  /**
   * 设置 Token
   */
  const setToken = (newToken: string) => {
    token.value = newToken
    try {
      uni.setStorageSync(TOKEN_KEY, newToken)
    } catch (error) {
      console.error('[UserStore] 保存 Token 失败', error)
    }
  }
  
  /**
   * 设置用户信息
   */
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    try {
      uni.setStorageSync(USER_INFO_KEY, JSON.stringify(info))
    } catch (error) {
      console.error('[UserStore] 保存用户信息失败', error)
    }
  }
  
  /**
   * 清除登录状态
   */
  const clearAuth = () => {
    token.value = ''
    userInfo.value = null
    try {
      uni.removeStorageSync(TOKEN_KEY)
      uni.removeStorageSync(USER_INFO_KEY)
    } catch (error) {
      console.error('[UserStore] 清除登录状态失败', error)
    }
  }
  
  /**
   * 退出登录
   */
  const logout = () => {
    clearAuth()
  }
  
  return {
    token,
    userInfo,
    isLoggedIn,
    init,
    setToken,
    setUserInfo,
    clearAuth,
    logout
  }
})
