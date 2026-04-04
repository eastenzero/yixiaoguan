<template>
  <view class="chat-page">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="title">医小管</text>
    </view>

    <!-- 消息列表 -->
    <scroll-view
      class="message-list"
      scroll-y
      :scroll-top="scrollTop"
      :scroll-with-animation="true"
      @scrolltoupper="loadMoreHistory"
    >
      <!-- 空状态 -->
      <view v-if="!messages.length" class="empty-state">
        <view class="empty-icon">
          <IconSparkles :size="48" color="#ffffff" />
        </view>
        <text class="empty-title">医小管</text>
        <text class="empty-desc">同学你好！我是医小管智能助手。关于校园生活、选课安排、奖学金申请或办事流程，你都可以问我。</text>
        
        <!-- 快捷问题 -->
        <view class="quick-chips">
          <view
            v-for="q in quickQuestions"
            :key="q"
            class="chip"
            @click="sendQuickQuestion(q)"
          >
            <IconBookOpen :size="14" color="#006a64" />
            <text>{{ q }}</text>
          </view>
        </view>
      </view>

      <!-- 消息项 -->
      <view
        v-for="(msg, index) in messages"
        :key="msg.id"
        class="message-item"
        :class="msg.role"
      >
        <!-- AI 头像 -->
        <view v-if="msg.role === 'assistant'" class="avatar ai-avatar">
          <IconBot :size="24" color="#ffffff" />
        </view>

        <!-- 消息内容区 -->
        <view class="message-content">
          <!-- AI 名称标签 -->
          <text v-if="msg.role === 'assistant'" class="sender-name">医小管</text>

          <!-- 消息气泡 -->
          <view class="message-bubble" :class="msg.role">
            <!-- 打字中动画 -->
            <view v-if="msg.isStreaming && !msg.content" class="typing-animation">
              <view class="dot"></view>
              <view class="dot"></view>
              <view class="dot"></view>
            </view>

            <!-- AI 消息：使用 markdown-it 渲染富文本 -->
            <view
              v-else-if="msg.role === 'assistant'"
              class="message-text markdown-body"
              v-html="renderMarkdown(msg.content)"
            ></view>

            <!-- 用户消息：纯文本 -->
            <view v-else class="message-text">
              <text>{{ msg.content }}</text>
            </view>

            <!-- 流式输出闪烁光标（追加在气泡内容后） -->
            <text v-if="msg.isStreaming && msg.content" class="cursor">|</text>
          </view>

          <!-- 来源引用 -->
          <view v-if="msg.sources && msg.sources.length && !msg.isStreaming" class="message-sources">
            <view class="sources-header">
              <IconBookOpen :size="12" color="#76777A" />
              <text>参考资料：</text>
            </view>
            <view
              v-for="(source, si) in msg.sources"
              :key="source.entry_id || si"
              class="source-item"
              @click="handleSourceClick(source)"
            >
              <text class="source-num">{{ si + 1 }}.</text>
              <text class="source-title">{{ source.title }}</text>
            </view>
          </view>

          <!-- 时间戳和复制按钮 -->
          <view class="message-meta">
            <text class="timestamp">{{ formatTime(msg.timestamp) }}</text>
            <view
              v-if="msg.role === 'assistant' && msg.content"
              class="copy-btn"
              @click="copyMessage(msg)"
            >
              <IconCheck v-if="copiedId === msg.id" :size="14" color="#4CAF50" />
              <IconCopy v-else :size="14" color="#76777A" />
            </view>
          </view>
        </view>

        <!-- 用户头像 -->
        <view v-if="msg.role === 'user'" class="avatar user-avatar">
          <IconUser :size="20" color="#76777A" />
        </view>
      </view>

      <!-- 正在输入指示器（AI 思考中） -->
      <view v-if="isTyping" class="typing-indicator">
        <view class="avatar ai-avatar">
          <IconBot :size="24" color="#ffffff" />
        </view>
        <view class="typing-content">
          <text class="typing-text">AI 正在思考</text>
          <view class="thinking-dots">
            <view class="dot"></view>
            <view class="dot"></view>
            <view class="dot"></view>
          </view>
        </view>
      </view>

      <!-- 底部占位 -->
      <view class="list-footer"></view>
    </scroll-view>

    <!-- 快捷问题（有消息时显示在输入框上方） -->
    <view v-if="messages.length > 0" class="quick-questions-bar">
      <scroll-view scroll-x class="quick-questions-scroll" show-scrollbar="false">
        <view class="quick-questions-content">
          <view
            v-for="q in quickQuestions"
            :key="q"
            class="question-chip"
            @click="sendQuickQuestion(q)"
          >
            {{ q }}
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- 输入区域 -->
    <view class="input-area" :style="{ paddingBottom: safeAreaBottom + 'px' }">
      <view class="input-wrapper">
        <input
          v-model="inputMessage"
          class="message-input"
          placeholder="请输入问题..."
          :disabled="isStreaming"
          confirm-type="send"
          @confirm="sendMessage"
        />
        <button
          class="send-btn"
          :disabled="!canSend"
          :class="{ active: canSend }"
          @click="sendMessage"
        >
          <IconSend :size="20" :color="canSend ? '#ffffff' : '#C7C6CA'" />
        </button>
      </view>
    </view>

    <view v-if="sourcePreview.visible" class="source-preview-mask" @click="closeSourcePreview">
      <view class="source-preview-panel" @click.stop>
        <view class="source-preview-header">
          <text class="source-preview-label">参考摘要</text>
          <text class="source-preview-score" v-if="sourcePreview.score !== undefined">
            相关度 {{ Math.round(sourcePreview.score * 100) }}%
          </text>
        </view>

        <text class="source-preview-title">{{ sourcePreview.title }}</text>
        <text class="source-preview-content">{{ sourcePreview.content }}</text>

        <view class="source-preview-actions">
          <button
            v-if="sourcePreview.entryId"
            class="preview-btn preview-btn-primary"
            @click="openSourceDetailFromPreview"
          >
            查看完整资料
          </button>
          <button class="preview-btn preview-btn-ghost" @click="closeSourcePreview">
            知道了
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import MarkdownIt from 'markdown-it'
import IconSend from '@/components/icons/IconSend.vue'
import IconCopy from '@/components/icons/IconCopy.vue'
import IconCheck from '@/components/icons/IconCheck.vue'
import IconBot from '@/components/icons/IconBot.vue'
import IconUser from '@/components/icons/IconUser.vue'
import IconSparkles from '@/components/icons/IconSparkles.vue'
import IconBookOpen from '@/components/icons/IconBookOpen.vue'

