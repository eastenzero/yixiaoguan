<template>
  <view class="home-page">
    <!-- 背景渐变洗刷 -->
    <view class="bg-wash"></view>

    <!-- 顶部欢迎区 - 紧凑型 + 状态小卡片 -->
    <view class="welcome-section staggered-1">
      <view class="welcome-text">
        <text class="greeting">{{ timeGreeting }}</text>
        <text class="user-name">{{ userName }}</text>
      </view>
      <!-- 状态小卡片 -->
      <view class="status-pill" @click="goToApplyStatus">
        <view class="pulse-dot"></view>
        <text class="status-text">当前活跃申请: {{ latestApplication ? 1 : 0 }}</text>
      </view>
    </view>

    <!-- AI 输入区 - 药丸形 + 大阴影 -->
    <view class="ai-input-bar staggered-2" @click="goToChatWithQuery('')">
      <view class="ai-badge">AI</view>
      <text class="input-placeholder">问问你的AI学术助教...</text>
      <view class="send-btn-round">
        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
          <path d="M5 12h14"/>
          <path d="m12 5 7 7-7 7"/>
        </svg>
      </view>
    </view>

    <!-- 快捷标签 - pill 样式 -->
    <scroll-view class="tags-scroll staggered-3" scroll-x :show-scrollbar="false">
      <view class="tags-container">
        <view class="tag-pill" v-for="tag in quickTags" :key="tag" @click="goToChatWithQuery(tag)">
          <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
            <path d="M2 12h20"/>
            <path d="M20 12v6a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-6"/>
            <path d="m12 2 10 10"/>
            <path d="M2 12 12 2"/>
          </svg>
          <text>{{ tag }}</text>
        </view>
      </view>
    </scroll-view>

    <!-- Bento Grid 服务矩阵 -->
    <view class="bento-grid staggered-4">
      <!-- 跨列大卡片 - 任务指引 -->
      <BentoCard 
        size="large"
        bgClass="bg-gradient-primary"
        :icon="ClipboardCheckIcon"
        title="任务指引"
        desc="查看本周待完成的学术与行政任务"
        hasArrow
        @click="goToServices"
      />
      
      <!-- 下方两个小卡片 -->
      <view class="bento-row">
        <BentoCard
          size="normal"
          bgClass="bg-surface"
          :icon="ArmchairIcon"
          title="空教室预约"
          desc="实时查看并预约学习空间"
          @click="goToClassroomApply"
        />
        <BentoCard
          size="normal"
          bgClass="bg-surface"
          :icon="ActivityIcon"
          title="申请进度"
          desc="追踪您的所有审批状态"
          @click="goToApplyStatus"
        />
      </view>
    </view>

    <!-- 官方校园链接区 -->
    <view class="links-section staggered-5">
      <text class="section-title">官方校园链接</text>
      <view class="links-list">
        <LinkCard 
          :icon="GlobeIcon"
          title="教务管理系统"
          subtitle="Course Management System"
          @click="showDeveloping"
        />
        <LinkCard 
          :icon="LibraryIcon"
          title="图书馆资源库"
          subtitle="Digital Library Resources"
          @click="showDeveloping"
        />
        <LinkCard 
          :icon="MailIcon"
          title="学生邮箱"
          subtitle="Campus Mail Services"
          @click="showDeveloping"
        />
      </view>
    </view>

    <!-- 底部通知 Banner -->
    <view class="notice-banner staggered-6">
      <svg class="notice-icon" viewBox="0 0 24 24" width="20" height="20" stroke="#8b4823" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 16v-4"/>
        <path d="M12 8h.01"/>
      </svg>
      <view class="notice-content">
        <text class="notice-title">新学期注册提醒</text>
        <text class="notice-desc">2023秋季学期注册将于下周五截止，请尚未完成学费缴纳及学籍确认的同学尽快办理。</text>
      </view>
    </view>

    <!-- TabBar 占位 -->
    <view class="tabbar-spacer"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useUserStore } from '@/stores/user'
import { getNotificationList } from '@/api/notification'
import type { Notification } from '@/types/api'

// 导入 UI 组件
import BentoCard from '@/components/BentoCard.vue'
import LinkCard from '@/components/LinkCard.vue'

// SVG 图标组件定义
const ClipboardCheckIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '32', 
  height: '32',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('rect', { x: '8', y: '2', width: '8', height: '4', rx: '1', ry: '1' }),
  h('path', { d: 'M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2' }),
  h('path', { d: 'm9 14 2 2 4-4' })
])

const ArmchairIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '24', 
  height: '24',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M19 9V6a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v3' }),
  h('path', { d: 'M3 16a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5a2 2 0 0 0-4 0v1.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V11a2 2 0 0 0-4 0z' }),
  h('path', { d: 'M5 18v2' }),
  h('path', { d: 'M19 18v2' })
])

const ActivityIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '24', 
  height: '24',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'M22 12h-4l-3 9L9 3l-3 9H2' })
])

const GlobeIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '24', 
  height: '24',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('circle', { cx: '12', cy: '12', r: '10' }),
  h('path', { d: 'M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20' }),
  h('path', { d: 'M2 12h20' })
])

const LibraryIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '24', 
  height: '24',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('path', { d: 'm16 6 4 14' }),
  h('path', { d: 'M12 6v14' }),
  h('path', { d: 'M8 8v12' }),
  h('path', { d: 'M4 4v16' })
])

const MailIcon = () => h('svg', { 
  viewBox: '0 0 24 24', 
  width: '24', 
  height: '24',
  stroke: 'currentColor',
  strokeWidth: '2',
  fill: 'none',
  strokeLinecap: 'round',
  strokeLinejoin: 'round'
}, [
  h('rect', { width: '20', height: '16', x: '2', y: '4', rx: '2' }),
  h('path', { d: 'm22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7' })
])

const userStore = useUserStore()

// 时间问候语
const timeGreeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 12) return '早上好'
  if (hour < 18) return '下午好'
  return '晚上好'
})

// 用户名显示
const userName = computed(() => {
  return userStore.userInfo?.realName || userStore.userInfo?.username || '同学'
})

const userDeptAndGrade = computed(() => {
  const info = userStore.userInfo as any
  if (info && info.deptName && info.grade) {
    return `${info.deptName} · ${info.grade}级`
  } else if (info && info.deptName) {
    return info.deptName
  }
  return ''
})

const userAvatar = computed(() => (userStore.userInfo as any)?.avatar || '')

// 通知列表
const notifications = ref<Notification[]>([])

// 最新申请状态
const latestApplication = ref<any>(null)

// 快捷标签数据
const quickTags = ['奖学金申请截止日期', '如何预约研讨室？', '选课指南']

// 跳转到 AI 咨询带参数
const goToChatWithQuery = (query: string) => {
  if (query) {
    uni.setStorageSync('chat_init_query', query)
  }
  uni.switchTab({ url: '/pages/chat/index' })
}

// 跳转到空教室申请
const goToClassroomApply = () => {
  uni.navigateTo({ url: '/pages/apply/classroom' })
}

// 跳转到申请进度
const goToApplyStatus = () => {
  uni.switchTab({ url: '/pages/apply/status' })
}

// 跳转到个人中心
const goToProfile = () => {
  uni.switchTab({ url: '/pages/profile/index' })
}

// 跳转到服务页面
const goToServices = () => {
  uni.switchTab({ url: '/pages/apply/status' })
}

// 功能开发中提示
const showDeveloping = () => {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

// 查看更多通知
const viewMoreNotifications = () => {
  uni.showToast({
    title: '功能开发中',
    icon: 'none'
  })
}

// 查看通知详情
const viewNotification = (item: Notification) => {
  uni.showModal({
    title: item.title,
    content: item.content || '暂无详情',
    showCancel: false
  })
}

// 格式化时间
const formatTime = (timeStr: string): string => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  if (diff < 24 * 60 * 60 * 1000) {
    if (diff < 60 * 60 * 1000) {
      return '刚刚'
    }
    return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  }
  return `${date.getMonth() + 1}月${date.getDate()}日`
}

const getStatusText = (status: number) => {
  const map: Record<number, string> = {
    0: '审核中',
    1: '已通过',
    2: '已拒绝'
  }
  return map[status] || '处理中'
}

// 加载通知
const loadNotifications = async () => {
  try {
    const res = await getNotificationList(1, 3)
    notifications.value = res.rows || []
  } catch (error) {
    console.error('加载通知失败', error)
    notifications.value = []
  }
}

// 加载最新申请
const loadLatestApplication = async () => {
  try {
    const res: any = await uni.request({
      url: '/api/v1/classroom-applications?pageSize=1&pageNum=1',
      method: 'GET',
      header: {
        'Authorization': `Bearer ${userStore.token}`
      }
    })
    if (res.data?.data?.rows && res.data.data.rows.length > 0) {
      latestApplication.value = res.data.data.rows[0]
    }
  } catch (error) {
    console.error('加载最新申请失败', error)
  }
}

// 页面显示时加载数据
onMounted(() => {
  loadNotifications()
  loadLatestApplication()
})
</script>

<style scoped lang="scss">
// MD3 颜色变量
$primary: #006a64;
$primary-container: #00A79D;
$on-primary: #ffffff;
$on-primary-container: #00201e;
$surface: #f5fbf9;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$surface-variant: #dce5e2;
$on-surface: #171d1c;
$on-surface-variant: #5a635f;
$outline: #6f7977;
$outline-variant: #bec9c6;
$tertiary: #8b4823;

