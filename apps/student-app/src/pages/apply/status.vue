<template>
  <view class="apply-status-page">
    <!-- 页面标题区 -->
    <view class="page-hero">
      <text class="hero-label">Progress Tracking</text>
      <text class="hero-title">我的申请</text>
      <text class="hero-subtitle">查看空教室申请进度与历史记录</text>
    </view>

    <!-- 新建申请按钮 -->
    <view class="action-section">
      <view class="apply-btn" @click="goToApply">
        <IconPlus size="24" />
        <text class="btn-text">新建申请</text>
      </view>
    </view>

    <!-- 申请列表 -->
    <view class="list-section">
      <!-- 加载中 -->
      <view v-if="isLoading" class="loading-state">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- 空列表 -->
      <view v-else-if="applications.length === 0" class="empty-state">
        <text class="empty-icon">📋</text>
        <text class="empty-title">暂无申请记录</text>
        <text class="empty-desc">您还没有提交过空教室申请，点击下方按钮开始申请</text>
      </view>

      <!-- 列表内容 -->
      <view v-else class="application-list">
        <view 
          v-for="item in applications" 
          :key="item.id"
          class="application-card"
          @click="toggleExpand(item.id)"
        >
          <!-- 状态步骤指示器 -->
          <view class="stepper-bar">
            <view 
              v-for="(step, idx) in getStatusSteps(item.status)" 
              :key="idx"
              class="step-item"
              :class="{ 'step-active': step.active, 'step-completed': step.completed }"
            >
              <view class="step-dot"></view>
              <text class="step-label">{{ step.label }}</text>
            </view>
          </view>

          <!-- 卡片头部 -->
          <view class="card-header">
            <view class="room-info">
              <text class="room-name">{{ item.building || '未知教学楼' }} {{ item.roomNumber || '' }}</text>
              <StatusBadge :status="item.status" />
            </view>
            <text class="time-range">{{ formatTimeRange(item) }}</text>
          </view>

          <!-- 卡片内容 -->
          <view class="card-body">
            <view class="info-row">
              <text class="info-label">用途：</text>
              <text class="info-value purpose">{{ item.purpose }}</text>
            </view>
            <view v-if="item.attendeeCount" class="info-row">
              <text class="info-label">人数：</text>
              <text class="info-value">{{ item.attendeeCount }} 人</text>
            </view>
            <view v-if="item.contactPhone" class="info-row">
              <text class="info-label">联系：</text>
              <text class="info-value">{{ item.contactPhone }}</text>
            </view>
          </view>

          <!-- 展开内容：审批意见 -->
          <view v-if="expandedId === item.id && item.reviews && item.reviews.length > 0" class="card-expand">
            <view class="divider"></view>
            <view class="review-section">
              <text class="review-title">审批意见</text>
              <view v-for="(review, idx) in item.reviews" :key="idx" class="review-item">
                <view class="review-header">
                  <text class="reviewer">{{ review.reviewerName || '审批老师' }}</text>
                  <text class="review-action" :class="review.action === 1 ? 'action-approve' : 'action-reject'">
                    {{ review.action === 1 ? '通过' : '拒绝' }}
                  </text>
                </view>
                <text v-if="review.opinion" class="review-opinion">{{ review.opinion }}</text>
                <text class="review-time">{{ formatDateTime(review.createdAt) }}</text>
              </view>
            </view>
          </view>

          <!-- 卡片底部：操作按钮 -->
          <view class="card-footer">
            <view class="submit-time">申请时间：{{ formatDateTime(item.createdAt) }}</view>
            <view v-if="canCancel(item.status)" class="action-btns">
              <button class="cancel-btn" size="mini" @click.stop="handleCancel(item.id)">取消申请</button>
            </view>
          </view>
        </view>

        <!-- 加载更多 -->
        <view v-if="hasMore" class="load-more">
          <text class="load-text" @click="loadMore">加载更多</text>
        </view>
        <view v-else-if="applications.length > 0" class="no-more">
          <text class="no-more-text">没有更多了</text>
        </view>
      </view>
    </view>

    <!-- 底部留白 -->
    <view class="bottom-safe"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { 
  getMyApplications, 
  cancelApplication, 
  getApplicationDetail,
  getStatusText as getStatusTextUtil,
  getStatusColor as getStatusColorUtil,
  type Application,
  type ApplicationDetail,
  ApplicationStatus
} from '@/api/apply'
import { useUserStore } from '@/stores/user'
import StatusBadge from '@/components/StatusBadge.vue'
import IconPlus from '@/components/icons/IconPlus.vue'