// ============ Markdown 渲染器 ============
const md = new MarkdownIt({
  html: false,        // 禁止 HTML 注入（安全）
  linkify: true,      // 自动识别 URL
  typographer: false,
  breaks: true        // \n 转 <br>
})

function renderMarkdown(content: string): string {
  if (!content) return ''
  return md.render(content)
}

// ============ 类型定义 ============
interface Source {
  entry_id: string
  title: string
  content?: string
  url: string        // 备用外链（当前 AI 服务暂不提供）
  score?: number
}

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  sources?: Source[]
  timestamp: number
  isStreaming?: boolean
}

// ============ 响应式状态 ============
const messages = ref<Message[]>([])
const inputMessage = ref('')
const isStreaming = ref(false)
const isTyping = ref(false)
const scrollTop = ref(0)
const safeAreaBottom = ref(0)
const copiedId = ref<string | null>(null)
const sourcePreview = ref<{
  visible: boolean
  entryId: string
  title: string
  content: string
  score?: number
}>({
  visible: false,
  entryId: '',
  title: '',
  content: '',
  score: undefined
})

// ============ 快捷问题 ============
const quickQuestions = [
  '请假流程是什么？',
  '如何申请奖学金？',
  '图书馆几点开门？',
  '成绩怎么查询？'
]

