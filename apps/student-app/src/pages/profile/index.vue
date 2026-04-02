<template>
  <view class="profile-page">
    <view class="profile-bg-wash"></view>

    <!-- 头部身份区（大头像编辑排版） -->
    <view class="user-hero staggered-1">
      <view class="user-info-text">
        <view class="verified-badge">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none" class="check-icon">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <text class="badge-text">已认证身份</text>
        </view>
        <text class="user-name">{{ userName }}</text>
        <text class="user-dept">{{ userDeptAndGrade }}</text>
      </view>
      <view class="avatar-giant">
        <image v-if="userAvatar" :src="userAvatar" class="avatar-img" mode="aspectFill" />
        <text v-else class="avatar-alpha">{{ userName.charAt(0) }}</text>
      </view>
    </view>

    <!-- 功能流转矩阵 (双列宫格) -->
    <view class="action-matrix staggered-2">
      <view class="matrix-card" @click="goToQuestions">
        <view class="matrix-icon-box bg-history">
          <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" stroke-width="2" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        </view>
        <view class="matrix-text">
          <text class="matrix-title">问答历史</text>
          <text class="matrix-desc">知识回顾</text>
        </view>
      </view>
      
      <view class="matrix-card" @click="goToApplyStatus">
        <view class="matrix-icon-box bg-progress">
          <svg viewBox="0 0 24 24" width="32" height="32" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        </view>
        <view class="matrix-text">
          <text class="matrix-title">申请进度</text>
          <text class="matrix-desc">流程追踪</text>
        </view>
      </view>
    </view>

    <!-- Bento Grid 区域 -->
    <view class="bento-grid staggered-3">
      <!-- 学期进度卡片 -->
      <view class="bento-card semester-card">
        <view class="card-bg-primary">
          <text class="card-title">学期进度</text>
          <view class="progress-header">
            <text class="progress-label">第 12 周 / 共 18 周</text>
            <text class="progress-percent">67%</text>
          </view>
          <view class="progress-track">
            <view class="progress-fill" style="width: 67%"></view>
          </view>
          <view class="todo-section">
            <text class="todo-label">待办提醒</text>
            <text class="todo-text">您有 2 项课程作业即将截止，请及时提交。</text>
          </view>
        </view>
      </view>

      <!-- AI 助手历史卡片 -->
      <view class="bento-card ai-history-card">
        <view class="card-header" @click="goToChat">
          <view class="header-left">
            <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none" class="header-icon">
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
              <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <text class="card-title">AI 助手历史</text>
          </view>
          <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" class="header-arrow">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </view>
        <view class="history-list">
          <view class="history-item" v-for="item in aiHistory" :key="item.id" @click="goToChat">
            <text class="item-question">{{ item.question }}</text>
            <text class="item-answer" line-clamp-1>{{ item.answer }}</text>
            <view class="item-meta">
              <text class="item-time">{{ item.time }}</text>
              <text class="item-tag" :class="item.tagClass">{{ item.tag }}</text>
            </view>
          </view>
        </view>
      </view>

      <!-- 常用服务列表 -->
      <view class="bento-card favorite-services">
        <text class="card-title">常用服务</text>
        <view class="service-list">
          <view class="service-item" v-for="svc in favoriteServices" :key="svc.name" @click="showDeveloping">
            <view class="service-icon" :class="svc.bgClass">
              <svg v-if="svc.icon === 'calendar'" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line>
              </svg>
              <svg v-else-if="svc.icon === 'star'" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
              </svg>
              <svg v-else-if="svc.icon === 'wallet'" viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2" fill="none">
                <path d="M20 12V8H6a2 2 0 0 1-2-2c0-1.1.9-2 2-2h12v4"></path><path d="M4 6v12a2 2 0 0 0 2 2h14v-4"></path><path d="M18 12a2 2 0 0 0-2 2c0 1.1.9 2 2 2h4v-4h-4z"></path>
              </svg>
            </view>
            <view class="service-info">
              <text class="service-name">{{ svc.name }}</text>
              <text class="service-desc">{{ svc.desc }}</text>
            </view>
            <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" class="service-arrow">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </view>
        </view>
      </view>
    </view>

    <!-- 设置列表区域 -->
    <view class="settings-wrapper staggered-4">
      <!-- 设置与隐私组 -->
      <view class="bento-card settings-card">
        <text class="group-title">设置与隐私</text>
        <view class="settings-list">
          <view class="settings-item" @click="showDeveloping">
            <view class="settings-icon-wrap bg-primary-light">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
                <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path><path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
              </svg>
            </view>
            <text class="settings-label">消息与通知</text>
            <view class="settings-action">
              <text class="settings-prompt">3条未读</text>
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" class="settings-arrow">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </view>
          </view>
          <view class="settings-item" @click="showDeveloping">
            <view class="settings-icon-wrap bg-secondary-light">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
            </view>
            <text class="settings-label">系统设置</text>
            <view class="settings-action">
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" class="settings-arrow">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </view>
          </view>
        </view>
      </view>

      <!-- 反馈与支持组 -->
      <view class="bento-card settings-card">
        <text class="group-title">反馈与支持</text>
        <view class="settings-list">
          <view class="settings-item" @click="showDeveloping">
            <view class="settings-icon-wrap bg-success-light">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path>
              </svg>
            </view>
            <text class="settings-label">服务反馈</text>
            <view class="settings-action">
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" class="settings-arrow">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </view>
          </view>
          <view class="settings-item" @click="showDeveloping">
            <view class="settings-icon-wrap bg-warning-light">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </view>
            <text class="settings-label">帮助中心</text>
            <view class="settings-action">
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" class="settings-arrow">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </view>
          </view>
        </view>
      </view>

      <!-- 关于系统组 -->
      <view class="bento-card settings-card">
        <text class="group-title">关于系统</text>
        <view class="settings-list">
          <view class="settings-item" @click="showDeveloping">
            <view class="settings-icon-wrap bg-info-light">
              <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none">
                <circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
            </view>
            <text class="settings-label">关于医小管</text>
            <view class="settings-action">
              <text class="settings-prompt">v1.0.0</text>
              <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none" class="settings-arrow">
                <polyline points="9 18 15 12 9 6"></polyline>
              </svg>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 退出登录区 -->
    <view class="signout-section staggered-5">
      <button class="signout-btn" @click="handleLogout">退出当前账号</button>
    </view>

    <!-- 底部 Footer -->
    <view class="app-footer staggered-5">
      <view class="footer-brand">
        <view class="footer-logo"></view>
        <text class="footer-name">医小管</text>
      </view>
      <text class="footer-version">版本 1.0.0 (Build 2024.04)</text>
      <text class="footer-copyright">© 2024 医小管智能化平台</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

