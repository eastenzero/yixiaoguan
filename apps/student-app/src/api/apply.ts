import { get, post, put, del } from '@/utils/request'
import type { PageResult } from '@/types/api'

// ===== 类型定义 =====

/**
 * 教室信息
 */
export interface Classroom {
  id: number
  building: string
  roomNumber: string
  capacity?: number
  equipment?: string
  location?: string
  status: number
}

/**
 * 申请表单提交数据
 */
export interface ApplyForm {
  classroomId: number
  applyDate: string       // "YYYY-MM-DD"
  startTime: string       // "HH:mm"
  endTime: string         // "HH:mm"
  purpose: string
  attendeeCount?: number
  contactPhone?: string
}

/**
 * 申请状态枚举
 * 0-待审批 1-已通过 2-已拒绝 3-已取消 4-已过期
 */
export enum ApplicationStatus {
  PENDING = 0,   // 待审批
  APPROVED = 1,  // 已通过
  REJECTED = 2,  // 已拒绝
  CANCELLED = 3, // 已取消
  EXPIRED = 4    // 已过期
}

/**
 * 申请记录
 */
export interface Application {
  id: number
  applicantId: number
  classroomId: number
  building?: string
  roomNumber?: string
  applyDate: string
  startTime: string
  endTime: string
  purpose: string
  attendeeCount?: number
  contactPhone?: string
  status: ApplicationStatus
  remark?: string
  createdAt: string
  updatedAt: string
}

/**
 * 审批记录
 */
export interface ApplicationReview {
  id: number
  applicationId: number
  reviewerId: number
  reviewerName?: string
  action: number      // 1-通过 2-拒绝
  opinion?: string
  createdAt: string
}

/**
 * 申请详情（含审批记录）
 */
export interface ApplicationDetail extends Application {
  reviews?: ApplicationReview[]
}

// ===== API 函数 =====

/**
 * 获取教室列表
 * GET /api/v1/classrooms
 */
export function getClassroomList(params?: { building?: string; status?: number; pageNum?: number; pageSize?: number }): Promise<PageResult<Classroom>> {
  return get('/api/v1/classrooms', params)
}

/**
 * 提交申请
 * POST /api/v1/classroom-applications
 */
export function submitApplication(data: ApplyForm): Promise<Application> {
  return post('/api/v1/classroom-applications', data)
}

/**
 * 获取我的申请列表
 * GET /api/v1/classroom-applications?applicantId={userId}
 * 注：后端暂无 /my 接口，使用 applicantId 参数筛选
 * @param userId 当前用户ID（必需）
 * @param params 其他可选参数（状态、分页等）
 */
export function getMyApplications(
  userId: number,
  params?: { status?: number; pageNum?: number; pageSize?: number }
): Promise<PageResult<Application>> {
  return get('/api/v1/classroom-applications', { applicantId: userId, ...params })
}

/**
 * 获取申请详情
 * GET /api/v1/classroom-applications/{id}
 */
export function getApplicationDetail(id: number): Promise<ApplicationDetail> {
  return get(`/api/v1/classroom-applications/${id}`)
}

/**
 * 取消申请
 * PUT /api/v1/classroom-applications/{id}/cancel
 */
export function cancelApplication(id: number): Promise<void> {
  return put(`/api/v1/classroom-applications/${id}/cancel`, {})
}

/**
 * 删除申请
 * DELETE /api/v1/classroom-applications/{id}
 */
export function deleteApplication(id: number): Promise<void> {
  return del(`/api/v1/classroom-applications/${id}`)
}

// ===== 工具函数 =====

/**
 * 获取状态文本
 */
export function getStatusText(status: ApplicationStatus): string {
  const map: Record<number, string> = {
    [ApplicationStatus.PENDING]: '待审批',
    [ApplicationStatus.APPROVED]: '已通过',
    [ApplicationStatus.REJECTED]: '已拒绝',
    [ApplicationStatus.CANCELLED]: '已取消',
    [ApplicationStatus.EXPIRED]: '已过期'
  }
  return map[status] || '未知状态'
}

/**
 * 获取状态颜色
 */
export function getStatusColor(status: ApplicationStatus): string {
  const map: Record<number, string> = {
    [ApplicationStatus.PENDING]: '#F59E0B',   // 橙黄
    [ApplicationStatus.APPROVED]: '#00685f',  // 主题绿
    [ApplicationStatus.REJECTED]: '#EF4444',  // 红
    [ApplicationStatus.CANCELLED]: '#9CA3AF', // 灰
    [ApplicationStatus.EXPIRED]: '#9CA3AF'    // 灰
  }
  return map[status] || '#9CA3AF'
}

/**
 * 格式化日期时间
 */
export function formatDateTime(dateStr: string, timeStr: string): string {
  return `${dateStr} ${timeStr}`
}

/**
 * 格式化时间段
 */
export function formatTimeRange(dateStr: string, startTime: string, endTime: string): string {
  return `${dateStr} ${startTime}~${endTime}`
}
