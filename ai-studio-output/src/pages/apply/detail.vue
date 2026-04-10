<template>
  <view class="detail-page" v-if="detail">
    <view class="hero-section">
      <view class="status-header">
        <text class="room-name">{{ detail.classroomName }}</text>
        <view class="status-badge" :class="detail.status">
          <view class="pulse-dot" v-if="detail.status === 'processing'"></view>
          <text>{{ getStatusText(detail.status) }}</text>
        </view>
      </view>
      <text class="time-range">{{ detail.date }} {{ detail.startTime }}-{{ detail.endTime }}</text>
    </view>

    <view class="content-container">
      <!-- 步骤卡片 -->
      <view class="step-card">
        <view class="step-list">
          <view class="step-item active">
            <view class="step-icon">✓</view>
            <text class="step-text">已提交</text>
          </view>
          <view class="step-line active"></view>
          <view class="step-item" :class="{ active: detail.status !== 'pending' }">
            <view class="step-icon">{{ detail.status !== 'pending' ? '✓' : '2' }}</view>
            <text class="step-text">审核中</text>
          </view>
          <view class="step-line" :class="{ active: detail.status === 'approved' || detail.status === 'rejected' }"></view>
          <view class="step-item" :class="{ active: detail.status === 'approved' || detail.status === 'rejected' }">
            <view class="step-icon">{{ detail.status === 'approved' ? '✓' : (detail.status === 'rejected' ? '✕' : '3') }}</view>
            <text class="step-text">{{ detail.status === 'rejected' ? '已驳回' : '已完成' }}</text>
          </view>
        </view>
      </view>

      <!-- 申请信息摘要 -->
      <view class="info-card">
        <text class="card-title">申请信息</text>
        <view class="info-list">
          <view class="info-item">
            <text class="label">申请编号</text>
            <text class="value">{{ detail.id }}</text>
          </view>
          <view class="info-item">
            <text class="label">提交时间</text>
            <text class="value">{{ formatTime(detail.createdAt) }}</text>
          </view>
          <view class="info-item">
            <text class="label">使用用途</text>
            <text class="value">{{ detail.reason }}</text>
          </view>
          <view class="info-item">
            <text class="label">预计人数</text>
            <text class="value">{{ detail.peopleCount }}人</text>
          </view>
          <view class="info-item">
            <text class="label">联系电话</text>
            <text class="value">{{ detail.phone }}</text>
          </view>
        </view>
      </view>

      <!-- 审批历史时间线 -->
      <view class="timeline-card" v-if="detail.logs && detail.logs.length">
        <text class="card-title">审批历史</text>
        <view class="timeline">
          <view class="timeline-item" v-for="(log, index) in detail.logs" :key="index">
            <view class="timeline-icon">👤</view>
            <view class="timeline-content">
              <view class="timeline-header">
                <text class="timeline-title">{{ log.action }}</text>
                <text class="timeline-time">{{ formatTime(log.createdAt) }}</text>
              </view>
              <text class="timeline-desc">{{ log.operatorName }}</text>
              <view class="timeline-quote" v-if="log.comment">
                <text class="quote-text">"{{ log.comment }}"</text>
              </view>
            </view>
          </view>
        </view>
      </view>

      <!-- 辅助信息 -->
      <view class="helper-card">
        <view class="helper-item">
          <text class="icon">⏱️</text>
          <text class="text">预计处理时间：1-2 个工作日</text>
        </view>
        <view class="helper-item link" @click="goToHelp">
          <text class="icon">❓</text>
          <text class="text">帮助中心</text>
          <text class="arrow">></text>
        </view>
      </view>
    </view>

    <!-- 操作按钮 -->
    <view class="bottom-bar">
      <button class="action-btn outline" @click="contactApprover">联系审批人</button>
      <button 
        v-if="detail.status === 'pending' || detail.status === 'rejected'" 
        class="action-btn primary" 
        @click="modifyApplication"
      >
        修改申请
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { getApplicationDetail } from '@/api/apply'

const detail = ref<any>(null)

onLoad((options: any) => {
  if (options.id) {
    loadDetail(options.id)
  }
})

const loadDetail = async (id: string) => {
  try {
    const res = await getApplicationDetail(id)
    detail.value = res.data
  } catch (error) {
    console.error('Failed to load detail', error)
  }
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'pending': '待审批',
    'processing': '审核中',
    'approved': '已通过',
    'rejected': '已驳回',
    'cancelled': '已取消'
  }
  return map[status] || '未知'
}

