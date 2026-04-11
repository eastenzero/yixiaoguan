<template>
  <div class="knowledge-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">知识库管理</h1>
        <p class="page-desc">管理学术智治系统的知识条目，共 <strong>156</strong> 条知识，本周新增 <strong>12</strong> 条</p>
      </div>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索知识条目..."
          :prefix-icon="Search"
          class="search-input"
          clearable
        />
        <el-button type="primary" :icon="Plus" size="large" class="new-btn">
          新建知识条目
        </el-button>
      </div>
    </div>

    <!-- 分类标签 -->
    <div class="category-tabs">
      <button 
        v-for="cat in categories" 
        :key="cat.key"
        class="tab-btn"
        :class="{ active: activeCategory === cat.key }"
        @click="activeCategory = cat.key"
      >
        {{ cat.label }}
        <span class="count">({{ cat.count }})</span>
      </button>
    </div>

    <!-- 知识库快捷入口（参考图3） -->
    <div class="quick-access">
      <div class="access-title">
        <el-icon :size="18" color="#8B5CF6"><Collection /></el-icon>
        <span>知识库快捷入口</span>
      </div>
      <div class="access-grid">
        <div class="access-item" v-for="item in quickAccess" :key="item.name">
          <div class="access-icon" :style="{ backgroundColor: item.bgColor, color: item.color }">
            <el-icon :size="24">
              <component :is="item.icon" />
            </el-icon>
          </div>
          <span class="access-name">{{ item.name }}</span>
        </div>
      </div>
    </div>

    <!-- 知识列表 -->
    <div class="knowledge-list">
      <div class="list-header">
        <div class="header-col checkbox-col">
          <el-checkbox v-model="selectAll" />
        </div>
        <div class="header-col flex-2">知识标题</div>
        <div class="header-col center">分类</div>
        <div class="header-col center">适用对象</div>
        <div class="header-col center">浏览量</div>
        <div class="header-col center">状态</div>
        <div class="header-col right">操作</div>
      </div>

      <div class="list-body">
        <div class="list-item" v-for="(item, index) in knowledgeList" :key="index">
          <div class="item-col checkbox-col">
            <el-checkbox />
          </div>
          <div class="item-col flex-2 content-col">
            <div class="content-title">{{ item.title }}</div>
            <div class="content-tags">
              <el-tag v-if="item.tagType" size="small" :type="item.tagType" effect="light">{{ item.tag }}</el-tag>
            </div>
          </div>
          <div class="item-col center">
            <span class="category-badge">{{ item.category }}</span>
          </div>
          <div class="item-col center">
            <span class="target-text">{{ item.target }}</span>
          </div>
          <div class="item-col center">
            <div class="view-count">
              <el-icon><View /></el-icon>
              <span>{{ item.views }}</span>
            </div>
          </div>
          <div class="item-col center">
            <el-tag :type="item.statusType" size="small" effect="light">
              {{ item.status }}
            </el-tag>
          </div>
          <div class="item-col right">
            <el-button link type="primary">编辑</el-button>
            <el-button link type="danger">删除</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- AI 舆情预警卡片（参考图3） -->
    <div class="ai-warning-card">
      <div class="warning-header">
        <el-icon :size="24" color="#fff"><StarFilled /></el-icon>
        <span class="warning-title">AI 舆情预警</span>
      </div>
      <div class="warning-content">
        <p class="warning-desc">
          本周关于 <span class="highlight">"综合测评"</span> 的提问量异常上升 <strong>150%</strong>，
          建议发布统一政策说明文件。
        </p>
        <el-button type="primary" class="warning-btn" text bg>
          生成公告草稿
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Search,
  Plus,
  Collection,
  Document,
  Reading,
  ChatLineRound,
  QuestionFilled,
  View,
  StarFilled
} from '@element-plus/icons-vue'

const searchQuery = ref('')
const selectAll = ref(false)
const activeCategory = ref('all')

const categories = [
  { key: 'all', label: '全部', count: 156 },
  { key: 'academic', label: '学工政策', count: 42 },
  { key: 'teaching', label: '教务咨询', count: 38 },
  { key: 'service', label: '后勤服务', count: 28 },
  { key: 'it', label: '技术故障', count: 24 },
  { key: 'other', label: '其他', count: 24 }
]

const quickAccess = [
  { name: '学工政策', icon: Document, bgColor: '#F5F3FF', color: '#8B5CF6' },
  { name: '教学大纲', icon: Reading, bgColor: '#EFF6FF', color: '#3B82F6' },
  { name: '客服话术', icon: ChatLineRound, bgColor: '#F5F3FF', color: '#8B5CF6' },
  { name: '常见Q&A', icon: QuestionFilled, bgColor: '#FFF7ED', color: '#F97316' }
]

