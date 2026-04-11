<template>
  <view class="dashboard-page">
    <!-- 自定义顶栏 -->
    <view class="custom-app-bar">
      <view class="app-bar-content">
        <view class="app-bar-left">
          <IconDashboard :size="24" :color="primaryColor" />
          <text class="app-bar-title">工作台</text>
        </view>
        <view class="app-bar-right" @click="handleNotification">
          <IconBell :size="24" :color="onSurfaceColor" />
          <view class="notification-dot"></view>
        </view>
      </view>
    </view>

    <!-- 主内容区域 -->
    <view class="main-content">
      <!-- 欢迎横幅 -->
      <view class="welcome-banner animate-fade-up">
        <view class="welcome-content">
          <view class="welcome-text">
            <text class="welcome-greeting">早上好，梁老师 👋</text>
            <text class="welcome-subtitle">今天有 3 条待处理提问</text>
          </view>
          <view class="avatar-placeholder"></view>
        </view>
        <view class="welcome-decoration"></view>
      </view>

      <!-- 快捷操作 -->
      <view class="quick-actions animate-fade-up delay-1">
        <scroll-view scroll-x class="quick-actions-scroll" show-scrollbar="false">
          <view class="quick-actions-content">
            <view class="quick-action-btn" @click="handleQuickAction('knowledge')">
              <IconPlus :size="20" :color="primaryColor" />
              <text class="quick-action-text">新建知识</text>
            </view>
            <view class="quick-action-btn" @click="handleQuickAction('notice')">
              <IconMegaphone :size="20" :color="primaryColor" />
              <text class="quick-action-text">发布通知</text>
            </view>
            <view class="quick-action-btn" @click="handleQuickAction('report')">
              <IconChart :size="20" :color="primaryColor" />
              <text class="quick-action-text">数据报告</text>
            </view>
            <view class="quick-action-btn" @click="handleQuickAction('settings')">
              <IconSettings :size="20" :color="primaryColor" />
              <text class="quick-action-text">系统设置</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- 统计网格 -->
      <view class="stats-grid animate-fade-up delay-2">
        <view class="stat-card stat-card-1">
          <view class="stat-header">
            <IconDashboard :size="24" :color="primaryColor" />
            <text class="stat-number">12</text>
          </view>
          <text class="stat-label">今日提问</text>
        </view>
        <view class="stat-card stat-card-2">
          <view class="stat-header">
            <IconAlert :size="24" :color="errorColor" />
            <text class="stat-number">3</text>
          </view>
          <text class="stat-label">待处理</text>
        </view>
        <view class="stat-card stat-card-3">
          <view class="stat-header">
            <IconBook :size="24" :color="emeraldColor" />
            <text class="stat-number">731</text>
          </view>
          <text class="stat-label">知识条目</text>
        </view>
        <view class="stat-card stat-card-4">
          <view class="stat-header">
            <IconCheck :size="24" :color="amberColor" />
            <text class="stat-number">5</text>
          </view>
          <text class="stat-label">今日审批</text>
        </view>
      </view>

      <!-- 待处理提问列表 -->
      <view class="questions-section animate-fade-up delay-3">
        <view class="section-header">
          <text class="section-title">待处理提问</text>
          <text class="section-link" @click="viewAllQuestions">查看全部</text>
        </view>

        <view class="question-list">
          <view
            v-for="(question, index) in pendingQuestions"
            :key="index"
            class="question-card"
            @click="viewQuestion(question.id)"
          >
            <view class="question-header">
              <view class="question-author">
                <text class="author-name">{{ question.author }}</text>
                <view class="department-tag">
                  <text class="department-text">{{ question.department }}</text>
                </view>
              </view>
              <text class="question-time">{{ question.time }}</text>
            </view>
            <text class="question-content">{{ question.content }}</text>
            <view class="question-footer">
              <view class="status-badge">
                <view class="status-dot" :class="`status-${question.status}`"></view>
                <text class="status-text" :class="`status-text-${question.status}`">{{ question.statusText }}</text>
              </view>
              <IconArrowRight :size="16" :color="onSurfaceVariantColor" />
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 底部导航栏 -->
    <BottomNavBar :current="0" :badge="3" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import IconDashboard from '../../components/icons/IconDashboard.vue'
import IconBell from '../../components/icons/IconBell.vue'
import IconPlus from '../../components/icons/IconPlus.vue'
import IconMegaphone from '../../components/icons/IconMegaphone.vue'
import IconChart from '../../components/icons/IconChart.vue'
import IconSettings from '../../components/icons/IconSettings.vue'
import IconAlert from '../../components/icons/IconAlert.vue'
import IconBook from '../../components/icons/IconBook.vue'
import IconCheck from '../../components/icons/IconCheck.vue'
import IconArrowRight from '../../components/icons/IconArrowRight.vue'
import BottomNavBar from '../../components/BottomNavBar.vue'

// 主题色
const primaryColor = '#702ae1'
const onSurfaceColor = '#2f2e32'
const onSurfaceVariantColor = '#5d5b5f'
const errorColor = '#b41340'
const emeraldColor = '#059669'
const amberColor = '#d97706'

// Mock 数据
const pendingQuestions = ref([
  {
    id: 1,
    author: '张晓明',
    department: '软件工程系',
    time: '10:24',
    content: '老师，请问关于 React 的 useEffect 钩子函数中的依赖项...',
    status: 'pending',
    statusText: '待处理'
  },
  {
    id: 2,
    author: '李思源',
    department: '计算机科学',
    time: '09:15',
    content: '大模型微调时，Lora参数的选择一般基于什么标准？',
    status: 'processing',
    statusText: '处理中'
  },
  {
    id: 3,
    author: '陈锦',
    department: '数学系',
    time: '昨天',
    content: '关于线性代数中特征值分解在图像压缩中的应用...',
    status: 'pending',
    statusText: '待处理'
  }
])

