<template>
  <view class="questions-page">
    <view class="filter-tabs">
      <view 
        class="tab-item" 
        v-for="tab in tabs" 
        :key="tab.value"
        :class="{ active: currentTab === tab.value }"
        @click="switchTab(tab.value)"
      >
        <text>{{ tab.label }}</text>
        <view class="indicator" v-if="currentTab === tab.value"></view>
      </view>
    </view>

    <scroll-view scroll-y class="list-container">
      <view v-if="!questions.length" class="empty-state">
        <text class="empty-icon">❓</text>
        <text class="empty-text">暂无提问记录</text>
        <button class="empty-btn" @click="goToChat">去提问</button>
      </view>

      <view class="question-card" v-for="item in questions" :key="item.id" @click="goToChatHistory(item.conversationId)">
        <view class="card-header">
          <view class="status-tag" :class="item.status">
            {{ getStatusText(item.status) }}
          </view>
          <text class="time">{{ formatTime(item.createdAt) }}</text>
        </view>

        <view class="card-body">
          <text class="summary">{{ item.summary || '暂无摘要' }}</text>
        </view>

        <view class="card-footer">
          <text class="conv-id">会话 ID: {{ item.conversationId }}</text>
          <view class="teacher-info" v-if="item.teacherName">
            <text class="icon">👨‍🏫</text>
            <text>{{ item.teacherName }} 处理中</text>
          </view>
          <view class="teacher-info pending" v-else>
            <text class="icon">⏳</text>
            <text>等待分配老师</text>
          </view>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMyEscalations } from '@/api/chat'

const currentTab = ref('')
const questions = ref<any[]>([])

const tabs = [
  { label: '全部', value: '' },
  { label: '待处理', value: 'pending' },
  { label: '处理中', value: 'processing' },
  { label: '已解决', value: 'resolved' }
]

const loadData = async () => {
  try {
    const res = await getMyEscalations(currentTab.value)
    questions.value = res.rows || []
  } catch (error) {
    console.error('Failed to load questions', error)
  }
}

onMounted(() => {
  loadData()
})

const switchTab = (value: string) => {
  currentTab.value = value
  loadData()
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'pending': '待处理',
    'processing': '处理中',
    'resolved': '已解决'
  }
  return map[status] || '未知'
}

const formatTime = (time: string) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const goToChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}

const goToChatHistory = (id: number) => {
  uni.navigateTo({ url: `/pages/chat/index?conversationId=${id}` })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.questions-page {
  min-height: 100vh;
  background: $bg-page;
  display: flex;
  flex-direction: column;
}

.filter-tabs {
  display: flex;
  background: $bg-card;
  padding: 0 $spacing-md;
  height: 88rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
  position: sticky;
  top: 0;
  z-index: 10;

  .tab-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-size: 28rpx;
    color: $text-secondary;
    position: relative;

    &.active {
      color: $primary-40;
      font-weight: 600;
    }

    .indicator {
      position: absolute;
      bottom: 0;
      width: 40rpx;
      height: 6rpx;
      background: $primary-40;
      border-radius: 6rpx 6rpx 0 0;
    }
  }
}

.list-container {
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

  .empty-btn {
    background: $primary-40;
    color: $text-inverse;
    border-radius: $radius-pill;
    padding: 0 64rpx;
    height: 88rpx;
    line-height: 88rpx;
    font-size: 32rpx;
  }
}

.question-card {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-md;
  margin-bottom: $spacing-md;
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

    .status-tag {
      font-size: 24rpx;
      padding: 4rpx 16rpx;
      border-radius: $radius-chip;
      
      &.pending { background: #FEF3C7; color: $warning; }
      &.processing { background: #E0F2FE; color: #0284C7; }
      &.resolved { background: #D1FAE5; color: $success; }
    }

    .time {
      font-size: 24rpx;
      color: $text-tertiary;
    }
  }

  .card-body {
    margin-bottom: $spacing-md;

    .summary {
      font-size: 30rpx;
      color: $text-primary;
      line-height: 1.5;
      display: -webkit-box;
      -webkit-box-orient: vertical;
      -webkit-line-clamp: 2;
      overflow: hidden;
    }
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: $spacing-sm;
    border-top: 1px solid $border-color;

    .conv-id {
      font-size: 24rpx;
      color: $text-tertiary;
    }

    .teacher-info {
      display: flex;
      align-items: center;
      gap: 8rpx;
      font-size: 24rpx;
      color: $primary-40;

      &.pending {
        color: $warning;
      }

      .icon {
        font-size: 28rpx;
      }
    }
  }
}
</style>