// ============ 计算属性 ============
const canSend = computed(() => {
  return inputMessage.value.trim().length > 0 && !isStreaming.value
})

// ============ 生命周期 ============
onLoad(() => {
  // 获取安全区域高度
  const systemInfo = uni.getSystemInfoSync()
  safeAreaBottom.value = systemInfo.safeAreaInsets?.bottom || 0
  
  // 加载历史消息
  loadHistory()
})

// ============ 历史消息加载 ============
async function loadHistory() {
  try {
    const { data, statusCode } = await uni.request({
      url: '/api/chat/history?limit=50',
      method: 'GET',
      header: {
        'Authorization': `Bearer ${uni.getStorageSync('token') || ''}`
      }
    }) as any
    
    // API 不存在时不报错（404）
    if (statusCode === 404) {
      console.log('历史消息 API 未实现，跳过加载')
      return
    }
    
    if (data && Array.isArray(data.data)) {
      messages.value = data.data.map((m: any) => ({
        id: m.id || String(Date.now() + Math.random()),
        role: m.role || 'assistant',
        content: m.content || '',
        sources: m.sources || [],
        timestamp: m.timestamp || Date.now()
      }))
      scrollToBottom()
    }
  } catch (error) {
    // 静默处理，不显示错误（首次使用或 API 未实现）
    console.log('历史消息加载:', error)
  }
}

// ============ 加载更多历史（分页） ============
async function loadMoreHistory() {
  // P1 功能：后续可实现分页加载
}

// ============ 发送消息 ============
async function sendMessage() {
  const content = inputMessage.value.trim()
  if (!content || isStreaming.value) return

  // 添加用户消息
  const userMessage: Message = {
    id: `user-${Date.now()}`,
    role: 'user',
    content,
    timestamp: Date.now()
  }
  messages.value.push(userMessage)
  inputMessage.value = ''
  scrollToBottom()

  // 开始流式响应
  await streamResponse(content)
}

// ============ 快捷问题发送 ============
function sendQuickQuestion(question: string) {
  if (isStreaming.value) return
  // 直接设置输入和发送，避免 async 读取竞态
  inputMessage.value = question
  sendMessage()
}

