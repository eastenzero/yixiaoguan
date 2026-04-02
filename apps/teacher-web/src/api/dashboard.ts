/**
 * Dashboard API 模块
 * 工作台数据聚合接口
 */
import request from '@/utils/request'
import type { ApiResponse, PageParams, PageResult } from './types'

// ===== 类型定义 =====

/** 统计数据 */
export interface DashboardStats {
  todayQuestions: number      // 今日处理提问
  todayQuestionsGrowth: number // 同比昨日增长率
  pendingApprovals: number    // 待审批事项
  urgentApprovals: number     // 即将超时审批
  aiResolutionRate: number    // AI 自动解决率
  avgResponseTime: number     // 平均响应时间（分钟）
  responseTimeImprovement: number // 较上周改善时间
}

/** 今日提问项 */
export interface TodayQuestion {
  id: number
  time: string
  studentName: string
  studentClass: string
  avatarColor: string
  title: string
  category: string
  aiStatus: 'resolved' | 'pending' | 'handled'
  aiText: string
  needHandle: boolean
}

/** 高频问题 */
export interface HotQuestion {
  name: string
  count: number
  percent: number
}

/** 快捷入口配置 */
export interface QuickAccess {
  name: string
  icon: string
  bgColor: string
  color: string
  path?: string
}

/** 待审批项 */
export interface PendingApproval {
  id: string
  type: string
  title: string
  timeRange: string
  isUrgent: boolean
  remainingTime?: string
}

/** AI 舆情预警 */
export interface AIWarning {
  topic: string
  increasePercent: number
  suggestion: string
}

// ===== 接口函数 =====

/**
 * 获取工作台统计数据
 */
export function getDashboardStats() {
  return request({
    url: '/api/v1/dashboard/stats',
    method: 'get'
  }) as Promise<ApiResponse<DashboardStats>>
}

/**
 * 获取今日学生提问列表
 */
export function getTodayQuestions(params?: PageParams) {
  return request({
    url: '/api/v1/dashboard/today-questions',
    method: 'get',
    params
  }) as Promise<ApiResponse<PageResult<TodayQuestion>>>
}

/**
 * 获取高频问题热度统计
 */
export function getHotQuestions(limit: number = 5) {
  return request({
    url: '/api/v1/dashboard/hot-questions',
    method: 'get',
    params: { limit }
  }) as Promise<ApiResponse<HotQuestion[]>>
}

/**
 * 获取待审批事项列表
 */
export function getPendingApprovals(limit: number = 5) {
  return request({
    url: '/api/v1/dashboard/pending-approvals',
    method: 'get',
    params: { limit }
  }) as Promise<ApiResponse<PendingApproval[]>>
}

/**
 * 获取 AI 舆情预警
 */
export function getAIWarnings() {
  return request({
    url: '/api/v1/dashboard/ai-warnings',
    method: 'get'
  }) as Promise<ApiResponse<AIWarning[]>>
}

/**
 * 获取工作台聚合数据（一次请求获取所有数据）
 */
export function getDashboardOverview() {
  return request({
    url: '/api/v1/dashboard/overview',
    method: 'get'
  }) as Promise<ApiResponse<{
    stats: DashboardStats
    questions: TodayQuestion[]
    hotQuestions: HotQuestion[]
    pendingApprovals: PendingApproval[]
    aiWarning: AIWarning | null
  }>>
}
