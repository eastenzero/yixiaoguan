/**
 * WebSocket 客户端封装
 * 
 * 特性：
 * - 自动心跳保活
 * - 断线自动重连（指数退避）
 * - 消息订阅/发布模式
 * - Token 鉴权（通过 Query Param）
 * 
 * 后端握手鉴权：
 *   URL: ws://host/ws/chat/{conversationId}?token=xxx
 *   Token 格式：Bearer xxx 或直接 xxx（后端兼容处理）
 */

import { useUserStore } from '@/stores/user'

// ===== 配置常量 =====
const WS_CONFIG = {
  HEARTBEAT_INTERVAL: 30000,      // 心跳间隔 30s
  HEARTBEAT_TIMEOUT: 10000,       // 心跳超时 10s
  RECONNECT_INITIAL_DELAY: 1000,  // 首次重连延迟 1s
  RECONNECT_MAX_DELAY: 30000,     // 最大重连延迟 30s
  RECONNECT_MAX_ATTEMPTS: 10,     // 最大重连次数
}

// ===== 消息类型定义 =====
export enum WsMessageType {
  // 客户端 → 服务端
  HEARTBEAT_PING = 'PING',
  CHAT_MESSAGE = 'CHAT_MESSAGE',
  TYPING_INDICATOR = 'typing',
  TEACHER_JOIN = 'TEACHER_JOIN',
  TEACHER_LEAVE = 'TEACHER_LEAVE',
  
  // 服务端 → 客户端
  HEARTBEAT_PONG = 'PONG',
  NEW_MESSAGE = 'new_message',
  AI_STREAM_CHUNK = 'ai_stream_chunk',
  AI_STREAM_END = 'ai_stream_end',
  TEACHER_JOINED = 'TEACHER_JOINED',
  SYSTEM_NOTIFY = 'SYSTEM_NOTIFY',
  ERROR = 'error'
}

/** WebSocket 消息包 */
export interface WsMessagePacket {
  type: WsMessageType
  payload?: any
  timestamp?: number
}

/** WebSocket 配置选项 */
export interface WsClientOptions {
  conversationId: number | string
  onMessage?: (message: WsMessagePacket) => void
  onConnect?: () => void
  onDisconnect?: (event: CloseEvent) => void
  onError?: (error: Event) => void
  onReconnect?: (attempt: number) => void
}

/** WebSocket 连接状态 */
export enum WsConnectionState {
  CONNECTING = 'CONNECTING',
  OPEN = 'OPEN',
  CLOSING = 'CLOSING',
  CLOSED = 'CLOSED',
  RECONNECTING = 'RECONNECTING'
}

/**
 * WebSocket 客户端类
 */
export class WsClient {
  private ws: WebSocket | null = null
  private url: string = ''
  private options: WsClientOptions
  private state: WsConnectionState = WsConnectionState.CLOSED
  
  // 心跳定时器
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null
  private heartbeatTimeoutTimer: ReturnType<typeof setTimeout> | null = null
  
  // 重连控制
  private reconnectAttempts = 0
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null
  private shouldReconnect = true
  
  // 消息队列（断线期间缓存）
  private messageQueue: WsMessagePacket[] = []

  constructor(options: WsClientOptions) {
    this.options = options
    this.buildUrl()
  }

  // ===== 公共方法 =====

  /**
   * 建立 WebSocket 连接
   */
  connect(): void {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.warn('[WsClient] 连接已存在，无需重复连接')
      return
    }

    this.shouldReconnect = true
    this.state = WsConnectionState.CONNECTING
    
