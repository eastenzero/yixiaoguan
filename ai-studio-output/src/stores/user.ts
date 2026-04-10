import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface UserInfo {
  id: number | string
  username: string
  realName: string
  nickName: string
  avatarUrl?: string
  email?: string
  phone?: string
  roles?: string[]
  permissions?: string[]
  deptName?: string
}

// ⚠️ 不可修改 - Storage Key 与持久化逻辑
const TOKEN_KEY = 'Admin-Token'
const USER_INFO_KEY = 'User-Info'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  
  const isLoggedIn = computed(() => !!token.value)
  
  const init = () => {
    const storedToken = uni.getStorageSync(TOKEN_KEY)
    const storedUserInfo = uni.getStorageSync(USER_INFO_KEY)
    if (storedToken) token.value = storedToken
    if (storedUserInfo) userInfo.value = JSON.parse(storedUserInfo)
  }
  
  const setToken = (newToken: string) => {
    token.value = newToken
    uni.setStorageSync(TOKEN_KEY, newToken)
  }
  
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    uni.setStorageSync(USER_INFO_KEY, JSON.stringify(info))
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync(TOKEN_KEY)
    uni.removeStorageSync(USER_INFO_KEY)
  }
  
  return { token, userInfo, isLoggedIn, init, setToken, setUserInfo, logout }
})
