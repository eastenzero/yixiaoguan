<template>
  <div class="approval-page">
    <!-- 统计卡片（参考图2） -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon blue">
          <el-icon :size="22"><OfficeBuilding /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.pendingCount }}</div>
          <div class="stat-label">待审批教室</div>
          <div v-if="stats.urgentCount > 0" class="stat-alert">
            <el-icon><WarningFilled /></el-icon>
            <span>{{ stats.urgentCount }}个申请即将超时</span>
          </div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon orange">
          <el-icon :size="22"><Timer /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.todayApproved }}</div>
          <div class="stat-label">今日已审批</div>
          <div class="stat-trend">
            <el-icon><Top /></el-icon>
            <span>较昨日 {{ formatGrowth(stats.todayApprovedGrowth) }}</span>
          </div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">
          <el-icon :size="22"><CircleCheck /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.monthlyApproved }}</div>
          <div class="stat-label">本月通过</div>
          <div class="stat-desc">通过率 {{ stats.monthlyApprovalRate }}%</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">
          <el-icon :size="22"><Calendar /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.weeklyTotal }}</div>
          <div class="stat-label">本周申请</div>
          <div class="stat-desc">日均 {{ stats.weeklyAverage }} 个申请</div>
        </div>
      </div>
    </div>

    <!-- 审批列表（参考图1 + 图2） -->
    <div class="approval-section">
      <div class="section-tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.key"
          class="tab-btn"
          :class="{ active: activeTab === tab.key }"
          @click="handleTabChange(tab.key)"
        >
          {{ tab.label }}
          <span v-if="tab.count !== undefined" class="tab-count">{{ tab.count }}</span>
        </button>
      </div>

      <div class="approval-content">
        <!-- 左侧申请列表 -->
        <div class="approval-list">
          <el-skeleton :rows="5" animated v-if="loading.list" />
          <template v-else>
            <div 
              v-for="(item, index) in approvalList" 
              :key="item.id"
              class="approval-card"
              :class="{ active: selectedId === item.id, urgent: item.isUrgent }"
              @click="selectItem(item)"
            >
              <div class="card-header-row">
                <span class="request-id">单号：{{ formatRequestId(item.id) }}</span>
                <el-tag :type="getStatusType(item.status)" size="small" effect="light">
                  {{ getStatusText(item.status) }}
                </el-tag>
              </div>
              <h4 class="request-title">{{ item.title || '空教室申请' }}</h4>
              <div class="request-meta">
                <div class="meta-row">
                  <span class="meta-label">申请人</span>
                  <span class="meta-value">{{ item.applicantName }}</span>
                </div>
                <div class="meta-row">
                  <span class="meta-label">联系电话</span>
                  <span class="meta-value">{{ maskPhone(item.contactPhone) }}</span>
                </div>
                <div class="meta-row">
                  <span class="meta-label">使用时间</span>
                  <span class="meta-value highlight">{{ formatTimeRange(item) }}</span>
                </div>
                <div class="meta-row">
                  <span class="meta-label">教室</span>
                  <span class="meta-value">{{ item.building }} {{ item.roomNumber }}</span>
                </div>
              </div>
              <div v-if="item.isUrgent" class="urgent-badge">
                <el-icon><AlarmClock /></el-icon>
                即将超时
              </div>
            </div>
            <el-empty v-if="approvalList.length === 0" description="暂无数据" :image-size="80" />
          </template>
        </div>

        <!-- 右侧详情（参考图1） -->
        <div class="approval-detail" v-if="selectedItem">
          <div class="detail-header">
            <span class="detail-id">单号：{{ formatRequestId(selectedItem.id) }}</span>
            <el-tag :type="getStatusType(selectedItem.status)" effect="light">
              {{ getStatusText(selectedItem.status) }}
            </el-tag>
          </div>
          <h2 class="detail-title">{{ selectedItem.title || '空教室使用申请' }}</h2>
          <div class="detail-time">
            提交时间 {{ formatDateTime(selectedItem.createdAt) }}
          </div>

          <div class="detail-grid">
            <!-- 申请人信息 -->
            <div class="info-card">
              <div class="card-title">
                <el-icon><User /></el-icon>
                申请人信息
              </div>
              <div class="applicant-profile">
                <el-avatar :size="48" :style="{ backgroundColor: '#8B5CF6' }">
                  {{ selectedItem.applicantName?.charAt(0) || '?' }}
                </el-avatar>
                <div class="profile-info">
                  <div class="profile-name">{{ selectedItem.applicantName }}</div>
                  <div class="profile-dept">申请人</div>
                </div>
              </div>
              <div class="info-list">
                <div class="info-item">
                  <span class="info-label">学号</span>
                  <span class="info-value">{{ selectedItem.applicantId }}</span>
                </div>
                <div class="info-item">
                  <span class="info-label">联系电话</span>
                  <span class="info-value">{{ selectedItem.contactPhone }}</span>
                </div>
              </div>
            </div>

            <!-- 使用需求 -->
            <div class="info-card">
              <div class="card-title">
                <el-icon><OfficeBuilding /></el-icon>
                使用需求
              </div>
              <div class="demand-grid">
                <div class="demand-item">
                  <div class="demand-label">预期人数</div>
                  <div class="demand-value">{{ selectedItem.attendeeCount }} 人</div>
                </div>
                <div class="demand-item">
                  <div class="demand-label">教室</div>
                  <div class="demand-value highlight">{{ selectedItem.building }} {{ selectedItem.roomNumber }}</div>
                </div>
              </div>
              <div class="demand-note">
                <el-icon><Document /></el-icon>
                <span>{{ selectedItem.purpose || '无特殊需求' }}</span>
              </div>
            </div>

            <!-- 时段安排 -->
            <div class="info-card full-width">
              <div class="card-title">
                <el-icon><Calendar /></el-icon>
                时段安排
              </div>
              <div class="schedule-content">
                <div class="schedule-main">
                  <div class="schedule-date">
                    <div class="date-day">{{ formatDate(selectedItem.applyDate) }}</div>
                    <div class="date-week">{{ formatWeekday(selectedItem.applyDate) }}</div>
                  </div>
                  <div class="schedule-time">
                    <div class="time-range">{{ formatTime(selectedItem.startTime) }} - {{ formatTime(selectedItem.endTime) }}</div>
                    <div class="time-note">申请使用时段</div>
                  </div>
                </div>
                <div class="schedule-location">
                  <el-icon><Location /></el-icon>
                  <div>
                    <div class="location-label">教室位置</div>
                    <div class="location-value">{{ selectedItem.building }} {{ selectedItem.roomNumber }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 申请用途详情 -->
            <div class="info-card full-width">
              <div class="card-title">
                <el-icon><Document /></el-icon>
                申请用途详情
              </div>
              <div class="purpose-content">
                <p>{{ selectedItem.purpose || '申请人未填写详细用途' }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="approval-detail empty" v-else>
          <el-empty description="请选择申请查看详情" :image-size="120" />
        </div>

        <!-- 右侧审批决策 -->
        <div class="approval-action" v-if="selectedItem?.status === 0">
          <div class="action-title">
            <el-icon><Edit /></el-icon>
            审批决策
          </div>
          <div class="action-form">
            <div class="form-label">审批意见（选填）</div>
            <el-input
              v-model="approvalComment"
              type="textarea"
              :rows="4"
              placeholder="请输入您的审批意见或修改建议..."
              class="comment-input"
            />
          </div>
          <el-button 
            type="primary" 
            size="large" 
            class="approve-btn"
            :loading="loading.action"
            @click="handleApprove"
          >
            <el-icon><CircleCheck /></el-icon>
            同意申请
          </el-button>
          <div class="action-secondary">
            <el-button class="secondary-btn" :loading="loading.action">
              <el-icon><ChatDotRound /></el-icon>
              要求补充
            </el-button>
            <el-button class="secondary-btn" type="danger" plain :loading="loading.action" @click="handleReject">
              <el-icon><CircleClose /></el-icon>
              驳回
            </el-button>
          </div>

          <!-- 审批提示 -->
          <div class="approval-tip">
            <div class="tip-header">
              <el-icon color="#F59E0B"><WarningFilled /></el-icon>
              <span>审批提示</span>
            </div>
            <p>此教室在该时段暂无排课冲突。</p>
            <p v-if="selectedItem.attendeeCount > 40">请注意该申请人数量接近教室容量上限。</p>
          </div>

          <!-- 教室今日状态 -->
          <div class="room-status">
            <div class="status-title">教室今日状态 ({{ selectedItem.building }}-{{ selectedItem.roomNumber }})</div>
            <div class="status-list">
              <div class="status-item">
                <span class="time">08:00-11:45</span>
                <el-tag size="small" type="info" effect="light">有课</el-tag>
              </div>
              <div class="status-item">
                <span class="time">12:00-13:30</span>
                <el-tag size="small" type="success" effect="light">空闲</el-tag>
              </div>
              <div class="status-item current">
                <span class="time">{{ formatTime(selectedItem.startTime) }}-{{ formatTime(selectedItem.endTime) }}</span>
                <el-tag size="small" type="warning" effect="light">当前申请</el-tag>
              </div>
            </div>
          </div>
        </div>
        <div class="approval-action disabled" v-else-if="selectedItem">
          <div class="action-title">
            <el-icon><CircleCheck /></el-icon>
            审批完成
          </div>
          <div class="completed-status">
            <el-result
              :icon="selectedItem.status === 1 ? 'success' : 'error'"
              :title="selectedItem.status === 1 ? '已通过' : '已驳回'"
              :sub-title="selectedItem.remark || '无审批意见'"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  OfficeBuilding,
  Timer,
  CircleCheck,
  Calendar,
  WarningFilled,
  Top,
  User,
  Location,
  Document,
  Edit,
  ChatDotRound,
  CircleClose,
  AlarmClock
} from '@element-plus/icons-vue'

import {
  getApprovalStats,
  getApprovalList,
  approveApplication,
  rejectApplication,
  ApprovalStatus,
  type ClassroomApplication,
  type ApprovalStats
} from '@/api/approval'

// ===== 响应式数据 =====
const activeTab = ref('pending')
const selectedId = ref<number | null>(null)
const approvalComment = ref('')

const loading = reactive({
  list: false,
  stats: false,
  action: false
})

const stats = reactive<ApprovalStats>({
  pendingCount: 0,
  urgentCount: 0,
  todayApproved: 0,
  todayApprovedGrowth: 0,
  monthlyApproved: 0,
  monthlyApprovalRate: 0,
  weeklyTotal: 0,
  weeklyAverage: 0
})

const approvalList = ref<ClassroomApplication[]>([])

// ===== 计算属性 =====
const tabs = computed(() => [
  { key: 'pending', label: '待审批', count: stats.pendingCount },
  { key: 'approved', label: '已通过', count: undefined },
  { key: 'rejected', label: '已驳回', count: undefined }
])

const selectedItem = computed<ClassroomApplication | null>(() => {
  if (!selectedId.value) return null
  return approvalList.value.find(item => item.id === selectedId.value) || null
})

// ===== 辅助函数 =====
function formatRequestId(id?: number): string {
  return id ? `REQ-${String(id).padStart(6, '0')}` : 'REQ-000000'
}

function formatGrowth(growth: number): string {
  const sign = growth >= 0 ? '+' : ''
  return `${sign}${growth}`
}

function maskPhone(phone: string): string {
  if (!phone) return '--'
  return phone.replace(/(\d{3})\d{4}(\d{4})/, '$1****$2')
}

function formatTimeRange(item: ClassroomApplication): string {
  if (!item.applyDate) return '--'
  const date = formatDate(item.applyDate)
  const start = formatTime(item.startTime)
  const end = formatTime(item.endTime)
  return `${date} ${start}-${end}`
}

function formatDate(dateStr: string): string {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' }).replace(/\//g, '-')
}

function formatTime(timeStr: string): string {
  if (!timeStr) return '--'
  // 处理 HH:mm:ss 格式
  return timeStr.substring(0, 5)
}

function formatWeekday(dateStr?: string): string {
  if (!dateStr) return ''
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  const date = new Date(dateStr)
  return weekdays[date.getDay()] || ''
}

function formatDateTime(dateStr: string): string {
  if (!dateStr) return '--'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  }).replace(/\//g, '-')
}

