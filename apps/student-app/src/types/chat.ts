/**
 * 会话与会话相关类型定义
 */

/**
 * 会话信息
 */
export interface Conversation {
  id: number
  userId: number
  title?: string
  status: number // 0-已关闭 1-进行中 2-教师已介入
  teacherId?: number
  teacherJoinedAt?: string
  lastMessageAt?: string
  messageCount: number
  createdAt: string
  updatedAt: string
}

/**
 * 消息发送者类型
 */
export enum SenderType {
  STUDENT = 1,
  AI = 2,
  TEACHER = 3,
  SYSTEM = 4
}

/**
 * 消息内容类型
 */
export enum MessageType {
  TEXT = 1,
  RICH_TEXT = 2,
  CARD = 3,
  SYSTEM_NOTICE = 4
}

/**
 * 消息
 */
export interface Message {
  id: number
  conversationId: number
  senderType: SenderType
  senderId?: number
  content: string
  messageType: MessageType
  parentMessageId?: number
  aiConfidence?: number
  aiSourceEntryIds?: string
  aiSourceLinkIds?: string
  createdAt: string
}

/**
 * 发送消息请求
 */
export interface SendMessageParams {
  content: string
  messageType?: number
  parentMessageId?: number
}

/**
 * 工单上报状态
 */
export enum EscalationStatus {
  PENDING = 0,      // 待处理
  PROCESSING = 1,   // 处理中
  RESOLVED = 2,     // 已解决
  CLOSED = 3,       // 已关闭
  TO_KNOWLEDGE = 4  // 已转知识库
}

/**
 * 工单触发类型
 */
export enum EscalationTriggerType {
  STUDENT_INITIATED = 1,  // 学生主动呼叫
  AI_AUTO = 2             // AI 判断自动上报
}

/**
 * 工单信息
 */
export interface Escalation {
  id: number
  conversationId: number
  messageId: number
  studentId: number
  teacherId?: number
  questionSummary?: string
  status: EscalationStatus
  priority: number
  triggerType: EscalationTriggerType
  teacherReply?: string
  resolvedAt?: string
  knowledgeEntryId?: number
  remark?: string
  createdAt: string
  updatedAt: string
}

/**
 * 创建工单请求
 */
export interface CreateEscalationParams {
  conversationId: number
  messageId: number
  questionSummary?: string
  priority?: number
}

/**
 * AI 对话请求
 */
export interface AIChatRequest {
  query: string
  history?: AIChatMessageDTO[]
  use_kb?: boolean
  top_k?: number
}

/**
 * AI 对话消息传输对象
 */
export interface AIChatMessageDTO {
  role: 'system' | 'user' | 'assistant'
  content: string
}

/**
 * AI 对话响应
 */
export interface AIChatResponse {
  code: number
  msg: string
  data?: {
    answer: string
    sources: AIChatSourceItem[]
  }
}

/**
 * AI 引用来源
 */
export interface AIChatSourceItem {
  entry_id: string
  title: string
  content: string
  score: number
}