// 通知点击
const handleNotification = () => {
  uni.navigateTo({ url: '/pages/notifications/index' })
}

// 快捷操作
const handleQuickAction = (type: string) => {
  const routes: Record<string, string> = {
    knowledge: '/pages/knowledge/create',
    notice: '/pages/notice/create',
    report: '/pages/report/index',
    settings: '/pages/settings/index'
  }
  uni.navigateTo({ url: routes[type] || '/pages/dashboard/index' })
}

// 查看全部提问
const viewAllQuestions = () => {
  uni.switchTab({ url: '/pages/questions/index' })
}

// 查看单个提问
const viewQuestion = (id: number) => {
  uni.navigateTo({ url: `/pages/questions/detail?id=${id}` })
}
</script>

<style lang="scss" scoped>
@import '../../styles/theme.scss';

.dashboard-page {
  min-height: 100vh;
  background: $surface;
  padding-bottom: calc(80px + env(safe-area-inset-bottom));
}

// 自定义顶栏
.custom-app-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 50;
  height: 56px;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.app-bar-content {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
}

.app-bar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-bar-title {
  font-family: $font-headline;
  font-size: 20px;
  font-weight: 700;
  color: $on-surface;
}

.app-bar-right {
  position: relative;
  padding: 8px;
  
  &:active {
    transform: scale(0.9);
  }
}

.notification-dot {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 8px;
  height: 8px;
  background: $error;
  border-radius: 50%;
  border: 2px solid white;
}

// 主内容区域
.main-content {
  padding-top: 72px;
  padding-left: 16px;
  padding-right: 16px;
}

// 欢迎横幅
.welcome-banner {
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, $primary, $primary-container);
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 12px 32px -4px rgba($primary, 0.15);
}

.welcome-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  position: relative;
  z-index: 10;
}

.welcome-text {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.welcome-greeting {
  font-family: $font-headline;
  font-size: 20px;
  font-weight: 700;
  color: $on-primary;
}

.welcome-subtitle {
  font-family: $font-body;
  font-size: 14px;
  font-weight: 400;
  color: rgba($on-primary, 0.8);
}

.avatar-placeholder {
  width: 64px;
  height: 64px;
  background: $surface-container-high;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.3);
}

.welcome-decoration {
  position: absolute;
  right: -16px;
  bottom: -16px;
  width: 128px;
  height: 128px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  filter: blur(30px);
}

// 快捷操作
.quick-actions {
  margin-top: 24px;
}

.quick-actions-scroll {
  white-space: nowrap;
}

.quick-actions-content {
  display: inline-flex;
  gap: 12px;
  padding-bottom: 8px;
}

.quick-action-btn {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  background: $surface-container-low;
  padding: 12px 16px;
  border-radius: 9999px;
  
  &:active {
    background: $surface-container;
    transform: scale(0.95);
  }
}

.quick-action-text {
  font-family: $font-body;
  font-size: 12px;
  font-weight: 700;
  color: $on-surface;
  white-space: nowrap;
}

// 统计网格
.stats-grid {
  margin-top: 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.stat-card {
  padding: 16px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-card-1 {
  background: rgba($secondary-container, 0.3);
}

.stat-card-2 {
  background: rgba($error-container, 0.1);
}

.stat-card-3 {
  background: #e2f5ec;
}

.stat-card-4 {
  background: #fef3c7;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.stat-number {
  font-family: $font-headline;
  font-size: 24px;
  font-weight: 900;
  color: $on-surface;
}

.stat-label {
  font-family: $font-body;
  font-size: 12px;
  font-weight: 500;
  color: $on-surface-variant;
}

// 待处理提问
.questions-section {
  margin-top: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  padding: 0 4px;
  margin-bottom: 16px;
}

.section-title {
  font-family: $font-headline;
  font-size: 20px;
  font-weight: 700;
  color: $on-surface;
}

.section-link {
  font-family: $font-body;
  font-size: 12px;
  font-weight: 700;
  color: $primary;
}

.question-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.question-card {
  background: $surface-container-low;
  border-radius: 16px;
  padding: 16px;
  
  &:active {
    background: $surface-container;
  }
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.question-author {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-family: $font-body;
  font-size: 14px;
  font-weight: 700;
  color: $on-surface;
}

.department-tag {
  background: $surface-container-highest;
  padding: 2px 8px;
  border-radius: 9999px;
}

.department-text {
  font-family: $font-body;
  font-size: 10px;
  color: $on-surface-variant;
}

.question-time {
  font-family: $font-body;
  font-size: 11px;
  color: $on-surface-variant;
}

.question-content {
  font-family: $font-body;
  font-size: 14px;
  color: rgba($on-surface, 0.8);
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
}

.question-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-pending {
  background: $error;
}

.status-processing {
  background: #f59e0b;
}

.status-text {
  font-family: $font-body;
  font-size: 11px;
  font-weight: 700;
}

.status-text-pending {
  color: $error;
}

.status-text-processing {
  color: #d97706;
}

// 动画
.animate-fade-up {
  opacity: 0;
  animation: fadeUp 0.6s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.delay-1 {
  animation-delay: 0.1s;
}

.delay-2 {
  animation-delay: 0.15s;
}

.delay-3 {
  animation-delay: 0.2s;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