function getStatusType(status: number): 'success' | 'warning' | 'danger' | 'info' {
  switch (status) {
    case ApprovalStatus.APPROVED: return 'success'
    case ApprovalStatus.PENDING: return 'warning'
    case ApprovalStatus.REJECTED: return 'danger'
    case ApprovalStatus.CANCELLED: return 'info'
    default: return 'info'
  }
}

function getStatusText(status: number): string {
  switch (status) {
    case ApprovalStatus.PENDING: return '待审批'
    case ApprovalStatus.APPROVED: return '已通过'
    case ApprovalStatus.REJECTED: return '已驳回'
    case ApprovalStatus.CANCELLED: return '已取消'
    case ApprovalStatus.EXPIRED: return '已过期'
    default: return '未知'
  }
}

// ===== 事件处理 =====
function handleTabChange(tab: string) {
  activeTab.value = tab
  selectedId.value = null
  loadApprovalList()
}

function selectItem(item: ClassroomApplication) {
  selectedId.value = item.id
  approvalComment.value = ''
}

async function handleApprove() {
  if (!selectedItem.value) return
  
  loading.action = true
  try {
    const res = await approveApplication(selectedItem.value.id, approvalComment.value)
    if (res.code === 200) {
      ElMessage.success('审批通过')
      // 更新本地状态
      selectedItem.value.status = ApprovalStatus.APPROVED
      selectedItem.value.remark = approvalComment.value
      // 刷新列表
      loadApprovalList()
      loadStats()
    }
  } catch (error) {
    console.error('审批失败:', error)
  } finally {
    loading.action = false
  }
}

