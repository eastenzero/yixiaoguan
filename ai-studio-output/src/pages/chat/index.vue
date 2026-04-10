<template>
  <view class="chat-page">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="title">医小管</text>
      <!-- 新增历史按钮 -->
      <view class="nav-actions">
        <view class="history-btn" @click="goToHistory">
          <text class="icon">📋</text>
        </view>
      </view>
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
            <IconBookOpen :size="14" color="var(--color-primary, #7C3AED)" />
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
              <IconBookOpen :size="12" color="#94A3B8" />
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
              <IconCheck v-if="copiedId === msg.id" :size="14" color="#059669" />
              <IconCopy v-else :size="14" color="#94A3B8" />
            </view>
          </view>
        </view>

        <!-- 用户头像 -->
        <view v-if="msg.role === 'user'" class="avatar user-avatar">
          <IconUser :size="20" color="#94A3B8" />
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
          <IconSend :size="20" :color="canSend ? '#ffffff' : '#94A3B8'" />
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
        <view 
          class="source-preview-content markdown-body" 
          v-html="renderMarkdown(sourcePreview.content)"
        ></view>

        <view class="source-preview-actions">
          <button
            v-if="sourcePreview.entryId || sourcePreview.materialFileUrl"
            class="preview-btn preview-btn-primary"
            :class="{ 'preview-btn-disabled': !sourcePreview.materialFileUrl && !sourcePreview.entryId }"
            :disabled="!sourcePreview.materialFileUrl && !sourcePreview.entryId"
            @click="openSourceDetailFromPreview"
          >
            查看详细资料
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
import { ref, computed, nextTick, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import MarkdownIt from 'markdown-it'
import IconSend from '@/components/icons/IconSend.vue'
import IconCopy from '@/components/icons/IconCopy.vue'
import IconCheck from '@/components/icons/IconCheck.vue'
import IconBot from '@/components/icons/IconBot.vue'
import IconUser from '@/components/icons/IconUser.vue'
import IconSparkles from '@/components/icons/IconSparkles.vue'
import IconBookOpen from '@/components/icons/IconBookOpen.vue'
import { 
  createConversation, 
  getHistory, 
  sendMessage as sendMessageAPI
} from '@/api/chat'

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
  material_file_url?: string
  material_title?: string
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
const conversationId = ref<number | null>(null)
const sourcePreview = ref<{
  visible: boolean
  entryId: string
  title: string
  content: string
  score?: number
  materialFileUrl?: string
}>({
  visible: false,
  entryId: '',
  title: '',
  content: '',
  score: undefined,
  materialFileUrl: undefined
})

// ============ 快捷问题 ============
const DEFAULT_QUESTIONS = [
  '请假流程是什么？',
  '如何申请奖学金？',
  '图书馆几点开门？',
  '成绩怎么查询？'
]

const quickQuestions = ref<string[]>(DEFAULT_QUESTIONS)

// ============ 计算属性 ============
const canSend = computed(() => {
  return inputMessage.value.trim().length > 0 && !isStreaming.value
})

// ============ 生命周期 ============
onLoad((options: any) => {
  // 获取安全区域高度
  const systemInfo = uni.getSystemInfoSync()
  safeAreaBottom.value = systemInfo.safeAreaInsets?.bottom || 0
  
  // 如有 conversationId 参数则加载历史消息
  if (options?.conversationId) {
    conversationId.value = parseInt(options.conversationId)
    loadHistory()
  }
})

// ============ 历史消息加载 ============
async function loadHistory() {
  if (!conversationId.value) return
  
  try {
    const history = await getHistory(conversationId.value)
    if (history && Array.isArray(history)) {
      messages.value = history.map((m: any) => ({
        id: m.id || String(Date.now() + Math.random()),
        role: m.role || 'assistant',
        content: m.content || '',
        sources: m.sources || [],
        timestamp: m.timestamp ? new Date(m.timestamp).getTime() : Date.now()
      }))
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载历史消息失败:', error)
  }
}

// ============ 加载更多历史（分页） ============
async function loadMoreHistory() {
  // P1 功能：后续可实现分页加载
}

// ============ 跳转到历史页面 ============
const goToHistory = () => {
  uni.navigateTo({
    url: '/pages/chat/history'
  })
}

// ============ 发送消息 ============
async function sendMessage() {
  const content = inputMessage.value.trim()
  if (!content || isStreaming.value) return

  // 如果没有 conversationId，先创建会话
  if (!conversationId.value) {
    try {
      const conv = await createConversation(content.slice(0, 20))
      conversationId.value = conv.id
    } catch (error) {
      console.error('创建会话失败:', error)
    }
  }

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

  // 保存用户消息到后端
  if (conversationId.value) {
    try {
      await sendMessageAPI(conversationId.value, {
        content: content,
        messageType: 1
      })
    } catch (error) {
      console.error('保存用户消息失败:', error)
    }
  }

  // 开始流式响应
  await streamResponse(content)
}

// ============ 快捷问题发送 ============
function sendQuickQuestion(question: string) {
  if (isStreaming.value) return
  inputMessage.value = question
  sendMessage()
}

// ⚠️ 不可修改 - SSE 流式响应核心逻辑
async function streamResponse(userContent: string): Promise<string> {
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
    // 延迟一点显示 AI 消息
    await new Promise(resolve => setTimeout(resolve, 500))
    isTyping.value = false
    messages.value.push(aiMessage)
    scrollToBottom()

    // 发起 SSE 请求
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
    let allChunks: string[] = []
    let pendingSources: Source[] = []

    // 读取流数据
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      buffer += chunk
      
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.trim() === '') continue
        if (line.startsWith('data: ')) {
          const dataStr = line.slice(6).trim()
          try {
            const data = JSON.parse(dataStr)
            if (data.chunk !== undefined && data.chunk !== '') {
              allChunks.push(data.chunk)
            }
            if (data.sources && Array.isArray(data.sources) && data.sources.length) {
              pendingSources = data.sources.map((s: any) => ({
                entry_id: s.entry_id || '',
                title: s.title || '未知来源',
                content: s.content || '',
                url: s.url || '',
                score: s.score,
                material_file_url: s.material_file_url || '',
                material_title: s.material_title || ''
              }))
            }
            if (data.is_end === true) break
            if (data.error) throw new Error(data.error)
          } catch (e: any) {
            if (e.message && !e.message.includes('JSON')) throw e
          }
        }
      }
    }

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
              score: s.score,
              material_file_url: s.material_file_url || '',
              material_title: s.material_title || ''
            }))
          }
        } catch (e) { }
      }
    }

    // 打字机效果播放
    await playChunks(aiMessage, allChunks, pendingSources)
    return allChunks.join('')
    
  } catch (error: any) {
    console.error('Stream error:', error)
    isTyping.value = false
    
    let errorMsg = '抱歉，AI 服务暂时不可用，请稍后重试。'
    const index = messages.value.findIndex(m => m.id === aiMessage.id)
    if (index !== -1) {
      messages.value[index].content = errorMsg
      messages.value[index].isStreaming = false
    } else {
      messages.value.push({
        id: `assistant-error-${Date.now()}`,
        role: 'assistant',
        content: errorMsg,
        timestamp: Date.now(),
        isStreaming: false
      })
    }
    scrollToBottom()
    return errorMsg
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
  const getReactiveMsg = () => messages.value.find(m => m.id === aiMessage.id) || aiMessage
  
  if (chunks.length === 0) {
    getReactiveMsg().isStreaming = false
    return
  }
  
  if (sources.length > 0) {
    getReactiveMsg().sources = sources
  }
  
  let accumulated = ''
  for (let i = 0; i < chunks.length; i++) {
    accumulated += chunks[i]
    getReactiveMsg().content = accumulated
    scrollToBottom()
    await new Promise(resolve => setTimeout(resolve, 30))
  }
  
  getReactiveMsg().isStreaming = false
  scrollToBottom()
}

