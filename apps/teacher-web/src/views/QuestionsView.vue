<template>
  <div class="questions-page">
    <!-- 页面头部（参考图5） -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">今日学生提问</h1>
        <p class="page-desc">
          当前共有 <strong>{{ stats.totalUnsolved }}</strong> 条新提问需要处理。AI 已自动聚合 <strong>{{ stats.hotQuestions }}</strong> 组高频相似问题，
          系统建议优先处理 <strong>{{ stats.needHuman }}</strong> 条人工介入类咨询。
        </p>
      </div>
      <div class="header-stats">
        <div class="stat-mini">
          <span class="stat-label">待解决</span>
          <span class="stat-value warning">{{ padNumber(stats.totalUnsolved) }}</span>
        </div>
        <div class="stat-mini">
          <span class="stat-label">高频</span>
          <span class="stat-value danger">{{ padNumber(stats.hotQuestions) }}</span>
        </div>
        <div class="stat-mini">
          <span class="stat-label">需人工</span>
          <span class="stat-value primary">{{ padNumber(stats.needHuman) }}</span>
        </div>
      </div>
    </div>

    <!-- 标签切换和批量操作 -->
    <div class="filter-bar">
      <div class="filter-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="handleTabChange(tab.key)"
        >
          {{ tab.label }}
        </button>
      </div>
      <div class="filter-actions">
        <el-dropdown @command="handleSort">
          <el-button :icon="Sort" class="action-btn">
            {{ sortLabel }}
            <el-icon class="el-icon--right"><ArrowDown /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="time">按提问时间排序</el-dropdown-item>
              <el-dropdown-item command="confidence">按AI置信度排序</el-dropdown-item>
              <el-dropdown-item command="priority">按紧急程度排序</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <el-button :icon="CircleCheck" class="action-btn" plain @click="handleBatchResolve">批量标记解决</el-button>
        <el-button :icon="Collection" class="action-btn" plain @click="handleBatchToKnowledge">批量转知识库</el-button>
      </div>
    </div>

    <!-- 提问列表 -->
    <div class="question-list-card">
      <div class="list-header">
        <div class="header-col checkbox-col">
          <el-checkbox v-model="selectAll" @change="handleSelectAll" />
        </div>
        <div class="header-col">提问摘要 & 标签</div>
        <div class="header-col center">年级班级</div>
        <div class="header-col center">提问时间</div>
        <div class="header-col center">AI 置信度</div>
        <div class="header-col center">状态</div>
        <div class="header-col right">快捷操作</div>
      </div>

      <div class="list-body">
        <el-skeleton :rows="5" animated v-if="loading.list" />
        <template v-else>
          <div 
            v-for="item in questionList" 
            :key="item.id"
            class="list-item"
            :class="{ 'has-ai-reply': item.status === 2 }"
          >
            <div class="item-col checkbox-col">
              <el-checkbox v-model="selectedIds" :label="item.id" />
            </div>
            <div class="item-col content-col">
              <div class="content-title">{{ item.questionSummary }}</div>
              <div class="content-tags">
                <el-tag size="small" :type="getPriorityType(item.priority)" effect="light" class="tag">
                  {{ getPriorityText(item.priority) }}
                </el-tag>
                <el-tag v-if="item.isHot" size="small" type="danger" effect="plain" class="tag hot">
                  高频
                </el-tag>
                <el-tag v-if="item.triggerType === 1" size="small" type="warning" effect="plain" class="tag">
                  需人工
                </el-tag>
              </div>
            </div>
            <div class="item-col center">
              <div class="student-info">
                <div class="student-grade">{{ item.studentGrade || '未知年级' }}</div>
                <div class="student-major">{{ item.studentMajor || '未知专业' }}</div>
              </div>
            </div>
            <div class="item-col center time-col">
              <div class="time-main">{{ formatDate(item.createdAt) }}</div>
              <div class="time-sub">{{ formatTime(item.createdAt) }}</div>
            </div>
            <div class="item-col center">
              <div class="confidence-bar">
                <div class="confidence-track">
                  <div 
                    class="confidence-fill" 
                    :style="{ width: (item.aiConfidence || 0) + '%', backgroundColor: getConfidenceColor(item.aiConfidence) }"
                  ></div>
                </div>
                <span class="confidence-text">{{ item.aiConfidence || 0 }}%</span>
              </div>
            </div>
            <div class="item-col center">
              <div class="status-badge" :class="getStatusClass(item.status)">
                <span class="status-dot"></span>
                <span>{{ getStatusText(item.status) }}</span>
              </div>
              <div v-if="item.status === 2" class="ai-reply-tag">
                <el-icon><StarFilled /></el-icon>
                AI 已答复
              </div>
            </div>
            <div class="item-col right">
              <el-button link type="primary" @click="handleViewDetail(item)">详情</el-button>
            </div>
          </div>
          <el-empty v-if="questionList.length === 0" description="暂无数据" :image-size="80" />
        </template>
      </div>

      <!-- 分页 -->
      <div class="list-footer">
        <span class="total-text">显示 {{ pagination.start }}-{{ pagination.end }} 条，共 {{ pagination.total }} 条记录</span>
        <el-pagination
          v-model:current-page="pagination.pageNum"
          :page-size="pagination.pageSize"
          :total="pagination.total"
          layout="prev, pager, next"
          background
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 底部双栏（参考图5） -->
    <div class="bottom-section">
      <!-- AI 提问聚类分析 -->
      <div class="ai-analysis-card" v-if="aiAnalysis">
        <div class="ai-header">
          <el-icon :size="24" color="#fff"><StarFilled /></el-icon>
          <span class="ai-title">AI 提问聚类分析</span>
        </div>
        <div class="ai-content">
          <p class="ai-desc">
            过去 24 小时内，共有 <strong>{{ aiAnalysis.relatedCount }}</strong> 名学生询问了关于
            <span class="highlight">"{{ aiAnalysis.topic }}"</span>的问题。
            建议更新知识库中的 <span class="highlight">"{{ aiAnalysis.knowledgeBaseEntry || '相关模块' }}"</span> 模块以减少重复咨询。
          </p>
          <div class="ai-actions">
            <el-button type="primary" class="ai-btn" @click="handleUnifiedReply">
              统一回复此聚合组
            </el-button>
            <el-button class="ai-btn-outline" text bg @click="handleViewSimilar">
              查看相似问题串
            </el-button>
          </div>
        </div>
      </div>
      <div class="ai-analysis-card" v-else>
        <div class="ai-header">
          <el-icon :size="24" color="#fff"><StarFilled /></el-icon>
          <span class="ai-title">AI 提问聚类分析</span>
        </div>
        <div class="ai-content">
          <p class="ai-desc">暂无聚类分析数据</p>
        </div>
      </div>

      <!-- 快捷处理技巧 -->
      <div class="tips-card">
        <div class="tips-header">
          <el-icon :size="20" color="#F59E0B"><InfoFilled /></el-icon>
          <span class="tips-title">快捷处理技巧</span>
        </div>
        <div class="tips-list">
          <div class="tip-item">
            <span class="tip-dot"></span>
            <span class="tip-text">使用 <kbd>Enter</kbd> 快速进入详情页查看学生具体报错截图。</span>
          </div>
          <div class="tip-item">
            <span class="tip-dot"></span>
            <span class="tip-text">勾选多条记录后点击"转知识库"，可由 AI 自动提取关键 Q&A 对。</span>
          </div>
          <div class="tip-item">
            <span class="tip-dot"></span>
            <span class="tip-text">点击 AI 置信度低于 50% 的条目，优先进行人工介入回复。</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Sort,
  ArrowDown,
  CircleCheck,
  Collection,
  StarFilled,
  InfoFilled
} from '@element-plus/icons-vue'