const userStore = useUserStore()

// ===== 状态数据 =====
const applications = ref<ApplicationDetail[]>([])
const isLoading = ref(false)
const expandedId = ref<number | null>(null)
const pageNum = ref(1)
const pageSize = 10
const hasMore = ref(true)
const isLoadingMore = ref(false)

// 状态步骤配置
interface StatusStep {
  label: string
  active: boolean
  completed: boolean
}

function getStatusSteps(status: number): StatusStep[] {
  const steps = [
    { label: '已提交', active: true, completed: true },
    { label: '审核中', active: false, completed: false },
    { label: '已完成', active: false, completed: false }
  ]
  
  switch (status) {
    case ApplicationStatus.PENDING:
      steps[1].active = true
      break
    case ApplicationStatus.APPROVED:
      steps[1].active = true
      steps[1].completed = true
      steps[2].active = true
      steps[2].completed = true
      break
    case ApplicationStatus.REJECTED:
      steps[1].active = true
      steps[1].completed = true
      steps[2].label = '已拒绝'
      steps[2].active = true
      break
    case ApplicationStatus.CANCELLED:
      steps[1].label = '已取消'
      steps[1].active = true
      steps[1].completed = true
      break
    case ApplicationStatus.EXPIRED:
      steps[1].label = '已过期'
      steps[1].active = true
      steps[1].completed = true
      break
  }
  
  return steps
}

// ===== 方法 =====

// 获取状态文本
function getStatusText(status: number): string {
  return getStatusTextUtil(status as ApplicationStatus)
}

// 获取状态颜色（文字）
function getStatusColor(status: number): string {
  return getStatusColorUtil(status as ApplicationStatus)
}

// 格式化日期时间
function formatDateTime(dateStr: string): string {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  const hour = String(date.getHours()).padStart(2, '0')
  const minute = String(date.getMinutes()).padStart(2, '0')
  return `${month}-${day} ${hour}:${minute}`
}

// 格式化时间段
function formatTimeRange(item: Application): string {
  if (!item.applyDate) return ''
  const date = item.applyDate.slice(5) // 取 MM-DD
  return `${date} ${item.startTime || ''}~${item.endTime || ''}`
}

// 是否可取消
function canCancel(status: number): boolean {
  // 只有待审批状态的申请可以取消
  return status === ApplicationStatus.PENDING
}

// 展开/收起详情，点击跳转到详情页
async function toggleExpand(id: number) {
  // 直接跳转到详情页
  uni.navigateTo({ url: `/pages/apply/detail?id=${id}` })
}

// 加载申请列表
async function loadApplications(isRefresh = false) {
  if (isLoading.value) return
  
  if (isRefresh) {
    pageNum.value = 1
    hasMore.value = true
  }
  
  isLoading.value = true
  try {
    const res = await getMyApplications(userStore.userInfo.id, {
      pageNum: pageNum.value,
      pageSize
    })
    
    const list = res.rows || []
    // 将 Application 转为 ApplicationDetail（添加 reviews 字段）
    const detailList: ApplicationDetail[] = list.map(item => ({
      ...item,
      reviews: undefined
    }))
    
    if (isRefresh) {
      applications.value = detailList
    } else {
      applications.value.push(...detailList)
    }
    
    // 判断是否还有更多
    const total = res.total || 0
    hasMore.value = applications.value.length < total
  } catch (error) {
    console.error('加载申请列表失败', error)
    if (isRefresh) {
      applications.value = []
    }
  } finally {
    isLoading.value = false
  }
}

