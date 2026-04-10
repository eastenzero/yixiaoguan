<template>
  <view class="profile-page">
    <view class="header-section">
      <view class="user-info">
        <view class="badge">已认证身份</view>
        <text class="username">{{ userInfo?.realName || userInfo?.nickName || '未登录' }}</text>
        <text class="dept">{{ userInfo?.deptName || '山东第一医科大学' }}</text>
      </view>
      <view class="avatar-wrapper">
        <image v-if="userInfo?.avatarUrl" class="avatar" :src="userInfo.avatarUrl" mode="aspectFill" />
        <view v-else class="avatar-placeholder">
          <text>{{ (userInfo?.realName || userInfo?.nickName || '用')[0] }}</text>
        </view>
      </view>
    </view>

    <view class="func-matrix">
      <view class="func-card" @click="goToHistory">
        <text class="icon">💬</text>
        <view class="card-text">
          <text class="title">问答历史</text>
          <text class="desc">查看与 AI 的对话记录</text>
        </view>
      </view>
      <view class="func-card" @click="goToApplyStatus">
        <text class="icon">📋</text>
        <view class="card-text">
          <text class="title">申请进度</text>
          <text class="desc">追踪事务办理状态</text>
        </view>
      </view>
    </view>

    <view class="bento-grid">
      <view class="bento-card semester-card">
        <view class="card-header">
          <text class="title">学期进度</text>
          <text class="week">第 8 周</text>
        </view>
        <view class="progress-bar">
          <view class="progress-inner" style="width: 40%"></view>
        </view>
        <text class="todo-hint">本周有 2 项待办事项</text>
      </view>

      <view class="bento-card services-card">
        <text class="title">常用服务</text>
        <view class="services-list">
          <view class="service-item" @click="showDevToast">
            <text class="icon">📅</text>
            <text>课表</text>
          </view>
          <view class="service-item" @click="showDevToast">
            <text class="icon">💯</text>
            <text>成绩</text>
          </view>
          <view class="service-item" @click="showDevToast">
            <text class="icon">💳</text>
            <text>一卡通</text>
          </view>
        </view>
      </view>
    </view>

    <view class="settings-group">
      <view class="setting-item" @click="showDevToast">
        <text class="icon">🔔</text>
        <text class="label">消息通知</text>
        <text class="arrow">></text>
      </view>
      <view class="setting-item" @click="showDevToast">
        <text class="icon">⚙️</text>
        <text class="label">系统设置</text>
        <text class="arrow">></text>
      </view>
      <view class="setting-item" @click="showDevToast">
        <text class="icon">📝</text>
        <text class="label">服务反馈</text>
        <text class="arrow">></text>
      </view>
      <view class="setting-item" @click="showDevToast">
        <text class="icon">❓</text>
        <text class="label">帮助中心</text>
        <text class="arrow">></text>
      </view>
      <view class="setting-item" @click="showDevToast">
        <text class="icon">ℹ️</text>
        <text class="label">关于</text>
        <text class="arrow">></text>
      </view>
    </view>

    <view class="footer">
      <button class="logout-btn" @click="handleLogout">退出登录</button>
      <text class="version">v1.0.0</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { logout } from '@/api/auth'

const userStore = useUserStore()
const userInfo = computed(() => userStore.userInfo)

const goToHistory = () => {
  uni.navigateTo({ url: '/pages/chat/history' })
}

const goToApplyStatus = () => {
  uni.navigateTo({ url: '/pages/apply/status' })
}

const showDevToast = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

