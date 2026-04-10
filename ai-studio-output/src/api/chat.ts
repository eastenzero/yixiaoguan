import { request } from '@/utils/request'

export const createConversation = (title?: string) => {
  return request({ url: '/api/v1/conversations', method: 'POST', data: { title } })
}

export const getConversationList = (status?: string, params?: any) => {
  return request({ url: '/api/v1/conversations', method: 'GET', data: { status, ...params } })
}

export const getHistory = (conversationId: number | string) => {
  return request({ url: `/api/v1/conversations/${conversationId}/messages`, method: 'GET' })
}

export const sendMessage = (id: number | string, params: any) => {
  return request({ url: `/api/v1/conversations/${id}/messages`, method: 'POST', data: params })
}

export const callTeacher = (params: any) => {
  return request({ url: '/api/v1/escalations', method: 'POST', data: params })
}

export const getMyEscalations = (status?: string, params?: any) => {
  return request({ url: '/api/v1/escalations/my', method: 'GET', data: { status, ...params } })
}