async function handleReject() {
  if (!selectedItem.value) return
  
  const { value: reason } = await ElMessageBox.prompt(
    '请输入驳回原因',
    '驳回申请',
    {
      confirmButtonText: '确认驳回',
      cancelButtonText: '取消',
      inputPattern: /\S+/,
      inputErrorMessage: '请输入驳回原因',
      inputType: 'textarea',
      inputValue: approvalComment.value
    }
  ).catch(() => ({ value: null }))
  
  if (!reason) return
  
  loading.action = true
  try {
    const res = await rejectApplication(selectedItem.value.id, reason)
    if (res.code === 200) {
      ElMessage.success('已驳回申请')
      // 更新本地状态
      selectedItem.value.status = ApprovalStatus.REJECTED
      selectedItem.value.remark = reason
      // 刷新列表
      loadApprovalList()
      loadStats()
    }
  } catch (error) {
    console.error('驳回失败:', error)
  } finally {
    loading.action = false
  }
}

// ===== 数据加载 =====
async function loadStats() {
  loading.stats = true
  try {
    const res = await getApprovalStats()
    if (res.code === 200 && res.data) {
      Object.assign(stats, res.data)
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  } finally {
    loading.stats = false
  }
}

async function loadApprovalList() {
  loading.list = true
  try {
    const status = activeTab.value === 'pending' 
      ? ApprovalStatus.PENDING 
      : activeTab.value === 'approved' 
        ? ApprovalStatus.APPROVED 
        : ApprovalStatus.REJECTED
    
    const res = await getApprovalList(status, { pageSize: 20 })
    if (res.code === 200 && res.data) {
      approvalList.value = (res.data.rows || []).map(item => ({
        ...item,
        isUrgent: isUrgent(item) // 计算是否即将超时
      }))
      
      // 默认选中第一项
      if (approvalList.value.length > 0 && !selectedId.value) {
        selectedId.value = approvalList.value[0]?.id ?? null
      }
    }
  } catch (error) {
    console.error('加载申请列表失败:', error)
  } finally {
    loading.list = false
  }
}

// 判断申请是否即将超时（24小时内）
function isUrgent(item: ClassroomApplication): boolean {
  if (!item.applyDate || !item.startTime) return false
  const applyDateTime = new Date(`${item.applyDate}T${item.startTime}`)
  const now = new Date()
  const diffHours = (applyDateTime.getTime() - now.getTime()) / (1000 * 60 * 60)
  return diffHours > 0 && diffHours <= 24 && item.status === ApprovalStatus.PENDING
}

// ===== 生命周期 =====
onMounted(() => {
  loadStats()
  loadApprovalList()
})
</script>

<style scoped lang="scss">
.approval-page {
  max-width: 1600px;
  margin: 0 auto;
}

// ========================================
// 统计卡片
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
  display: flex;
  align-items: flex-start;
  gap: 16px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);

  .stat-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &.blue {
      background: #EFF6FF;
      color: #3B82F6;
    }

    &.orange {
      background: #FFF7ED;
      color: #F97316;
    }

    &.green {
      background: #ECFDF5;
      color: #10B981;
    }

    &.purple {
      background: #F5F3FF;
      color: #8B5CF6;
    }
  }

  .stat-info {
    flex: 1;
  }

  .stat-value {
    font-size: 28px;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1.2;
    margin-bottom: 4px;
  }

  .stat-label {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 8px;
  }

  .stat-alert {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: #F59E0B;
    font-weight: 500;
  }

  .stat-trend {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    color: #10B981;
    font-weight: 500;
  }

  .stat-desc {
    font-size: 12px;
    color: var(--text-tertiary);
  }
}

