<template>
  <view class="detail-page">
    <!-- 页面头部（Hero Section） -->
    <view class="detail-hero">
      <view class="hero-badge">Progress Tracking</view>
      <text class="hero-title">{{ applicationTitle }}</text>
      <view class="status-row">
        <view class="pulse-indicator">
          <view class="pulse-ring"></view>
          <view class="pulse-dot"></view>
        </view>
        <text class="status-text">{{ currentStatus }}</text>
      </view>
    </view>

    <!-- 状态步骤指示器（Stepper） -->
    <view class="stepper-card">
      <view class="stepper">
        <view class="step" v-for="(step, index) in steps" :key="step.key" :class="step.status">
          <view class="step-icon">
            <component :is="step.icon" size="20" />
          </view>
          <text class="step-label">{{ step.label }}</text>
          <view v-if="index < steps.length - 1" class="step-line" :class="step.lineStatus"></view>
        </view>
      </view>
      
      <!-- 申请信息摘要 -->
      <view class="info-summary">
        <view class="info-item">
          <text class="info-label">申请编号</text>
          <text class="info-value">#{{ application.id }}</text>
        </view>
        <view class="info-item">
          <text class="info-label">提交时间</text>
          <text class="info-value">{{ formatDate(application.createdAt) }}</text>
        </view>
      </view>
    </view>

    <!-- 时间线历史（Timeline） -->
    <view class="timeline-card">
      <view class="card-header">
        <IconHistory size="20" color="#006565" />
        <text class="card-title">审批历史</text>
      </view>
      
      <view class="timeline">
        <view class="timeline-item" v-for="(item, index) in timeline" :key="index" :class="item.type">
          <view class="timeline-icon" :class="item.iconBg">
            <component :is="item.icon" size="16" />
          </view>
          <view class="timeline-content">
            <view class="timeline-header">
              <text class="timeline-title">{{ item.title }}</text>
              <text class="timeline-time">{{ item.time }}</text>
            </view>
            <text class="timeline-desc">{{ item.desc }}</text>
            <view v-if="item.comment" class="timeline-comment">
              <text>{{ item.comment }}</text>
            </view>
          </view>
        </view>
      </view>
    </view>

    <!-- 辅助信息 -->
    <view class="aux-info">
      <view class="aux-card">
        <IconClock size="24" color="#006565" />
        <view class="aux-content">
          <text class="aux-label">预计处理时间</text>
          <text class="aux-value">1-2 个工作日</text>
        </view>
      </view>
      <view class="aux-card" @click="goToHelp">
        <IconHelpCircle size="24" color="#006565" />
        <view class="aux-content">
          <text class="aux-label">需要帮助</text>
          <text class="aux-value">查看帮助中心</text>
        </view>
      </view>
    </view>

    <!-- 操作按钮区 -->
    <view class="action-bar">
      <button class="action-btn secondary" @click="contactReviewer">
        <IconMessageSquare size="18" />
        <text>联系审批人</text>
      </button>
      <button class="action-btn primary" @click="updateApplication">
        <IconEdit2 size="18" />
        <text>修改申请</text>
      </button>
    </view>

    <!-- 底部留白 -->
    <view class="bottom-safe"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
import { 
  getApplicationDetail, 
  getStatusText,
  ApplicationStatus,
  type ApplicationDetail 
} from '@/api/apply'
import IconCheck from '@/components/icons/IconCheck.vue'
import IconSearch from '@/components/icons/IconSearch.vue'
import IconClock from '@/components/icons/IconClock.vue'
import IconCheckCircle2 from '@/components/icons/IconCheckCircle2.vue'
import IconHistory from '@/components/icons/IconHistory.vue'
import IconFileSignature from '@/components/icons/IconFileSignature.vue'
import IconClipboardCheck from '@/components/icons/IconClipboardCheck.vue'
import IconSend from '@/components/icons/IconSend.vue'
import IconMessageSquare from '@/components/icons/IconMessageSquare.vue'
import IconEdit2 from '@/components/icons/IconEdit2.vue'
import IconHelpCircle from '@/components/icons/IconHelpCircle.vue'

