<template>
  <div class="analytics-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title font-display">数据看板</h1>
        <p class="page-desc">查看学院各项指标的实时数据与趋势分析</p>
      </div>
      <div class="header-right">
        <el-select v-model="timeRange" class="time-select" placeholder="时间范围">
          <el-option label="最近 7 天" value="7days" />
          <el-option label="最近 30 天" value="30days" />
          <el-option label="本学期" value="semester" />
        </el-select>
        <el-button type="primary" :icon="Download" class="export-btn">
          导出报告
        </el-button>
      </div>
    </div>

    <!-- 统计卡片（带更多动效） -->
    <div class="stats-row">
      <div class="stat-card hover-lift">
        <div class="stat-icon primary">
          <el-icon :size="22"><User /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">活跃学生数</p>
          <h3 class="stat-value font-display">2,845</h3>
        </div>
        <div class="stat-badge success">
          <el-icon><Top /></el-icon>
          <span>+12.5%</span>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-icon secondary">
          <el-icon :size="22"><Cpu /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">系统处理总量</p>
          <h3 class="stat-value font-display">14,230</h3>
        </div>
        <div class="stat-badge success">
          <el-icon><Top /></el-icon>
          <span>+5.2%</span>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-icon tertiary">
          <el-icon :size="22"><Timer /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">平均解决时长</p>
          <h3 class="stat-value font-display">3.2<span class="unit">小时</span></h3>
        </div>
        <div class="stat-badge error">
          <el-icon><Bottom /></el-icon>
          <span>-2.1%</span>
        </div>
      </div>

      <div class="stat-card hover-lift">
        <div class="stat-icon quaternary">
          <el-icon :size="22"><TrendCharts /></el-icon>
        </div>
        <div class="stat-content">
          <p class="stat-label">知识库命中率</p>
          <h3 class="stat-value font-display">89.4%</h3>
        </div>
        <div class="stat-badge success">
          <el-icon><Top /></el-icon>
          <span>+18.4%</span>
        </div>
      </div>
    </div>

    <!-- 图表区域（使用 ECharts 真实图表） -->
    <div class="charts-row">
      <!-- 提问与解决趋势 - 面积图 -->
      <div class="chart-card large hover-lift">
        <div class="chart-header">
          <h3 class="chart-title font-display">提问与解决趋势</h3>
          <div class="chart-legend">
            <span class="legend-item">
              <span class="dot primary"></span>
              新增提问
            </span>
            <span class="legend-item">
              <span class="dot secondary"></span>
              已解决
            </span>
          </div>
        </div>
        <div class="chart-body">
          <v-chart class="chart" :option="areaChartOption" autoresize />
        </div>
      </div>

      <!-- 各类审批申请量 - 柱状图 -->
      <div class="chart-card hover-lift">
        <div class="chart-header">
          <h3 class="chart-title font-display">各类审批申请量</h3>
        </div>
        <div class="chart-body">
          <v-chart class="chart" :option="barChartOption" autoresize />
        </div>
      </div>
    </div>

    <!-- 问题类型分布 -->
    <div class="charts-row">
      <div class="chart-card hover-lift">
        <div class="chart-header">
          <h3 class="chart-title font-display">问题类型分布</h3>
        </div>
        <div class="chart-body">
          <v-chart class="chart pie-chart" :option="pieChartOption" autoresize />
        </div>
      </div>

      <!-- 高频问题排行 -->
      <div class="content-card hover-lift">
        <div class="card-header">
          <h3 class="card-title font-display">
            <el-icon><Histogram /></el-icon>
            高频问题排行
          </h3>
          <el-link type="primary" underline="never">查看全部</el-link>
        </div>
        <div class="card-body">
          <div class="rank-list">
            <div class="rank-item" v-for="(item, index) in rankData" :key="index">
              <div class="rank-info">
                <span class="rank-name">{{ item.name }}</span>
                <span class="rank-count">{{ item.count }} 次</span>
              </div>
              <div class="rank-bar">
                <div class="rank-fill" :style="{ width: item.percent + '%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 审批状态统计 -->
      <div class="content-card hover-lift">
        <div class="card-header">
          <h3 class="card-title font-display">
            <el-icon><Checked /></el-icon>
            本周审批状态
          </h3>
        </div>
        <div class="card-body">
          <div class="approval-stats">
            <div class="approval-item">
              <div class="approval-icon approved">
                <el-icon><CircleCheck /></el-icon>
              </div>
              <div class="approval-info">
                <span class="approval-label">已通过</span>
                <span class="approval-value">156</span>
              </div>
            </div>
            <div class="approval-item">
              <div class="approval-icon pending">
                <el-icon><Clock /></el-icon>
              </div>
              <div class="approval-info">
                <span class="approval-label">待审批</span>
                <span class="approval-value">42</span>
              </div>
            </div>
            <div class="approval-item">
              <div class="approval-icon rejected">
                <el-icon><CircleClose /></el-icon>
              </div>
              <div class="approval-info">
                <span class="approval-label">已驳回</span>
                <span class="approval-value">18</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  User,
  Cpu,
  Timer,
  TrendCharts,
  Top,
  Bottom,
  Download,
  Histogram,
  Checked,
  CircleCheck,
  Clock,
  CircleClose
} from '@element-plus/icons-vue'

