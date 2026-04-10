<template>
  <view class="services-page">
    <view class="navbar">
      <text class="title">服务大厅</text>
    </view>

    <view class="hero-section">
      <text class="hero-tag">CAMPUS SERVICES</text>
      <text class="hero-title">智慧校园服务</text>
      <text class="hero-subtitle">一站式办理各类校园事务</text>
    </view>

    <view class="stats-grid">
      <view class="stat-card" @click="goToApplyStatus">
        <text class="stat-value">{{ activeApplies }}</text>
        <text class="stat-label">进行中的申请</text>
      </view>
      <view class="stat-card" @click="goToNotifications">
        <text class="stat-value">{{ unreadNotices }}</text>
        <text class="stat-label">待处理通知</text>
      </view>
    </view>

    <view class="service-matrix">
      <text class="section-title">校园事务</text>
      <view class="matrix-grid">
        <view 
          class="matrix-item" 
          v-for="item in services" 
          :key="item.name"
          :class="{ disabled: !item.enabled }"
          @click="handleServiceClick(item)"
        >
          <view class="icon-wrapper">
            <text class="icon">{{ item.icon }}</text>
          </view>
          <text class="name">{{ item.name }}</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMyApplications } from '@/api/apply'
import { getUnreadCount } from '@/api/notification'

const userStore = useUserStore()
const activeApplies = ref(0)
const unreadNotices = ref(0)

const services = [
  { name: '空教室申请', icon: '🏫', enabled: true, url: '/pages/apply/classroom' },
  { name: '我的申请', icon: '📋', enabled: true, url: '/pages/apply/status' },
  { name: '请假销假', icon: '📝', enabled: false },
  { name: '学籍管理', icon: '🎓', enabled: false },
  { name: '证明开具', icon: '📄', enabled: false },
  { name: '心理服务', icon: '❤️', enabled: false },
  { name: '缓考申请', icon: '⏳', enabled: false },
  { name: '学校官网', icon: '🌐', enabled: true, url: 'https://www.sdfmu.edu.cn', isExternal: true }
]

const loadData = async () => {
  try {
    if (userStore.userInfo?.id) {
      const applyRes = await getMyApplications(userStore.userInfo.id, { status: 'processing' })
      activeApplies.value = applyRes.total || 0
    }
    const noticeRes = await getUnreadCount()
    unreadNotices.value = noticeRes.count || 0
  } catch (error) {
    console.error('Failed to load services data', error)
  }
}

onMounted(() => {
  loadData()
})

const goToApplyStatus = () => {
  uni.navigateTo({ url: '/pages/apply/status' })
}

const goToNotifications = () => {
  // 跳转到通知列表
}

const handleServiceClick = (item: any) => {
  if (!item.enabled) {
    uni.showToast({ title: '功能开发中', icon: 'none' })
    return
  }
  
  if (item.isExternal) {
    // #ifdef H5
    window.open(item.url, '_blank')
    // #endif
    // #ifndef H5
    uni.setClipboardData({
      data: item.url,
      success: () => uni.showToast({ title: '链接已复制', icon: 'none' })
    })
    // #endif
  } else {
    uni.navigateTo({ url: item.url })
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.services-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: calc($spacing-md + env(safe-area-inset-bottom));
}

.navbar {
  height: 88rpx;
  padding-top: var(--status-bar-height, 44rpx);
  background: rgba(248, 250, 252, 0.85);
  backdrop-filter: blur(20px);
  display: flex;
  align-items: center;
  justify-content: center;
  position: sticky;
  top: 0;
  z-index: 100;
  
  .title {
    font-size: 36rpx;
    font-weight: 600;
    color: $text-primary;
  }
}

.hero-section {
  padding: $spacing-xl $spacing-md;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  animation: $animation-fade-in-up;

  .hero-tag {
    font-size: 24rpx;
    color: $primary-40;
    font-weight: 700;
    letter-spacing: 2rpx;
    margin-bottom: $spacing-xs;
  }

  .hero-title {
    font-size: 56rpx;
    font-weight: 800;
    color: $text-primary;
    margin-bottom: $spacing-xs;
  }

  .hero-subtitle {
    font-size: 28rpx;
    color: $text-secondary;
  }
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
  padding: 0 $spacing-md;
  margin-bottom: $spacing-xl;
  animation: $animation-fade-in-up;
  animation-delay: 0.1s;
  animation-fill-mode: both;

  .stat-card {
    background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
    border-radius: $radius-lg;
    padding: $spacing-lg;
    display: flex;
    flex-direction: column;
    box-shadow: $elevation-2;

    .stat-value {
      font-size: 48rpx;
      font-weight: 700;
      color: $text-inverse;
      margin-bottom: $spacing-xs;
    }

    .stat-label {
      font-size: 24rpx;
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

.service-matrix {
  padding: 0 $spacing-md;
  animation: $animation-fade-in-up;
  animation-delay: 0.2s;
  animation-fill-mode: both;

  .section-title {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: $spacing-md;
    display: block;
  }

  .matrix-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: $spacing-md $spacing-sm;
    background: $bg-card;
    border-radius: $radius-lg;
    padding: $spacing-lg $spacing-sm;
    box-shadow: $elevation-1;

    .matrix-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $spacing-sm;

      .icon-wrapper {
        width: 96rpx;
        height: 96rpx;
        border-radius: $radius-md;
        background: $primary-95;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: $transition-base;

        .icon {
          font-size: 48rpx;
        }
      }

      .name {
        font-size: 24rpx;
        color: $text-primary;
        text-align: center;
      }

      &.disabled {
        opacity: 0.5;
        
        .icon-wrapper {
          background: $bg-secondary;
          filter: grayscale(100%);
        }
      }

      &:active:not(.disabled) .icon-wrapper {
        transform: scale(0.9);
        background: $primary-90;
      }
    }
  }
}
</style>
