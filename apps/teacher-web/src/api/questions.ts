/**
 * 学生提问/工单 API 模块
 * 对应后端: EscalationController, ConversationController
 * 
 * ⚠️ 字段适配说明：
 * 后端字段名 → 前端字段名映射：
 * - studentRealName → studentName
 * - teacherRealName → teacherName  
 * - studentClassName → 解析为 studentGrade + studentMajor
 * - createdAt/updatedAt → 直接透传
 */
import request from '@/utils/request'
import type { ApiResponse, PageParams, PageResult } from './types'

// ===== 状态枚举 =====

/** 工单状态 */
export enum EscalationStatus {
  PENDING = 0,    // 待分配
  ASSIGNED = 1,   // 已分配
  RESOLVED = 2,   // 已解决
  CLOSED = 3      // 已关闭
}

/** 工单优先级 */
export enum EscalationPriority {
  LOW = 0,        // 低
  NORMAL = 1,     // 普通
  HIGH = 2,       // 高
  URGENT = 3      // 紧急
}

/** 会话状态 */
export enum ConversationStatus {
  CLOSED = 0,     // 已关闭
  ACTIVE = 1,     // 进行中
  TEACHER_JOINED = 2 // 教师已介入
}

// ===== 类型定义 =====

/** 后端原始工单数据结构 */
interface RawEscalationItem {
  id: number
  conversationId: number
  messageId?: number
  studentId: number
  studentRealName?: string        // 后端字段
  studentClassName?: string       // 后端字段：如 "2022级 计算机科学"
  questionSummary: string
  priority: number
  status: number
  teacherId?: number
  teacherRealName?: string        // 后端字段
  teacherReply?: string
  triggerType: 1 | 2
  createdAt: string
  updatedAt: string
  // 扩展字段
  aiConfidence?: number
  tags?: string[]
  isHot?: boolean
}

/** 工单/提问项（前端标准化结构） */
export interface EscalationItem {
  id: number
  conversationId: number
  messageId?: number
  studentId: number
  studentName: string
  studentGrade?: string
  studentMajor?: string
  questionSummary: string
  priority: EscalationPriority
  status: EscalationStatus
  teacherId?: number
  teacherName?: string
  teacherReply?: string
  triggerType: 1 | 2  // 1-学生主动呼叫 2-AI自动上报
  createdAt: string
  updatedAt: string
  // 前端展示扩展字段
  aiConfidence?: number
  tags?: string[]
  isHot?: boolean
}

/** 提问列表筛选参数 */
export interface QuestionListParams extends PageParams {
  status?: EscalationStatus
  priority?: EscalationPriority
  keyword?: string
}

/** 提问统计数据 */
export interface QuestionStats {
  totalUnsolved: number     // 待解决总数
  hotQuestions: number      // 高频问题数
  needHuman: number         // 需人工处理数
  aiReplied: number         // AI已答复数
  transferred: number       // 已转办数
}

/** AI 聚类分析结果 */
export interface AIClusterAnalysis {
  topic: string
  relatedCount: number
  studentIds: number[]
  suggestedAction: string
  knowledgeBaseEntry?: string
}

/** 会话消息 */
export interface ConversationMessage {
  id: number
  conversationId: number
  senderType: 1 | 2 | 3  // 1-学生 2-AI 3-教师
  senderId: number
  senderName: string
  content: string
  messageType: number
  parentMessageId?: number
  createdAt: string
}

/** 会话详情 */
export interface ConversationDetail {
  id: number
  userId: number
  userName: string
  title?: string
  status: ConversationStatus
  teacherId?: number
  teacherName?: string
  messageCount: number
  createdAt: string
  lastMessageAt?: string
}

// ===== 字段适配器 =====

/**
 * 解析班级信息为年级和专业
 * @param className 如 "2022级 计算机科学" 或 "2022级计算机科学"
 */