function extractBaseEntryId(rawEntryId: string): string {
  if (!rawEntryId) return ''
  return rawEntryId.split('__chunk_')[0]
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

function showSourcePreviewPopup(source: Source) {
  sourcePreview.value = {
    visible: true,
    entryId: source.entry_id || '',
    title: source.material_title || source.title || '参考资料',
    content: source.content || '暂未获取到摘要内容，可稍后重试查看详情。',
    score: source.score,
    materialFileUrl: source.material_file_url || ''
  }
}

function closeSourcePreview() {
  sourcePreview.value.visible = false
}

async function openSourceDetailFromPreview() {
  const source = sourcePreview.value
  const baseEntryId = extractBaseEntryId(source.entryId)
  if (baseEntryId) {
    try {
      await navigateToPage(
        '/pages/knowledge/detail?entry_id=' + encodeURIComponent(baseEntryId)
        + '&title=' + encodeURIComponent(source.title)
        + '&summary=' + encodeURIComponent(source.content)
        + '&score=' + (source.score ?? '')
        + '&material_file_url=' + encodeURIComponent(source.materialFileUrl || '')
      )
      closeSourcePreview()
      return
    } catch {}
  }
  closeSourcePreview()
}

async function handleSourceClick(source: Source) {
  if (source.entry_id) {
    const baseEntryId = extractBaseEntryId(source.entry_id)
    if (baseEntryId) {
      try {
        await navigateToPage(
          '/pages/knowledge/detail?entry_id=' + encodeURIComponent(baseEntryId)
          + '&title=' + encodeURIComponent(source.title || '')
          + '&summary=' + encodeURIComponent((source.content || '').slice(0, 300))
          + '&score=' + (source.score ?? '')
          + '&material_file_url=' + encodeURIComponent(source.material_file_url || '')
          + '&material_title=' + encodeURIComponent(source.material_title || '')
        )
        return
      } catch (error) {
        console.warn('知识详情跳转失败，降级弹层:', error)
      }
    }
  }
  if (source.content) { showSourcePreviewPopup(source); return }
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
  
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (date.toDateString() === now.toDateString()) {
    return `今天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
  }
  const yesterday = new Date(now)
  yesterday.setDate(yesterday.getDate() - 1)
  if (date.toDateString() === yesterday.toDateString()) {
    return `昨天 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
  }
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

function scrollToBottom() {
  nextTick(() => {
    scrollTop.value = 9999999 + Math.random()
  })
}
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background: $bg-page;
  overflow: hidden;
}

.navbar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 88rpx;
  padding-top: var(--status-bar-height, 44rpx);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  flex-shrink: 0;
  position: relative;

  .title {
    font-size: 36rpx;
    font-weight: 600;
    color: $text-primary;
  }

  .nav-actions {
    position: absolute;
    right: $spacing-md;
    display: flex;
    align-items: center;
  }

  .history-btn {
    width: 72rpx;
    height: 72rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: $radius-md;
    background: rgba(124, 58, 237, 0.08);
    transition: $transition-base;

    &:active {
      transform: scale(0.92);
      background: rgba(124, 58, 237, 0.15);
    }

    .icon {
      font-size: 36rpx;
    }
  }
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: $spacing-md;
  background: $bg-page;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 96rpx 64rpx;
  text-align: center;

  .empty-icon {
    width: 160rpx;
    height: 160rpx;
    border-radius: $radius-xl;
    background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: $spacing-md;
    animation: float 3s ease-in-out infinite;
  }

  .empty-title {
    font-size: 40rpx;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: $spacing-xs;
  }

  .empty-desc {
    font-size: 28rpx;
    color: $text-secondary;
    line-height: 1.6;
    max-width: 560rpx;
    margin-bottom: $spacing-xl;
  }
}

