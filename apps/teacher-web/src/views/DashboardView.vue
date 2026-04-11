<template>
  <div class="dashboard-page">
    <!-- 统计卡片区域（带悬停动效） -->
    <div class="stats-row">
      <div class="stat-card primary hover-lift">
        <div class="stat-header">
          <span class="stat-label">今日处理提问</span>
          <div class="stat-icon">
            <el-icon :size="20"><ChatDotRound /></el-icon>
          </div>
        </div>
        <div class="stat-value font-display">{{ stats.todayQuestions }}</div>
        <div class="stat-badge">
          <span>{{ formatGrowth(stats.todayQuestionsGrowth) }} 同比昨日</span>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-header">
          <span class="stat-label">待审批事项</span>
          <div class="stat-icon warning">
            <el-icon :size="20"><Warning /></el-icon>
          </div>
        </div>
        <div class="stat-value font-display">{{ stats.pendingApprovals }}</div>
        <div v-if="stats.urgentApprovals > 0" class="stat-alert">
          <el-icon><WarningFilled /></el-icon>
          <span>{{ stats.urgentApprovals }}项即将超时</span>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-header">
          <span class="stat-label">AI 自动解决率</span>
          <div class="stat-icon success">
            <el-icon :size="20"><Cpu /></el-icon>
          </div>
        </div>
        <div class="stat-value font-display">{{ stats.aiResolutionRate }}%</div>
        <div class="stat-progress">
          <div class="progress-track">
            <div class="progress-fill" :style="{ width: stats.aiResolutionRate + '%' }"></div>
          </div>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-header">
          <span class="stat-label">平均响应时间</span>
          <div class="stat-icon info">
            <el-icon :size="20"><Timer /></el-icon>
          </div>
        </div>
        <div class="stat-value font-display">
          {{ stats.avgResponseTime }}
          <span class="unit">min</span>
        </div>
        <div class="stat-trend down">
          <el-icon><Bottom /></el-icon>
          <span>较上周缩短 {{ stats.responseTimeImprovement }}min</span>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-grid">
      <!-- 左侧：今日学生提问列表 -->
      <div class="content-col">
        <div class="table-card hover-lift">
          <div class="card-header">
            <div class="header-title">
              <el-icon :size="20" color="#7C3AED"><ChatDotRound /></el-icon>
              <span class="font-display">今日学生提问列表</span>
            </div>
            <el-link type="primary" underline="never" class="view-link" @click="$router.push('/questions')">
              查看全部
            </el-link>
          </div>
          <div class="table-body">
            <el-skeleton :rows="3" animated v-if="loading.questions" />
            <table v-else class="data-table">
              <thead>
                <tr>
                  <th>提问时间</th>
                  <th>学生信息</th>
                  <th>问题摘要</th>
                  <th>分类</th>
                  <th>AI状态</th>
                  <th class="text-right">操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in questionList" :key="index" class="hover-row">
                  <td class="time-cell">{{ formatTime(item.time) }}</td>
                  <td>
                    <div class="student-info">
                      <el-avatar :size="28" :style="{ backgroundColor: getAvatarColor(item.studentName) }">
                        {{ item.studentName?.charAt(0) || '?' }}
                      </el-avatar>
                      <span class="student-name">{{ item.studentName }} {{ item.studentClass }}</span>
                    </div>
                  </td>
                  <td class="content-cell">{{ item.title }}</td>
                  <td>
                    <span class="category-tag">{{ item.category }}</span>
                  </td>
                  <td>
                    <span class="status-badge" :class="item.aiStatus">
                      <span class="dot"></span>
                      {{ item.aiText }}
                    </span>
                  </td>
                  <td class="text-right">
                    <el-button link type="primary" class="action-btn" @click="handleViewQuestion(item)">
                      {{ item.needHandle ? '处理' : '查看' }}
                    </el-button>
                  </td>
                </tr>
                <tr v-if="questionList.length === 0">
                  <td colspan="6" class="empty-cell">
                    <el-empty description="暂无数据" :image-size="60" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 底部双卡片 -->
        <div class="sub-cards">
          <div class="sub-card hover-lift">
            <div class="card-header">
              <div class="header-title">
                <el-icon :size="18" color="#7C3AED"><Histogram /></el-icon>
                <span class="font-display">高频问题热度统计</span>
              </div>
              <el-link type="primary" underline="never">查看全部</el-link>
            </div>
            <div class="card-body">
              <el-skeleton :rows="3" animated v-if="loading.hotQuestions" />
              <div v-else class="hot-list">
                <div class="hot-item" v-for="(item, index) in hotQuestions" :key="index">
                  <div class="hot-info">
                    <span class="hot-name">{{ item.name }}</span>
                    <span class="hot-count">{{ item.count }} 次</span>
                  </div>
                  <div class="hot-bar">
                    <div class="hot-fill" :style="{ width: item.percent + '%' }"></div>
                  </div>
                </div>
                <el-empty v-if="hotQuestions.length === 0" description="暂无数据" :image-size="60" />
              </div>
            </div>
          </div>

          <div class="sub-card hover-lift">
            <div class="card-header">
              <div class="header-title">
                <el-icon :size="18" color="#7C3AED"><Collection /></el-icon>
                <span class="font-display">知识库快捷入口</span>
              </div>
            </div>
            <div class="card-body">
              <div class="quick-grid">
                <div class="quick-item" v-for="item in quickAccess" :key="item.name" @click="handleQuickAccess(item)">
                  <div class="quick-icon" :style="{ backgroundColor: item.bgColor, color: item.color }">
                    <el-icon :size="20"><component :is="getIconComponent(item.icon)" /></el-icon>
                  </div>
                  <span class="quick-name">{{ item.name }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧：待审批事项 + AI预警 -->
      <div class="sidebar-col">
        <div class="sidebar-card hover-lift">
          <div class="card-header">
            <div class="header-title">
              <el-icon :size="20" color="#7C3AED"><Checked /></el-icon>
              <span class="font-display">待审批事项</span>
            </div>
            <el-tag size="small" type="danger" effect="light" class="count-tag">
              {{ pendingApprovals.length }} 个待办
            </el-tag>
          </div>
          <div class="card-body">
            <el-skeleton :rows="3" animated v-if="loading.approvals" />
            <template v-else>
              <div class="approval-list">
                <div 
                  class="approval-item" 
                  :class="{ urgent: item.isUrgent }" 
                  v-for="item in pendingApprovals.slice(0, 3)" 
                  :key="item.id"
                  @click="handleViewApproval(item)"
                >
                  <div class="item-header">
                    <span class="item-tag">{{ item.type }}</span>
                    <span v-if="item.isUrgent" class="urgent-badge">{{ item.remainingTime }}</span>
                  </div>
                  <h4 class="item-title">{{ item.title }}</h4>
                  <div class="item-meta">
                    <span><el-icon><Calendar /></el-icon> {{ item.timeRange }}</span>
                  </div>
                </div>
                <el-empty v-if="pendingApprovals.length === 0" description="暂无待办" :image-size="60" />
              </div>
              <button class="view-all-btn" @click="$router.push('/approval')">
                查看所有待审批项
              </button>
            </template>
          </div>
        </div>

        <!-- AI 舆情预警（渐变卡片） -->
        <div class="ai-warning-card hover-lift" v-if="aiWarning">
          <div class="warning-content">
            <div class="warning-header">
              <el-icon :size="20"><StarFilled /></el-icon>
              <span class="font-display">AI 舆情预警</span>
            </div>
            <p class="warning-desc">
              本周关于 <strong>"{{ aiWarning.topic }}"</strong> 的提问量异常上升 <strong>{{ aiWarning.increasePercent }}%</strong>，{{ aiWarning.suggestion }}
            </p>
            <el-button type="primary" class="warning-btn" text bg @click="handleGenerateDraft">
              生成公告草稿
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ChatDotRound,
  Warning,
  WarningFilled,
  Cpu,
  Timer,
  Bottom,
  Histogram,
  Collection,
  Calendar,
  StarFilled,
  Document,
  Reading,
  ChatLineRound,
  QuestionFilled,
  Checked
} from '@element-plus/icons-vue'
import type { Component } from 'vue'