// ===== 状态数据 =====
const applicationId = ref<number>(0)
const application = ref<Partial<ApplicationDetail>>({})
const isLoading = ref(false)

// 步骤配置
interface Step {
  key: string
  label: string
  icon: typeof IconCheck
  status: string
  lineStatus: string
}

const baseSteps: Omit<Step, 'status' | 'lineStatus'>[] = [
  { key: 'submitted', label: '已提交', icon: IconCheck },
  { key: 'reviewing', label: '审核中', icon: IconSearch },
  { key: 'pending', label: '待补充', icon: IconClock },
  { key: 'approved', label: '已通过', icon: IconCheckCircle2 }
]

// 计算步骤状态
const steps = computed<Step[]>(() => {
  const status = application.value.status ?? ApplicationStatus.PENDING
  const currentSteps: Step[] = []
  
  // 根据实际状态确定当前步骤索引
  let currentIndex = 1 // 默认审核中
  if (status === ApplicationStatus.PENDING) {
    currentIndex = 1
  } else if (status === ApplicationStatus.APPROVED) {
    currentIndex = 3
  } else if (status === ApplicationStatus.REJECTED) {
    currentIndex = 2
  } else if (status === ApplicationStatus.CANCELLED || status === ApplicationStatus.EXPIRED) {
    currentIndex = 1
  }
  
  baseSteps.forEach((step, index) => {
    let stepStatus = 'pending'
    let lineStatus = ''
    
    if (index < currentIndex) {
      stepStatus = 'completed'
      lineStatus = 'active'
    } else if (index === currentIndex) {
      stepStatus = 'active'
      if (index < baseSteps.length - 1) {
        lineStatus = ''
      }
    }
    
    currentSteps.push({
      ...step,
      status: stepStatus,
      lineStatus
    })
  })
  
  return currentSteps
})

// 申请标题
const applicationTitle = computed(() => {
  const building = application.value.building || '未知教学楼'
  const room = application.value.roomNumber || ''
  return `${building} ${room}`.trim()
})

// 当前状态文本
const currentStatus = computed(() => {
  if (application.value.status !== undefined) {
    return getStatusText(application.value.status)
  }
  return '加载中...'
})

// 时间线数据
const timeline = computed(() => {
  const items: {
    type: string
    icon: typeof IconSend
    iconBg: string
    title: string
    time: string
    desc: string
    comment?: string
  }[] = []
  
  // 当前状态项
  const status = application.value.status ?? ApplicationStatus.PENDING
  if (status === ApplicationStatus.PENDING) {
    items.push({
      type: 'current',
      icon: IconFileSignature,
      iconBg: 'bg-primary-light',
      title: '审核中',
      time: '进行中',
      desc: '审批老师正在评估申请',
      comment: '"请确保使用人数不超过教室容量。"'
    })
  } else if (status === ApplicationStatus.APPROVED) {
    items.push({
      type: 'current',
      icon: IconCheckCircle2,
      iconBg: 'bg-success',
      title: '已通过',
      time: '刚刚',
      desc: '申请已通过审批'
    })
  } else if (status === ApplicationStatus.REJECTED) {
    items.push({
      type: 'current',
      icon: IconClock,
      iconBg: 'bg-error',
      title: '已拒绝',
      time: '刚刚',
      desc: '申请未通过审批'
    })
  }
  
  // 审批记录
  if (application.value.reviews && application.value.reviews.length > 0) {
    application.value.reviews.forEach(review => {
      items.push({
        type: 'past',
        icon: IconClipboardCheck,
        iconBg: 'bg-gray',
        title: review.action === 1 ? '审批通过' : '审批拒绝',
        time: formatDateTime(review.createdAt),
        desc: `${review.reviewerName || '审批老师'} ${review.action === 1 ? '通过了' : '拒绝了'}申请`,
        comment: review.opinion
      })
    })
  }
  
  // 提交记录
  if (application.value.createdAt) {
    items.push({
      type: 'past',
      icon: IconSend,
      iconBg: 'bg-gray',
      title: '申请已提交',
      time: formatDateTime(application.value.createdAt),
      desc: '您提交了空教室申请'
    })
  }
  
  return items
})

