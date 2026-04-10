<template>
  <view class="home-page">
    <!-- 欢迎区 -->
    <view class="welcome-section">
      <view class="greeting">
        <text class="time-text">{{ greetingText }}</text>
        <text class="username">{{ userInfo?.nickName || '同学' }}</text>
      </view>
      <view class="status-card" @click="goToApplyStatus">
        <text class="status-num">{{ activeApplies }}</text>
        <text class="status-label">进行中</text>
      </view>
    </view>

    <!-- AI 输入区 -->
    <view class="ai-search-section">
      <view class="search-bar" @click="goToChat('')">
        <view class="ai-badge">
          <text class="icon">✨</text>
        </view>
        <text class="placeholder">问我关于校园的任何问题...</text>
        <view class="arrow-btn">
          <text class="icon">→</text>
        </view>
      </view>
      
      <!-- 快捷标签 -->
      <scroll-view scroll-x class="quick-tags" :show-scrollbar="false">
        <view class="tags-container">
          <view 
            class="pill-tag" 
            v-for="tag in quickTags" 
            :key="tag"
            @click="goToChat(tag)"
          >
            {{ tag }}
          </view>
        </view>
      </scroll-view>
    </view>

    <!-- Bento Grid -->
    <view class="bento-grid">
      <view class="bento-item large-card" @click="goToServices">
        <view class="card-content">
          <text class="card-title">校园事务导办</text>
          <text class="card-desc">一站式办理请假、证明等业务</text>
        </view>
        <view class="card-icon">📋</view>
      </view>
      
      <view class="bento-row">
        <view class="bento-item small-card" @click="goToClassroomApply">
          <view class="card-icon">🏫</view>
          <text class="card-title">空教室预约</text>
        </view>
        <view class="bento-item small-card" @click="goToApplyStatus">
          <view class="card-icon">⏳</view>
          <text class="card-title">申请进度</text>
        </view>
      </view>
    </view>

    <!-- 官方链接区 -->
    <view class="links-section">
      <text class="section-title">常用链接</text>
      <view class="links-grid">
        <view class="link-card" v-for="link in officialLinks" :key="link.name" @click="openLink(link.url)">
          <text class="link-icon">{{ link.icon }}</text>
          <text class="link-name">{{ link.name }}</text>
        </view>
      </view>
    </view>

    <!-- 通知 Banner -->
    <view class="notice-banner" v-if="latestNotice" @click="viewNotice">
      <text class="notice-icon">🔔</text>
      <text class="notice-text">{{ latestNotice.title }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'
import { getMyApplications } from '@/api/apply'
import { getNotificationList } from '@/api/notification'

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

const greetingText = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好，'
  if (hour < 18) return '下午好，'
  return '晚上好，'
})

const activeApplies = ref(0)
const latestNotice = ref<any>(null)

const quickTags = ['奖学金申请', '选课指南', '图书馆开放时间', '校历查询']

const officialLinks = [
  { name: '教务管理', icon: '📚', url: 'https://jw.sdfmu.edu.cn' },
  { name: '图书馆', icon: '📖', url: 'https://lib.sdfmu.edu.cn' },
  { name: '学生邮箱', icon: '📧', url: 'https://mail.sdfmu.edu.cn' }
]

const loadData = async () => {
  try {
    if (userInfo.value?.id) {
      const applyRes = await getMyApplications(userInfo.value.id, { status: 'processing' })
      activeApplies.value = applyRes.total || 0
    }
    const noticeRes = await getNotificationList(1, 1)
    if (noticeRes.rows && noticeRes.rows.length > 0) {
      latestNotice.value = noticeRes.rows[0]
    }
  } catch (error) {
    console.error('Failed to load home data', error)
  }
}

onMounted(() => {
  loadData()
})

const goToChat = (query: string) => {
  uni.switchTab({
    url: `/pages/chat/index?query=${encodeURIComponent(query)}`
  })
}

const goToServices = () => {
  uni.switchTab({ url: '/pages/services/index' })
}

const goToClassroomApply = () => {
  uni.navigateTo({ url: '/pages/apply/classroom' })
}

const goToApplyStatus = () => {
  uni.navigateTo({ url: '/pages/apply/status' })
}

const openLink = (url: string) => {
  // #ifdef H5
  window.open(url, '_blank')
  // #endif
  // #ifndef H5
  uni.setClipboardData({
    data: url,
    success: () => uni.showToast({ title: '链接已复制', icon: 'none' })
  })
  // #endif
}

