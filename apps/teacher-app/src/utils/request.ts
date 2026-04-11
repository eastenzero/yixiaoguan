import { useUserStore } from '@/stores/user'
import type { ApiResponse } from '@/types/api'

// ===== 配置区 =====
const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''
const REQUEST_TIMEOUT = 30000
const TOKEN_PREFIX = 'Bearer '

/**
 * 统一请求封装（基于 uni.request）
 */
export function request<T = any>(options: UniApp.RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const userStore = useUserStore()
    
    // 构建完整 URL
    let url = options.url
    if (url.startsWith('/')) {
      url = BASE_URL + url
    }
    
    // 请求配置
    const requestOptions: UniApp.RequestOptions = {
      ...options,
      url,
      timeout: options.timeout || REQUEST_TIMEOUT,
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      success: (res) => {
        handleResponse(res, resolve, reject, userStore)
      },
      fail: (err) => {
        handleError(err, reject)
      }
    }
    
    // 注入 JWT Token
    if (userStore.token) {
      const token = userStore.token.startsWith('Bearer') 
        ? userStore.token 
        : `${TOKEN_PREFIX}${userStore.token}`
      requestOptions.header = {
        ...requestOptions.header,
        'Authorization': token
      }
    }
    
    uni.request(requestOptions)
  })
}

/**
 * 处理响应
 */
function handleResponse<T>(
  res: UniApp.RequestSuccessCallbackResult, 
  resolve: (value: T) => void, 
  reject: (reason: any) => void,
  userStore: ReturnType<typeof useUserStore>
): void {
  const data = res.data as ApiResponse<T>
  
  // HTTP 错误处理
  if (res.statusCode < 200 || res.statusCode >= 300) {
    uni.showToast({
      title: `请求失败(${res.statusCode})`,
      icon: 'none'
    })
    reject(new Error(`HTTP ${res.statusCode}`))
    return
  }
  
  // 业务逻辑处理
  if (data.code !== 200) {
    handleBusinessError(data, reject, userStore)
    return
  }
  
  resolve(data.data)
}

/**
 * 业务错误处理
 */
function handleBusinessError<T>(
  data: ApiResponse<T>, 
  reject: (reason: any) => void,
  userStore: ReturnType<typeof useUserStore>
): void {
  const { code, msg } = data
  
  switch (code) {
    case 401:
      // 未授权，清除状态并跳转登录
      uni.showToast({
        title: msg || '登录已过期',
        icon: 'none'
      })
      userStore.logout()
      setTimeout(() => {
        uni.reLaunch({ url: '/pages/login/index' })
      }, 1500)
      break
    case 403:
      uni.showToast({
        title: msg || '没有权限',
        icon: 'none'
      })
      break
    case 404:
      uni.showToast({
        title: msg || '资源不存在',
        icon: 'none'
      })
      break
    case 500:
      uni.showToast({
        title: msg || '服务器错误',
        icon: 'none'
      })
      break
    default:
      uni.showToast({
        title: msg || '请求失败',
        icon: 'none'
      })
  }
  
  reject(new Error(msg || '请求失败'))
}

/**
 * 网络错误处理
 */
function handleError(err: UniApp.GeneralCallbackResult, reject: (reason: any) => void): void {
  console.error('[Request Error]', err)
  uni.showToast({
    title: '网络连接失败',
    icon: 'none'
  })
  reject(err)
}

// ===== HTTP 方法封装 =====

export function get<T = any>(url: string, params?: Record<string, any>, options?: Partial<UniApp.RequestOptions>): Promise<T> {
  let fullUrl = url
  if (params) {
    const queryString = Object.entries(params)
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&')
    fullUrl += (url.includes('?') ? '&' : '?') + queryString
  }
  
  return request<T>({
    url: fullUrl,
    method: 'GET',
    ...options
  })
}

export function post<T = any>(url: string, data?: any, options?: Partial<UniApp.RequestOptions>): Promise<T> {
  return request<T>({
    url,
    method: 'POST',
    data,
    ...options
  })
}

export function put<T = any>(url: string, data?: any, options?: Partial<UniApp.RequestOptions>): Promise<T> {
  return request<T>({
    url,
    method: 'PUT',
    data,
    ...options
  })
}

export function del<T = any>(url: string, data?: any, options?: Partial<UniApp.RequestOptions>): Promise<T> {
  return request<T>({
    url,
    method: 'DELETE',
    data,
    ...options
  })
}

export default request
