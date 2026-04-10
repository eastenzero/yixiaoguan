import { request } from '@/utils/request'

export const getClassroomList = (params?: any) => {
  return request({ url: '/api/v1/classrooms', method: 'GET', data: params })
}

export const submitApplication = (data: any) => {
  return request({ url: '/api/v1/classroom-applications', method: 'POST', data })
}

export const getMyApplications = (userId: string | number, params?: any) => {
  return request({ url: '/api/v1/classroom-applications', method: 'GET', data: { userId, ...params } })
}

export const getApplicationDetail = (id: string | number) => {
  return request({ url: `/api/v1/classroom-applications/${id}`, method: 'GET' })
}

export const cancelApplication = (id: string | number) => {
  return request({ url: `/api/v1/classroom-applications/${id}/cancel`, method: 'PUT' })
}