.quick-chips {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: $spacing-sm;
  max-width: 640rpx;

  .chip {
    display: flex;
    align-items: center;
    gap: 12rpx;
    padding: 20rpx 32rpx;
    background: $bg-card;
    border-radius: $radius-pill;
    border: 1px solid $primary-40;
    font-size: 28rpx;
    color: $primary-40;
    box-shadow: $elevation-1;
    transition: $transition-base;

    &:active {
      transform: scale(0.96);
      background: $primary-95;
    }
  }
}

.message-item {
  display: flex;
  align-items: flex-start;
  flex-shrink: 0;
  margin-bottom: 40rpx;
  animation: $animation-fade-in-up;

  &.user {
    justify-content: flex-end;
  }

  &.assistant {
    justify-content: flex-start;
  }
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &.ai-avatar {
    background: linear-gradient(135deg, $primary-40 0%, $primary-50 100%);
    margin-right: 20rpx;
    box-shadow: $elevation-2;
  }

  &.user-avatar {
    background: $bg-card;
    margin-left: 20rpx;
    box-shadow: $elevation-1;
  }
}

.message-content {
  display: flex;
  flex-direction: column;
  max-width: 75%;
  flex: 1 1 auto;
  min-height: 0;
}

.sender-name {
  font-size: 24rpx;
  color: $text-secondary;
  margin-bottom: 8rpx;
  margin-left: 24rpx;
}