import {
  getDashboardStats,
  getTodayQuestions,
  getHotQuestions,
  getPendingApprovals,
  getAIWarnings,
  type DashboardStats,
  type TodayQuestion,
  type HotQuestion,
  type PendingApproval,
  type AIWarning
} from '@/api/dashboard'

const router = useRouter()

// ===== 图标映射 =====
const iconMap: Record<string, Component> = {
  Document,
  Reading,
  ChatLineRound,
  QuestionFilled
}

function getIconComponent(name: string): Component {
  return iconMap[name] || Document
}

// ===== 响应式数据 =====
const loading = reactive({
  stats: false,
  questions: false,
  hotQuestions: false,
  approvals: false
})

const stats = reactive<DashboardStats>({
  todayQuestions: 0,
  todayQuestionsGrowth: 0,
  pendingApprovals: 0,
  urgentApprovals: 0,
  aiResolutionRate: 0,
  avgResponseTime: 0,
  responseTimeImprovement: 0
})

const questionList = ref<TodayQuestion[]>([])
const hotQuestions = ref<HotQuestion[]>([])
const pendingApprovals = ref<PendingApproval[]>([])
const aiWarning = ref<AIWarning | null | undefined>(null)

// ===== 静态数据（知识库快捷入口）=====
const quickAccess = [
  { name: '学工政策', icon: 'Document', bgColor: '#F5F3FF', color: '#7C3AED' },
  { name: '教学大纲', icon: 'Reading', bgColor: '#EFF6FF', color: '#3B82F6' },
  { name: '客服话术', icon: 'ChatLineRound', bgColor: '#F5F3FF', color: '#8B5CF6' },
  { name: '常见Q&A', icon: 'QuestionFilled', bgColor: '#FFF7ED', color: '#F97316' }
]