const userName = computed(() => {
  return userStore.userInfo?.realName || userStore.userInfo?.username || '未登录'
})

const userDeptAndGrade = computed(() => {
  const info = userStore.userInfo as any
  if (info && info.deptName && info.grade) {
    return `${info.deptName} · ${info.grade}级`
  } else if (info && info.deptName) {
    return info.deptName
  }
  return '未绑定院系'
})

const userAvatar = computed(() => (userStore.userInfo as any)?.avatar || '')

// AI 助手历史数据
const aiHistory = ref([
  { id: 1, question: '如何申请跨专业学术交流项目？', answer: '您好！根据学校规定，跨专业学术交流项目需要在每学期开学后两周内提交申请...', time: '2小时前', tag: '学业咨询', tagClass: 'tag-primary' },
  { id: 2, question: '图书馆数字化资源访问权限', answer: '在校外访问图书馆资源需要通过学校VPN或者使用CARSI联盟认证...', time: '昨天', tag: '资源获取', tagClass: 'tag-secondary' }
])

// 常用服务数据
const favoriteServices = ref([
  { name: '我的课表', desc: '查看今日排课与教室', icon: 'calendar', bgClass: 'bg-teal' },
  { name: '成绩查询', desc: '本学期及历史成绩', icon: 'star', bgClass: 'bg-blue' },
  { name: '校园一卡通', desc: '余额: ￥154.20', icon: 'wallet', bgClass: 'bg-orange' }
])