function parseStudentClass(className?: string): { grade?: string; major?: string } {
  if (!className) return { grade: undefined, major: undefined }
  
  // 匹配模式：2022级 计算机科学 或 2022级计算机科学
  const match = className.match(/(\d{4}级)\s*(.+)/)
  if (match) {
    return {
      grade: match[1],
      major: match[2]
    }
  }
  
  // 如果无法解析，将整串作为年级
  return {
    grade: className,
    major: undefined
  }
}

/**
 * 适配单条工单数据
 * 将后端字段名转换为前端标准字段名
 */
function adaptEscalationItem(raw: RawEscalationItem): EscalationItem {
  const { grade, major } = parseStudentClass(raw.studentClassName)
  
  return {
    id: raw.id,
    conversationId: raw.conversationId,
    messageId: raw.messageId,
    studentId: raw.studentId,
    studentName: raw.studentRealName || '未知学生',
    studentGrade: grade,
    studentMajor: major,
    questionSummary: raw.questionSummary,
    priority: raw.priority as EscalationPriority,
    status: raw.status as EscalationStatus,
    teacherId: raw.teacherId,
    teacherName: raw.teacherRealName,
    teacherReply: raw.teacherReply,
    triggerType: raw.triggerType,
    createdAt: raw.createdAt,
    updatedAt: raw.updatedAt,
    aiConfidence: raw.aiConfidence,
    tags: raw.tags,
    isHot: raw.isHot
  }
}

/**
 * 适配分页结果
 */
function adaptPageResult<T, R>(
  raw: PageResult<T>, 
  adapter: (item: T) => R
): PageResult<R> {
  return {
    total: raw.total,
    rows: raw.rows.map(adapter),
    pageNum: raw.pageNum,
    pageSize: raw.pageSize
  }
}

// ===== 接口函数 =====

/**
 * 获取提问统计数据
 * 
 * ⚠️ 后端暂未实现此接口，当前返回 mock 数据
 * 待后端实现后删除 mock 逻辑
 */
export async function getQuestionStats(): Promise<ApiResponse<QuestionStats>> {
  try {
    const res = await request({
      url: '/api/v1/escalations/stats',
      method: 'get'
    }) as ApiResponse<QuestionStats>
    
    // 如果后端返回了有效数据，直接返回
    if (res.code === 200 && res.data) {
      return res
    }
    
    // 否则返回 mock 数据
    throw new Error('Stats API not implemented')
  } catch (error) {
    // Mock 数据 - 待后端实现后删除
    return {
      code: 200,
      msg: 'success (mock)',
      data: {
        totalUnsolved: 12,
        hotQuestions: 3,
        needHuman: 5,
        aiReplied: 8,
        transferred: 2
      }
    }
  }
}

/**
 * 获取待处理工单列表（教师视角）
 */
export async function getPendingEscalations(params?: PageParams): Promise<ApiResponse<PageResult<EscalationItem>>> {
  const res = await request({
    url: '/api/v1/escalations/pending',
    method: 'get',
    params
  }) as ApiResponse<PageResult<RawEscalationItem>>
  
  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptPageResult(res.data, adaptEscalationItem)
    }
  }
  
  return res as unknown as ApiResponse<PageResult<EscalationItem>>
}

/**
 * 获取已分配给我的工单
 */
export async function getMyAssignedEscalations(
  status?: EscalationStatus, 
  params?: PageParams
): Promise<ApiResponse<PageResult<EscalationItem>>> {
  const res = await request({
    url: '/api/v1/escalations/assigned',
    method: 'get',
    params: {
      status,
      ...params
    }
  }) as ApiResponse<PageResult<RawEscalationItem>>
  
  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptPageResult(res.data, adaptEscalationItem)
    }
  }
  
  return res as unknown as ApiResponse<PageResult<EscalationItem>>
}

/**
 * 获取所有工单（分页）
 */
export async function getEscalationList(params?: QuestionListParams): Promise<ApiResponse<PageResult<EscalationItem>>> {
  const res = await request({
    url: '/api/v1/escalations',
    method: 'get',
    params
  }) as ApiResponse<PageResult<RawEscalationItem>>
  
  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptPageResult(res.data, adaptEscalationItem)
    }
  }
  
  return res as unknown as ApiResponse<PageResult<EscalationItem>>
}