// ===== 辅助函数 =====
function formatTime(time?: string): string {
  // 如果后端返回完整日期，格式化为时间
  if (time?.includes('T') || time?.includes(' ')) {
    const date = new Date(time)
    return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
  }
  return time || '--'
}

function formatGrowth(growth: number): string {
  const sign = growth >= 0 ? '+' : ''
  return `${sign}${growth}%`
}

function getAvatarColor(name?: string): string {
  const colors = ['#3B82F6', '#EF4444', '#10B981', '#F59E0B', '#8B5CF6', '#EC4899', '#06B6D4']
  let hash = 0
  const safeName = name || ''
  for (let i = 0; i < safeName.length; i++) {
    hash = safeName.charCodeAt(i) + ((hash << 5) - hash)
  }
  return colors[Math.abs(hash) % colors.length] || '#3B82F6'
}

// ===== 事件处理 =====
function handleViewQuestion(item: TodayQuestion) {
  router.push(`/questions?id=${item.id}`)
}

function handleViewApproval(item: PendingApproval) {
  router.push(`/approval?id=${item.id}`)
}

function handleQuickAccess(item: typeof quickAccess[0]) {
  ElMessage.info(`即将跳转到: ${item.name}`)
  // router.push(`/knowledge?category=${item.name}`)
}

function handleGenerateDraft() {
  ElMessage.success('正在生成公告草稿...')
}

// ===== 数据加载 =====
async function loadDashboardData() {
  // 并行加载所有数据
  await Promise.all([
    loadStats(),
    loadQuestions(),
    loadHotQuestions(),
    loadPendingApprovals(),
    loadAIWarnings()
  ])
}