import {
  getQuestionStats,
  getPendingEscalations,
  getMyAssignedEscalations,
  assignEscalation,
  resolveEscalation,
  batchResolve,
  batchTransferToKnowledge,
  getAIClusterAnalysis,
  EscalationStatus,
  EscalationPriority,
  type EscalationItem,
  type QuestionStats,
  type AIClusterAnalysis
} from '@/api/questions'

const router = useRouter()

// ===== 响应式数据 =====
const selectAll = ref(false)
const selectedIds = ref<number[]>([])
const activeTab = ref('unsolved')
const sortBy = ref<'time' | 'confidence' | 'priority'>('time')

const loading = reactive({
  list: false,
  stats: false,
  action: false
})

const stats = reactive<QuestionStats>({
  totalUnsolved: 0,
  hotQuestions: 0,
  needHuman: 0,
  aiReplied: 0,
  transferred: 0
})

const questionList = ref<EscalationItem[]>([])
const aiAnalysis = ref<AIClusterAnalysis | null | undefined>(null)

interface PaginationState {
  pageNum: number
  pageSize: number
  total: number
  start: number
  end: number
}

const pagination = reactive<PaginationState>({
  pageNum: 1,
  pageSize: 10,
  total: 0,
  start: 1,
  end: 10
})

// 更新分页计算值
function updatePagination() {
  pagination.start = (pagination.pageNum - 1) * pagination.pageSize + 1
  pagination.end = Math.min(pagination.pageNum * pagination.pageSize, pagination.total)
}

