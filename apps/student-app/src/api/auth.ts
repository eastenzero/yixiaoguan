/**
 * 认证相关 API
 *
 * ⚠️ 重要说明：
 * RuoYi 框架的认证接口（/login、/captchaImage、/getInfo、/logout）
 * 响应格式与项目业务接口不同，不走 request.ts 的通用封装：
 *
 *   /captchaImage → { code: 200, uuid, img, captchaEnabled, ... }
 *   /login        → { code: 200, token, msg }   （token 在顶层，无 data 字段）
 *   /getInfo      → { code: 200, user, roles, permissions }
 *
 * 因此此文件直接使用 uni.request，自行处理响应。
 */

/** 原始请求（不走通用 handleResponse） */
function rawRequest<T>(options: UniApp.RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    uni.request({
      ...options,
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          const data = res.data as any
          if (data && (data.code === 200 || data.code === 0)) {
            resolve(data as T)
          } else {
            uni.showToast({ title: (data && data.msg) || '请求失败', icon: 'none' })
            reject(new Error((data && data.msg) || '请求失败'))
          }
        } else {
          uni.showToast({ title: `请求失败(${res.statusCode})`, icon: 'none' })
          reject(new Error(`HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => {
        uni.showToast({ title: '网络连接失败', icon: 'none' })
        reject(err)
      }
    })
  })
}

// ── 响应类型 ──────────────────────────────────────────────

export interface CaptchaResult {
  captchaEnabled: boolean
  uuid: string
  img: string // base64
}

export interface LoginResult {
  token: string
}

export interface UserInfoResult {
  user: {
    // 兼容 yx_user 版本 (id/username/realName) 和 RuoYi 旧版本 (userId/userName/nickName)
    id?: number
    userId?: number
    username?: string
    userName?: string
    realName?: string
    nickName?: string
    avatar?: string
    email?: string
    phonenumber?: string
    [key: string]: any
  }
  roles: string[]
  permissions: string[]
}

// ── 接口函数 ──────────────────────────────────────────────

/**
 * 获取验证码图片
 * Vite proxy: /api/captchaImage → localhost:8080/captchaImage
 */
export function getCaptcha(): Promise<CaptchaResult> {
  return rawRequest<CaptchaResult>({
    url: '/api/captchaImage',
    method: 'GET'
  })
}

/**
 * 用户登录
 * Vite proxy: /api/login → localhost:8080/login
 * 响应: { code: 200, token: "...", msg: "操作成功" }
 */
export function login(params: {
  username: string
  password: string
  code?: string
  uuid?: string
}): Promise<LoginResult> {
  return rawRequest<LoginResult>({
    url: '/api/login',
    method: 'POST',
    data: params,
    header: { 'Content-Type': 'application/json' }
  })
}

/**
 * 获取当前用户信息
 * Vite proxy: /api/getInfo → localhost:8080/getInfo
 * 响应: { code: 200, user: {...}, roles: [...], permissions: [...] }
 */
export function getUserInfo(token: string): Promise<UserInfoResult> {
  return rawRequest<UserInfoResult>({
    url: '/api/getInfo',
    method: 'GET',
    header: { Authorization: `Bearer ${token}` }
  })
}

/**
 * 退出登录
 * Vite proxy: /api/logout → localhost:8080/logout
 */
export function logout(token: string): Promise<void> {
  return rawRequest<void>({
    url: '/api/logout',
    method: 'POST',
    header: { Authorization: `Bearer ${token}` }
  })
}