const knowledgeList = [
  {
    title: '奖学金评定政策详解与申请流程指南',
    tag: '高频',
    tagType: 'danger',
    category: '学工政策',
    target: '在校本科生',
    views: 2341,
    status: '已发布',
    statusType: 'success' as const
  },
  {
    title: '选课系统操作手册及常见问题解答',
    tag: '更新',
    tagType: 'warning',
    category: '教务咨询',
    target: '全体学生',
    views: 1892,
    status: '已发布',
    statusType: 'success' as const
  },
  {
    title: '宿舍调换申请流程与注意事项',
    tag: '待完善',
    tagType: 'info',
    category: '后勤服务',
    target: '住宿学生',
    views: 876,
    status: '草稿',
    statusType: 'info' as const
  },
  {
    title: '校园网账号密码重置操作指南',
    tag: '',
    tagType: '',
    category: '技术故障',
    target: '全体师生',
    views: 1567,
    status: '已发布',
    statusType: 'success' as const
  }
]
</script>

<style scoped lang="scss">
.knowledge-page {
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
  margin-bottom: 24px;

  .header-left {
    .page-title {
      font-size: 22px;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 6px;
    }

    .page-desc {
      font-size: 14px;
      color: var(--text-secondary);

      strong {
        color: var(--primary-color);
        font-weight: 600;
      }
    }
  }

  .header-actions {
    display: flex;
    gap: 12px;

    .search-input {
      width: 280px;

      :deep(.el-input__wrapper) {
        border-radius: var(--radius-md);
      }
    }

    .new-btn {
      border-radius: var(--radius-md);
      font-weight: 500;
    }
  }
}

// ========================================
// 分类标签
// ========================================
.category-tabs {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
  flex-wrap: wrap;

  .tab-btn {
    padding: 8px 16px;
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

    .count {
      margin-left: 4px;
      opacity: 0.7;
    }
  }
}

// ========================================
// 快捷入口
// ========================================
.quick-access {
  background: #fff;
  border-radius: var(--radius-lg);
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);

  .access-title {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 16px;
  }

  .access-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
  }

  .access-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
    padding: 20px;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all var(--transition-fast);
    border: 1px solid transparent;

    &:hover {
      background: #F8FAFC;
      border-color: var(--card-border);
    }

    .access-icon {
      width: 56px;
      height: 56px;
      border-radius: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .access-name {
      font-size: 14px;
      color: var(--text-secondary);
      font-weight: 500;
    }
  }
}

// ========================================
// 知识列表
// ========================================
.knowledge-list {
  background: #fff;
  border-radius: var(--radius-lg);
  box-shadow: var(--card-shadow);
  border: 1px solid var(--card-border);
  margin-bottom: 20px;
  overflow: hidden;
}

.list-header {
  display: grid;
  grid-template-columns: 40px 2fr 120px 120px 100px 100px 120px;
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

    &.flex-2 {
      flex: 2;
    }
  }
}

.list-body {
  .list-item {
    display: grid;
    grid-template-columns: 40px 2fr 120px 120px 100px 100px 120px;
    align-items: center;
    padding: 14px 20px;
    border-bottom: 1px solid #F1F5F9;
    transition: background-color var(--transition-fast);

    &:hover {
      background-color: #F8FAFC;
    }

    &:last-child {
      border-bottom: none;
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
      margin-bottom: 6px;
    }

    .content-tags {
      display: flex;
      gap: 6px;
    }
  }

  .category-badge {
    font-size: 13px;
    color: var(--primary-color);
    background: var(--primary-bg);
    padding: 4px 12px;
    border-radius: 12px;
  }

  .target-text {
    font-size: 13px;
    color: var(--text-secondary);
  }

  .view-count {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    color: var(--text-tertiary);

    .el-icon {
      font-size: 14px;
    }
  }
}

// ========================================
// AI 预警卡片
// ========================================
.ai-warning-card {
  background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%);
  border-radius: var(--radius-lg);
  padding: 24px;
  color: #fff;
  display: flex;
  gap: 20px;
  align-items: center;

  .warning-header {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-shrink: 0;

    .warning-title {
      font-size: 16px;
      font-weight: 600;
    }
  }

  .warning-content {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 20px;

    .warning-desc {
      font-size: 14px;
      line-height: 1.6;
      color: rgba(255, 255, 255, 0.9);

      strong {
        color: #fff;
        font-weight: 700;
      }

      .highlight {
        color: #5EEAD4;
        font-weight: 600;
      }
    }

    .warning-btn {
      background: rgba(255, 255, 255, 0.15);
      color: #fff;
      border-color: rgba(255, 255, 255, 0.3);
      font-weight: 500;
      flex-shrink: 0;

      &:hover {
        background: rgba(255, 255, 255, 0.25);
      }
    }
  }
}

// 响应式
@media (max-width: 1200px) {
  .quick-access {
    .access-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  .list-header,
  .list-body .list-item {
    grid-template-columns: 40px 2fr 100px 100px 80px;

    .item-col:nth-child(4),
    .header-col:nth-child(5) {
      display: none;
    }
  }

  .ai-warning-card {
    flex-direction: column;
    align-items: flex-start;

    .warning-content {
      flex-direction: column;
      align-items: flex-start;
    }
  }
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .quick-access {
    .access-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>
