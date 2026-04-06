<template>
  <view class="questions-page">
    <!-- 页面标题 -->
    <view class="page-header">
      <text class="header-title">我的提问</text>
      <text class="header-subtitle">查看您的问题处理进度</text>
    </view>

    <!-- 筛选标签 -->
    <view class="filter-tabs">
      <view
        v-for="tab in filterTabs"
        :key="tab.value"
        class="filter-tab"
        :class="{ 'tab-active': currentFilter === tab.value }"
        @click="handleFilterChange(tab.value)"
      >
        <text class="tab-text">{{ tab.label }}</text>
      </view>
    </view>

    <!-- 工单列表 -->
    <scroll-view
      class="escalation-list"
      scroll-y
      :refresher-enabled="true"
      :refresher-triggered="refreshing"
      @refresherrefresh="onRefresh"
      @scrolltolower="loadMore"
    >
      <!-- 空状态 -->
      <view v-if="!loading && escalationList.length === 0" class="empty-state">
        <view class="empty-icon">
          <text class="icon-text">📝</text>
        </view>
        <text class="empty-title">暂无问题记录</text>
        <text class="empty-desc">您还没有提交过问题，快去咨询 AI 或呼叫老师吧</text>
        <button class="empty-btn" @click="goToChat">去提问</button>
      </view>

      <!-- 列表内容 -->
      <view v-else class="list-content">
        <view
          v-for="item in escalationList"
          :key="item.id"
          class="escalation-card"
          @click="goToConversation(item)"
        >
          <!-- 卡片头部 -->
          <view class="card-header">
            <view class="status-badge" :class="getStatusClass(item.status)">
              <text class="status-text">{{ getStatusText(item.status) }}</text>
            </view>
            <text class="create-time">{{ formatTime(item.createdAt) }}</text>
          </view>

          <!-- 问题摘要 -->
          <view class="question-content">
            <text class="question-text">{{ item.questionSummary || '暂无问题描述' }}</text>
          </view>

          <!-- 卡片底部 -->
          <view class="card-footer">
            <view class="footer-item">
              <text class="footer-label">会话 ID:</text>
              <text class="footer-value">#{{ item.conversationId }}</text>
            </view>
            <view v-if="item.teacherId" class="footer-item">
              <text class="footer-label">处理老师:</text>
              <text class="footer-value">已分配</text>
            </view>
            <text class="arrow-icon">›</text>
          </view>
        </view>

        <!-- 加载更多 -->
        <view v-if="loadingMore" class="load-more">
          <text class="load-text">加载中...</text>
        </view>

        <!-- 没有更多 -->
        <view v-if="!hasMore && escalationList.length > 0" class="no-more">
          <text class="no-more-text">没有更多了</text>
        </view>
      </view>
    </scroll-view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import { getMyEscalations } from '@/api/chat'
import { EscalationStatus, type Escalation } from '@/types/chat'

// ===== 筛选配置 =====
const filterTabs = [
  { label: '全部', value: undefined },
  { label: '待处理', value: EscalationStatus.PENDING },
  { label: '处理中', value: EscalationStatus.PROCESSING },
  { label: '已解决', value: EscalationStatus.RESOLVED }
]

// ===== 状态管理 =====
const currentFilter = ref<number | undefined>(undefined)
const escalationList = ref<Escalation[]>([])
const loading = ref(false)
const refreshing = ref(false)
const loadingMore = ref(false)
const hasMore = ref(true)

// 分页参数
const pageNum = ref(1)
const pageSize = 10

// ===== 生命周期 =====
onShow(() => {
  // 每次显示页面都刷新数据
  loadData(true)
})

// ===== 数据加载 =====

/**
 * 加载数据
 * @param reset 是否重置列表
 */
async function loadData(reset = false) {
  if (reset) {
    pageNum.value = 1
    hasMore.value = true
    escalationList.value = []
  }

  if (loading.value || (!hasMore.value && !reset)) return

  loading.value = true

  try {
    const result = await getMyEscalations(currentFilter.value, {
      pageNum: pageNum.value,
      pageSize
    })

    if (reset) {
      escalationList.value = result.rows
    } else {
      escalationList.value.push(...result.rows)
    }

    // 判断是否还有更多
    hasMore.value = result.rows.length === pageSize

  } catch (error) {
    console.error('加载工单列表失败:', error)
    uni.showToast({
      title: '加载失败',
      icon: 'none'
    })
  } finally {
    loading.value = false
    refreshing.value = false
    loadingMore.value = false
  }
}

/**
 * 下拉刷新
 */
function onRefresh() {
  refreshing.value = true
  loadData(true)
}

/**
 * 加载更多
 */
function loadMore() {
  if (!hasMore.value || loadingMore.value) return
  loadingMore.value = true
  pageNum.value++
  loadData()
}

/**
 * 切换筛选条件
 */
function handleFilterChange(value: number | undefined) {
  if (currentFilter.value === value) return
  currentFilter.value = value
  loadData(true)
}

// ===== 状态显示 =====

function getStatusText(status: EscalationStatus): string {
  const statusMap: Record<number, string> = {
    [EscalationStatus.PENDING]: '待处理',
    [EscalationStatus.PROCESSING]: '处理中',
    [EscalationStatus.RESOLVED]: '已解决',
    [EscalationStatus.CLOSED]: '已关闭',
    [EscalationStatus.TO_KNOWLEDGE]: '已转知识库'
  }
  return statusMap[status] || '未知'
}

