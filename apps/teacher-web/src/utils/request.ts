/**
 * Axios 请求封装
 * 统一配置 baseURL、拦截器、错误处理
 */

import axios from 'axios'
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'

// 创建 Axios 实例
const service: AxiosInstance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

// 请求拦截器
service.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
        // TODO: 从 store 获取 token 并添加到请求头
        const token = localStorage.getItem('token')
        if (token && config.headers) {
            config.headers['Authorization'] = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    },
)

// 响应拦截器
service.interceptors.response.use(
    (response: AxiosResponse) => {
        const res = response.data
        // 统一响应格式：{ code, msg, data }
        if (res.code !== undefined && res.code !== 0 && res.code !== 200) {
            // TODO: 使用 Element Plus 的 ElMessage 进行错误提示
            console.error(`[API Error] code=${res.code}, msg=${res.msg}`)
            return Promise.reject(new Error(res.msg || '请求失败'))
        }
        return res
    },
    (error) => {
        // TODO: 统一错误处理（401 跳转登录、500 提示等）
        console.error('[Request Error]', error.message)
        return Promise.reject(error)
    },
)

export default service
