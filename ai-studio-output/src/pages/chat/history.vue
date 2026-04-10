<template>
  <view class="history-page">
    <view class="navbar">
      <text class="title">对话历史</text>
    </view>

    <scroll-view scroll-y class="history-list">
      <view v-if="!historyList.length" class="empty-state">
        <view class="empty-icon">💬</view>
        <text class="empty-text">还没有对话记录</text>
        <button class="new-chat-btn" @click="startNewChat">开始新对话</button>
      </view>

      <view v-else class="list-container">
        <view 
          class="history-card" 
          v-for="item in historyList" 
          :key="item.id"
          @click="goToChat(item.id)"
        >
          <view class="card-header">
            <text class="card-title">{{ item.title || '新对话' }}</text>
            <view class="status-tag" :class="item.status">
              {{ getStatusText(item.status) }}
            </view>
          </view>
          <view class="card-footer">
            <text class="time">{{ formatTime(item.updatedAt) }}</text>
            <text class="msg-count">{{ item.messageCount }} 条消息</text>
          </view>
        </view>
      </view>
    </scroll-view>

    <view class="fab" @click="startNewChat">
      <text class="icon">+</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getConversationList } from '@/api/chat'

const historyList = ref<any[]>([])

const loadData = async () => {
  try {
    const res = await getConversationList()
    historyList.value = res.rows || []
  } catch (error) {
    console.error('Failed to load history', error)
  }
}

onMounted(() => {
  loadData()
})

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'active': '进行中',
    'closed': '已关闭',
    'escalated': '教师介入'
  }
  return map[status] || '未知'
}

const formatTime = (time: string) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getMonth() + 1}月${date.getDate()}日 ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const goToChat = (id: number) => {
  uni.navigateTo({ url: `/pages/chat/index?conversationId=${id}` })
}

const startNewChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.history-page {
  min-height: 100vh;
  background: $bg-page;
  display: flex;
  flex-direction: column;
}

.navbar {
  height: 88rpx;
  padding-top: var(--status-bar-height, 44rpx);
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  
  .title {
    font-size: 36rpx;
    font-weight: 600;
    color: $text-inverse;
  }
}

.history-list {
  flex: 1;
  padding: $spacing-md;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding-top: 200rpx;

  .empty-icon {
    font-size: 120rpx;
    margin-bottom: $spacing-md;
    opacity: 0.5;
  }

  .empty-text {
    font-size: 32rpx;
    color: $text-secondary;
    margin-bottom: $spacing-lg;
  }

  .new-chat-btn {
    background: $primary-40;
    color: $text-inverse;
    border-radius: $radius-pill;
    padding: 0 64rpx;
    height: 88rpx;
    line-height: 88rpx;
    font-size: 32rpx;
  }
}

.list-container {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.history-card {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-md;
  box-shadow: $elevation-1;
  animation: $animation-fade-in-up;

  &:active {
    transform: scale(0.98);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-sm;

    .card-title {
      font-size: 32rpx;
      font-weight: 600;
      color: $text-primary;
      flex: 1;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .status-tag {
      font-size: 24rpx;
      padding: 4rpx 16rpx;
      border-radius: $radius-chip;
      
      &.active { background: $primary-95; color: $primary-40; }
      &.closed { background: $bg-secondary; color: $text-secondary; }
      &.escalated { background: #FEF3C7; color: $warning; }
    }
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    font-size: 24rpx;
    color: $text-tertiary;
  }
}

.fab {
  position: fixed;
  right: 48rpx;
  bottom: calc(48rpx + env(safe-area-inset-bottom));
  width: 112rpx;
  height: 112rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, $primary-40 0%, $primary-50 100%);
  box-shadow: $elevation-3;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: $transition-base;

  &:active {
    transform: scale(0.9);
  }

  .icon {
    font-size: 64rpx;
    color: $text-inverse;
    font-weight: 300;
  }
}
</style>