// 加载更多
async function loadMore() {
  if (isLoadingMore.value || !hasMore.value) return
  isLoadingMore.value = true
  pageNum.value++
  await loadApplications(false)
  isLoadingMore.value = false
}

// 取消申请
function handleCancel(id: number) {
  uni.showModal({
    title: '确认取消',
    content: '确定要取消该申请吗？取消后不可恢复。',
    confirmColor: '#006a64',
    success: async (res) => {
      if (res.confirm) {
        try {
          uni.showLoading({ title: '处理中...' })
          await cancelApplication(id)
          uni.hideLoading()
          uni.showToast({
            title: '已取消申请',
            icon: 'success'
          })
          // 刷新列表
          setTimeout(() => {
            loadApplications(true)
          }, 500)
        } catch (error) {
          uni.hideLoading()
          console.error('取消申请失败', error)
        }
      }
    }
  })
}

// 跳转到申请页面
function goToApply() {
  uni.navigateTo({
    url: '/pages/apply/classroom'
  })
}

// ===== 生命周期 =====
onMounted(async () => {
  // 确保用户信息已初始化
  userStore.init()
  
  // 检查用户登录状态
  if (!userStore.userInfo?.id) {
    uni.showToast({
      title: '请先登录',
      icon: 'none'
    })
    setTimeout(() => {
      uni.reLaunch({ url: '/pages/login/index' })
    }, 1500)
    return
  }
  
  await loadApplications(true)
})

// 页面显示时刷新
onShow(() => {
  // 可选：每次显示都刷新
  // loadApplications(true)
})
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

page {
  background-color: #f0f7f5;
}

// 颜色变量（遵循设计规范）
$primary-container: #8bf2e8;
$on-primary: #ffffff;
$surface: #f0f7f5;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$surface-container-high: #d8e3e1;
$on-surface: #171d1c;
$on-surface-variant: #3f4947;
$outline-variant: #bec9c6;

// MD3 状态颜色
$pending-color: #f57c00;
$pending-bg: #fff3e0;
$approved-color: #006565;
$approved-bg: rgba(0, 101, 101, 0.1);
$rejected-color: #d32f2f;
$rejected-bg: #ffebee;
$cancelled-color: #757575;
$cancelled-bg: rgba(117, 117, 117, 0.1);

.apply-status-page {
  min-height: 100vh;
  background: $surface;
}

// 页面标题区
.page-hero {
  padding: 48rpx 32rpx 32rpx;
  background: linear-gradient(135deg, $primary, #00a79d);
}

.hero-label {
  display: block;
  font-size: 24rpx;
  font-weight: 500;
  color: rgba($on-primary, 0.7);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 8rpx;
}

.hero-title {
  display: block;
  font-size: 44rpx;
  font-weight: 700;
  color: $on-primary;
  margin-bottom: 12rpx;
}

.hero-subtitle {
  display: block;
  font-size: 28rpx;
  color: rgba($on-primary, 0.85);
}

// 操作区域
.action-section {
  padding: 24rpx 32rpx;
  background: $surface;
}

.apply-btn {
  background: $primary;
  border-radius: 48rpx;
  padding: 28rpx 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 106, 100, 0.25);
  border: none;
  color: $on-primary;
  
  &:active {
    opacity: 0.9;
    transform: translateY(2rpx);
  }
}

.btn-text {
  font-size: 32rpx;
  font-weight: 600;
  color: $on-primary;
}

// 列表区域
.list-section {
  padding: 0 32rpx 32rpx;
}

// 加载状态
.loading-state {
  padding: 120rpx 0;
  text-align: center;
}

.loading-text {
  font-size: 28rpx;
  color: $on-surface-variant;
}