// ===== 计算属性 =====
const tabs = [
  { key: 'unsolved', label: '未解决' },
  { key: 'hot', label: '高频问题' },
  { key: 'human', label: '需人工处理' },
  { key: 'kb', label: '已转知识库' }
]

const sortLabel = computed(() => {
  const labels: Record<string, string> = {
    time: '按提问时间排序',
    confidence: '按AI置信度排序',
    priority: '按紧急程度排序'
  }
  return labels[sortBy.value]
})

// ===== 辅助函数 =====
function padNumber(num: number): string {
  return String(num).padStart(2, '0')
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  const now = new Date()
  const isToday = date.toDateString() === now.toDateString()
  
  if (isToday) {
    return '今天'
  }
  return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' }).replace(/\//g, '-')
}

function formatTime(dateStr: string): string {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

function getPriorityType(priority: number): 'success' | 'warning' | 'danger' | 'info' {
  switch (priority) {
    case EscalationPriority.URGENT: return 'danger'
    case EscalationPriority.HIGH: return 'warning'
    case EscalationPriority.NORMAL: return 'success'
    case EscalationPriority.LOW: return 'info'
    default: return 'info'
  }
}

function getPriorityText(priority: number): string {
  switch (priority) {
    case EscalationPriority.URGENT: return '紧急'
    case EscalationPriority.HIGH: return '高'
    case EscalationPriority.NORMAL: return '普通'
    case EscalationPriority.LOW: return '低'
    default: return '普通'
  }
}

function getStatusClass(status: number): string {
  switch (status) {
    case EscalationStatus.PENDING: return 'pending'
    case EscalationStatus.ASSIGNED: return 'transferred'
    case EscalationStatus.RESOLVED: return 'resolved'
    case EscalationStatus.CLOSED: return 'resolved'
    default: return 'pending'
  }
}

function getStatusText(status: number): string {
  switch (status) {
    case EscalationStatus.PENDING: return '待分配'
    case EscalationStatus.ASSIGNED: return '处理中'
    case EscalationStatus.RESOLVED: return '已解决'
    case EscalationStatus.CLOSED: return '已关闭'
    default: return '未知'
  }
}

function getConfidenceColor(confidence?: number): string {
  if (!confidence) return '#EF4444'
  if (confidence > 80) return '#0D9488'
  if (confidence > 50) return '#F59E0B'
  return '#EF4444'
}

// ===== 事件处理 =====
function handleTabChange(tab: string) {
  activeTab.value = tab
  pagination.pageNum = 1
  selectedIds.value = []
  selectAll.value = false
  loadQuestionList()
}

function handleSort(command: 'time' | 'confidence' | 'priority') {
  sortBy.value = command
  loadQuestionList()
}

function handleSelectAll(val: boolean) {
  if (val) {
    selectedIds.value = questionList.value.map(item => item.id)
  } else {
    selectedIds.value = []
  }
}

function handlePageChange(page: number) {
  pagination.pageNum = page
  loadQuestionList()
}

async function handleBatchResolve() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要标记的记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定将选中的 ${selectedIds.value.length} 条记录标记为已解决？`,
      '批量操作',
      { confirmButtonText: '确认', cancelButtonText: '取消', type: 'warning' }
    )
    
    const res = await batchResolve(selectedIds.value)
    if (res.code === 200) {
      ElMessage.success('批量标记成功')
      selectedIds.value = []
      selectAll.value = false
      loadQuestionList()
      loadStats()
    }
  } catch (error) {
    // 用户取消
  }
}

async function handleBatchToKnowledge() {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要转知识库的记录')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定将选中的 ${selectedIds.value.length} 条记录转入知识库？`,
      '批量操作',
      { confirmButtonText: '确认', cancelButtonText: '取消', type: 'info' }
    )
    
    const res = await batchTransferToKnowledge(selectedIds.value)
    if (res.code === 200) {
      ElMessage.success('已转入知识库')
      selectedIds.value = []
      selectAll.value = false
      loadQuestionList()
    }
  } catch (error) {
    // 用户取消
  }
}

