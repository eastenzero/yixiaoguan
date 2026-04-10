import { useUserStore } from '@/stores/user'

// ⚠️ 不可修改 - Token 注入逻辑
export function request<T = any>(options: UniApp.RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const userStore = useUserStore()
    
    // 构建请求配置
    const requestOptions: UniApp.RequestOptions = {
      ...options,
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      success: (res) => handleResponse(res, resolve, reject, userStore),
      fail: (err) => handleError(err, reject)
    }
    
    // 注入 JWT Token
    if (userStore.token) {
      const token = userStore.token.startsWith('Bearer') 
        ? userStore.token 
        : `Bearer ${userStore.token}`
      requestOptions.header = {
        ...requestOptions.header,
        'Authorization': token
      }
    }
    
    uni.request(requestOptions)
  })
}

function handleResponse(res: any, resolve: any, reject: any, userStore: any) {
  const data = res.data
  if (res.statusCode >= 200 && res.statusCode < 300) {
    if (data.code && data.code !== 200) {
      handleBusinessError(data, reject, userStore)
      reject(data)
    } else {
      resolve(data)
    }
  } else {
    handleError(res, reject)
  }
}

// ⚠️ 不可修改 - 401 处理
function handleBusinessError(data: any, reject: any, userStore: any) {
  switch (data.code) {
    case 401:
      uni.showToast({ title: data.msg || '登录已过期', icon: 'none' })
      userStore.logout()
      setTimeout(() => {
        uni.reLaunch({ url: '/pages/login/index' })
      }, 1500)
      break
    // ...
  }
}

function handleError(err: any, reject: any) {
  console.error('Request failed:', err)
  uni.showToast({ title: '网络请求失败', icon: 'none' })
  reject(err)
}
