/**
 * uni-app HTTP 请求封装
 * 统一处理 baseURL、token 注入、响应格式 { code, msg, data }
 */

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

interface RequestOptions {
    url: string
    method?: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
    data?: Record<string, unknown>
    header?: Record<string, string>
}

interface ApiResponse<T = unknown> {
    code: number
    msg: string
    data: T
}

/**
 * 封装 uni.request，返回 Promise
 */
function request<T = unknown>(options: RequestOptions): Promise<ApiResponse<T>> {
    return new Promise((resolve, reject) => {
        // 从本地存储获取 token
        const token = uni.getStorageSync('token')

        uni.request({
            url: `${BASE_URL}${options.url}`,
            method: options.method || 'GET',
            data: options.data,
            header: {
                'Content-Type': 'application/json',
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
                ...options.header,
            },
            success: (res) => {
                const result = res.data as ApiResponse<T>
                if (result.code === 0 || result.code === 200) {
                    resolve(result)
                } else {
                    // TODO: 使用 uni.showToast 统一提示
                    console.error(`[API Error] code=${result.code}, msg=${result.msg}`)
                    reject(new Error(result.msg || '请求失败'))
                }
            },
            fail: (err) => {
                console.error('[Request Fail]', err)
                reject(err)
            },
        })
    })
}

export default request
