/**
 * 统一 API 响应格式
 */
export interface ApiResponse<T = any> {
  code: number
  msg: string
  data: T
}

/**
 * 登录请求参数
 */
export interface LoginParams {
  username: string
  password: string
  code: string
  uuid: string
}

/**
 * 登录响应数据
 */
export interface LoginResult {
  token: string
}

/**
 * 用户信息
 */
export interface UserInfo {
  id: number
  username: string
  realName: string
  nickName?: string
  avatarUrl?: string
  email?: string
  phone?: string
  studentId?: string
  className?: string
  grade?: string
  department?: string
  major?: string
  bio?: string
  roles?: string[]
  permissions?: string[]
  admin?: boolean
}

/**
 * 通知消息
 */
export interface Notification {
  id: number
  title: string
  content?: string
  type: number
  isRead: boolean
  createdAt: string
}

/**
 * 分页参数
 */
export interface PageParams {
  pageNum?: number
  pageSize?: number
}

/**
 * 分页响应
 */
export interface PageResult<T> {
  total: number
  rows: T[]
}