const goToQuestions = () => {
  uni.navigateTo({ url: '/pages/questions/index' })
}

const goToApplyStatus = () => {
  uni.switchTab({ url: '/pages/apply/status' })
}

const goToChat = () => {
  uni.switchTab({ url: '/pages/chat/index' })
}

const showDeveloping = () => {
  uni.showToast({ title: '功能开发中', icon: 'none' })
}

const handleLogout = () => {
  uni.showModal({
    title: '提示',
    content: '确定要退出登录吗？',
    success: (res) => {
      if (res.confirm) {
        userStore.logout()
        uni.reLaunch({ url: '/pages/login/index' })
      }
    }
  })
}
</script>

<style scoped lang="scss">
// MD3 颜色变量
$primary: #006a64;
$primary-container: #00A79D;
$on-primary: #ffffff;
$on-primary-container: #00201e;
$secondary: #4a6360;
$secondary-container: #cce8e4;
$surface: #f5fbf9;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$surface-variant: #dbe5e2;
$on-surface: #171d1c;
$on-surface-variant: #5a635f;
$error: #ba1a1a;
$outline: #6f7977;
$outline-variant: #bec9c6;

// 语义化颜色
$success: #4caf50;
$warning: #ff9800;
$info: #2196f3;

page {
  background-color: $surface;
}

.profile-page {
  min-height: 100vh;
  position: relative;
  background-color: $surface;
  padding: 0 40rpx 60rpx;
  display: flex;
  flex-direction: column;
}

.profile-bg-wash {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 500rpx;
  background: linear-gradient(180deg, rgba($primary, 0.08) 0%, rgba($surface, 0) 100%);
  pointer-events: none;
  z-index: 0;
}