async function loadStats() {
  loading.stats = true
  try {
    const res = await getDashboardStats()
    if (res.code === 200 && res.data) {
      Object.assign(stats, res.data)
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    // 使用默认值，避免页面空白
  } finally {
    loading.stats = false
  }
}

async function loadQuestions() {
  loading.questions = true
  try {
    const res = await getTodayQuestions({ pageSize: 5 })
    if (res.code === 200 && res.data) {
      // 如果后端没有这些字段，做数据适配
      questionList.value = (res.data.rows || []).map((item: any) => ({
        ...item,
        aiStatus: mapStatusToAiStatus(item.status),
        aiText: mapStatusToAiText(item.status),
        needHandle: item.status === 0 || item.status === 1
      }))
    }
  } catch (error) {
    console.error('加载提问列表失败:', error)
  } finally {
    loading.questions = false
  }
}

async function loadHotQuestions() {
  loading.hotQuestions = true
  try {
    const res = await getHotQuestions(3)
    if (res.code === 200 && res.data) {
      hotQuestions.value = res.data
    }
  } catch (error) {
    console.error('加载高频问题失败:', error)
  } finally {
    loading.hotQuestions = false
  }
}

async function loadPendingApprovals() {
  loading.approvals = true
  try {
    const res = await getPendingApprovals(3)
    if (res.code === 200 && res.data) {
      pendingApprovals.value = res.data
    }
  } catch (error) {
    console.error('加载待审批事项失败:', error)
  } finally {
    loading.approvals = false
  }
}

async function loadAIWarnings() {
  try {
    const res = await getAIWarnings()
    if (res.code === 200 && res.data && res.data.length > 0) {
      aiWarning.value = res.data[0]
    }
  } catch (error) {
    console.error('加载 AI 预警失败:', error)
  }
}

// ===== 状态映射函数（后端状态 → 前端显示状态）=====
function mapStatusToAiStatus(status?: number): 'resolved' | 'pending' | 'handled' {
  switch (status) {
    case 0: return 'pending'    // 待处理
    case 1: return 'handled'    // 处理中
    case 2: return 'resolved'   // 已解决
    default: return 'pending'
  }
}

function mapStatusToAiText(status?: number): string {
  switch (status) {
    case 0: return '待人工确认'
    case 1: return '已处理'
    case 2: return '已自动回复'
    default: return '待处理'
  }
}

// ===== 生命周期 =====
onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped lang="scss">
.dashboard-page {
  max-width: 1400px;
  margin: 0 auto;
}

// ========================================
// 统计卡片（带悬停动效）
// ========================================
.stats-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 20px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  &.primary {
    background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
    color: #fff;
    border: none;

    .stat-label,
    .stat-badge {
      color: rgba(255, 255, 255, 0.85);
    }

    .stat-icon {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
    }
  }

  .stat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
  }

  .stat-label {
    font-size: 14px;
    color: var(--text-secondary);
    font-weight: 500;
  }

  .stat-icon {
    width: 40px;
    height: 40px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-bg);
    color: var(--primary-color);

    &.warning {
      background: #fef3c7;
      color: #f59e0b;
    }

    &.success {
      background: #d1fae5;
      color: #10b981;
    }

    &.info {
      background: #dbeafe;
      color: #3b82f6;
    }
  }

  .stat-value {
    font-size: 32px;
    font-weight: 800;
    color: var(--on-surface);
    margin-bottom: 8px;
    letter-spacing: -0.02em;

    .unit {
      font-size: 16px;
      font-weight: 500;
      color: var(--text-tertiary);
      margin-left: 4px;
    }
  }

  .stat-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    padding: 4px 10px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    font-weight: 500;
  }

  .stat-alert {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: #f59e0b;
    font-weight: 500;
  }

  .stat-trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 500;

    &.down {
      color: #10b981;
    }
  }

  .stat-progress {
    .progress-track {
      height: 4px;
      background: #e2e8f0;
      border-radius: 2px;
      overflow: hidden;

      .progress-fill {
        height: 100%;
        background: var(--primary-color);
        border-radius: 2px;
        transition: width 0.6s ease;
      }
    }
  }
}

// ========================================
// 主网格
// ========================================
.main-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
}

.content-col {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// ========================================
// 表格卡片
// ========================================
.table-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  overflow: hidden;
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 24px;
    border-bottom: 1px solid var(--surface-highest);

    .header-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      font-weight: 700;
      color: var(--on-surface);
    }

    .view-link {
      font-weight: 600;
    }
  }
}

.data-table {
  width: 100%;
  border-collapse: collapse;

  thead {
    background: var(--surface-low);

    th {
      padding: 14px 20px;
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
      text-align: left;
      font-family: var(--font-display);

      &.text-right {
        text-align: right;
      }
    }
  }

  tbody {
    tr {
      border-bottom: 1px solid var(--surface-low);
      transition: background-color var(--transition-fast);

      &:hover {
        background-color: var(--primary-bg);
      }

      &:last-child {
        border-bottom: none;
      }

      td {
        padding: 14px 20px;
        font-size: 13px;
        color: var(--text-primary);

        &.time-cell {
          color: var(--text-secondary);
        }

        &.content-cell {
          max-width: 200px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          color: var(--text-secondary);
        }

        &.text-right {
          text-align: right;
        }

        &.empty-cell {
          padding: 40px;
        }
      }
    }
  }
}

.student-info {
  display: flex;
  align-items: center;
  gap: 10px;

  .student-name {
    font-weight: 500;
    color: var(--on-surface);
  }
}

.category-tag {
  display: inline-block;
  padding: 4px 10px;
  background: var(--surface-low);
  border-radius: 6px;
  font-size: 11px;
  color: var(--text-secondary);
  font-weight: 500;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-weight: 500;

  &.resolved {
    color: #10b981;
  }

  &.pending {
    color: #f59e0b;
  }

  &.handled {
    color: var(--primary-color);
  }

  .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
  }
}