/**
 * 获取工单详情
 */
export async function getEscalationDetail(id: number): Promise<ApiResponse<EscalationItem>> {
  const res = await request({
    url: `/api/v1/escalations/${id}`,
    method: 'get'
  }) as ApiResponse<RawEscalationItem>
  
  // 字段适配
  if (res.code === 200 && res.data) {
    return {
      code: res.code,
      msg: res.msg,
      data: adaptEscalationItem(res.data)
    }
  }
  
  return res as unknown as ApiResponse<EscalationItem>
}

/**
 * 接单（教师抢单）
 */
export function assignEscalation(id: number) {
  return request({
    url: `/api/v1/escalations/${id}/assign`,
    method: 'put'
  }) as Promise<ApiResponse<null>>
}

/**
 * 回复并解决工单
 */
export function resolveEscalation(id: number, teacherReply: string) {
  return request({
    url: `/api/v1/escalations/${id}/resolve`,
    method: 'put',
    data: { teacherReply }
  }) as Promise<ApiResponse<null>>
}

/**
 * 关闭工单
 */
export function closeEscalation(id: number) {
  return request({
    url: `/api/v1/escalations/${id}/close`,
    method: 'put'
  }) as Promise<ApiResponse<null>>
}

/**
 * 获取会话详情
 */
export function getConversationDetail(id: number) {
  return request({
    url: `/api/v1/conversations/${id}`,
    method: 'get'
  }) as Promise<ApiResponse<ConversationDetail>>
}

/**
 * 获取会话历史消息
 */
export function getConversationMessages(id: number) {
  return request({
    url: `/api/v1/conversations/${id}/messages`,
    method: 'get'
  }) as Promise<ApiResponse<ConversationMessage[]>>
}

/**
 * 分页获取会话消息
 */
export function getConversationMessagesPage(id: number, params?: PageParams) {
  return request({
    url: `/api/v1/conversations/${id}/messages/page`,
    method: 'get',
    params
  }) as Promise<ApiResponse<PageResult<ConversationMessage>>>
}

/**
 * 发送消息（HTTP 方式）
 */
export function sendMessage(id: number, content: string, messageType: number = 1, parentMessageId?: number) {
  return request({
    url: `/api/v1/conversations/${id}/messages`,
    method: 'post',
    data: {
      content,
      messageType,
      parentMessageId
    }
  }) as Promise<ApiResponse<ConversationMessage>>
}

/**
 * 获取 AI 提问聚类分析
 * 
 * ⚠️ 后端暂未实现此接口，当前返回 mock 数据
 * 待后端实现后删除 mock 逻辑
 */
export async function getAIClusterAnalysis(): Promise<ApiResponse<AIClusterAnalysis[]>> {
  try {
    const res = await request({
      url: '/api/v1/questions/ai-cluster-analysis',
      method: 'get'
    }) as ApiResponse<AIClusterAnalysis[]>
    
    if (res.code === 200 && res.data) {
      return res
    }
    
    throw new Error('AI Cluster Analysis API not implemented')
  } catch (error) {
    // Mock 数据 - 待后端实现后删除
    return {
      code: 200,
      msg: 'success (mock)',
      data: [
        {
          topic: '奖学金评定标准',
          relatedCount: 15,
          studentIds: [1001, 1002, 1003, 1004, 1005],
          suggestedAction: '更新知识库中学工政策模块',
          knowledgeBaseEntry: '奖学金评定政策'
        }
      ]
    }
  }
}

/**
 * 批量标记为已解决
 */
export function batchResolve(ids: number[]) {
  return request({
    url: '/api/v1/escalations/batch-resolve',
    method: 'put',
    data: { ids }
  }) as Promise<ApiResponse<null>>
}

/**
 * 批量转知识库
 */
export function batchTransferToKnowledge(ids: number[]) {
  return request({
    url: '/api/v1/escalations/batch-to-knowledge',
    method: 'put',
    data: { ids }
  }) as Promise<ApiResponse<null>>
}