function getStatusClass(status: EscalationStatus): string {
  const classMap: Record<number, string> = {
    [EscalationStatus.PENDING]: 'status-pending',
    [EscalationStatus.PROCESSING]: 'status-processing',
    [EscalationStatus.RESOLVED]: 'status-resolved',
    [EscalationStatus.CLOSED]: 'status-closed',
    [EscalationStatus.TO_KNOWLEDGE]: 'status-resolved'
  }
  return classMap[status] || 'status-pending'
}

// ===== 时间格式化 =====

function formatTime(timeStr: string): string {
  if (!timeStr) return ''
  
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 小于 1 分钟
  if (diff < 60 * 1000) {
    return '刚刚'
  }
  
  // 小于 1 小时
  if (diff < 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 1000))}分钟前`
  }
  
  // 小于 24 小时
  if (diff < 24 * 60 * 60 * 1000) {
    return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  }
  
  // 小于 7 天
  if (diff < 7 * 24 * 60 * 60 * 1000) {
    return `${Math.floor(diff / (24 * 60 * 60 * 1000))}天前`
  }
  
  // 更早
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

// ===== 页面跳转 =====

function goToConversation(item: Escalation) {
  uni.navigateTo({
    url: `/pages/chat/index?conversationId=${item.conversationId}`
  })
}

function goToChat() {
  uni.switchTab({
    url: '/pages/chat/index'
  })
}
</script>

<style lang="scss" scoped>
page {
  background-color: #f0f7f5;
}

// 设计规范颜色
$primary: #006a64;
$primary-container: #00A79D;
$surface: #f0f7f5;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$on-surface: #171d1c;
$on-surface-variant: #5a635f;
$outline: #89938f;
$tertiary: #984623;
$error: #ba1a1a;

.questions-page {
  min-height: 100vh;
  background-color: $surface;
  display: flex;
  flex-direction: column;
}

// 页面头部
.page-header {
  padding: 48rpx 32rpx 32rpx;
  background: linear-gradient(135deg, $primary, $primary-container);
}

.header-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $surface-container-lowest;
  margin-bottom: 8rpx;
}

.header-subtitle {
  font-size: 26rpx;
  color: rgba($surface-container-lowest, 0.8);
}

// 筛选标签
.filter-tabs {
  display: flex;
  padding: 24rpx 32rpx;
  background-color: $surface-container-lowest;
  gap: 16rpx;
  overflow-x: auto;
}

.filter-tab {
  padding: 12rpx 28rpx;
  background-color: $surface-container-low;
  border-radius: 32rpx;
  flex-shrink: 0;
  
  &:active {
    opacity: 0.8;
  }
}

.tab-text {
  font-size: 26rpx;
  color: $on-surface-variant;
}

.tab-active {
  background-color: $primary;
  
  .tab-text {
    color: $surface-container-lowest;
    font-weight: 600;
  }
}

// 列表区
.escalation-list {
  flex: 1;
  padding: 16rpx 32rpx;
}

// 空状态
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 160rpx;
}

.empty-icon {
  width: 160rpx;
  height: 160rpx;
  background-color: $surface-container-low;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 32rpx;
}

.icon-text {
  font-size: 72rpx;
}

.empty-title {
  font-size: 32rpx;
  font-weight: 600;
  color: $on-surface;
  margin-bottom: 16rpx;
}

.empty-desc {
  font-size: 26rpx;
  color: $on-surface-variant;
  text-align: center;
  padding: 0 60rpx;
  margin-bottom: 48rpx;
  line-height: 1.6;
}

.empty-btn {
  padding: 20rpx 60rpx;
  font-size: 28rpx;
  font-weight: 600;
  color: $surface-container-lowest;
  background-color: $primary;
  border-radius: 40rpx;
  border: none;
  
  &:active {
    opacity: 0.9;
  }
}

// 卡片列表
.list-content {
  padding-bottom: 32rpx;
}

.escalation-card {
  background-color: $surface-container-lowest;
  border-radius: 24rpx;
  padding: 28rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: none;
  
  &:active {
    opacity: 0.95;
    transform: scale(0.995);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20rpx;
}

.status-badge {
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
}

.status-text {
  font-size: 22rpx;
  font-weight: 600;
}

.status-pending {
  background-color: rgba($tertiary, 0.12);
  .status-text {
    color: $tertiary;
  }
}

.status-processing {
  background-color: rgba($primary, 0.12);
  .status-text {
    color: $primary;
  }
}

.status-resolved {
  background-color: rgba(#2e7d32, 0.12);
  .status-text {
    color: #2e7d32;
  }
}

.status-closed {
  background-color: rgba($on-surface-variant, 0.12);
  .status-text {
    color: $on-surface-variant;
  }
}

.create-time {
  font-size: 22rpx;
  color: $on-surface-variant;
}

// 问题内容
.question-content {
  margin-bottom: 24rpx;
}



.question-text {
  display: block;
  font-size: 28rpx;
  color: $on-surface;
  line-height: 1.6;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

// 卡片底部
.card-footer {
  display: flex;
  align-items: center;
  padding-top: 20rpx;
  border-top: none;
}

.footer-item {
  display: inline-flex;
  align-items: center;
  margin-right: 32rpx;
}

.footer-label {
  font-size: 22rpx;
  color: $on-surface-variant;
  margin-right: 8rpx;
}

.footer-value {
  font-size: 22rpx;
  color: $on-surface;
  font-weight: 500;
}

.arrow-icon {
  margin-left: auto;
  font-size: 36rpx;
  color: $outline;
}

// 加载更多
.load-more {
  text-align: center;
  padding: 32rpx 0;
}

.load-text {
  font-size: 24rpx;
  color: $on-surface-variant;
}

.no-more {
  text-align: center;
  padding: 32rpx 0;
}

.no-more-text {
  font-size: 24rpx;
  color: $on-surface-variant;
}
</style>