// 空状态
.empty-state {
  padding: 160rpx 60rpx;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon {
  font-size: 120rpx;
  margin-bottom: 32rpx;
}

.empty-title {
  font-size: 34rpx;
  font-weight: 600;
  color: $on-surface;
  margin-bottom: 16rpx;
}

.empty-desc {
  font-size: 28rpx;
  color: $on-surface-variant;
  line-height: 1.5;
}

// 申请列表
.application-list {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
}

.application-card {
  background: $surface-container-lowest;
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 2rpx 12rpx rgba(0, 0, 0, 0.06);
  border: none;
}

// 状态步骤指示器
.stepper-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24rpx;
  padding: 0 16rpx;
  position: relative;
  
  &::before {
    content: '';
    position: absolute;
    top: 16rpx;
    left: 16%;
    right: 16%;
    height: 2rpx;
    background: $outline-variant;
    z-index: 0;
  }
}

.step-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8rpx;
  position: relative;
  z-index: 1;
  flex: 1;
}

.step-dot {
  width: 32rpx;
  height: 32rpx;
  border-radius: 50%;
  background: $surface-container-high;
  border: 4rpx solid $outline-variant;
  transition: all 0.3s ease;
}

.step-active .step-dot {
  background: $primary-container;
  border-color: $primary;
}

.step-completed .step-dot {
  background: $primary;
  border-color: $primary;
}

.step-label {
  font-size: 24rpx;
  color: $on-surface-variant;
  font-weight: 500;
}

.step-active .step-label {
  color: $primary;
  font-weight: 600;
}

// 卡片头部
.card-header {
  margin-bottom: 20rpx;
}

.room-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.room-name {
  font-size: 34rpx;
  font-weight: 600;
  color: $on-surface;
}

.time-range {
  font-size: 26rpx;
  color: $on-surface-variant;
}

// 卡片内容
.card-body {
  display: flex;
  flex-direction: column;
  gap: 12rpx;
  padding-bottom: 20rpx;
}

.info-row {
  display: flex;
  align-items: flex-start;
  gap: 8rpx;
}

.info-label {
  font-size: 28rpx;
  color: $on-surface-variant;
  flex-shrink: 0;
}

.info-value {
  font-size: 28rpx;
  color: $on-surface;
  flex: 1;
}

.info-value.purpose {
  word-break: break-all;
}

// 展开内容
.card-expand {
  margin-top: 8rpx;
}

.divider {
  display: none;
}

.review-section {
  background: $surface-container-low;
  border-radius: 16rpx;
  padding: 24rpx;
  margin-top: 20rpx;
}

.review-title {
  display: block;
  font-size: 28rpx;
  font-weight: 600;
  color: $on-surface;
  margin-bottom: 20rpx;
}

.review-item {
  padding: 20rpx 0;
  border-bottom: none;
  
  &:last-child {
    padding-bottom: 0;
  }
  
  &:first-child {
    padding-top: 0;
  }
}

.review-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12rpx;
}

.reviewer {
  font-size: 28rpx;
  font-weight: 500;
  color: $on-surface;
}

.review-action {
  font-size: 26rpx;
  font-weight: 600;
  
  &.action-approve {
    color: $approved-color;
  }
  
  &.action-reject {
    color: $rejected-color;
  }
}

.review-opinion {
  display: block;
  font-size: 28rpx;
  color: $on-surface;
  margin-bottom: 12rpx;
  line-height: 1.5;
}

.review-time {
  font-size: 24rpx;
  color: $on-surface-variant;
}

// 卡片底部
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 20rpx;
  padding-top: 20rpx;
  border-top: 1rpx solid $surface-container-high;
}

.submit-time {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.action-btns {
  display: flex;
  gap: 16rpx;
}

.cancel-btn {
  margin: 0;
  padding: 8rpx 24rpx;
  background: rgba(239, 68, 68, 0.1);
  border: none;
  border-radius: 48rpx;
  font-size: 26rpx;
  color: #ef4444;
  line-height: 1.5;
  
  &:active {
    background: rgba(239, 68, 68, 0.2);
  }
}

// 加载更多
.load-more {
  padding: 32rpx 0;
  text-align: center;
}

.load-text {
  font-size: 28rpx;
  color: $primary;
  padding: 16rpx 40rpx;
}

.no-more {
  padding: 32rpx 0;
  text-align: center;
}

.no-more-text {
  font-size: 26rpx;
  color: $on-surface-variant;
}

.bottom-safe {
  height: 40rpx;
}
</style>