const viewNotice = () => {
  // 跳转到通知详情
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.home-page {
  min-height: 100vh;
  background: $bg-page;
  padding: $spacing-md;
  padding-bottom: calc($spacing-md + env(safe-area-inset-bottom));
}

.welcome-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;

  .greeting {
    display: flex;
    flex-direction: column;

    .time-text {
      font-size: 28rpx;
      color: $text-secondary;
      margin-bottom: 4rpx;
    }

    .username {
      font-size: 40rpx;
      font-weight: 700;
      color: $text-primary;
    }
  }

  .status-card {
    background: $bg-card;
    padding: $spacing-sm $spacing-md;
    border-radius: $radius-md;
    box-shadow: $elevation-1;
    display: flex;
    flex-direction: column;
    align-items: center;

    .status-num {
      font-size: 32rpx;
      font-weight: 700;
      color: $primary-40;
    }

    .status-label {
      font-size: 20rpx;
      color: $text-secondary;
    }
  }
}

.ai-search-section {
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;
  animation-delay: 0.05s;
  animation-fill-mode: both;

  .search-bar {
    display: flex;
    align-items: center;
    background: $bg-card;
    height: 96rpx;
    border-radius: $radius-pill;
    padding: 0 $spacing-sm;
    box-shadow: $elevation-2;
    margin-bottom: $spacing-md;

    .ai-badge {
      width: 64rpx;
      height: 64rpx;
      border-radius: 50%;
      background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-right: $spacing-sm;

      .icon {
        color: $text-inverse;
        font-size: 32rpx;
      }
    }

    .placeholder {
      flex: 1;
      font-size: 28rpx;
      color: $text-tertiary;
    }

    .arrow-btn {
      width: 64rpx;
      height: 64rpx;
      border-radius: 50%;
      background: $bg-secondary;
      display: flex;
      align-items: center;
      justify-content: center;

      .icon {
        color: $primary-40;
        font-size: 32rpx;
      }
    }
  }

  .quick-tags {
    width: 100%;
    
    .tags-container {
      display: flex;
      gap: $spacing-sm;
      padding: 4rpx;
    }

    .pill-tag {
      padding: 12rpx 24rpx;
      background: $bg-card;
      border-radius: $radius-chip;
      font-size: 24rpx;
      color: $primary-40;
      border: 1px solid $primary-80;
      white-space: nowrap;
      box-shadow: $elevation-1;
    }
  }
}

.bento-grid {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;
  animation-delay: 0.1s;
  animation-fill-mode: both;

  .bento-item {
    background: $bg-card;
    border-radius: $radius-lg;
    box-shadow: $elevation-1;
    padding: $spacing-md;
    display: flex;
    transition: $transition-base;

    &:active {
      transform: scale(0.98);
    }
  }

  .large-card {
    background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
    color: $text-inverse;
    justify-content: space-between;
    align-items: center;
    height: 160rpx;

    .card-content {
      display: flex;
      flex-direction: column;
    }

    .card-title {
      font-size: 36rpx;
      font-weight: 700;
      margin-bottom: 8rpx;
    }

    .card-desc {
      font-size: 24rpx;
      opacity: 0.9;
    }

    .card-icon {
      font-size: 64rpx;
    }
  }

  .bento-row {
    display: flex;
    gap: $spacing-md;

    .small-card {
      flex: 1;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 160rpx;
      gap: $spacing-sm;

      .card-icon {
        font-size: 48rpx;
      }

      .card-title {
        font-size: 28rpx;
        font-weight: 600;
        color: $text-primary;
      }
    }
  }
}

.links-section {
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;
  animation-delay: 0.15s;
  animation-fill-mode: both;

  .section-title {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: $spacing-md;
    display: block;
  }

  .links-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: $spacing-md;

    .link-card {
      background: $bg-card;
      border-radius: $radius-md;
      padding: $spacing-md 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $spacing-xs;
      box-shadow: $elevation-1;

      .link-icon {
        font-size: 40rpx;
      }

      .link-name {
        font-size: 24rpx;
        color: $text-secondary;
      }
    }
  }
}

.notice-banner {
  background: $primary-95;
  border-radius: $radius-md;
  padding: $spacing-sm $spacing-md;
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  border: 1px solid $primary-80;
  animation: $animation-fade-in-up;
  animation-delay: 0.2s;
  animation-fill-mode: both;

  .notice-icon {
    font-size: 32rpx;
  }

  .notice-text {
    flex: 1;
    font-size: 26rpx;
    color: $primary-40;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}
</style>