// ===== 方法 =====

// 格式化日期
function formatDate(dateStr?: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 格式化日期时间
function formatDateTime(dateStr?: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  return `${month}-${day} ${hour}:${minute}`
}

// 加载申请详情
async function loadApplicationDetail() {
  if (!applicationId.value) return
  
  isLoading.value = true
  try {
    const detail = await getApplicationDetail(applicationId.value)
    application.value = detail
  } catch (error) {
    console.error('加载申请详情失败', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    isLoading.value = false
  }
}

// 联系审批人
function contactReviewer() {
  uni.showModal({
    title: '联系审批人',
    content: '是否拨打教务处电话？',
    confirmColor: '#006a64',
    success: (res) => {
      if (res.confirm) {
        uni.makePhoneCall({
          phoneNumber: '010-12345678'
        })
      }
    }
  })
}

// 修改申请
function updateApplication() {
  const status = application.value.status
  if (status !== ApplicationStatus.PENDING) {
    uni.showToast({
      title: '当前状态不可修改',
      icon: 'none'
    })
    return
  }
  
  uni.navigateTo({
    url: `/pages/apply/classroom?editId=${applicationId.value}`
  })
}

// 返回
function goBack() {
  uni.navigateBack()
}

// 前往帮助中心
function goToHelp() {
  uni.showToast({
    title: '帮助中心开发中',
    icon: 'none'
  })
}

// ===== 生命周期 =====
onLoad((options) => {
  if (options?.id) {
    applicationId.value = Number(options.id)
    loadApplicationDetail()
  }
})
</script>

<style scoped lang="scss">
page {
  background-color: #f0f7f5;
}

// 颜色变量（遵循 MD3 设计规范）
$primary: #006a64;
$primary-container: #8bf2e8;
$on-primary: #ffffff;
$on-primary-container: #00201e;
$surface: #f0f7f5;
$surface-variant: #dbe4e1;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$surface-container-high: #d8e3e1;
$on-surface: #171d1c;
$on-surface-variant: #3f4947;
$outline: #6f7977;
$outline-variant: #bec9c6;

// 状态颜色
$success-color: #006565;
$error-color: #d32f2f;
$pending-color: #f57c00;

.detail-page {
  min-height: 100vh;
  background: $surface;
  padding-bottom: 40rpx;
}

// 页面头部（Hero Section）
.detail-hero {
  padding: 48rpx 32rpx 40rpx;
  background: linear-gradient(135deg, $primary, #00a79d);
}

.hero-badge {
  display: inline-block;
  font-size: 24rpx;
  font-weight: 500;
  color: rgba($on-primary, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 16rpx;
  padding: 8rpx 16rpx;
  background: rgba($on-primary, 0.15);
  border-radius: 8rpx;
}

.hero-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $on-primary;
  margin-bottom: 24rpx;
}

.status-row {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

// 脉冲指示器
.pulse-indicator {
  position: relative;
  width: 24rpx;
  height: 24rpx;
}

.pulse-ring {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 24rpx;
  height: 24rpx;
  border-radius: 50%;
  background: rgba($on-primary, 0.4);
  animation: pulse 2s ease-out infinite;
}

.pulse-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 12rpx;
  height: 12rpx;
  border-radius: 50%;
  background: $on-primary;
}

@keyframes pulse {
  0% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
  100% {
    transform: translate(-50%, -50%) scale(2.5);
    opacity: 0;
  }
}

.status-text {
  font-size: 32rpx;
  font-weight: 600;
  color: $on-primary;
}

// 状态步骤指示器卡片
.stepper-card {
  margin: -20rpx 32rpx 24rpx;
  padding: 32rpx;
  background: $surface-container-lowest;
  border-radius: 24rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 1;
}

.stepper {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32rpx;
  position: relative;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  position: relative;
}

.step-icon {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12rpx;
  transition: all 0.3s ease;
}

// 已完成状态
.step.completed .step-icon {
  background: $primary;
  color: $on-primary;
}

// 当前状态
.step.active .step-icon {
  background: $primary-container;
  color: $on-primary-container;
  box-shadow: 0 0 0 4rpx rgba($primary, 0.2);
}

// 待办状态
.step.pending .step-icon {
  background: $surface-variant;
  color: $on-surface-variant;
}

.step-label {
  font-size: 24rpx;
  font-weight: 500;
  color: $on-surface-variant;
  transition: all 0.3s ease;
}

.step.completed .step-label {
  color: $primary;
  font-weight: 600;
}

.step.active .step-label {
  color: $primary;
  font-weight: 700;
}

// 步骤连线
.step-line {
  position: absolute;
  top: 24rpx;
  left: 60%;
  right: -40%;
  height: 2rpx;
  background: $surface-variant;
}

.step-line.active {
  background: $primary;
}

// 申请信息摘要
.info-summary {
  display: flex;
  justify-content: space-between;
  padding-top: 24rpx;
  border-top: 1rpx solid $surface-container-high;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 8rpx;
}

.info-label {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.info-value {
  font-size: 28rpx;
  font-weight: 600;
  color: $on-surface;
}

// 时间线卡片
.timeline-card {
  margin: 0 32rpx 24rpx;
  padding: 32rpx;
  background: $surface-container-lowest;
  border-radius: 24rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 32rpx;
}

.card-title {
  font-size: 32rpx;
  font-weight: 700;
  color: $on-surface;
}

// 时间线
.timeline {
  position: relative;
  padding-left: 20rpx;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 28rpx;
  top: 0;
  bottom: 0;
  width: 2rpx;
  background: $surface-container-high;
}

.timeline-item {
  position: relative;
  padding-left: 56rpx;
  padding-bottom: 32rpx;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-icon {
  position: absolute;
  left: 0;
  top: 0;
  width: 56rpx;
  height: 56rpx;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-primary-light {
  background: $primary-container;
  color: $on-primary-container;
}

.bg-gray {
  background: $surface-variant;
  color: $on-surface-variant;
}

.bg-success {
  background: rgba($success-color, 0.15);
  color: $success-color;
}

.bg-error {
  background: rgba($error-color, 0.15);
  color: $error-color;
}

.timeline-content {
  padding-top: 8rpx;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8rpx;
}

.timeline-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $on-surface;
}

.timeline-time {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.timeline-desc {
  font-size: 28rpx;
  color: $on-surface-variant;
  line-height: 1.5;
  margin-bottom: 12rpx;
}

.timeline-comment {
  padding: 16rpx 20rpx;
  background: $surface-container-low;
  border-radius: 12rpx;
  border-left: 4rpx solid $primary;
}

.timeline-comment text {
  font-size: 26rpx;
  color: $on-surface;
  font-style: italic;
}

// 当前类型高亮
.timeline-item.current .timeline-title {
  color: $primary;
}

// 辅助信息
.aux-info {
  margin: 0 32rpx 24rpx;
  display: flex;
  gap: 20rpx;
}

.aux-card {
  flex: 1;
  padding: 24rpx;
  background: $surface-container-lowest;
  border-radius: 20rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
}

.aux-content {
  display: flex;
  flex-direction: column;
  gap: 4rpx;
}

.aux-label {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.aux-value {
  font-size: 26rpx;
  font-weight: 600;
  color: $on-surface;
}

// 操作按钮区
.action-bar {
  margin: 0 32rpx;
  display: flex;
  gap: 24rpx;
  padding-top: 16rpx;
}

.action-btn {
  flex: 1;
  height: 88rpx;
  border-radius: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12rpx;
  font-size: 30rpx;
  font-weight: 600;
  border: none;
  transition: all 0.2s ease;
}

.action-btn.secondary {
  background: $surface-container-low;
  color: $on-surface;
}

.action-btn.secondary:active {
  background: $surface-container-high;
}

.action-btn.primary {
  background: $primary;
  color: $on-primary;
  box-shadow: 0 4rpx 16rpx rgba($primary, 0.3);
}

.action-btn.primary:active {
  opacity: 0.9;
  transform: translateY(2rpx);
}

// 底部留白
.bottom-safe {
  height: 40rpx;
}
</style>