function handleViewDetail(item: EscalationItem) {
  // 如果工单待分配，先自动接单
  if (item.status === EscalationStatus.PENDING) {
    assignAndView(item)
  } else {
    router.push(`/questions/${item.id}`)
  }
}

async function assignAndView(item: EscalationItem) {
  loading.action = true
  try {
    const res = await assignEscalation(item.id)
    if (res.code === 200) {
      ElMessage.success('已接单')
      router.push(`/questions/${item.id}`)
    }
  } catch (error) {
    console.error('接单失败:', error)
  } finally {
    loading.action = false
  }
}

function handleUnifiedReply() {
  ElMessage.info('功能开发中：统一回复聚合组')
}

function handleViewSimilar() {
  ElMessage.info('功能开发中：查看相似问题串')
}

// ===== 数据加载 =====
async function loadStats() {
  loading.stats = true
  try {
    const res = await getQuestionStats()
    if (res.code === 200 && res.data) {
      Object.assign(stats, res.data)
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  } finally {
    loading.stats = false
  }
}

async function loadQuestionList() {
  loading.list = true
  try {
    let res
    const params = { 
      pageNum: pagination.pageNum, 
      pageSize: pagination.pageSize 
    }
    
    // 根据标签筛选
    switch (activeTab.value) {
      case 'unsolved':
        res = await getPendingEscalations(params)
        break
      case 'human':
        res = await getMyAssignedEscalations(EscalationStatus.ASSIGNED, params)
        break
      default:
        res = await getPendingEscalations(params)
    }
    
    if (res.code === 200 && res.data) {
      questionList.value = res.data.rows || []
      pagination.total = res.data.total || 0
      updatePagination()
    }
  } catch (error) {
    console.error('加载提问列表失败:', error)
  } finally {
    loading.list = false
  }
}

async function loadAIAnalysis() {
  try {
    const res = await getAIClusterAnalysis()
    if (res.code === 200 && res.data && res.data.length > 0) {
      aiAnalysis.value = res.data[0]
    }
  } catch (error) {
    console.error('加载AI分析失败:', error)
  }
}

// ===== 生命周期 =====
onMounted(() => {
  loadStats()
  loadQuestionList()
  loadAIAnalysis()
})
</script>

<style scoped lang="scss">
.questions-page {
  max-width: 1400px;
  margin: 0 auto;
}

// ========================================
// 页面头部
// ========================================
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;

  .header-left {
    .page-title {
      font-size: 24px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 10px;
    }

    .page-desc {
      font-size: 14px;
      color: var(--text-secondary);
      line-height: 1.6;
      max-width: 600px;

      strong {
        color: var(--primary-color);
        font-weight: 600;
      }
    }
  }

  .header-stats {
    display: flex;
    gap: 16px;
  }

  .stat-mini {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 12px 20px;
    background: #fff;
    border-radius: var(--radius-lg);
    box-shadow: var(--card-shadow);
    border: 1px solid var(--card-border);
    min-width: 70px;

    .stat-label {
      font-size: 12px;
      color: var(--text-tertiary);
    }

    .stat-value {
      font-size: 28px;
      font-weight: 700;

      &.warning {
        color: #0D9488;
      }

      &.danger {
        color: #F59E0B;
      }

      &.primary {
        color: #EF4444;
      }
    }
  }
}

// ========================================
// 筛选栏
// ========================================
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;

  .filter-tabs {
    display: flex;
    gap: 4px;
  }

  .tab-btn {
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    background: #fff;
    border: 1px solid var(--card-border);
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-fast);

    &:hover {
      color: var(--primary-color);
      border-color: var(--primary-color);
    }

    &.active {
      color: #fff;
      background: var(--primary-color);
      border-color: var(--primary-color);
    }
  }

  .filter-actions {
    display: flex;
    gap: 10px;

    .action-btn {
      border-radius: var(--radius-md);
    }
  }
}

// ========================================
// 提问列表卡片
// ========================================
.question-list-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: 24px;
  overflow: hidden;
}

.list-header {
  display: grid;
  grid-template-columns: 40px 2fr 120px 100px 120px 100px 80px;
  align-items: center;
  padding: 14px 20px;
  background: #F8FAFC;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  border-bottom: 1px solid var(--card-border);

  .header-col {
    &.center {
      text-align: center;
    }

    &.right {
      text-align: right;
    }
  }
}

