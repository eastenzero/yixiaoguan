import request from '@/utils/request'

// 获取待处理工单列表
export function getPendingEscalations(pageNum = 1, pageSize = 10) {
  return request({
    url: '/api/v1/escalations/pending',
    method: 'get',
    params: { pageNum, pageSize }
  })
}

// 获取教师已接工单列表
export function getAssignedEscalations(status?: number, pageNum = 1, pageSize = 10) {
  return request({
    url: '/api/v1/escalations/assigned',
    method: 'get',
    params: { status, pageNum, pageSize }
  })
}

// 获取工单详情
export function getEscalationDetail(id: number) {
  return request({
    url: `/api/v1/escalations/${id}`,
    method: 'get'
  })
}

// 教师接单
export function assignEscalation(id: number) {
  return request({
    url: `/api/v1/escalations/${id}/assign`,
    method: 'put'
  })
}

// 教师回复解决
export function resolveEscalation(id: number, teacherReply: string) {
  return request({
    url: `/api/v1/escalations/${id}/resolve`,
    method: 'put',
    data: { teacherReply }
  })
}