const timeRange = ref('7days')

// 面积图配置
const areaChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#e0e3e5',
    borderWidth: 1,
    textStyle: { color: '#191c1e', fontSize: 13 },
    padding: [12, 16],
    borderRadius: 12,
    boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
  },
  legend: {
    show: false
  },
  grid: {
    left: 0,
    right: 20,
    bottom: 0,
    top: 20,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748b', fontSize: 12, margin: 14 }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748b', fontSize: 12 },
    splitLine: { lineStyle: { type: 'dashed', color: '#e0e3e5' } }
  },
  series: [
    {
      name: '新增提问',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { width: 3, color: '#00685f' },
      itemStyle: { color: '#00685f', borderWidth: 2, borderColor: '#fff' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(0, 104, 95, 0.3)' },
            { offset: 1, color: 'rgba(0, 104, 95, 0)' }
          ]
        }
      },
      data: [40, 30, 20, 27, 18, 23, 34]
    },
    {
      name: '已解决',
      type: 'line',
      smooth: true,
      symbol: 'circle',
      symbolSize: 8,
      lineStyle: { width: 3, color: '#008378' },
      itemStyle: { color: '#008378', borderWidth: 2, borderColor: '#fff' },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(0, 131, 120, 0.3)' },
            { offset: 1, color: 'rgba(0, 131, 120, 0)' }
          ]
        }
      },
      data: [38, 28, 18, 25, 16, 21, 30]
    }
  ]
}))

// 柱状图配置
const barChartOption = computed(() => ({
  tooltip: {
    trigger: 'axis',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#e0e3e5',
    borderWidth: 1,
    textStyle: { color: '#191c1e', fontSize: 13 },
    padding: [12, 16],
    borderRadius: 12,
    boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
  },
  grid: {
    left: 0,
    right: 10,
    bottom: 0,
    top: 20,
    containLabel: true
  },
  xAxis: {
    type: 'category',
    data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748b', fontSize: 12, margin: 14 }
  },
  yAxis: {
    type: 'value',
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: { color: '#64748b', fontSize: 12 },
    splitLine: { lineStyle: { type: 'dashed', color: '#e0e3e5' } }
  },
  series: [{
    name: '审批申请数',
    type: 'bar',
    barWidth: 24,
    itemStyle: {
      color: '#924628',
      borderRadius: [4, 4, 0, 0]
    },
    data: [24, 13, 98, 39, 48, 38, 43]
  }]
}))

// 饼图配置
const pieChartOption = computed(() => ({
  tooltip: {
    trigger: 'item',
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderColor: '#e0e3e5',
    borderWidth: 1,
    textStyle: { color: '#191c1e', fontSize: 13 },
    padding: [12, 16],
    borderRadius: 12,
    boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
  },
  legend: {
    orient: 'vertical',
    right: 20,
    top: 'center',
    itemGap: 16,
    textStyle: { color: '#475569', fontSize: 13 }
  },
  series: [{
    name: '问题类型',
    type: 'pie',
    radius: ['50%', '70%'],
    center: ['35%', '50%'],
    avoidLabelOverlap: false,
    itemStyle: {
      borderRadius: 8,
      borderColor: '#fff',
      borderWidth: 2
    },
    label: {
      show: false
    },
    emphasis: {
      label: {
        show: true,
        fontSize: 14,
        fontWeight: 'bold'
      }
    },
    data: [
      { value: 45, name: '教务相关', itemStyle: { color: '#00685f' } },
      { value: 30, name: '技术故障', itemStyle: { color: '#008378' } },
      { value: 15, name: '后勤申报', itemStyle: { color: '#14b8a6' } },
      { value: 10, name: '其他', itemStyle: { color: '#5eead4' } }
    ]
  }]
}))

const rankData = [
  { name: '奖学金评定政策', count: 342, percent: 85 },
  { name: '选课时间安排', count: 215, percent: 65 },
  { name: '宿舍调换申请', count: 188, percent: 45 },
  { name: '学分查询路径', count: 102, percent: 30 }
]
</script>

<style scoped lang="scss">
.analytics-page {
  max-width: 1400px;
  margin: 0 auto;
}