// 动画定义
@keyframes fadeUpEditorial {
  from { opacity: 0; transform: translateY(40rpx); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.1); }
}

// 阶梯入场动画
.staggered-1 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.05s; }
.staggered-2 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.1s; }
.staggered-3 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.15s; }
.staggered-4 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.2s; }
.staggered-5 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.25s; }
.staggered-6 { animation: fadeUpEditorial 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.3s; }

page {
  background-color: $surface;
}

.home-page {
  min-height: 100vh;
  background-color: $surface;
  position: relative;
  overflow-x: hidden;
  padding: 40rpx 32rpx;
}

.bg-wash {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 500rpx;
  background: linear-gradient(135deg, rgba($primary, 0.1) 0%, rgba($surface, 0) 70%);
  pointer-events: none;
  z-index: 0;
}

// 欢迎区 - 紧凑型
.welcome-section {
  position: relative;
  z-index: 1;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32rpx;

  .welcome-text {
    display: flex;
    flex-direction: column;
    gap: 4rpx;

    .greeting {
      font-size: 28rpx;
      color: $on-surface-variant;
      font-weight: 500;
    }

    .user-name {
      font-size: 48rpx;
      font-weight: 700;
      color: $on-surface;
    }
  }
}

// 状态小卡片
.status-pill {
  display: flex;
  align-items: center;
  gap: 12rpx;
  background: $surface-container-lowest;
  padding: 16rpx 24rpx;
  border-radius: 40rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.04);
  transition: transform 0.2s ease;

  &:active {
    transform: scale(0.96);
  }

  .pulse-dot {
    width: 16rpx;
    height: 16rpx;
    background: $primary;
    border-radius: 50%;
    animation: pulse 2s ease-in-out infinite;
  }

  .status-text {
    font-size: 24rpx;
    color: $on-surface;
    font-weight: 500;
  }
}

// AI 输入区 - 药丸形
.ai-input-bar {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 20rpx;
  background: $surface-container-lowest;
  padding: 16rpx 20rpx 16rpx 24rpx;
  border-radius: 60rpx;
  box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.08), 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
  margin-bottom: 24rpx;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:active {
    transform: scale(0.98);
    box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.06);
  }

  .ai-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48rpx;
    height: 48rpx;
    background: linear-gradient(135deg, $primary 0%, $primary-container 100%);
    color: $on-primary;
    font-size: 22rpx;
    font-weight: 700;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .input-placeholder {
    flex: 1;
    font-size: 28rpx;
    color: $on-surface-variant;
  }

  .send-btn-round {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 64rpx;
    height: 64rpx;
    background: $primary;
    border-radius: 50%;
    color: #fff;
    flex-shrink: 0;
  }
}

// 快捷标签滚动区
.tags-scroll {
  position: relative;
  z-index: 1;
  margin-bottom: 40rpx;
  white-space: nowrap;

  .tags-container {
    display: inline-flex;
    gap: 16rpx;
    padding: 4rpx 0;
  }
}

// Pill 标签样式
.tag-pill {
  display: inline-flex;
  align-items: center;
  gap: 12rpx;
  background: $surface-container-low;
  padding: 16rpx 28rpx;
  border-radius: 40rpx;
  transition: background 0.2s ease, transform 0.2s ease;

  &:active {
    background: rgba($primary, 0.1);
    transform: scale(0.96);
  }

  text {
    font-size: 26rpx;
    color: $on-surface;
    font-weight: 500;
  }
}

// Bento Grid
.bento-grid {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 40rpx;

  .bento-row {
    display: flex;
    gap: 24rpx;

    > * {
      flex: 1;
    }
  }
}

// 官方校园链接区
.links-section {
  position: relative;
  z-index: 1;
  margin-bottom: 40rpx;

  .section-title {
    display: block;
    font-size: 32rpx;
    font-weight: 700;
    color: $on-surface;
    margin-bottom: 20rpx;
  }

  .links-list {
    display: flex;
    flex-direction: column;
    gap: 16rpx;
  }
}

// 底部通知 Banner
.notice-banner {
  position: relative;
  z-index: 1;
  display: flex;
  gap: 20rpx;
  background: #fff8f0;
  padding: 28rpx;
  border-radius: 24rpx;
  border: 2rpx solid rgba($tertiary, 0.15);

  .notice-icon {
    flex-shrink: 0;
    margin-top: 4rpx;
  }

  .notice-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8rpx;

    .notice-title {
      font-size: 30rpx;
      font-weight: 600;
      color: $tertiary;
    }

    .notice-desc {
      font-size: 26rpx;
      color: $on-surface-variant;
      line-height: 1.5;
    }
  }
}

// TabBar 占位
.tabbar-spacer {
  height: 120rpx;
}
</style>
