import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// ===== 配置区 =====
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? ''
const REQUEST_TIMEOUT = 30000
const TOKEN_PREFIX = 'Bearer '

// ===== 创建 axios 实例 =====
const request: AxiosInstance = axios.create({
  baseURL: API_BASE_URL || '/',
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json'
  }
})

// ===== 请求队列管理（用于取消重复请求）=====
const pendingMap = new Map<string, AbortController>()

const getPendingKey = (config: AxiosRequestConfig): string => {
  return `${config.method}_${config.url}_${JSON.stringify(config.params)}_${JSON.stringify(config.data)}`
}

const addPending = (config: AxiosRequestConfig): void => {
  const key = getPendingKey(config)
  const controller = new AbortController()
  config.signal = controller.signal
  pendingMap.set(key, controller)
}

const removePending = (config: AxiosRequestConfig): void => {
  const key = getPendingKey(config)
  const controller = pendingMap.get(key)
  if (controller) {
    controller.abort()
    pendingMap.delete(key)
  }
}

const clearPending = (): void => {
  pendingMap.forEach(controller => controller.abort())
  pendingMap.clear()
}

// ===== 请求拦截器 =====
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 移除重复请求
    removePending(config)
    addPending(config)

    // 注入 JWT Token
    const userStore = useUserStore()
    if (userStore.token) {
      // 若依后端支持 Bearer Token 或直接 token
      config.headers.Authorization = userStore.token.startsWith('Bearer') 
        ? userStore.token 
        : `${TOKEN_PREFIX}${userStore.token}`
    }

    return config
  },
  (error) => {
    console.error('[Request Error]', error)
    return Promise.reject(error)
  }
)

// ===== 响应拦截器 =====
request.interceptors.response.use(
  (response: AxiosResponse) => {
    // 移除已完成请求
    removePending(response.config)

    const { data } = response
    
    // 若依后端标准返回格式: { code: 200, msg: "...", data: {...} }
    if (data.code !== 200) {
      // 业务错误处理
      return handleBusinessError(data)
    }

    return data
  },
  (error) => {
    // 处理网络/HTTP 错误
    return handleNetworkError(error)
  }
)

// ===== 业务错误处理 =====
function handleBusinessError(data: any): Promise<never> {
  const { code, msg } = data
  
  switch (code) {
    case 401:
      // 登录过期，清除状态并跳转
      handleUnauthorized(msg)
      break
    case 403:
      ElMessage.error(msg || '没有权限执行此操作')
      break
    case 404:
      ElMessage.error(msg || '请求的资源不存在')
      break
    case 500:
      ElMessage.error(msg || '服务器内部错误')
      break
    default:
      ElMessage.error(msg || '请求失败')
  }
  
  return Promise.reject(new Error(msg || '请求失败'))
}

// ===== 网络/HTTP 错误处理 =====
function handleNetworkError(error: any): Promise<never> {
  // 取消请求不弹窗
  if (error.name === 'AbortError' || error.message === 'canceled') {
    return Promise.reject(error)
  }

  const { response } = error
  
  if (response) {
    switch (response.status) {
      case 401:
        handleUnauthorized('登录状态已过期')
        break
      case 403:
        ElMessage.error('没有权限，请联系管理员')
        break
      case 404:
        ElMessage.error('访问的资源不存在')
        break
      case 408:
        ElMessage.error('请求超时，请稍后重试')
        break
      case 500:
        ElMessage.error('服务器内部错误')
        break
      case 502:
        ElMessage.error('网关错误')
        break
      case 503:
        ElMessage.error('服务不可用')
        break
      case 504:
        ElMessage.error('网关超时')
        break
      default:
        ElMessage.error(response.data?.msg || `网络错误(${response.status})`)
    }
  } else if (error.code === 'ECONNABORTED') {
    ElMessage.error('请求超时，请检查网络连接')
  } else {
    ElMessage.error('网络连接失败，请检查网络')
  }

  return Promise.reject(error)
}

// ===== 未授权统一处理 =====
let isRefreshing = false

function handleUnauthorized(msg: string): void {
  const userStore = useUserStore()
  
  // 防止重复弹窗
  if (isRefreshing) return
  isRefreshing = true
  
  ElMessageBox.confirm(
    msg || '登录状态已过期，您可以继续留在该页面，或者重新登录',
    '系统提示',
    {
      confirmButtonText: '重新登录',
      cancelButtonText: '取消',
      type: 'warning'
    }
  ).then(() => {
    // 清除登录状态
    userStore.logout()
    clearPending()
    router.push('/login')
  }).catch(() => {
    // 用户取消，仅清除状态
    userStore.logout()
  }).finally(() => {
    isRefreshing = false
  })
}

// ===== 导出工具方法 =====
export { clearPending }
export default request
