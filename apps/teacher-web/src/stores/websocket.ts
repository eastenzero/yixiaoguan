/**
 * WebSocket Store - 全局 WebSocket 状态管理
 * 
 * 用途：
 * - 管理与服务器的长连接
 * - 接收全局通知、消息推送
 * - 支持多会话管理
 * 
 * 注意：实际业务中的会话级 WebSocket 应在组件内使用 createWsClient 创建
 */

import { defineStore } from 'pinia'
import { ref, computed, markRaw } from 'vue'
import { ElMessage, ElNotification } from 'element-plus'
import { WsClient, WsConnectionState, WsMessageType, type WsMessagePacket } from '@/utils/ws'

export interface NotificationMessage {
  id: number
  type: 'info' | 'success' | 'warning' | 'error'
  title: string
  content: string
  timestamp: string
  isRead: boolean
}

export const useWebsocketStore = defineStore('websocket', () => {
  // ===== State =====
  const isConnected = ref(false)
  const connectionState = ref<WsConnectionState>(WsConnectionState.CLOSED)
  const reconnectAttempts = ref(0)
  const notifications = ref<NotificationMessage[]>([])
  const unreadCount = computed(() => notifications.value.filter(n => !n.isRead).length)
  
  // 当前激活的会话 WebSocket 客户端
  const activeClients = ref<Map<number, WsClient>>(new Map())

  // ===== Getters =====
  const hasUnread = computed(() => unreadCount.value > 0)
  
  // ===== Actions =====
  
  /**
   * 添加通知
   */
  function addNotification(notification: Omit<NotificationMessage, 'id' | 'timestamp' | 'isRead'>) {
    const newNotification: NotificationMessage = {
      ...notification,
      id: Date.now(),
      timestamp: new Date().toISOString(),
      isRead: false
    }
    notifications.value.unshift(newNotification)
    
    // 限制通知数量
    if (notifications.value.length > 50) {
      notifications.value = notifications.value.slice(0, 50)
    }
  }

  /**
   * 标记通知为已读
   */
  function markAsRead(id: number) {
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.isRead = true
    }
  }

  /**
   * 标记所有通知为已读
   */
  function markAllAsRead() {
    notifications.value.forEach(n => n.isRead = true)
  }

  /**
   * 清空通知
   */
  function clearNotifications() {
    notifications.value = []
  }

  /**
   * 创建并连接会话 WebSocket
   * @param conversationId 会话ID
   * @param callbacks 回调函数
   */
  function connectConversation(
    conversationId: number,
    callbacks?: {
      onMessage?: (msg: WsMessagePacket) => void
      onConnect?: () => void
      onDisconnect?: () => void
    }
  ): WsClient {
    // 如果已存在，先断开
    const existingClient = activeClients.value.get(conversationId)
    if (existingClient) {
      existingClient.disconnect(true)
    }

    const client = new WsClient({
      conversationId,
      onConnect: () => {
        console.log(`[WebSocketStore] 会话 ${conversationId} 连接成功`)
        callbacks?.onConnect?.()
      },
      onDisconnect: () => {
        console.log(`[WebSocketStore] 会话 ${conversationId} 连接断开`)
        activeClients.value.delete(conversationId)
        callbacks?.onDisconnect?.()
      },
      onMessage: (msg) => {
        handleConversationMessage(conversationId, msg)
        callbacks?.onMessage?.(msg)
      },
      onError: (error) => {
        console.error(`[WebSocketStore] 会话 ${conversationId} 连接错误:`, error)
      },
      onReconnect: (attempt) => {
        console.log(`[WebSocketStore] 会话 ${conversationId} 第 ${attempt} 次重连`)
      }
    })

    // 使用 markRaw 避免 Vue 代理 WebSocket 对象
    activeClients.value.set(conversationId, markRaw(client))
    client.connect()
    
    return client
  }

  /**
   * 断开会话 WebSocket
   */
  function disconnectConversation(conversationId: number, permanent: boolean = true) {
    const client = activeClients.value.get(conversationId)
    if (client) {
      client.disconnect(permanent)
      activeClients.value.delete(conversationId)
    }
  }

  /**
   * 断开所有 WebSocket 连接
   */
  function disconnectAll() {
    activeClients.value.forEach((client, id) => {
      client.disconnect(true)
    })
    activeClients.value.clear()
  }

  /**
   * 处理会话消息
   */
  function handleConversationMessage(conversationId: number, msg: WsMessagePacket) {
    switch (msg.type) {
      case WsMessageType.NEW_MESSAGE:
        // 收到新消息通知
        if (msg.payload?.senderType === 1) { // 学生发来的消息
          addNotification({
            type: 'info',
            title: '新消息',
            content: `会话 ${conversationId} 收到新消息: ${msg.payload.content?.slice(0, 30)}...`
          })
        }
        break
        
      case WsMessageType.TEACHER_JOINED:
        // 其他教师接入通知
        ElNotification({
          title: '会话更新',
          message: `其他教师已接入会话 ${conversationId}`,
          type: 'info'
        })
        break
        
      case WsMessageType.ERROR:
        // 错误通知
        ElMessage.error(msg.payload?.message || 'WebSocket 错误')
        break
        
      default:
        break
    }
  }

  /**
   * 发送消息到指定会话
   */
  function sendToConversation(conversationId: number, content: string, messageType: number = 1): boolean {
    const client = activeClients.value.get(conversationId)
    if (!client) {
      console.error(`[WebSocketStore] 会话 ${conversationId} 未连接`)
      return false
    }
    return client.sendChatMessage(content, messageType)
  }

  /**
   * 获取会话连接状态
   */
  function getConversationState(conversationId: number): WsConnectionState {
    const client = activeClients.value.get(conversationId)
    return client?.getState() || WsConnectionState.CLOSED
  }

  // ===== 测试功能：初始化全局通知 WebSocket =====
  /**
   * 初始化全局通知连接（测试用）
   * 连接到指定会话进行测试
   */
  function initTestConnection(conversationId: number = 1) {
    const client = connectConversation(conversationId, {
      onConnect: () => {
        isConnected.value = true
        connectionState.value = WsConnectionState.OPEN
        reconnectAttempts.value = 0
        
        ElNotification({
          title: 'WebSocket 已连接',
          message: `成功连接到会话 ${conversationId}`,
          type: 'success'
        })
        
        // 发送测试消息
        setTimeout(() => {
          sendToConversation(conversationId, '教师已接入会话', 1)
        }, 1000)
      },
      onDisconnect: () => {
        isConnected.value = false
        connectionState.value = WsConnectionState.CLOSED
      },
      onMessage: (msg) => {
        console.log('[WebSocketStore] 收到消息:', msg)
        
        if (msg.type === WsMessageType.NEW_MESSAGE && msg.payload?.senderType === 2) {
          // AI 回复
          ElNotification({
            title: 'AI 回复',
            message: msg.payload.content?.slice(0, 50) + '...',
            type: 'info'
          })
        }
      }
    })
    
    return client
  }

  return {
    // State
    isConnected,
    connectionState,
    reconnectAttempts,
    notifications,
    unreadCount,
    activeClients,
    
    // Getters
    hasUnread,
    
    // Actions
    addNotification,
    markAsRead,
    markAllAsRead,
    clearNotifications,
    connectConversation,
    disconnectConversation,
    disconnectAll,
    sendToConversation,
    getConversationState,
    initTestConnection
  }
})