// ========================================
// 审批区域
// ========================================
.approval-section {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  overflow: hidden;
}

.section-tabs {
  display: flex;
  gap: 4px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--card-border);
  background: #F8FAFC;

  .tab-btn {
    padding: 8px 16px;
    font-size: 14px;
    font-weight: 500;
    color: var(--text-secondary);
    background: transparent;
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-fast);
    display: flex;
    align-items: center;
    gap: 6px;

    &:hover {
      color: var(--primary-color);
      background: rgba(139, 92, 246, 0.05);
    }

    &.active {
      color: var(--primary-color);
      background: var(--primary-bg);
      font-weight: 600;
    }

    .tab-count {
      padding: 2px 8px;
      font-size: 11px;
      color: #fff;
      background: #EF4444;
      border-radius: 10px;
    }
  }
}

.approval-content {
  display: grid;
  grid-template-columns: 320px 1fr 320px;
  min-height: 600px;
}

// 左侧列表
.approval-list {
  border-right: 1px solid var(--card-border);
  overflow-y: auto;
  max-height: 700px;
  padding: 16px;
}

.approval-card {
  padding: 16px;
  border-bottom: 1px solid #F1F5F9;
  cursor: pointer;
  transition: all var(--transition-fast);
  position: relative;
  border-radius: var(--radius-md);
  margin-bottom: 8px;

  &:hover {
    background: #F8FAFC;
  }

  &.active {
    background: var(--primary-bg);
    border-left: 3px solid var(--primary-color);
  }

  &.urgent {
    background: #FEF2F2;
  }

  .card-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;

    .request-id {
      font-size: 11px;
      color: var(--text-tertiary);
      font-family: monospace;
    }
  }

  .request-title {
    font-size: 14px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 12px;
    line-height: 1.5;
  }

  .request-meta {
    .meta-row {
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
      font-size: 12px;

      .meta-label {
        color: var(--text-tertiary);
      }

      .meta-value {
        color: var(--text-secondary);
        font-weight: 500;

        &.highlight {
          color: var(--primary-color);
        }
      }
    }
  }

  .urgent-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 11px;
    color: #EF4444;
    background: #FECACA;
    padding: 2px 8px;
    border-radius: 10px;
    font-weight: 600;
  }
}