// 高级入场动画
@keyframes fadeUpRank {
  from { opacity: 0; transform: translateY(30rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.staggered-1 { animation: fadeUpRank 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.1s; }
.staggered-2 { animation: fadeUpRank 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.2s; }
.staggered-3 { animation: fadeUpRank 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.3s; }
.staggered-4 { animation: fadeUpRank 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.4s; }
.staggered-5 { animation: fadeUpRank 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.5s; }

// 头部身份区
.user-hero {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 120rpx;
  margin-bottom: 60rpx;
}

.user-info-text {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 16rpx;
}

.verified-badge {
  display: flex;
  align-items: center;
  gap: 10rpx;
  background: linear-gradient(135deg, rgba($primary, 0.12) 0%, rgba($primary, 0.06) 100%);
  padding: 8rpx 20rpx;
  border-radius: 30rpx;
  border: 1rpx solid rgba($primary, 0.1);
  
  .check-icon {
    color: $primary;
  }
  
  .badge-text {
    font-size: 22rpx;
    color: $primary;
    font-weight: 600;
    letter-spacing: 1rpx;
  }
}

.user-name {
  font-size: 56rpx;
  font-weight: 800;
  color: $on-surface;
  letter-spacing: 2rpx;
}

.user-dept {
  font-size: 28rpx;
  color: $on-surface-variant;
  font-weight: 500;
}

// 极大头像
.avatar-giant {
  width: 176rpx;
  height: 176rpx;
  border-radius: 56rpx;
  background: linear-gradient(135deg, $primary 0%, $primary-container 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 24rpx 48rpx rgba($primary, 0.25);
  overflow: hidden;
  transition: transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  
  &:active {
    transform: scale(0.94);
  }

  .avatar-alpha {
    font-size: 72rpx;
    font-weight: 800;
    color: #ffffff;
  }

  .avatar-img {
    width: 100%;
    height: 100%;
  }
}

// 功能流转矩阵 - Bento Grid 风格
.action-matrix {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 24rpx;
  margin-bottom: 48rpx;
}

.matrix-card {
  flex: 1;
  background-color: $surface-container-lowest;
  padding: 40rpx 32rpx;
  border-radius: 32rpx;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.03);
  transition: transform 0.15s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.15s;

  &:active {
    transform: scale(0.96);
    box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.02);
  }
}

.matrix-icon-box {
  width: 96rpx;
  height: 96rpx;
  border-radius: 28rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
  transition: transform 0.2s ease;
  
  .matrix-card:active & {
    transform: scale(0.95);
  }
  
  &.bg-history {
    background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
    color: #1976D2;
  }
  
  &.bg-progress {
    background: linear-gradient(135deg, #E8F5E9 0%, #C8E6C9 100%);
    color: #388E3C;
  }
}

.matrix-text {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.matrix-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $on-surface;
}

.matrix-desc {
  font-size: 24rpx;
  color: $on-surface-variant;
}

// Bento Grid 区域
.bento-grid {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 32rpx;
  margin-bottom: 48rpx;
}

.bento-card {
  background-color: $surface-container-lowest;
  border-radius: 32rpx;
  padding: 32rpx;
  box-shadow: 0 8rpx 32rpx rgba(0,0,0,0.03);
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $on-surface;
  margin-bottom: 24rpx;
}

// 学期进度卡片
.semester-card {
  padding: 0;
  overflow: hidden;
  
  .card-bg-primary {
    background: linear-gradient(135deg, $primary 0%, $primary-container 100%);
    padding: 32rpx;
    color: $on-primary;
  }
  
  .card-title {
    color: $on-primary;
    margin-bottom: 24rpx;
    opacity: 0.9;
  }
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.progress-label {
  font-size: 28rpx;
  color: rgba($on-primary, 0.85);
}

.progress-percent {
  font-size: 36rpx;
  font-weight: 700;
  color: $on-primary;
}

.progress-track {
  height: 12rpx;
  background-color: rgba($on-primary, 0.2);
  border-radius: 6rpx;
  overflow: hidden;
  margin-bottom: 32rpx;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, $on-primary 0%, rgba($on-primary, 0.7) 100%);
  border-radius: 6rpx;
  transition: width 0.3s ease;
}

.todo-section {
  background-color: rgba($on-primary, 0.1);
  border-radius: 20rpx;
  padding: 24rpx;
}

.todo-label {
  display: block;
  font-size: 26rpx;
  font-weight: 600;
  color: $on-primary;
  margin-bottom: 8rpx;
}

.todo-text {
  font-size: 24rpx;
  color: rgba($on-primary, 0.8);
  line-height: 1.5;
}

// AI 助手历史卡片
.ai-history-card {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24rpx;
    cursor: pointer;
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 16rpx;
    }
    
    .header-icon {
      color: $primary;
    }
    
    .card-title {
      margin-bottom: 0;
    }
    
    .header-arrow {
      color: $outline;
    }
  }
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.history-item {
  padding: 24rpx;
  background-color: $surface-container-low;
  border-radius: 24rpx;
  transition: background-color 0.15s ease;
  
  &:active {
    background-color: rgba($primary, 0.08);
  }
}

.item-question {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: $on-surface;
  margin-bottom: 8rpx;
}

.item-answer {
  display: block;
  font-size: 24rpx;
  color: $on-surface-variant;
  margin-bottom: 16rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-time {
  font-size: 22rpx;
  color: $outline;
}

.item-tag {
  font-size: 20rpx;
  font-weight: 600;
  padding: 6rpx 16rpx;
  border-radius: 20rpx;
  
  &.tag-primary {
    background-color: rgba($primary, 0.1);
    color: $primary;
  }
  
  &.tag-secondary {
    background-color: rgba($info, 0.1);
    color: $info;
  }
}

// 常用服务卡片
.favorite-services {
  .card-title {
    margin-bottom: 24rpx;
  }
}

.service-list {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
}

.service-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  background-color: $surface-container-low;
  border-radius: 24rpx;
  transition: background-color 0.15s ease;
  
  &:active {
    background-color: rgba($primary, 0.08);
  }
}

.service-icon {
  width: 64rpx;
  height: 64rpx;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
  
  &.bg-teal {
    background: linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%);
    color: #00695C;
  }
  
  &.bg-blue {
    background: linear-gradient(135deg, #E3F2FD 0%, #BBDEFB 100%);
    color: #1565C0;
  }
  
  &.bg-orange {
    background: linear-gradient(135deg, #FFF3E0 0%, #FFE0B2 100%);
    color: #E65100;
  }
}

.service-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.service-name {
  font-size: 30rpx;
  font-weight: 600;
  color: $on-surface;
}

.service-desc {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.service-arrow {
  color: $outline-variant;
  flex-shrink: 0;
}

// 设置区域包装
.settings-wrapper {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 32rpx;
  margin-bottom: 48rpx;
}

.settings-card {
  padding: 32rpx;
}

.group-title {
  font-size: 26rpx;
  font-weight: 600;
  color: $on-surface-variant;
  margin-bottom: 24rpx;
  padding-left: 8rpx;
}

.settings-list {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.settings-item {
  display: flex;
  align-items: center;
  padding: 24rpx;
  border-radius: 20rpx;
  transition: background-color 0.15s ease;
  
  &:active {
    background-color: rgba($primary, 0.04);
  }
}

.settings-icon-wrap {
  width: 56rpx;
  height: 56rpx;
  border-radius: 16rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 24rpx;
  flex-shrink: 0;
  
  &.bg-primary-light {
    background-color: rgba($primary, 0.1);
    color: $primary;
  }
  
  &.bg-secondary-light {
    background-color: rgba($secondary, 0.1);
    color: $secondary;
  }
  
  &.bg-success-light {
    background-color: rgba($success, 0.1);
    color: $success;
  }
  
  &.bg-warning-light {
    background-color: rgba($warning, 0.1);
    color: $warning;
  }
  
  &.bg-info-light {
    background-color: rgba($info, 0.1);
    color: $info;
  }
}

.settings-label {
  flex: 1;
  font-size: 30rpx;
  color: $on-surface;
  font-weight: 500;
}

.settings-action {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.settings-prompt {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.settings-arrow {
  color: $outline;
}

// 退出登录
.signout-section {
  position: relative;
  z-index: 1;
  margin-bottom: 48rpx;
}

.signout-btn {
  background-color: transparent;
  color: $error;
  border-radius: 48rpx;
  height: 96rpx;
  line-height: 96rpx;
  font-size: 30rpx;
  font-weight: 600;
  border: 2rpx solid rgba($error, 0.3);
  transition: transform 0.15s cubic-bezier(0.2, 0.8, 0.2, 1), background-color 0.15s;

  &:active {
    transform: scale(0.96);
    background-color: rgba($error, 0.05);
  }
  
  &::after {
    display: none;
  }
}

// 底部 Footer
.app-footer {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 0;
  position: relative;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.footer-logo {
  width: 40rpx;
  height: 40rpx;
  border-radius: 12rpx;
  background: linear-gradient(135deg, $primary 0%, $primary-container 100%);
}

.footer-name {
  font-size: 28rpx;
  font-weight: 700;
  color: $on-surface;
}

.footer-version {
  font-size: 22rpx;
  color: $on-surface-variant;
  margin-bottom: 8rpx;
}

.footer-copyright {
  font-size: 20rpx;
  color: rgba($on-surface-variant, 0.6);
}
</style>
