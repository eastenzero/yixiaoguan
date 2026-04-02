/**
 * 空教室审批 API 模块
 * 对应后端: ClassroomApplicationController
 */
import request from '@/utils/request'
import type { ApiResponse, PageParams, PageResult } from './types'

// ===== 状态枚举 =====
export enum ApprovalStatus {
  PENDING = 0,   // 待审批
  APPROVED = 1,  // 已通过
  REJECTED = 2,  // 已拒绝
  CANCELLED = 3, // 已取消
  EXPIRED = 4    // 已过期
}

// ===== 类型定义 =====

/** 空教室申请项 */
export interface ClassroomApplication {
  id: number
  applicantId: number
  applicantName: string
  classroomId: number
  building: string
  roomNumber: string
  applyDate: string
  startTime: string
  endTime: string
  purpose: string
  attendeeCount: number
  contactPhone: string
  status: ApprovalStatus
  remark?: string
  createdAt: string
  updatedAt: string
  // 前端扩展字段
  title?: string
  isUrgent?: boolean
}

/** 审批统计数据 */
export interface ApprovalStats {
  pendingCount: number      // 待审批数量
  urgentCount: number       // 即将超时数量
  todayApproved: number     // 今日已审批
  todayApprovedGrowth: number // 较昨日增长
  monthlyApproved: number   // 本月通过
  monthlyApprovalRate: number // 本月通过率
  weeklyTotal: number       // 本周申请
  weeklyAverage: number     // 日均申请
}

/** 教室信息 */
export interface ClassroomInfo {
  id: number
  building: string
  roomNumber: string
  capacity: number
  equipment: string[]
}

/** 审批操作参数 */
export interface ApprovalActionParams {
  opinion?: string
}

// ===== 接口函数 =====

/**
 * 获取审批统计数据
 */
export function getApprovalStats() {
  return request({
    url: '/api/v1/classroom-applications/stats',
    method: 'get'
  }) as Promise<ApiResponse<ApprovalStats>>
}

/**
 * 获取申请列表
 * @param status 状态筛选
 * @param params 分页参数
 */
export function getApprovalList(status?: ApprovalStatus, params?: PageParams) {
  return request({
    url: '/api/v1/classroom-applications',
    method: 'get',
    params: {
      status,
      ...params
    }
  }) as Promise<ApiResponse<PageResult<ClassroomApplication>>>
}

/**
 * 获取申请详情
 * @param id 申请ID
 */
export function getApprovalDetail(id: number) {
  return request({
    url: `/api/v1/classroom-applications/${id}`,
    method: 'get'
  }) as Promise<ApiResponse<ClassroomApplication>>
}

/**
 * 批准申请
 * @param id 申请ID
 * @param opinion 审批意见
 */
export function approveApplication(id: number, opinion?: string) {
  return request({
    url: `/api/v1/classroom-applications/${id}/approve`,
    method: 'put',
    data: { opinion }
  }) as Promise<ApiResponse<null>>
}

/**
 * 拒绝申请
 * @param id 申请ID
 * @param opinion 拒绝原因
 */
export function rejectApplication(id: number, opinion: string) {
  return request({
    url: `/api/v1/classroom-applications/${id}/reject`,
    method: 'put',
    data: { opinion }
  }) as Promise<ApiResponse<null>>
}

/**
 * 取消申请
 * @param id 申请ID
 */
export function cancelApplication(id: number) {
  return request({
    url: `/api/v1/classroom-applications/${id}/cancel`,
    method: 'put'
  }) as Promise<ApiResponse<null>>
}

/**
 * 删除申请
 * @param id 申请ID
 */
export function deleteApplication(id: number) {
  return request({
    url: `/api/v1/classroom-applications/${id}`,
    method: 'delete'
  }) as Promise<ApiResponse<null>>
}

/**
 * 获取教室信息
 * @param id 教室ID
 */
export function getClassroomInfo(id: number) {
  return request({
    url: `/api/v1/classrooms/${id}`,
    method: 'get'
  }) as Promise<ApiResponse<ClassroomInfo>>
}

/**
 * 获取教室今日状态
 * @param id 教室ID
 */
export function getClassroomTodayStatus(id: number) {
  return request({
    url: `/api/v1/classrooms/${id}/today-status`,
    method: 'get'
  }) as Promise<ApiResponse<{
    timeSlots: Array<{
      startTime: string
      endTime: string
      status: 'occupied' | 'free' | 'current' | 'pending'
    }>
  }>>
}