// 中间详情
.approval-detail {
  padding: 24px;
  overflow-y: auto;
  max-height: 700px;
  background: #FAFBFC;

  &.empty {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .detail-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;

    .detail-id {
      font-size: 12px;
      color: var(--text-tertiary);
      font-family: monospace;
    }
  }

  .detail-title {
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
    line-height: 1.4;
  }

  .detail-time {
    font-size: 13px;
    color: var(--text-tertiary);
    margin-bottom: 20px;
  }

  .detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  .info-card {
    background: #fff;
    border-radius: var(--radius-md);
    padding: 16px;
    border: 1px solid var(--card-border);

    &.full-width {
      grid-column: 1 / -1;
    }

    .card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 14px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 16px;

      .el-icon {
        color: var(--primary-color);
      }
    }

    .applicant-profile {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      padding-bottom: 16px;
      border-bottom: 1px solid #F1F5F9;

      .profile-info {
        .profile-name {
          font-size: 16px;
          font-weight: 600;
          color: var(--text-primary);
          margin-bottom: 2px;
        }

        .profile-dept {
          font-size: 12px;
          color: var(--text-secondary);
        }
      }
    }

    .info-list {
      .info-item {
        display: flex;
        justify-content: space-between;
        margin-bottom: 10px;
        font-size: 13px;

        .info-label {
          color: var(--text-tertiary);
        }

        .info-value {
          color: var(--text-primary);
          font-weight: 500;
        }
      }
    }

    .demand-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;

      .demand-item {
        padding: 12px;
        background: #F8FAFC;
        border-radius: var(--radius-md);

        .demand-label {
          font-size: 12px;
          color: var(--text-tertiary);
          margin-bottom: 4px;
        }

        .demand-value {
          font-size: 18px;
          font-weight: 600;
          color: var(--text-primary);

          &.highlight {
            color: var(--primary-color);
          }
        }
      }
    }

    .demand-note {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
      color: var(--text-secondary);
      padding: 10px 12px;
      background: #F8FAFC;
      border-radius: var(--radius-md);
    }

    .schedule-content {
      display: flex;
      align-items: center;
      gap: 20px;

      .schedule-main {
        flex: 1;
        display: flex;
        gap: 24px;

        .schedule-date {
          .date-day {
            font-size: 20px;
            font-weight: 700;
            color: var(--text-primary);
          }

          .date-week {
            font-size: 13px;
            color: var(--text-tertiary);
            margin-top: 2px;
          }
        }

        .schedule-time {
          .time-range {
            font-size: 18px;
            font-weight: 600;
            color: var(--text-primary);
          }

          .time-note {
            font-size: 13px;
            color: var(--text-tertiary);
            margin-top: 2px;
          }
        }
      }

      .schedule-location {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        background: var(--primary-bg);
        border-radius: var(--radius-md);

        .el-icon {
          color: var(--primary-color);
          font-size: 20px;
        }

        .location-label {
          font-size: 12px;
          color: var(--primary-color);
        }

        .location-value {
          font-size: 16px;
          font-weight: 600;
          color: var(--primary-color);
        }
      }
    }

    .purpose-content {
      font-size: 14px;
      line-height: 1.8;
      color: var(--text-secondary);

      p {
        margin-bottom: 8px;
      }
    }
  }
}