const formatTime = (time: string) => {
  if (!time) return ''
  const date = new Date(time)
  return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`
}

const goToHelp = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

const contactApprover = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

const modifyApplication = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.detail-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

.hero-section {
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  padding: 48rpx $spacing-md 80rpx;
  color: $text-inverse;

  .status-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: $spacing-sm;

    .room-name {
      font-size: 48rpx;
      font-weight: 700;
    }

    .status-badge {
      display: flex;
      align-items: center;
      gap: 8rpx;
      padding: 8rpx 24rpx;
      border-radius: $radius-pill;
      font-size: 24rpx;
      font-weight: 600;
      background: rgba(255, 255, 255, 0.2);
      border: 1px solid rgba(255, 255, 255, 0.4);

      .pulse-dot {
        width: 12rpx;
        height: 12rpx;
        border-radius: 50%;
        background: $warning;
        animation: pulse 2s infinite;
      }
    }
  }

  .time-range {
    font-size: 28rpx;
    opacity: 0.9;
  }
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0.7); }
  70% { box-shadow: 0 0 0 12rpx rgba(217, 119, 6, 0); }
  100% { box-shadow: 0 0 0 0 rgba(217, 119, 6, 0); }
}

.content-container {
  margin-top: -40rpx;
  padding: 0 $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.step-card {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-lg;
  box-shadow: $elevation-1;
  animation: $animation-fade-in-up;

  .step-list {
    display: flex;
    align-items: center;
    justify-content: space-between;

    .step-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $spacing-xs;
      z-index: 1;

      .step-icon {
        width: 48rpx;
        height: 48rpx;
        border-radius: 50%;
        background: $bg-secondary;
        color: $text-tertiary;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24rpx;
        font-weight: 600;
        transition: $transition-base;
      }

      .step-text {
        font-size: 24rpx;
        color: $text-secondary;
      }

      &.active {
        .step-icon {
          background: $primary-40;
          color: $text-inverse;
        }
        .step-text {
          color: $primary-40;
          font-weight: 600;
        }
      }
    }

    .step-line {
      flex: 1;
      height: 4rpx;
      background: $bg-secondary;
      margin: 0 -24rpx;
      margin-bottom: 40rpx;
      transition: $transition-base;

      &.active {
        background: $primary-40;
      }
    }
  }
}

.info-card, .timeline-card, .helper-card {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-md;
  box-shadow: $elevation-1;
  animation: $animation-fade-in-up;
  animation-delay: 0.1s;
  animation-fill-mode: both;

  .card-title {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: $spacing-md;
    display: block;
  }
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;

  .info-item {
    display: flex;
    font-size: 28rpx;

    .label {
      color: $text-secondary;
      width: 160rpx;
    }

    .value {
      color: $text-primary;
      flex: 1;
    }
  }
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;

  .timeline-item {
    display: flex;
    gap: $spacing-sm;

    .timeline-icon {
      width: 64rpx;
      height: 64rpx;
      border-radius: 50%;
      background: $primary-95;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 32rpx;
      flex-shrink: 0;
    }

    .timeline-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 4rpx;

      .timeline-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .timeline-title {
          font-size: 28rpx;
          font-weight: 600;
          color: $text-primary;
        }

        .timeline-time {
          font-size: 24rpx;
          color: $text-tertiary;
        }
      }

      .timeline-desc {
        font-size: 24rpx;
        color: $text-secondary;
      }

      .timeline-quote {
        margin-top: 8rpx;
        padding: 16rpx;
        background: $bg-secondary;
        border-radius: $radius-md;
        border-left: 4rpx solid $primary-40;

        .quote-text {
          font-size: 26rpx;
          color: $text-secondary;
          font-style: italic;
        }
      }
    }
  }
}

.helper-card {
  padding: 0 $spacing-md;
  display: flex;
  flex-direction: column;

  .helper-item {
    display: flex;
    align-items: center;
    padding: $spacing-md 0;
    border-bottom: 1px solid $border-color;

    &:last-child {
      border-bottom: none;
    }

    .icon {
      font-size: 32rpx;
      margin-right: $spacing-sm;
    }

    .text {
      flex: 1;
      font-size: 28rpx;
      color: $text-secondary;
    }

    .arrow {
      font-size: 28rpx;
      color: $text-tertiary;
    }

    &.link:active {
      opacity: 0.7;
    }
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: $bg-card;
  padding: $spacing-sm $spacing-md;
  padding-bottom: calc($spacing-sm + env(safe-area-inset-bottom));
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);
  display: flex;
  gap: $spacing-md;

  .action-btn {
    flex: 1;
    height: 88rpx;
    border-radius: $radius-pill;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0;

    &:active {
      transform: scale(0.98);
    }

    &.outline {
      background: $bg-card;
      color: $primary-40;
      border: 1px solid $primary-40;
    }

    &.primary {
      background: linear-gradient(90deg, $primary-40 0%, $primary-50 100%);
      color: $text-inverse;
      border: none;
    }
  }
}
</style>