.list-body {
  .list-item {
    display: grid;
    grid-template-columns: 40px 2fr 120px 100px 120px 100px 80px;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #F1F5F9;
    transition: all var(--transition-fast);

    &:hover {
      background-color: #F8FAFC;
    }

    &:last-child {
      border-bottom: none;
    }

    &.has-ai-reply {
      background: linear-gradient(90deg, #F0FDFA 0%, #fff 3%);
    }
  }

  .item-col {
    &.center {
      text-align: center;
    }

    &.right {
      text-align: right;
    }
  }

  .content-col {
    .content-title {
      font-size: 14px;
      font-weight: 500;
      color: var(--text-primary);
      margin-bottom: 8px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .content-tags {
      display: flex;
      gap: 6px;

      .tag {
        font-weight: 500;

        &.hot {
          border-color: #FECACA;
        }
      }
    }
  }

  .student-info {
    .student-grade {
      font-size: 13px;
      color: var(--text-primary);
      font-weight: 500;
    }

    .student-major {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }

  .time-col {
    .time-main {
      font-size: 13px;
      color: var(--text-primary);
      font-weight: 500;
    }

    .time-sub {
      font-size: 12px;
      color: var(--text-tertiary);
    }
  }

  .confidence-bar {
    display: flex;
    align-items: center;
    gap: 8px;

    .confidence-track {
      flex: 1;
      height: 4px;
      background: #E2E8F0;
      border-radius: 2px;
      overflow: hidden;
    }

    .confidence-fill {
      height: 100%;
      border-radius: 2px;
      transition: width 0.3s ease;
    }

    .confidence-text {
      font-size: 12px;
      font-weight: 600;
      color: var(--text-secondary);
      min-width: 32px;
    }
  }

  .status-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 500;
    padding: 4px 10px;
    border-radius: 12px;
    margin-bottom: 4px;

    &.pending {
      color: #F59E0B;
      background: #FFFBEB;
    }

    &.transferred {
      color: var(--text-tertiary);
      background: #F1F5F9;
    }

    &.resolved,
    &.ai-replied {
      color: var(--success);
      background: #ECFDF5;
    }

    .status-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: currentColor;
    }
  }

  .ai-reply-tag {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    color: var(--primary-color);
    font-weight: 500;
  }
}

.list-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-top: 1px solid var(--card-border);
  background: #F8FAFC;

  .total-text {
    font-size: 13px;
    color: var(--text-secondary);
  }
}

// ========================================
// 底部双栏
// ========================================
.bottom-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
}

.ai-analysis-card {
  background: linear-gradient(135deg, #0D9488 0%, #0F766E 100%);
  border-radius: var(--radius-lg);
  padding: 24px;
  color: #fff;

  .ai-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;

    .ai-title {
      font-size: 18px;
      font-weight: 600;
    }
  }

  .ai-desc {
    font-size: 14px;
    line-height: 1.8;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 20px;

    strong {
      color: #fff;
      font-weight: 700;
    }

    .highlight {
      color: #5EEAD4;
      font-weight: 600;
    }
  }

  .ai-actions {
    display: flex;
    gap: 12px;

    .ai-btn {
      background: #fff;
      color: var(--primary-color);
      border: none;
      font-weight: 600;

      &:hover {
        background: rgba(255, 255, 255, 0.95);
      }
    }

    .ai-btn-outline {
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
      background: rgba(255, 255, 255, 0.1);

      &:hover {
        background: rgba(255, 255, 255, 0.2);
      }
    }
  }
}

.tips-card {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  padding: 20px;

  .tips-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 16px;

    .tips-title {
      font-size: 15px;
      font-weight: 600;
      color: var(--text-primary);
    }
  }

  .tips-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .tip-item {
    display: flex;
    gap: 10px;
    align-items: flex-start;

    .tip-dot {
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--primary-color);
      margin-top: 6px;
      flex-shrink: 0;
    }

    .tip-text {
      font-size: 13px;
      color: var(--text-secondary);
      line-height: 1.6;

      kbd {
        display: inline-block;
        padding: 2px 6px;
        font-family: monospace;
        font-size: 12px;
        background: #F1F5F9;
        border: 1px solid #E2E8F0;
        border-radius: 4px;
        box-shadow: 0 1px 0 #E2E8F0;
      }
    }
  }
}

// 响应式
@media (max-width: 1200px) {
  .page-header {
    flex-direction: column;
    gap: 20px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .list-header,
  .list-body .list-item {
    grid-template-columns: 40px 2fr 100px 80px;

    .item-col:nth-child(5),
    .header-col:nth-child(6) {
      display: none;
    }
  }

  .bottom-section {
    grid-template-columns: 1fr;
  }
}
</style>
