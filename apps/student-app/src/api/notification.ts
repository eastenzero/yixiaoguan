import { get } from '@/utils/request'
import type { Notification, PageResult } from '@/types/api'

/**
 * 获取通知列表
 */
export function getNotificationList(pageNum = 1, pageSize = 10): Promise<PageResult<Notification>> {
  return get('/api/v1/notifications', { pageNum, pageSize })
}

/**
 * 获取未读通知数量
 */
export function getUnreadCount(): Promise<number> {
  return get('/api/v1/notifications/unread-count')
}

/**
 * 标记通知为已读
 */
export function markAsRead(id: number): Promise<void> {
  return get(`/api/v1/notifications/${id}/read`)
}
