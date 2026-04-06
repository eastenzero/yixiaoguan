<template>
  <view class="history-page">
    <!-- 顶部导航栏 -->
    <view class="navbar">
      <text class="title">对话历史</text>
    </view>

    <!-- 会话列表 -->
    <scroll-view
      class="conversation-list"
      scroll-y
      v-if="conversations.length > 0"
    >
      <view
        class="conversation-item"
        v-for="conv in conversations"
        :key="conv.id"
        @click="enterConversation(conv.id)"
      >
        <view class="conv-header">
          <text class="conv-title">{{ conv.title || '未命名对话' }}</text>
          <view class="conv-status" :class="getStatusClass(conv.status)">
            {{ getStatusText(conv.status) }}
          </view>
        </view>
        <view class="conv-meta">
          <text class="time">{{ formatTime(conv.updatedAt) }}</text>
          <text class="count">{{ conv.messageCount }} 条消息</text>
        </view>
      </view>
    </scroll-view>

    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <view class="empty-icon">
        <IconMessageSquare :size="48" color="#ffffff" />
      </view>
      <text class="empty-title">还没有对话记录</text>
      <text class="empty-desc">开始与医小管对话，获取校园生活、办事流程等帮助</text>
      <button class="new-btn" @click="createNew">开始新对话</button>
    </view>

    <!-- 新建按钮（固定底部） -->
    <view class="fab" v-if="conversations.length > 0">
      <button class="fab-btn" @click="createNew">
        <IconPlus :size="24" color="#ffffff" />
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getConversationList, createConversation } from '@/api/chat'
import type { Conversation } from '@/types/chat'
import IconMessageSquare from '@/components/icons/IconMessageSquare.vue'
import IconPlus from '@/components/icons/IconPlus.vue'

// ============ 响应式状态 ============
const conversations = ref<Conversation[]>([])
const loading = ref(false)

// ============ 生命周期 ============
onMounted(() => {
  loadConversations()
})

onShow(() => {
  // 页面显示时刷新列表
  loadConversations()
})

// ============ 加载会话列表 ============
async function loadConversations() {
  loading.value = true
  try {
    const result = await getConversationList()
    if (result && result.rows) {
      conversations.value = result.rows
    } else {
      conversations.value = []
    }
  } catch (error) {
    console.error('加载会话列表失败:', error)
    // 优雅处理 API 失败，显示空状态
    conversations.value = []
    uni.showToast({
      title: '加载失败，请稍后重试',
      icon: 'none'
    })
  } finally {
    loading.value = false
  }
}

// ============ 进入会话 ============
function enterConversation(conversationId: number) {
  uni.navigateTo({
    url: `/pages/chat/index?conversationId=${conversationId}`
  })
}

// ============ 新建会话 ============
async function createNew() {
  try {
    const newConv = await createConversation('新对话')
    uni.navigateTo({
      url: `/pages/chat/index?conversationId=${newConv.id}`
    })
  } catch (error) {
    console.error('创建会话失败:', error)
    uni.showToast({
      title: '创建会话失败',
      icon: 'none'
    })
  }
}

// ============ 状态相关 ============
function getStatusClass(status: number): string {
  const statusMap: Record<number, string> = {
    0: 'status-closed',
    1: 'status-active',
    2: 'status-teacher'
  }
  return statusMap[status] || 'status-active'
}

function getStatusText(status: number): string {
  const statusMap: Record<number, string> = {
    0: '已关闭',
    1: '进行中',
    2: '教师介入'
  }
  return statusMap[status] || '进行中'
}

// ============ 时间格式化 ============
function formatTime(timestamp: string | number): string {
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
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

// ============ 页面布局 ============
.history-page {
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
  background: linear-gradient(135deg, $primary 0%, #008a83 100%);
  flex-shrink: 0;

  .title {
    font: $text-headline-medium;
    color: #ffffff;
  }
}

// ============ 会话列表 ============
.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

// ============ 会话项 ============
.conversation-item {
  background: #ffffff;
  border-radius: $radius-lg;
  padding: 16px;
  margin-bottom: 12px;
  box-shadow: $md-sys-elevation-1;
  transition: all 0.2s ease;

  &:active {
    transform: scale(0.98);
    box-shadow: $md-sys-elevation-2;
  }

  .conv-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 8px;
  }

  .conv-title {
    font: $text-title-medium;
    color: $md-sys-color-on-background;
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 8px;
  }

  .conv-status {
    font: $text-label-small;
    padding: 2px 8px;
    border-radius: $radius-full;
    flex-shrink: 0;

    &.status-active {
      background: $success-90;
      color: $success-40;
    }

    &.status-closed {
      background: $neutral-90;
      color: $neutral-50;
    }

    &.status-teacher {
      background: $primary-90;
      color: $primary-40;
    }
  }

  .conv-meta {
    display: flex;
    align-items: center;
    gap: 12px;

    .time {
      font: $text-body-small;
      color: $neutral-50;
    }

    .count {
      font: $text-label-small;
      color: $primary-40;
      background: $primary-95;
      padding: 2px 8px;
      border-radius: $radius-full;
    }
  }
}

// ============ 空状态 ============
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex: 1;
  padding: 48px 32px;
  text-align: center;

  .empty-icon {
    width: 80px;
    height: 80px;
    border-radius: $radius-xl;
    background: linear-gradient(135deg, $primary 0%, #008a83 100%);
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

  .new-btn {
    height: 44px;
    padding: 0 32px;
    background: linear-gradient(135deg, $primary 0%, #008a83 100%);
    color: #ffffff;
    border-radius: $radius-full;
    font: $text-label-large;
    border: none;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;

    &:active {
      transform: scale(0.96);
      opacity: 0.9;
    }

    &::after {
      display: none;
    }
  }
}

// ============ 悬浮按钮 ============
.fab {
  position: fixed;
  right: 20px;
  bottom: calc(20px + env(safe-area-inset-bottom, 0));
  z-index: 100;

  .fab-btn {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: linear-gradient(135deg, $primary 0%, #008a83 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    border: none;
    padding: 0;
    margin: 0;
    box-shadow: 0 4px 12px rgba(0, 106, 100, 0.35);
    transition: all 0.2s ease;

    &:active {
      transform: scale(0.92);
      box-shadow: 0 2px 8px rgba(0, 106, 100, 0.25);
    }

    &::after {
      display: none;
    }
  }
}

// ============ 动画 ============
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}
</style>
