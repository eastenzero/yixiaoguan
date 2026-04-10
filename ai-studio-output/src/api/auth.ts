import { request } from '@/utils/request'

export const getCaptcha = () => {
  return request({ url: '/api/captchaImage', method: 'GET' })
}

export const login = (data: any) => {
  return request({ url: '/api/login', method: 'POST', data })
}

export const getUserInfo = (token?: string) => {
  return request({ url: '/api/getInfo', method: 'GET' })
}

export const logout = (token?: string) => {
  return request({ url: '/api/logout', method: 'POST' })
}
