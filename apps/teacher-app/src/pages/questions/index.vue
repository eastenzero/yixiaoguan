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
              <view class="avatar-circle" :style="{ background: avatarColors[index % avatarColors.length] }">
                <text class="avatar-initial">{{ item.studentRealName?.charAt(0) || '?' }}</text>
              </view>
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

const avatarColors = ['#702ae1', '#059669', '#d97706', '#0284c7', '#b41340']
const activeTab = ref(0)
const questions = ref<any[]>([])
const loading = ref(false)
const total = ref(0)

// Mock 数据 —— API 无数据时兜底展示
const mockQuestions = [
  {
    id: 1,
    studentRealName: '李明',
    studentClassName: '计算机2301班',
    createdAt: new Date(Date.now() - 1800000).toISOString(),
    status: 0,
    questionSummary: '老师您好，请问本学期的期末考试时间安排是什么时候？听说有几门课的考试时间调整了，能否确认一下最新的安排？',
    confidence: 92
  },
  {
    id: 2,
    studentRealName: '王小红',
    studentClassName: '软件工程2302班',
    createdAt: new Date(Date.now() - 7200000).toISOString(),
    status: 1,
    questionSummary: '请问学校图书馆的电子资源数据库该怎么访问？我在校外网络登录不了知网，需要 VPN 吗？',
    confidence: 78
  },
  {
    id: 3,
    studentRealName: '张伟',
    studentClassName: '信息安全2301班',
    createdAt: new Date(Date.now() - 86400000).toISOString(),
    status: 0,
    questionSummary: '我的校园卡在食堂刷不了，显示余额不足，但我昨天刚充了200块，请问这种情况怎么处理？',
    confidence: 85
  },
  {
    id: 4,
    studentRealName: '陈思思',
    studentClassName: '数据科学2301班',
    createdAt: new Date(Date.now() - 172800000).toISOString(),
    status: 2,
    questionSummary: '请问下学期的选课什么时候开始？有没有推荐的通识选修课？',
    confidence: 65
  },
  {
    id: 5,
    studentRealName: '刘洋',
    studentClassName: '人工智能2302班',
    createdAt: new Date(Date.now() - 3600000).toISOString(),
    status: 0,
    questionSummary: '宿舍的热水器坏了已经三天了，报修了但还没人来修，请问可以催一下吗？',
    confidence: 45
  }
]

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
    const rows = res.rows || []
    questions.value = rows.length > 0 ? rows : mockQuestions
    total.value = res.total || rows.length || mockQuestions.length
  } catch (e) {
    console.error('加载工单失败，使用 mock 数据', e)
    questions.value = mockQuestions
    total.value = mockQuestions.length
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
  position: relative;
  z-index: 1;
  padding-top: 72px;
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

  :deep(.uni-scroll-view::-webkit-scrollbar) {
    display: none;
  }
  :deep(.uni-scroll-view) {
    scrollbar-width: none;
  }
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
  background: $surface-container-low;
  transition: all 0.2s ease;
  white-space: nowrap;

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
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  min-width: 0;
  flex: 1;
}

.avatar-circle {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-initial {
  font-size: 18px;
  font-weight: 700;
  color: #ffffff;
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
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.status-tag {
  padding: 4px 12px;
  border-radius: 9999px;
  white-space: nowrap;
  flex-shrink: 0;
  margin-left: 8px;

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
  margin-bottom: 16px;
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
