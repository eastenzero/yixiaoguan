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
            :class="{ 'filter-tab--active': activeFilter === index }"
            @click="activeFilter = index"
          >
            <text class="tab-text">{{ tab.label }}({{ tab.count }})</text>
          </view>
        </view>
      </scroll-view>

      <!-- Question List -->
      <view class="question-list">
        <view 
          v-for="(question, index) in questions" 
          :key="question.id"
          class="question-card animate-fade-up"
          :class="`delay-${index + 2}`"
          @click="goToDetail(question.id)"
        >
          <view class="card-header">
            <view class="student-info">
              <view class="avatar-placeholder"></view>
              <view class="student-meta">
                <text class="student-name">{{ question.studentName }}</text>
                <text class="student-major">{{ question.major }} · {{ question.time }}</text>
              </view>
            </view>
            <view 
              class="status-tag"
              :class="`status-${question.status}`"
            >
              <text class="status-text">{{ getStatusText(question.status) }}</text>
            </view>
          </view>

          <text class="question-content">{{ question.content }}</text>

          <!-- AI Confidence Section -->
          <view class="ai-confidence">
            <view class="confidence-header">
              <view class="confidence-label">
                <IconBrain :size="12" color="#5d5b5f" />
                <text class="label-text">AI 匹配度</text>
              </view>
              <text class="confidence-value">{{ question.confidence }}%</text>
            </view>
            <view class="progress-bar">
              <view 
                class="progress-fill"
                :class="getProgressColorClass(question.confidence)"
                :style="{ width: `${question.confidence}%` }"
              ></view>
            </view>
          </view>
        </view>
      </view>
    </view>

    <BottomNavBar :current="1" :badge="3" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TopAppBar from '../../components/TopAppBar.vue'
import BottomNavBar from '../../components/BottomNavBar.vue'
import { IconBrain } from '../../components/icons'

// Filter tabs data
const filterTabs = [
  { label: '全部', count: 28 },
  { label: '待处理', count: 3 },
  { label: '处理中', count: 5 },
  { label: '已解决', count: 20 }
]

const activeFilter = ref(0)

// Mock questions data
const questions = [
  {
    id: 1,
    studentName: '陈小明',
    major: '计算机科学与技术',
    time: '10分钟前',
    status: 'pending',
    content: '老师您好，在最新的深度学习作业中，关于Transformer模型的多头注意力机制实现，我不太确定在多头拼接后的线性映射层是否需要添加Bias...',
    confidence: 92
  },
  {
    id: 2,
    studentName: '林静怡',
    major: '数字媒体艺术',
    time: '2小时前',
    status: 'processing',
    content: '关于期中作品集的排版，目前的C4D渲染结果噪点比较多，请问在Octane渲染器中如何平衡采样率和渲染时间？',
    confidence: 74
  },
  {
    id: 3,
    studentName: '张子涵',
    major: '应用数学系',
    time: '昨天',
    status: 'pending',
    content: '请问偏微分方程在金融定价模型中的具体推导过程，上课讲的Black-Scholes方程部分，热传导方程的变换还没完全理解。',
    confidence: 38
  }
]

const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    pending: '待处理',
    processing: '处理中',
    resolved: '已解决'
  }
  return statusMap[status] || status
}

const getProgressColorClass = (confidence: number) => {
  if (confidence >= 80) return 'progress-green'
  if (confidence >= 60) return 'progress-amber'
  return 'progress-red'
}

const goToDetail = (id: number) => {
  uni.navigateTo({ url: `/pages/questions/detail?id=${id}` })
}
</script>

<style lang="scss" scoped>
@import '../../styles/theme.scss';

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

  &.status-pending {
    background: rgba($error-container, 0.1);

    .status-text {
      color: $error;
    }
  }

  &.status-processing {
    background: rgba($primary-container, 0.2);

    .status-text {
      color: $primary;
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