// ========================================
// 页面头部
// ========================================
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 28px;

  .header-left {
    .page-title {
      font-size: 26px;
      font-weight: 800;
      color: var(--on-surface);
      margin-bottom: 6px;
      letter-spacing: -0.02em;
    }

    .page-desc {
      font-size: 14px;
      color: var(--text-secondary);
    }
  }

  .header-right {
    display: flex;
    gap: 12px;

    .time-select {
      width: 140px;
    }

    .export-btn {
      border-radius: var(--radius-md);
      font-weight: 600;
    }
  }
}

// ========================================
// 统计卡片（学习对方动效）
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
  align-items: center;
  gap: 16px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    &.primary {
      background: rgba(0, 104, 95, 0.1);
      color: var(--primary-color);
    }

    &.secondary {
      background: rgba(0, 106, 99, 0.1);
      color: var(--secondary);
    }

    &.tertiary {
      background: rgba(146, 70, 40, 0.1);
      color: var(--tertiary);
    }

    &.quaternary {
      background: rgba(13, 148, 136, 0.1);
      color: var(--primary-light);
    }
  }

  .stat-content {
    flex: 1;

    .stat-label {
      font-size: 13px;
      color: var(--text-secondary);
      font-weight: 500;
      margin-bottom: 4px;
    }

    .stat-value {
      font-size: 28px;
      font-weight: 800;
      color: var(--on-surface);
      letter-spacing: -0.02em;

      .unit {
        font-size: 14px;
        font-weight: 500;
        color: var(--text-secondary);
        margin-left: 4px;
      }
    }
  }

  .stat-badge {
    display: flex;
    align-items: center;
    gap: 4px;
    font-size: 12px;
    font-weight: 600;
    padding: 4px 10px;
    border-radius: 20px;

    &.success {
      color: var(--success);
      background: var(--success-bg);
    }

    &.error {
      color: var(--error);
      background: var(--error-container);
    }

    .el-icon {
      font-size: 12px;
    }
  }
}

// ========================================
// 图表区域
// ========================================
.charts-row {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;

  &:last-child {
    grid-template-columns: 1fr 1fr 1fr;
  }
}

.chart-card {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 24px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  transition: all var(--transition-normal);

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--card-shadow-hover);
  }

  &.large {
    min-height: 400px;
  }

  .chart-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 20px;

    .chart-title {
      font-size: 16px;
      font-weight: 700;
      color: var(--on-surface);
    }

    .chart-legend {
      display: flex;
      gap: 16px;

      .legend-item {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        color: var(--text-secondary);

        .dot {
          width: 8px;
          height: 8px;
          border-radius: 50%;

          &.primary {
            background: var(--primary-color);
          }

          &.secondary {
            background: var(--primary-container);
          }
        }
      }
    }
  }

  .chart-body {
    height: 300px;

    .chart {
      width: 100%;
      height: 100%;
    }

    .pie-chart {
      height: 260px;
    }
  }
}

// ========================================
// 内容卡片
// ========================================
.content-card {
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
    padding: 20px 24px;
    border-bottom: 1px solid var(--surface-highest);

    .card-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 15px;
      font-weight: 700;
      color: var(--on-surface);

      .el-icon {
        color: var(--primary-color);
      }
    }
  }

  .card-body {
    padding: 20px 24px;
  }
}

// 排行列表
.rank-list {
  display: flex;
  flex-direction: column;
  gap: 18px;

  .rank-item {
    .rank-info {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;

      .rank-name {
        font-size: 14px;
        color: var(--text-primary);
        font-weight: 500;
      }

      .rank-count {
        font-size: 13px;
        color: var(--text-secondary);
        font-weight: 600;
      }
    }

    .rank-bar {
      height: 6px;
      background: var(--surface-low);
      border-radius: 3px;
      overflow: hidden;

      .rank-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-color) 0%, var(--primary-container) 100%);
        border-radius: 3px;
        transition: width 0.6s ease;
      }
    }
  }
}

// 审批状态统计
.approval-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;

  .approval-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px;
    background: var(--surface-low);
    border-radius: var(--radius-md);
    transition: all var(--transition-fast);

    &:hover {
      background: var(--surface-high);
    }

    .approval-icon {
      width: 44px;
      height: 44px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;

      &.approved {
        background: var(--success-bg);
        color: var(--success);
      }

      &.pending {
        background: #fffbeb;
        color: #f59e0b;
      }

      &.rejected {
        background: var(--error-container);
        color: var(--error);
      }
    }

    .approval-info {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: space-between;

      .approval-label {
        font-size: 14px;
        color: var(--text-secondary);
      }

      .approval-value {
        font-size: 20px;
        font-weight: 700;
        color: var(--on-surface);
        font-family: var(--font-display);
      }
    }
  }
}

// 响应式
@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: 1fr;

    &:last-child {
      grid-template-columns: 1fr;
    }
  }

  .stats-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-row {
    grid-template-columns: 1fr;
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