.message-bubble {
  padding: 24rpx 32rpx;
  box-shadow: $elevation-1;
  word-break: break-word;
  flex-shrink: 0;

  &.user {
    background: linear-gradient(135deg, $primary-40 0%, $primary-50 100%);
    border-radius: 36rpx 36rpx 8rpx 36rpx;
    color: $text-inverse;
  }

  &.assistant {
    background: $bg-card;
    border-radius: 8rpx 36rpx 36rpx 36rpx;
    color: $text-primary;
  }
}

.message-text {
  font-size: 30rpx;
  line-height: 1.6;
}

.markdown-body {
  font-size: 28rpx;
  line-height: 1.7;

  :deep(p) { margin: 0 0 16rpx 0; &:last-child { margin-bottom: 0; } }
  :deep(strong) { font-weight: 600; color: $primary-40; }
  :deep(a) { color: $primary-40; text-decoration: underline; }
  :deep(code) {
    background: rgba(124, 58, 237, 0.1);
    border-radius: 8rpx;
    padding: 4rpx 10rpx;
    color: $primary-40;
  }
  :deep(pre) {
    background: $bg-secondary;
    border-radius: 16rpx;
    padding: 24rpx;
    margin: 16rpx 0;
    overflow-x: auto;
  }
}

.cursor {
  display: inline-block;
  color: $primary-40;
  animation: blink 1s infinite;
  margin-left: 4rpx;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

.typing-animation {
  display: flex;
  align-items: center;
  gap: 8rpx;
  height: 48rpx;

  .dot {
    width: 12rpx;
    height: 12rpx;
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

.message-sources {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-top: 16rpx;
  margin-left: 8rpx;
  padding: 24rpx 28rpx;
  background: $bg-card;
  border-radius: $radius-lg;
  box-shadow: $elevation-1;

  .sources-header {
    display: flex;
    align-items: center;
    gap: 8rpx;
    font-size: 24rpx;
    color: $text-secondary;
  }

  .source-item {
    display: flex;
    align-items: center;
    gap: 8rpx;
    padding: 16rpx 20rpx;
    border-radius: $radius-md;
    background: rgba(124, 58, 237, 0.04);
    border: 1px solid rgba(124, 58, 237, 0.15);
    transition: $transition-base;

    .source-num {
      font-size: 24rpx;
      color: $primary-40;
    }

    .source-title {
      flex: 1;
      font-size: 28rpx;
      color: $text-primary;
    }

    &:active {
      transform: scale(0.98);
      background: $bg-secondary;
    }
  }
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-top: 8rpx;
  margin-left: 24rpx;

  .timestamp {
    font-size: 24rpx;
    color: $text-tertiary;
  }

  .copy-btn {
    padding: 8rpx;
    border-radius: 8rpx;
    transition: $transition-base;

    &:active {
      background: rgba(0, 0, 0, 0.05);
    }
  }
}

.typing-indicator {
  display: flex;
  align-items: flex-start;
  margin-bottom: 40rpx;
  animation: fadeIn 0.3s ease-out;

  .typing-content {
    display: flex;
    align-items: center;
    gap: 16rpx;
    padding: 24rpx 32rpx;
    background: $primary-95;
    border-radius: 8rpx 36rpx 36rpx 36rpx;
    box-shadow: $elevation-1;
  }

  .typing-text {
    font-size: 28rpx;
    color: $text-secondary;
  }

  .thinking-dots {
    display: flex;
    gap: 6rpx;

    .dot {
      width: 8rpx;
      height: 8rpx;
      border-radius: 50%;
      background: $text-secondary;
      animation: typingBounce 1.4s infinite ease-in-out both;

      &:nth-child(1) { animation-delay: -0.32s; }
      &:nth-child(2) { animation-delay: -0.16s; }
    }
  }
}

.list-footer {
  height: 32rpx;
}

.quick-questions-bar {
  padding: 16rpx 0;
  background: transparent;
}

.quick-questions-scroll {
  white-space: nowrap;
}

.quick-questions-content {
  display: inline-flex;
  gap: 16rpx;
  padding: 0 32rpx;
}

.question-chip {
  padding: 16rpx 28rpx;
  background: $bg-card;
  border-radius: $radius-pill;
  font-size: 28rpx;
  color: $text-primary;
  box-shadow: $elevation-1;
  transition: $transition-base;

  &:active {
    transform: scale(0.96);
    background: $primary-95;
  }
}

.input-area {
  padding: 24rpx 32rpx;
  background: $bg-card;
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 20rpx;
}

.message-input {
  flex: 1;
  height: 88rpx;
  padding: 0 32rpx;
  background: $bg-secondary;
  border-radius: $radius-pill;
  font-size: 30rpx;
  color: $text-primary;
}

.send-btn {
  width: 88rpx;
  height: 88rpx;
  border-radius: 50%;
  background: $bg-secondary;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: $transition-base;

  &.active {
    background: linear-gradient(135deg, $primary-40 0%, $primary-50 100%);
    box-shadow: $elevation-2;
  }
}

.source-preview-mask {
  position: fixed;
  inset: 0;
  z-index: 9999;
  display: flex;
  align-items: flex-end;
  background: rgba(0, 0, 0, 0.4);
}

.source-preview-panel {
  width: 100%;
  background: $bg-card;
  border-radius: $radius-lg $radius-lg 0 0;
  padding: 36rpx 32rpx;
  max-height: 75vh;
  display: flex;
  flex-direction: column;
}

.source-preview-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20rpx;
}

.source-preview-label {
  font-size: 28rpx;
  color: $primary-40;
}

.source-preview-score {
  font-size: 24rpx;
  color: $text-secondary;
}

.source-preview-title {
  font-size: 36rpx;
  font-weight: 700;
  margin-bottom: 16rpx;
}

.source-preview-content {
  flex: 1;
  overflow-y: auto;
  font-size: 30rpx;
  color: $text-secondary;
  line-height: 1.6;
}

.source-preview-actions {
  display: flex;
  gap: 20rpx;
  margin-top: 32rpx;
}

.preview-btn {
  flex: 1;
  height: 88rpx;
  border-radius: $radius-pill;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;

  &-primary {
    background: $primary-40;
    color: $text-inverse;
  }

  &-ghost {
    background: rgba(124, 58, 237, 0.08);
    color: $primary-40;
  }

  &-disabled {
    background: $bg-secondary;
    color: $text-tertiary;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-12rpx); }
}
</style>
