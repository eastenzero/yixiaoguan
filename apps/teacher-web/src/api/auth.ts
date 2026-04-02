import request from '@/utils/request'

export interface LoginParams {
  username: string
  password: string
  code?: string
  uuid?: string
}

// 后端 /login 实际返回：{ code, msg, token }（AjaxResult 直接 put）
export interface LoginResponse {
  code: number
  msg: string
  token: string
}

// 后端 /captchaImage 实际返回：{ code, msg, captchaEnabled, img?, uuid? }
export interface CaptchaResponse {
  code: number
  msg: string
  captchaEnabled: boolean
  img?: string
  uuid?: string
}

// 后端 /getInfo 实际返回：{ code, msg, user: YxUser, roles, permissions }
export interface UserInfoResponse {
  code: number
  msg: string
  user: {
    id: number
    username: string
    realName: string
    nickname: string
    avatarUrl: string
    email: string
    phone: string
    department: string
    admin: boolean
    roles?: { roleKey: string; roleName: string }[]
  }
  roles: string[]
  permissions: string[]
}

// 前端视图层统一模型（适配器目标结构）
export interface UserInfoResult {
  user: {
    userId: number
    userName: string
    nickName: string
    avatar: string
    email: string
    phonenumber: string
    dept: {
      deptName: string
    }
  }
  roles: string[]
  permissions: string[]
}

/**
 * 用户信息适配器：将后端 YxUser 结构转译为前端旧模型
 * 严禁删减 UI 列，所有缺失字段用空值兜底
 */
export function adaptUserInfo(raw: UserInfoResponse): UserInfoResult {
  const u = raw.user
  return {
    user: {
      userId: u?.id ?? 0,
      userName: u?.username ?? '',
      nickName: u?.nickname ?? u?.realName ?? '',
      avatar: u?.avatarUrl ?? '',
      email: u?.email ?? '',
      phonenumber: u?.phone ?? '',
      dept: {
        deptName: u?.department ?? ''
      }
    },
    roles: raw.roles ?? [],
    permissions: raw.permissions ?? []
  }
}

// 登录
export function login(data: LoginParams) {
  return request({
    url: '/api/login',
    method: 'post',
    data
  }) as Promise<LoginResponse>
}

// 获取验证码
export function getCaptcha() {
  return request({
    url: '/api/captchaImage',
    method: 'get'
  }) as Promise<CaptchaResponse>
}

// 获取用户信息
export function getUserInfo() {
  return request({
    url: '/api/getInfo',
    method: 'get'
  }) as Promise<UserInfoResponse>
}

// 退出登录
export function logout() {
  return request({
    url: '/api/logout',
    method: 'post'
  }) as Promise<{ code: number; msg: string; data?: any }>
}