// 右侧操作
.approval-action {
  padding: 20px;
  border-left: 1px solid var(--card-border);
  background: #fff;

  &.disabled {
    background: #F8FAFC;
  }

  .action-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
  }

  .action-form {
    margin-bottom: 16px;

    .form-label {
      font-size: 13px;
      color: var(--text-secondary);
      margin-bottom: 8px;
    }

    .comment-input {
      :deep(.el-textarea__inner) {
        border-radius: var(--radius-md);
        background: #F8FAFC;
        border-color: #E2E8F0;
      }
    }
  }

  .approve-btn {
    width: 100%;
    height: 44px;
    font-size: 15px;
    font-weight: 600;
    border-radius: var(--radius-md);
    margin-bottom: 12px;
    background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
    border: none;
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
  }

  .action-secondary {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 20px;

    .secondary-btn {
      height: 40px;
      font-weight: 500;
      border-radius: var(--radius-md);
    }
  }

  .approval-tip {
    padding: 14px;
    background: #FFFBEB;
    border-radius: var(--radius-md);
    margin-bottom: 20px;

    .tip-header {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 13px;
      font-weight: 600;
      color: #92400E;
      margin-bottom: 8px;
    }

    p {
      font-size: 12px;
      color: #A16207;
      line-height: 1.6;
      margin-bottom: 4px;
    }
  }

  .room-status {
    .status-title {
      font-size: 14px;
      font-weight: 600;
      color: var(--text-primary);
      margin-bottom: 12px;
    }

    .status-list {
      .status-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 0;
        border-bottom: 1px solid #F1F5F9;

        &.current {
          background: var(--primary-bg);
          margin: 0 -4px;
          padding: 10px;
          border-radius: var(--radius-md);
          border-bottom: none;
        }

        .time {
          font-size: 13px;
          color: var(--text-secondary);
        }
      }
    }
  }

  .completed-status {
    padding: 40px 0;
  }
}

// 响应式
@media (max-width: 1400px) {
  .approval-content {
    grid-template-columns: 280px 1fr 280px;
  }
}

@media (max-width: 1200px) {
  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }

  .approval-content {
    grid-template-columns: 1fr;
  }

  .approval-list {
    max-height: 300px;
    border-right: none;
    border-bottom: 1px solid var(--card-border);
  }

  .approval-detail {
    max-height: none;
  }

  .approval-action {
    border-left: none;
    border-top: 1px solid var(--card-border);
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .detail-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