const handleLogout = async () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: async (res) => {
      if (res.confirm) {
        try {
          if (userStore.token) {
            await logout(userStore.token)
          }
        } catch (e) {
          console.error(e)
        } finally {
          userStore.logout()
          uni.reLaunch({ url: '/pages/login/index' })
        }
      }
    }
  })
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.profile-page {
  min-height: 100vh;
  background: $bg-page;
  padding: $spacing-md;
  padding-bottom: calc($spacing-xl + env(safe-area-inset-bottom));
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--status-bar-height, 44rpx);
  margin-bottom: $spacing-xl;
  animation: $animation-fade-in-up;

  .user-info {
    display: flex;
    flex-direction: column;
    align-items: flex-start;

    .badge {
      background: $primary-95;
      color: $primary-40;
      font-size: 20rpx;
      padding: 4rpx 16rpx;
      border-radius: $radius-chip;
      margin-bottom: $spacing-sm;
      border: 1px solid $primary-80;
    }

    .username {
      font-size: 48rpx;
      font-weight: 700;
      color: $text-primary;
      margin-bottom: $spacing-xs;
    }

    .dept {
      font-size: 28rpx;
      color: $text-secondary;
    }
  }

  .avatar-wrapper {
    width: 144rpx;
    height: 144rpx;
    border-radius: 50%;
    background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
    padding: 6rpx;
    box-shadow: $elevation-2;

    .avatar {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: $bg-card;
    }

    .avatar-placeholder {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      background: $bg-card;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 64rpx;
      color: $primary-40;
      font-weight: 600;
    }
  }
}

.func-matrix {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;
  animation-delay: 0.1s;
  animation-fill-mode: both;

  .func-card {
    background: $bg-card;
    border-radius: $radius-lg;
    padding: $spacing-md;
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    box-shadow: $elevation-1;

    &:active {
      transform: scale(0.98);
    }

    .icon {
      font-size: 48rpx;
    }

    .card-text {
      display: flex;
      flex-direction: column;

      .title {
        font-size: 28rpx;
        font-weight: 600;
        color: $text-primary;
      }

      .desc {
        font-size: 20rpx;
        color: $text-tertiary;
      }
    }
  }
}

.bento-grid {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  margin-bottom: $spacing-lg;
  animation: $animation-fade-in-up;
  animation-delay: 0.2s;
  animation-fill-mode: both;

  .bento-card {
    background: $bg-card;
    border-radius: $radius-lg;
    padding: $spacing-md;
    box-shadow: $elevation-1;
  }

  .semester-card {
    .card-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: $spacing-sm;

      .title {
        font-size: 28rpx;
        font-weight: 600;
      }

      .week {
        font-size: 24rpx;
        color: $primary-40;
      }
    }

    .progress-bar {
      height: 12rpx;
      background: $bg-secondary;
      border-radius: $radius-pill;
      margin-bottom: $spacing-sm;
      overflow: hidden;

      .progress-inner {
        height: 100%;
        background: linear-gradient(90deg, $primary-40 0%, $primary-50 100%);
        border-radius: $radius-pill;
      }
    }

    .todo-hint {
      font-size: 24rpx;
      color: $text-secondary;
    }
  }

  .services-card {
    .title {
      font-size: 28rpx;
      font-weight: 600;
      margin-bottom: $spacing-md;
      display: block;
    }

    .services-list {
      display: flex;
      justify-content: space-around;

      .service-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: $spacing-xs;

        .icon {
          font-size: 48rpx;
        }

        text {
          font-size: 24rpx;
          color: $text-secondary;
        }
      }
    }
  }
}

.settings-group {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: 0 $spacing-md;
  margin-bottom: $spacing-xl;
  box-shadow: $elevation-1;
  animation: $animation-fade-in-up;
  animation-delay: 0.3s;
  animation-fill-mode: both;

  .setting-item {
    display: flex;
    align-items: center;
    padding: $spacing-md 0;
    border-bottom: 1px solid $border-color;

    &:last-child {
      border-bottom: none;
    }

    &:active {
      opacity: 0.7;
    }

    .icon {
      font-size: 36rpx;
      margin-right: $spacing-sm;
    }

    .label {
      flex: 1;
      font-size: 28rpx;
      color: $text-primary;
    }

    .arrow {
      font-size: 28rpx;
      color: $text-tertiary;
    }
  }
}

.footer {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-md;
  animation: $animation-fade-in-up;
  animation-delay: 0.4s;
  animation-fill-mode: both;

  .logout-btn {
    width: 100%;
    height: 88rpx;
    border-radius: $radius-pill;
    background: $bg-card;
    color: $error;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid rgba(220, 38, 38, 0.2);

    &:active {
      background: rgba(220, 38, 38, 0.05);
    }
  }

  .version {
    font-size: 24rpx;
    color: $text-tertiary;
  }
}
</style>