.action-btn {
  font-weight: 600;
  transition: all var(--transition-fast);

  &:hover {
    transform: scale(1.05);
  }
}

// ========================================
// 子卡片
// ========================================
.sub-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.sub-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 20px;
    border-bottom: 1px solid var(--surface-highest);

    .header-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 15px;
      font-weight: 700;
      color: var(--on-surface);
    }
  }

  .card-body {
    padding: 20px;
  }
}

// 高频问题
.hot-list {
  display: flex;
  flex-direction: column;
  gap: 18px;

  .hot-item {
    .hot-info {
      display: flex;
      justify-content: space-between;
      margin-bottom: 8px;

      .hot-name {
        font-size: 13px;
        color: var(--text-primary);
      }

      .hot-count {
        font-size: 12px;
        color: var(--text-secondary);
        font-weight: 600;
      }
    }

    .hot-bar {
      height: 6px;
      background: var(--surface-low);
      border-radius: 3px;
      overflow: hidden;

      .hot-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color), var(--primary-container));
        border-radius: 3px;
        transition: width 0.6s ease;
      }
    }
  }
}

// 快捷入口
.quick-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;

  .quick-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 16px 12px;
    border-radius: var(--radius-md);
    background: var(--surface-low);
    cursor: pointer;
    transition: all var(--transition-normal);

    &:hover {
      background: var(--primary-bg);
      transform: translateY(-2px);
    }

    &:active {
      transform: scale(0.98);
    }

    .quick-icon {
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform var(--transition-fast);
    }

    &:hover .quick-icon {
      transform: scale(1.1);
    }

    .quick-name {
      font-size: 12px;
      color: var(--text-secondary);
      font-weight: 500;
    }
  }
}

// ========================================
// 侧边栏
// ========================================
.sidebar-col {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  overflow: hidden;
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 20px;
    border-bottom: 1px solid var(--surface-highest);

    .header-title {
      display: flex;
      align-items: center;
      gap: 10px;
      font-size: 16px;
      font-weight: 700;
      color: var(--on-surface);
    }

    .count-tag {
      font-weight: 600;
    }
  }

  .card-body {
    padding: 20px;
  }
}

.approval-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.approval-item {
  padding: 16px;
  background: var(--surface-low);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--primary-color);
  transition: all var(--transition-fast);
  cursor: pointer;

  &:hover {
    background: var(--surface-high);
  }

  &.urgent {
    border-left-color: #f59e0b;
  }

  .item-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;

    .item-tag {
      font-size: 10px;
      font-weight: 700;
      color: var(--text-tertiary);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    .urgent-badge {
      font-size: 11px;
      color: #f59e0b;
      background: #fef3c7;
      padding: 2px 8px;
      border-radius: 10px;
      font-weight: 600;
    }
  }

  .item-title {
    font-size: 15px;
    font-weight: 700;
    color: var(--on-surface);
    margin-bottom: 8px;
  }

  .item-meta {
    font-size: 12px;
    color: var(--text-secondary);

    .el-icon {
      font-size: 12px;
      margin-right: 4px;
    }
  }
}

.view-all-btn {
  width: 100%;
  padding: 12px;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-tertiary);
  background: transparent;
  border: 1px dashed var(--surface-highest);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-fast);

  &:hover {
    border-color: var(--primary-color);
    color: var(--primary-color);
    background: var(--primary-bg);
  }
}

// AI 预警卡片
.ai-warning-card {
  background: linear-gradient(135deg, #7C3AED 0%, #6D28D9 100%);
  border-radius: var(--radius-lg);
  padding: 24px;
  color: #fff;
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 32px -4px rgba(124, 58, 237, 0.2);
  }

  .warning-content {
    .warning-header {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
      font-size: 16px;
      font-weight: 700;
    }

    .warning-desc {
      font-size: 13px;
      line-height: 1.7;
      color: rgba(255, 255, 255, 0.85);
      margin-bottom: 16px;

      strong {
        color: #5eead4;
        font-weight: 600;
      }
    }

    .warning-btn {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
      font-weight: 600;

      &:hover {
        background: rgba(255, 255, 255, 0.25);
      }
    }
  }
}

// 响应式
@media (max-width: 1200px) {
  .main-grid {
    grid-template-columns: 1fr;
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .sub-cards {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
}
</style>
