<template>
  <view class="questions-page">
    <TopAppBar title="学生提问" showBack action="search" />

    <view class="main-content">
      <!-- Filter Tabs -->
      <scroll-view scroll-x class="filter-section animate-fade-up delay-1" show-scrollbar="false">
        <view class="filter-tabs">
          <view 
            v-for="(tab, index) in filterTabs" 
            :key="index"
            class="filter-tab"
            :class="{ 'filter-tab--active': activeTab === index }"
            @click="switchTab(index)"
          >
            <text class="tab-text">{{ tab.label }}</text>
          </view>
        </view>
      </scroll-view>

      <!-- Loading State -->
      <view v-if="loading" class="loading-container">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- Empty State -->
      <view v-else-if="questions.length === 0" class="empty-container">
        <text class="empty-text">暂无工单</text>
      </view>

      <!-- Question List -->
      <view v-else class="question-list">
        <view 
          v-for="(item, index) in questions" 
          :key="item.id"
          class="question-card animate-fade-up"
          :class="`delay-${Math.min(index + 2, 4)}`"
          @click="goToDetail(item.id)"
        >
          <view class="card-header">
            <view class="student-info">
              <view class="avatar-placeholder"></view>
              <view class="student-meta">
                <text class="student-name">{{ item.studentRealName }}</text>
                <text class="student-major">{{ item.studentClassName }} · {{ formatTime(item.createdAt) }}</text>
              </view>
            </view>
            <view 
              class="status-tag"
              :class="`status-${item.status}`"
            >
              <text class="status-text">{{ getStatusText(item.status) }}</text>
            </view>
          </view>

          <text class="question-content">{{ item.questionSummary }}</text>

          <!-- AI Confidence Section -->
          <view class="ai-confidence">
            <view class="confidence-header">
              <view class="confidence-label">
                <IconBrain :size="12" color="#5d5b5f" />
                <text class="label-text">AI 匹配度</text>
              </view>
              <text class="confidence-value">{{ item.confidence || 80 }}%</text>
            </view>
            <view class="progress-bar">
              <view 
                class="progress-fill"
                :class="getProgressColorClass(item.confidence || 80)"
                :style="{ width: `${item.confidence || 80}%` }"
              ></view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <BottomNavBar :current="1" :badge="total > 99 ? 99 : total" />
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import TopAppBar from '../../components/TopAppBar.vue'
import BottomNavBar from '../../components/BottomNavBar.vue'
import { IconBrain } from '../../components/icons'
import { getPendingEscalations, getAssignedEscalations } from '@/api/escalation'

// Filter tabs data
const filterTabs = [
  { label: '全部' },
  { label: '待处理' },
  { label: '处理中' },
  { label: '已解决' }
]

const activeTab = ref(0)
const questions = ref<any[]>([])
const loading = ref(false)
const total = ref(0)

