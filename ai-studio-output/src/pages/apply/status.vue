<template>
  <view class="status-page">
    <view class="hero-section">
      <text class="title">我的申请</text>
      <button class="new-btn" @click="goToApply">新建申请</button>
    </view>

    <view class="list-container">
      <view v-if="!applications.length" class="empty-state">
        <text class="empty-icon">📝</text>
        <text class="empty-text">暂无申请记录</text>
        <button class="empty-btn" @click="goToApply">去申请</button>
      </view>

      <view class="apply-card" v-for="item in applications" :key="item.id" @click="goToDetail(item.id)">
        <view class="card-header">
          <text class="room-name">{{ item.classroomName }}</text>
          <view class="status-tag" :class="item.status">
            {{ getStatusText(item.status) }}
          </view>
        </view>

        <view class="step-indicator">
          <view class="step" :class="{ active: true }">已提交</view>
          <view class="line" :class="{ active: item.status !== 'pending' }"></view>
          <view class="step" :class="{ active: item.status === 'processing' || item.status === 'approved' || item.status === 'rejected' }">审核中</view>
          <view class="line" :class="{ active: item.status === 'approved' || item.status === 'rejected' }"></view>
          <view class="step" :class="{ active: item.status === 'approved' || item.status === 'rejected' }">已完成</view>
        </view>

        <view class="info-list">
          <view class="info-item">
            <text class="label">使用时间</text>
            <text class="value">{{ item.date }} {{ item.startTime }}-{{ item.endTime }}</text>
          </view>
          <view class="info-item">
            <text class="label">使用用途</text>
            <text class="value">{{ item.reason }}</text>
          </view>
          <view class="info-item">
            <text class="label">预计人数</text>
            <text class="value">{{ item.peopleCount }}人</text>
          </view>
        </view>

        <view class="card-footer">
          <text class="time">申请时间：{{ formatTime(item.createdAt) }}</text>
          <button 
            v-if="item.status === 'pending'" 
            class="cancel-btn" 
            @click.stop="handleCancel(item.id)"
          >
            取消申请
          </button>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMyApplications, cancelApplication } from '@/api/apply'

const userStore = useUserStore()
const applications = ref<any[]>([])

const loadData = async () => {
  try {
    if (userStore.userInfo?.id) {
      const res = await getMyApplications(userStore.userInfo.id)
      applications.value = res.rows || []
    }
  } catch (error) {
    console.error('Failed to load applications', error)
  }
}

onMounted(() => {
  loadData()
})

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

const goToApply = () => {
  uni.navigateTo({ url: '/pages/apply/classroom' })
}

const goToDetail = (id: number) => {
  uni.navigateTo({ url: `/pages/apply/detail?id=${id}` })
}

const handleCancel = (id: number) => {
  uni.showModal({
    title: '提示',
    content: '确定要取消该申请吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          await cancelApplication(id)
          uni.showToast({ title: '已取消', icon: 'success' })
          loadData()
        } catch (error) {
          uni.showToast({ title: '取消失败', icon: 'none' })
        }
      }
    }
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.status-page {
  min-height: 100vh;
  background: $bg-page;
}

.hero-section {
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  padding: 64rpx $spacing-md 80rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .title {
    font-size: 48rpx;
    font-weight: 700;
    color: $text-inverse;
  }

  .new-btn {
    background: rgba(255, 255, 255, 0.2);
    color: $text-inverse;
    border-radius: $radius-pill;
    font-size: 28rpx;
    padding: 0 32rpx;
    height: 64rpx;
    line-height: 64rpx;
    margin: 0;
    border: 1px solid rgba(255, 255, 255, 0.4);

    &:active {
      background: rgba(255, 255, 255, 0.3);
    }
  }
}

.list-container {
  margin-top: -40rpx;
  padding: 0 $spacing-md $spacing-xl;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.empty-state {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: 96rpx 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: $elevation-1;

  .empty-icon {
    font-size: 96rpx;
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
    height: 80rpx;
    line-height: 80rpx;
    font-size: 28rpx;
  }
}

.apply-card {
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
    margin-bottom: $spacing-md;

    .room-name {
      font-size: 36rpx;
      font-weight: 600;
      color: $text-primary;
    }

    .status-tag {
      font-size: 24rpx;
      padding: 4rpx 16rpx;
      border-radius: $radius-chip;
      
      &.pending { background: $primary-95; color: $primary-40; }
      &.processing { background: #E0F2FE; color: #0284C7; }
      &.approved { background: #D1FAE5; color: $success; }
      &.rejected { background: #FEE2E2; color: $error; }
      &.cancelled { background: $bg-secondary; color: $text-secondary; }
    }
  }

  .step-indicator {
    display: flex;
    align-items: center;
    margin-bottom: $spacing-md;
    padding: $spacing-sm 0;
    background: $bg-secondary;
    border-radius: $radius-md;

    .step {
      flex: 1;
      text-align: center;
      font-size: 24rpx;
      color: $text-tertiary;

      &.active {
        color: $primary-40;
        font-weight: 600;
      }
    }

    .line {
      width: 40rpx;
      height: 4rpx;
      background: $border-color;

      &.active {
        background: $primary-40;
      }
    }
  }

  .info-list {
    display: flex;
    flex-direction: column;
    gap: 12rpx;
    margin-bottom: $spacing-md;

    .info-item {
      display: flex;
      font-size: 28rpx;

      .label {
        color: $text-secondary;
        width: 140rpx;
      }

      .value {
        color: $text-primary;
        flex: 1;
      }
    }
  }

  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: $spacing-sm;
    border-top: 1px solid $border-color;

    .time {
      font-size: 24rpx;
      color: $text-tertiary;
    }

    .cancel-btn {
      margin: 0;
      padding: 0 24rpx;
      height: 56rpx;
      line-height: 56rpx;
      font-size: 24rpx;
      color: $text-secondary;
      background: $bg-secondary;
      border-radius: $radius-pill;

      &:active {
        background: $border-color;
      }
    }
  }
}
</style>