// ============ SSE 流式响应 ============
async function streamResponse(userContent: string) {
  isStreaming.value = true
  isTyping.value = true

  // 创建 AI 消息占位
  const aiMessage: Message = {
    id: `assistant-${Date.now()}`,
    role: 'assistant',
    content: '',
    sources: [],
    timestamp: Date.now(),
    isStreaming: true
  }

  try {
    // 延迟一点显示 AI 消息（更自然的体验）
    await new Promise(resolve => setTimeout(resolve, 500))
    isTyping.value = false
    messages.value.push(aiMessage)
    scrollToBottom()

    // 发起 SSE 请求（通过代理转发到 AI 服务 :8000）
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${uni.getStorageSync('token') || ''}`
      },
      body: JSON.stringify({
        query: userContent,
        use_kb: true
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    
    // 用于打字机及来源显示的临时变量
    let allChunks: string[] = []
    let pendingSources: Source[] = []

    while (true) {
      const { value, done } = await reader.read()
      if (done) break

      const chunk = decoder.decode(value, { stream: true })
      buffer += chunk

      // 处理 buffer 中的完整行
      const lines = buffer.split('\n')
      buffer = lines.pop() || '' // 保留不完整的最后一行

      for (const line of lines) {
        if (line.trim() === '') continue
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6).trim()

          try {
            const data = JSON.parse(dataStr)

            // 收集所有 chunk，最后统一打字机
            if (data.chunk !== undefined && data.chunk !== '') {
              allChunks.push(data.chunk)
            }

            // 收集来源
            if (data.sources && Array.isArray(data.sources) && data.sources.length) {
              pendingSources = data.sources.map((s: any) => ({
                entry_id: s.entry_id || '',
                title: s.title || '未知来源',
                content: s.content || '',
                url: s.url || '',
                score: s.score
              }))
            }

            if (data.is_end === true) break
            if (data.error) throw new Error(data.error)

          } catch (e: any) {
            if (e.message && !e.message.includes('JSON')) throw e
            console.warn('SSE JSON parse skipped:', dataStr.substring(0, 50))
          }
        }
      }
    }

    // 处理 buffer 中剩余的数据
    if (buffer.trim()) {
      const line = buffer.trim()
      if (line.startsWith('data: ')) {
        const dataStr = line.slice(6).trim()
        try {
          const data = JSON.parse(dataStr)
          if (data.chunk !== undefined && data.chunk !== '') allChunks.push(data.chunk)
          if (data.sources && Array.isArray(data.sources) && data.sources.length) {
            pendingSources = data.sources.map((s: any) => ({
              entry_id: s.entry_id || '',
              title: s.title || '未知来源',
              content: s.content || '',
              url: s.url || '',
              score: s.score
            }))
          }
        } catch (e) { /* 忽略不完整 JSON */ }
      }
    }

    // ======================================================
    // 前端打字机效果
    // 所有 chunk 已接收完毕（DashScope 每个 chunk 是累积全文）
    // 逐步播放，每个 chunk 显示一小段时间再更新
    // ======================================================
    await playChunks(aiMessage, allChunks, pendingSources)

  } catch (error: any) {
    console.error('Stream error:', error)
    isTyping.value = false
    
    // 根据错误类型显示不同提示
    let errorMsg = '抱歉，AI 服务暂时不可用，请稍后重试。'
    if (error.message?.includes('404')) {
      errorMsg = 'AI 服务接口暂未实现，请联系管理员。'
    } else if (error.message?.includes('Failed to fetch') || error.message?.includes('NetworkError')) {
      errorMsg = '网络连接失败，请检查网络或后端服务是否启动。'
    } else if (error.message?.includes('401')) {
      errorMsg = '登录已过期，请重新登录。'
    }
    
    // 更新为错误消息或兜底回复
    const index = messages.value.findIndex(m => m.id === aiMessage.id)
    if (index !== -1) {
      messages.value[index].content = errorMsg
      messages.value[index].isStreaming = false
    } else if (messages.value[messages.value.length - 1]?.role !== 'assistant') {
      // 如果 AI 消息还未添加，添加一个错误消息
      messages.value.push({
        id: `assistant-error-${Date.now()}`,
        role: 'assistant',
        content: errorMsg,
        timestamp: Date.now(),
        isStreaming: false
      })
    }
    scrollToBottom()
  } finally {
    isStreaming.value = false
    isTyping.value = false
  }
}

// ============ 前端打字机效果驱动函数 ============
async function playChunks(
  aiMessage: Message, 
  chunks: string[], 
  sources: Source[]
) {
  // 获取具有响应式的 proxy 对象
  const getReactiveMsg = () => messages.value.find(m => m.id === aiMessage.id) || aiMessage
  
  if (chunks.length === 0) {
    getReactiveMsg().isStreaming = false
    return
  }
  
  // 必须赋值给 Proxy 对象，否则 sources 的增加不会触发 Vue 视图刷新
  if (sources.length > 0) {
    getReactiveMsg().sources = sources
  }
  
  // 对于 Dashscope，由于都是增量累积全文，只需模拟进度
  for (let i = 0; i < chunks.length; i++) {
    getReactiveMsg().content = chunks[i]
    scrollToBottom()
    
    // 我们控制最快 30ms 一帧的播放速度，给 Vue 渲染喘息时间
    await new Promise(resolve => setTimeout(resolve, 30))
  }
  
  getReactiveMsg().isStreaming = false
  scrollToBottom()
}

// ============ 获取会话 ID ============
function getConversationId(): string {
  // 从第一条消息生成或使用存储的 ID
  return uni.getStorageSync('chat_conversation_id') || `conv-${Date.now()}`
}

function normalizeEntryId(rawEntryId: string): number | null {
  if (!rawEntryId) return null
  const parsed = Number(rawEntryId)
  if (!Number.isFinite(parsed) || parsed <= 0) return null
  return parsed
}

function buildKnowledgeDetailUrl(source: Source, entryId: number): string {
  const title = encodeURIComponent(source.title || '')
  const summary = encodeURIComponent((source.content || '').slice(0, 300))
  const score = source.score !== undefined ? source.score : ''
  return `/pages/knowledge/detail?id=${entryId}&title=${title}&summary=${summary}&score=${score}`
}

function navigateToPage(url: string): Promise<void> {
  return new Promise((resolve, reject) => {
    uni.navigateTo({
      url,
      success: () => resolve(),
      fail: (error) => reject(error)
    })
  })
}

function showSourcePreview(source: Source) {
  sourcePreview.value = {
    visible: true,
    entryId: source.entry_id || '',
    title: source.title || '参考资料',
    content: source.content || '暂未获取到摘要内容，可稍后重试查看详情。',
    score: source.score
  }
}

function closeSourcePreview() {
  sourcePreview.value.visible = false
}

async function openSourceDetailFromPreview() {
  const source = sourcePreview.value
  if (!source.entryId) {
    closeSourcePreview()
    return
  }
  try {
    await navigateToPage(
      `/pages/knowledge/detail?id=${encodeURIComponent(source.entryId)}&title=${encodeURIComponent(source.title)}&summary=${encodeURIComponent(source.content)}&score=${source.score ?? ''}`
    )
    closeSourcePreview()
  } catch {
    uni.showToast({
      title: '详情页暂不可用',
      icon: 'none'
    })
  }
}

async function handleSourceClick(source: Source) {
  if (source.entry_id) {
    try {
      await navigateToPage(
        `/pages/knowledge/detail?id=${encodeURIComponent(source.entry_id)}&title=${encodeURIComponent(source.title || '')}&summary=${encodeURIComponent((source.content || '').slice(0, 300))}&score=${source.score ?? ''}`
      )
      return
    } catch (error) {
      console.warn('来源详情跳转失败，尝试降级展示：', error)
    }
  }

  if (source.url) {
    handleLinkClick(source.url)
    return
  }

  showSourcePreview(source)
}

// ============ Markdown 链接解析 ============
interface ContentPart {
  type: 'text' | 'link'
  content: string
  url?: string
}

function parseContent(content: string): ContentPart[] {
  if (!content) return [{ type: 'text', content: '' }]
  
  const parts: ContentPart[] = []
  // 匹配 [文本](/路径) 格式的正则
  const regex = /\[([^\]]+)\]\(([^)]+)\)/g
  let lastIndex = 0
  let match

  while ((match = regex.exec(content)) !== null) {
    // 添加匹配前的文本
    if (match.index > lastIndex) {
      parts.push({
        type: 'text',
        content: content.slice(lastIndex, match.index)
      })
    }
    // 添加链接
    parts.push({
      type: 'link',
      content: match[1],
      url: match[2]
    })
    lastIndex = match.index + match[0].length
  }

  // 添加剩余文本
  if (lastIndex < content.length) {
    parts.push({
      type: 'text',
      content: content.slice(lastIndex)
    })
  }

  return parts.length > 0 ? parts : [{ type: 'text', content }]
}

// ============ 链接点击处理 ============
function handleLinkClick(url: string) {
  if (!url) return
  
  // 内部导航
  if (url.startsWith('/')) {
    uni.navigateTo({
      url,
      fail: () => {
        uni.switchTab({ url })
      }
    })
  } else {
    // 外部链接
    uni.showModal({
      title: '外部链接',
      content: `是否打开链接：${url}`,
      success: (res) => {
        if (res.confirm) {
          // #ifdef H5
          window.open(url, '_blank')
          // #endif
          // #ifndef H5
          uni.setClipboardData({
            data: url,
            success: () => {
              uni.showToast({
                title: '链接已复制',
                icon: 'success'
              })
            }
          })
          // #endif
        }
      }
    })
  }
}

// ============ 复制消息 ============
function copyMessage(msg: Message) {
  uni.setClipboardData({
    data: msg.content,
    success: () => {
      copiedId.value = msg.id
      uni.showToast({
        title: '已复制',
        icon: 'success',
        duration: 1500
      })
      setTimeout(() => {
        copiedId.value = null
      }, 2000)
    }
  })
}

// ============ 时间格式化 ============
function formatTime(timestamp: number): string {
  if (!timestamp) return ''
  
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 小于 1 分钟
  if (diff < 60000) {
    return '刚刚'
  }
  
  // 小于 1 小时
  if (diff < 3600000) {
    return `${Math.floor(diff / 60000)}分钟前`
  }
  
  // 今天
  if (date.toDateString() === now.toDateString()) {
    return `今天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
  }
  
  // 昨天
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return `昨天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
  }
  
  // 更早
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

// ============ 滚动到底部 ============
function scrollToBottom() {
  nextTick(() => {
    scrollTop.value = 9999999 + Math.random()
  })
}
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

// ============ 页面布局 ============
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background: linear-gradient(180deg, #f5f5f9 0%, #f0f4f3 100%);
  overflow: hidden;
}

// ============ 导航栏 ============
.navbar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  padding-top: var(--status-bar-height, 44px);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  flex-shrink: 0;

  .title {
    font: $text-headline-medium;
    color: $md-sys-color-on-background;
  }
}

// ============ 消息列表 ============
.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: $md-sys-color-background;
}

// ============ 空状态 ============
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 32px;
  text-align: center;

  .empty-icon {
    width: 80px;
    height: 80px;
    border-radius: $radius-xl;
    background: linear-gradient(135deg, #006a64 0%, #008a83 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 16px;
    animation: float 3s ease-in-out infinite;
  }

  .empty-title {
    font: $text-headline-medium;
    color: $md-sys-color-on-background;
    margin-bottom: 8px;
  }

  .empty-desc {
    font: $text-body-medium;
    color: $md-sys-color-on-surface-variant;
    line-height: 1.6;
    max-width: 280px;
    margin-bottom: 24px;
  }
}

// ============ 快捷问题 Chips（空状态） ============
.quick-chips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 10px;
  max-width: 320px;

  .chip {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    background: white;
    border-radius: $radius-full;
    border: 1px solid $primary-40;
    font: $text-body-small;
    color: $primary-40;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    transition: all 0.2s ease;

    &:active {
      transform: scale(0.96);
      background: $primary-95;
    }
  }
}

// ============ 消息项 ============
.message-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  animation: fadeInUp 0.3s ease-out;

  &.user {
    justify-content: flex-end;
  }

  &.assistant {
    justify-content: flex-start;
  }
}

// ============ 头像 ============
.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &.ai-avatar {
    background: linear-gradient(135deg, $primary-40 0%, #008a7a 100%);
    margin-right: 10px;
    box-shadow: 0 2px 8px rgba(0, 106, 100, 0.25);
  }

  &.user-avatar {
    background: white;
    margin-left: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }
}

// ============ 消息内容区 ============
.message-content {
  display: flex;
  flex-direction: column;
  max-width: 75%;
}

.sender-name {
  font: $text-label-small;
  color: $md-sys-color-on-surface-variant;
  margin-bottom: 4px;
  margin-left: 12px;
}

// ============ 消息气泡 ============
.message-bubble {
  padding: 12px 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  word-break: break-word;

  &.user {
    background: linear-gradient(135deg, #006a64 0%, #007c75 100%);
    border-radius: 18px 18px 4px 18px;
    color: #ffffff;
  }

  &.assistant {
    background: #ffffff;
    border-radius: 4px 18px 18px 18px;
    color: $md-sys-color-on-background;
    box-shadow: 0 6px 16px rgba(23, 29, 28, 0.06);
  }
}

.message-text {
  font: $text-body-medium;
  line-height: 1.6;
}

// ============ Markdown 渲染样式 ============
.markdown-body {
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;

  > *:first-child { margin-top: 0 !important; }
  > *:last-child  { margin-bottom: 0 !important; }

  p { margin: 0 0 8px 0; &:last-child { margin-bottom: 0; } }

  strong, b { font-weight: 600; color: #006a64; }

  h1, h2, h3, h4 {
    font-weight: 600;
    margin: 12px 0 6px 0;
    line-height: 1.4;
  }
  h1 { font-size: 18px; }
  h2 { font-size: 16px; }
  h3 { font-size: 15px; }

  ul, ol { margin: 6px 0; padding-left: 20px; }
  li { margin: 3px 0; line-height: 1.6; }

  code {
    background: rgba(0, 106, 100, 0.1);
    border-radius: 4px;
    padding: 2px 5px;
    font-family: 'Menlo', 'Monaco', monospace;
    font-size: 12px;
    color: #006a64;
  }

  pre {
    background: rgba(0, 0, 0, 0.04);
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
    margin: 8px 0;
    code { background: transparent; padding: 0; color: inherit; }
  }

  a { color: $primary-40; text-decoration: underline; }

  blockquote {
    border-left: 3px solid rgba(0, 106, 100, 0.4);
    padding-left: 12px;
    margin: 8px 0;
    color: $md-sys-color-on-surface-variant;
  }

  hr { border: none; border-top: 1px solid rgba(0,0,0,0.08); margin: 10px 0; }
}

// ============ 旧版 Markdown 链接样式（兼容保留） ============
.markdown-link {
  color: $primary-40;
  text-decoration: underline;
  text-decoration-color: rgba(0, 106, 100, 0.4);
  cursor: pointer;
  &:active { opacity: 0.7; }
}

// ============ 闪烁光标（打字机效果） ============
.cursor {
  display: inline-block;
  color: $primary-40;
  animation: blink 1s infinite;
  margin-left: 2px;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

// ============ 打字动画（AI 思考中） ============
.typing-animation {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 24px;
  padding: 0 4px;

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: $primary-40;
    animation: typingBounce 1.4s infinite ease-in-out both;

    &:nth-child(1) { animation-delay: -0.32s; }
    &:nth-child(2) { animation-delay: -0.16s; }
  }
}

@keyframes typingBounce {
  0%, 80%, 100% { transform: scale(0.6); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

// ============ 来源引用 ============
.message-sources {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  margin-top: 8px;
  margin-left: 4px;
  padding: 12px 14px;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: $md-sys-elevation-1;

  .sources-header {
    display: flex;
    align-items: center;
    gap: 4px;
    font: $text-label-small;
    color: $md-sys-color-on-surface-variant;
  }

  .source-item {
    display: flex;
    align-items: center;
    gap: 4px;
    width: 100%;
    padding: 8px 10px;
    border-radius: 8px;
    background: $md-sys-color-surface-container-low;
    transition: all 0.2s ease;

    .source-num {
      font: $text-label-small;
      color: $primary-40;
      flex-shrink: 0;
    }

    .source-title {
      flex: 1;
      font: $text-label-medium;
      color: $md-sys-color-on-surface;
    }

    &::after {
      content: '›';
      font-size: 16px;
      color: $md-sys-color-outline;
      margin-left: 4px;
    }

    &:active {
      transform: scale(0.98);
      background: $md-sys-color-surface-container;
    }
  }
}

// ============ 消息元信息（时间戳、复制） ============
.message-meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
  margin-left: 12px;

  .timestamp {
    font: $text-label-small;
    color: $neutral-50;
  }

  .copy-btn {
    padding: 4px;
    border-radius: 4px;
    transition: background 0.2s;

    &:active {
      background: rgba(0, 0, 0, 0.05);
    }
  }
}

// ============ 正在输入指示器 ============
.typing-indicator {
  display: flex;
  align-items: flex-start;
  margin-bottom: 20px;
  animation: fadeIn 0.3s ease-out;

  .typing-content {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    background: linear-gradient(135deg, #e8f5f4 0%, #f0f9f7 100%);
    border-radius: 4px 18px 18px 18px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  }

  .typing-text {
    font: $text-body-small;
    color: $neutral-50;
  }

  .thinking-dots {
    display: flex;
    gap: 3px;

    .dot {
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: $neutral-50;
      animation: typingBounce 1.4s infinite ease-in-out both;

      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
    }
  }
}

// ============ 底部占位 ============
.list-footer {
  height: 16px;
}

// ============ 快捷问题栏（有消息时） ============
.quick-questions-bar {
  flex-shrink: 0;
  padding: 8px 0;
  background: transparent;
}

.quick-questions-scroll {
  white-space: nowrap;
}

.quick-questions-content {
  display: inline-flex;
  gap: 8px;
  padding: 0 16px;
}

.question-chip {
  display: inline-flex;
  padding: 8px 14px;
  background: white;
  border-radius: 16px;
  font: $text-body-small;
  color: $md-sys-color-on-background;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.96);
    background: $primary-95;
  }
}

// ============ 输入区域 ============
.input-area {
  flex-shrink: 0;
  padding: 12px 16px;
  padding-bottom: calc(12px + env(safe-area-inset-bottom, 0));
  background: $md-sys-color-surface;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 10px;
}

.message-input {
  flex: 1;
  height: 44px;
  padding: 0 16px;
  background: $neutral-95;
  border-radius: 22px;
  font: $text-body-medium;
  color: $md-sys-color-on-background;
  border: none;
  outline: none;

  &::placeholder {
    color: $neutral-50;
  }
}

.send-btn {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: $neutral-90;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin: 0;
  border: none;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.95);
  }

  &.active {
    background: linear-gradient(135deg, $primary-40 0%, #008a7a 100%);
    box-shadow: 0 2px 8px rgba(0, 106, 100, 0.3);
  }

  &:disabled {
    opacity: 0.6;
  }
}

.source-preview-mask {
  position: fixed;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  z-index: 30;
  display: flex;
  align-items: flex-end;
  background: rgba(0, 0, 0, 0.38);
}

.source-preview-panel {
  width: 100%;
  border-radius: 20px 20px 0 0;
  background: #ffffff;
  padding: 18px 16px 0;
  box-shadow: 0 -8px 24px rgba(23, 29, 28, 0.12);
  max-height: 75vh;
  display: flex;
  flex-direction: column;
}

.source-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.source-preview-label {
  font: $text-label-medium;
  color: #006a64;
}

.source-preview-score {
  font: $text-label-small;
  color: #5b5e66;
}

.source-preview-title {
  display: block;
  font: $text-title-medium;
  color: #1a1c1e;
  margin-bottom: 8px;
}

.source-preview-content {
  display: block;
  flex: 1;
  min-height: 0;
  font: $text-body-medium;
  color: #2f3033;
  line-height: 1.6;
  overflow-y: auto;
}

.source-preview-actions {
  flex-shrink: 0;
  display: flex;
  gap: 10px;
  margin-top: 16px;
  padding-bottom: calc(18px + env(safe-area-inset-bottom, 0));
}

.preview-btn {
  flex: 1;
  height: 40px;
  line-height: 40px;
  border-radius: 999px;
  border: none;
  margin: 0;
  padding: 0;
  font: $text-label-large;

  &:active {
    transform: scale(0.98);
  }
}

.preview-btn-primary {
  background: #006a64;
  color: #ffffff;
}

.preview-btn-ghost {
  background: rgba(0, 106, 100, 0.08);
  color: #006a64;
}

// ============ 动画 ============
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
</style>
