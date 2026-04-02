import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import Cookies from 'js-cookie'

// Token 键名（与若依后端保持一致）
const TOKEN_KEY = 'Admin-Token'

export interface UserInfo {
  userId: number
  userName: string
  nickName: string
  avatar?: string
  email?: string
  phonenumber?: string
  deptName?: string
  roles?: string[]
  permissions?: string[]
}

export const useUserStore = defineStore('user', () => {
  // State
  const token = ref<string>(Cookies.get(TOKEN_KEY) || '')
  const userInfo = ref<UserInfo | null>(null)
  const isLoggedIn = computed(() => !!token.value)

  // Actions
  const setToken = (newToken: string) => {
    token.value = newToken
    Cookies.set(TOKEN_KEY, newToken, { expires: 7 })
  }

  const clearToken = () => {
    token.value = ''
    userInfo.value = null
    Cookies.remove(TOKEN_KEY)
  }

  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }

  const logout = () => {
    clearToken()
    userInfo.value = null
  }

  return {
    token,
    userInfo,
    isLoggedIn,
    setToken,
    clearToken,
    setUserInfo,
    logout
  }
})