    try {
      this.ws = new WebSocket(this.url)
      this.bindEvents()
    } catch (error) {
      console.error('[WsClient] 创建连接失败:', error)
      this.handleError(error as Event)
    }
  }

  /**
   * 断开连接
   * @param permanent 是否永久断开（不再重连）
   */
  disconnect(permanent: boolean = false): void {
    if (permanent) {
      this.shouldReconnect = false
    }
    
    this.clearTimers()
    
    if (this.ws) {
      this.state = WsConnectionState.CLOSING
      this.ws.close(1000, 'Client disconnect')
      this.ws = null
    }
    
    this.state = WsConnectionState.CLOSED
  }

  /**
   * 发送消息
   */
  send(message: WsMessagePacket): boolean {
    if (this.ws?.readyState !== WebSocket.OPEN) {
      console.warn('[WsClient] 连接未就绪，消息已缓存')
      this.messageQueue.push(message)
      return false
    }

    try {
      this.ws.send(JSON.stringify(message))
      return true
    } catch (error) {
      console.error('[WsClient] 发送消息失败:', error)
      this.messageQueue.push(message)
      return false
    }
  }

  /**
   * 发送聊天消息
   */
  sendChatMessage(content: string, messageType: number = 1): boolean {
    return this.send({
      type: WsMessageType.CHAT_MESSAGE,
      payload: { content, messageType },
      timestamp: Date.now()
    })
  }

  /**
   * 获取当前连接状态
   */
  getState(): WsConnectionState {
    return this.state
  }

  /**
   * 检查是否已连接
   */
  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN
  }

  // ===== 私有方法 =====

  /**
   * 构建 WebSocket URL
   */
  private buildUrl(): void {
    const userStore = useUserStore()
    const token = userStore.token
    
    if (!token) {
      throw new Error('[WsClient] 未登录，无法建立 WebSocket 连接')
    }

    // 去除 Bearer 前缀（后端兼容处理，但统一格式更规范）
    const cleanToken = token.startsWith('Bearer ') ? token.slice(7) : token
    
    // 优先使用 VITE_WS_BASE_URL，否则从 VITE_API_BASE_URL 推断
    const wsBaseUrl = import.meta.env.VITE_WS_BASE_URL
    let wsProtocol: string, wsHost: string

    if (wsBaseUrl) {
      const url = new URL(String(wsBaseUrl).replace(/^ws/, 'http')) // 借用 URL 解析器
      wsProtocol = String(wsBaseUrl).startsWith('wss') ? 'wss' : 'ws'
      wsHost = url.host
    } else {
      const apiBaseUrl = import.meta.env.VITE_API_BASE_URL || window.location.origin
      wsProtocol = apiBaseUrl.startsWith('https') ? 'wss' : 'ws'
      wsHost = apiBaseUrl.replace(/^https?:\/\//, '')
    }

    this.url = `${wsProtocol}://${wsHost}/ws/chat/${this.options.conversationId}?token=${encodeURIComponent(cleanToken)}`
    
    if (import.meta.env.DEV) {
      console.log('[WsClient] WS URL:', this.url.replace(cleanToken, '***'))
    }
  }

  /**
   * 绑定 WebSocket 事件
   */
  private bindEvents(): void {
    if (!this.ws) return

    this.ws.onopen = this.handleOpen.bind(this)
    this.ws.onmessage = this.handleMessage.bind(this)
    this.ws.onclose = this.handleClose.bind(this)
    this.ws.onerror = this.handleError.bind(this)
  }

  /**
   * 连接建立
   */
  private handleOpen(): void {
    console.log('[WsClient] 连接已建立')
    this.state = WsConnectionState.OPEN
    this.reconnectAttempts = 0
    
    // 启动心跳
    this.startHeartbeat()
    
    // 发送缓存消息
    this.flushMessageQueue()
    
    // 回调
    this.options.onConnect?.()
  }

  /**
   * 收到消息
   */
  private handleMessage(event: MessageEvent): void {
    try {
      const message: WsMessagePacket = JSON.parse(event.data)
      
      // 处理心跳响应
      if (message.type === WsMessageType.HEARTBEAT_PONG) {
        this.handleHeartbeatPong()
        return
      }
      
      if (import.meta.env.DEV) {
        console.log('[WsClient] 收到消息:', message.type, message.payload)
      }
      
      // 透传给业务层
      this.options.onMessage?.(message)
    } catch (error) {
      console.error('[WsClient] 解析消息失败:', error, event.data)
    }
  }

  /**
   * 连接关闭
   */
  private handleClose(event: CloseEvent): void {
    console.log(`[WsClient] 连接已关闭 - Code: ${event.code}, Reason: ${event.reason}`)
    this.state = WsConnectionState.CLOSED
    this.clearTimers()
    
    this.options.onDisconnect?.(event)
    
    // 判断是否需要重连
    if (this.shouldReconnect && this.isReconnectable(event.code)) {
      this.scheduleReconnect()
    }
  }

  /**
   * 错误处理
   */
  private handleError(error: Event): void {
    console.error('[WsClient] 连接错误:', error)
    this.options.onError?.(error)
    
    // 鉴权失败不上报，由业务层处理
    if (this.ws?.readyState === WebSocket.CLOSED) {
      console.error('[WsClient] 连接已关闭，可能是鉴权失败或服务器拒绝')
    }
  }

  /**
   * 判断是否可以重连
   */
  private isReconnectable(closeCode: number): boolean {
    // 1000: 正常关闭
    // 1001: 终端离开
    // 1005: 无状态码
    // 1006: 异常关闭（网络断开等）
    // 1011: 服务器异常
    const nonReconnectableCodes = [1000, 1001, 1008, 1011]
    return !nonReconnectableCodes.includes(closeCode)
  }

  /**
   * 计划重连
   */
  private scheduleReconnect(): void {
    if (this.reconnectAttempts >= WS_CONFIG.RECONNECT_MAX_ATTEMPTS) {
      console.error('[WsClient] 重连次数已达上限，停止重连')
      return
    }

    this.state = WsConnectionState.RECONNECTING
    this.reconnectAttempts++
    
    // 指数退避 + 抖动
    const delay = Math.min(
      WS_CONFIG.RECONNECT_INITIAL_DELAY * Math.pow(2, this.reconnectAttempts - 1),
      WS_CONFIG.RECONNECT_MAX_DELAY
    ) + Math.random() * 1000
    
    console.log(`[WsClient] 计划第 ${this.reconnectAttempts} 次重连，延迟 ${Math.round(delay)}ms`)
    this.options.onReconnect?.(this.reconnectAttempts)
    
    this.reconnectTimer = setTimeout(() => {
      this.connect()
    }, delay)
  }

  /**
   * 启动心跳
   */
  private startHeartbeat(): void {
    this.heartbeatTimer = setInterval(() => {
      if (this.ws?.readyState === WebSocket.OPEN) {
        // 发送心跳
        this.send({
          type: WsMessageType.HEARTBEAT_PING,
          timestamp: Date.now()
        })
        
        // 设置超时检测
        this.heartbeatTimeoutTimer = setTimeout(() => {
          console.warn('[WsClient] 心跳超时，关闭连接进行重连')
          this.ws?.close(3000, 'Heartbeat timeout')
        }, WS_CONFIG.HEARTBEAT_TIMEOUT)
      }
    }, WS_CONFIG.HEARTBEAT_INTERVAL)
  }

  /**
   * 处理心跳响应
   */
  private handleHeartbeatPong(): void {
    if (this.heartbeatTimeoutTimer) {
      clearTimeout(this.heartbeatTimeoutTimer)
      this.heartbeatTimeoutTimer = null
    }
  }

  /**
   * 清空定时器
   */
  private clearTimers(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer)
      this.heartbeatTimer = null
    }
    if (this.heartbeatTimeoutTimer) {
      clearTimeout(this.heartbeatTimeoutTimer)
      this.heartbeatTimeoutTimer = null
    }
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
  }

  /**
   * 发送缓存的消息
   */
  private flushMessageQueue(): void {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift()
      if (message) {
        this.send(message)
      }
    }
  }
}

/**
 * 创建 WebSocket 客户端的工厂函数
 */
export function createWsClient(options: WsClientOptions): WsClient {
  return new WsClient(options)
}

export default WsClient
