import { get, post } from '@/utils/request'
import type {
  Conversation,
  Message,
  SendMessageParams,
  Escalation,
  CreateEscalationParams,
  AIChatRequest,
  AIChatResponse
} from '@/types/chat'
import type { PageResult, PageParams } from '@/types/api'

// AI 服务地址（直连，不走业务后端）
const AI_SERVICE_URL = 'http://localhost:8000'

/**
 * 创建新会话
 * @param title 会话标题（可选）
 * @returns 创建的会话信息
 */
export function createConversation(title?: string): Promise<Conversation> {
  return post('/api/v1/conversations', { title })
}

/**
 * 获取会话列表
 * @param status 会话状态筛选（可选）
 * @param params 分页参数
 * @returns 会话分页列表
 */
export function getConversationList(
  status?: number,
  params?: PageParams
): Promise<PageResult<Conversation>> {
  // 过滤 undefined 参数，避免发送 ?status=undefined
  const query: Record<string, any> = { ...params }
  if (status !== undefined) query.status = status
  return get('/api/v1/conversations', query)
}

/**
 * 获取会话详情
 * @param id 会话 ID
 * @returns 会话详情
 */
export function getConversationDetail(id: number): Promise<Conversation> {
  return get(`/api/v1/conversations/${id}`)
}

/**
 * 更新会话标题
 * @param id 会话 ID
 * @param title 新标题
 */
export function updateConversationTitle(id: number, title: string): Promise<void> {
  return put(`/api/v1/conversations/${id}/title`, { title })
}

/**
 * 关闭会话
 * @param id 会话 ID
 */
export function closeConversation(id: number): Promise<void> {
  return del(`/api/v1/conversations/${id}`)
}

/**
 * 获取会话历史消息（全量）
 * @param conversationId 会话 ID
 * @returns 消息列表
 */
export function getHistory(conversationId: number): Promise<Message[]> {
  return get(`/api/v1/conversations/${conversationId}/messages`)
}

/**
 * 分页获取会话消息
 * @param conversationId 会话 ID
 * @param params 分页参数
 * @returns 消息分页列表
 */
export function getMessagePage(
  conversationId: number,
  params?: PageParams
): Promise<PageResult<Message>> {
  return get(`/api/v1/conversations/${conversationId}/messages/page`, params)
}

/**
 * 发送消息
 * @param conversationId 会话 ID
 * @param params 消息参数
 * @returns 发送的消息
 */
export function sendMessage(
  conversationId: number,
  params: SendMessageParams
): Promise<Message> {
  return post(`/api/v1/conversations/${conversationId}/messages`, params)
}

/**
 * 学生主动呼叫老师（创建工单）
 * @param params 工单参数
 * @returns 创建的工单
 */
export function callTeacher(params: CreateEscalationParams): Promise<Escalation> {
  return post('/api/v1/escalations', params)
}

/**
 * 获取我的工单列表
 * @param status 状态筛选（可选）
 * @param params 分页参数
 * @returns 工单分页列表
 */
export function getMyEscalations(
  status?: number,
  params?: PageParams
): Promise<PageResult<Escalation>> {
  const query: Record<string, any> = { ...params }
  if (status !== undefined && status !== null) {
    query.status = status
  }
  return get('/api/v1/escalations/my', query)
}

/**
 * 调用 AI 服务进行对话（非流式）
 * @param request AI 对话请求
 * @returns AI 响应
 */
export function aiChat(request: AIChatRequest): Promise<AIChatResponse> {
  return new Promise((resolve, reject) => {
    uni.request({
      url: `${AI_SERVICE_URL}/api/chat`,
      method: 'POST',
      header: {
        'Content-Type': 'application/json'
      },
      data: request,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data as AIChatResponse)
        } else {
          reject(new Error(`AI 服务请求失败: ${res.statusCode}`))
        }
      },
      fail: (err) => {
        console.error('[AI Chat Error]', err)
        reject(err)
      }
    })
  })
}

// TODO: 后端实现 /api/chat/suggestions 后取消注释
// export function getSuggestions(): Promise<string[]> {
//   return get('/api/chat/suggestions')
// }

// ===== 辅助 HTTP 方法（request.ts 中已有，但为保持独立引用）=====

import { request } from '@/utils/request'

function put<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({
    url,
    method: 'PUT',
    data
  })
}

function del<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({
    url,
    method: 'DELETE',
    data
  })
}