// 格式化时间
const formatTime = (timeStr: string) => {
  if (!timeStr) return ''
  const date = new Date(timeStr)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 小于1小时
  if (diff < 3600000) {
    const minutes = Math.floor(diff / 60000)
    return minutes < 1 ? '刚刚' : `${minutes}分钟前`
  }
  // 小于24小时
  if (diff < 86400000) {
    return `${Math.floor(diff / 3600000)}小时前`
  }
  // 小于7天
  if (diff < 604800000) {
    return `${Math.floor(diff / 86400000)}天前`
  }
  
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

// 状态映射
const getStatusText = (status: number) => {
  const statusMap: Record<number, string> = {
    0: '待处理',
    1: '处理中',
    2: '已解决',
    3: '已关闭'
  }
  return statusMap[status] || '未知'
}

const getProgressColorClass = (confidence: number) => {
  if (confidence >= 80) return 'progress-green'
  if (confidence >= 60) return 'progress-amber'
  return 'progress-red'
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    let res: any
    if (activeTab.value === 1) {
      // 待处理 = pending (status=0, 未分配)
      res = await getPendingEscalations(1, 20)
    } else {
      // 全部/处理中/已解决 = assigned (带 status 筛选)
      const statusMap: Record<number, number | undefined> = {
        0: undefined, // 全部
        2: 1,         // 处理中
        3: 2          // 已解决
      }
      res = await getAssignedEscalations(statusMap[activeTab.value], 1, 20)
    }
    questions.value = res.rows || []
    total.value = res.total || 0
  } catch (e) {
    console.error('加载工单失败', e)
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}

// Tab 切换
const switchTab = (index: number) => {
  activeTab.value = index
  loadData()
}

const goToDetail = (id: number) => {
  uni.navigateTo({ url: `/pages/questions/detail?id=${id}` })
}

onMounted(() => {
  loadData()
})

onShow(() => {
  loadData()
})
</script>

<style lang="scss" scoped>
.questions-page {
  min-height: 100vh;
  background: $surface;
  padding-bottom: 112px;
}

.main-content {
  padding-top: 80px;
  padding-left: 20px;
  padding-right: 20px;
}

// Loading & Empty State
.loading-container,
.empty-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
}

.loading-text,
.empty-text {
  font-size: 14px;
  color: $on-surface-variant;
}

// Filter Tabs
.filter-section {
  margin-left: -20px;
  margin-right: -20px;
  padding-left: 20px;
  padding-right: 20px;
  white-space: nowrap;
}

.filter-tabs {
  display: flex;
  gap: 12px;
  padding-bottom: 8px;
}

.filter-tab {
  flex-shrink: 0;
  padding: 10px 24px;
  border-radius: 9999px;
  background: $surface-container;
  transition: all 0.2s ease;

  .tab-text {
    font-size: 14px;
    font-weight: 500;
    color: $on-surface-variant;
  }

  &--active {
    background: $primary;
    box-shadow: 0 8px 16px -4px rgba($primary, 0.2);

    .tab-text {
      color: $on-primary;
    }
  }
}

// Question List
.question-list {
  margin-top: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// Question Card
.question-card {
  background: $surface-container-lowest;
  border-radius: 24px;
  padding: 20px;
  transition: transform 0.2s ease;

  &:active {
    transform: scale(0.98);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.student-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: $surface-container;
}

.student-meta {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.student-name {
  font-size: 16px;
  font-weight: 700;
  color: $on-surface;
}

.student-major {
  font-size: 12px;
  color: $on-surface-variant;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 9999px;

  .status-text {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  &.status-0 {
    background: rgba($error-container, 0.1);

    .status-text {
      color: $error;
    }
  }

  &.status-1 {
    background: rgba($primary-container, 0.2);

    .status-text {
      color: $primary;
    }
  }

  &.status-2 {
    background: rgba(#10b981, 0.1);

    .status-text {
      color: #10b981;
    }
  }

  &.status-3 {
    background: rgba($on-surface-variant, 0.1);

    .status-text {
      color: $on-surface-variant;
    }
  }
}

.question-content {
  font-size: 14px;
  line-height: 1.6;
  color: $on-surface-variant;
  margin-bottom: 24px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

// AI Confidence
.ai-confidence {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.confidence-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.confidence-label {
  display: flex;
  align-items: center;
  gap: 4px;

  .label-text {
    font-size: 10px;
    font-weight: 700;
    color: rgba($on-surface-variant, 0.6);
  }
}

.confidence-value {
  font-size: 10px;
  font-weight: 700;
  color: rgba($on-surface-variant, 0.6);
}

.progress-bar {
  height: 4px;
  width: 100%;
  background: $surface-container;
  border-radius: 9999px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 9999px;
  transition: width 0.3s ease;

  &.progress-green {
    background: #10b981;
  }

  &.progress-amber {
    background: #f59e0b;
  }

  &.progress-red {
    background: $error;
  }
}

// Animation delays
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
</style>
