import { request } from '@/utils/request'

export const getNotificationList = (pageNum?: number, pageSize?: number) => {
  return request({ url: '/api/v1/notifications', method: 'GET', data: { pageNum, pageSize } })
}

export const getUnreadCount = () => {
  return request({ url: '/api/v1/notifications/unread-count', method: 'GET' })
}
