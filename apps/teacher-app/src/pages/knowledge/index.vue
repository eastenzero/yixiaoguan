<template>
  <view class="knowledge-page">
    <TopAppBar title="知识库" :showBack="true" action="add" />

    <view class="main-content">
      <!-- Search Bar Section -->
      <view class="section animate-fade-up delay-1">
        <view class="search-wrapper">
          <view class="search-icon">
            <IconSearch :size="20" color="#5d5b5f" />
          </view>
          <input 
            v-model="searchText"
            class="search-input" 
            placeholder="搜索知识文档、指南或规章..." 
            type="text"
            @confirm="handleSearch"
          />
        </view>
      </view>

      <!-- Category Tabs -->
      <view class="section tabs-section animate-fade-up delay-2">
        <scroll-view class="tabs-scroll" scroll-x show-scrollbar="false">
          <view class="tabs-wrapper">
            <view 
              v-for="(tab, index) in categories" 
              :key="index"
              class="tab-item"
              :class="{ 'tab-item--active': activeCategory === index }"
              @click="switchCategory(index)"
            >
              <text class="tab-text">{{ tab }}</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- Loading State -->
      <view v-if="loading" class="loading-state">
        <text class="loading-text">加载中...</text>
      </view>

      <!-- Empty State -->
      <view v-else-if="entries.length === 0" class="empty-state">
        <text class="empty-text">暂无知识文档</text>
      </view>

      <!-- Knowledge List -->
      <view v-else class="knowledge-list">
        <view 
          v-for="(item, index) in entries" 
          :key="item.id"
          class="knowledge-card animate-fade-up"
          :class="`delay-${Math.min(index + 3, 5)}`"
          @click="goToDetail(item.id)"
        >
          <view class="card-header">
            <view class="category-tag" :class="getCategoryClass(item.categoryId)">
              <text class="tag-text">{{ item.categoryName || getCategoryName(item.categoryId) }}</text>
            </view>
            <view class="status-tag">
              <view class="status-dot" :class="getStatusClass(item.status)"></view>
              <text class="status-text" :class="getStatusTextClass(item.status)">{{ getStatusText(item.status) }}</text>
            </view>
          </view>
          <text class="card-title">{{ item.title }}</text>
          <text class="card-summary">{{ getSummary(item.content) }}</text>
          <view class="card-footer">
            <view class="author-info">
              <view class="avatar-placeholder"></view>
              <text class="author-name">{{ item.authorName || '未知作者' }}</text>
            </view>
            <text class="time-text">{{ formatTime(item.updatedAt || item.createdAt) }}</text>
          </view>
        </view>
      </view>
    </view>

    <BottomNavBar :current="2" />
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { onShow } from '@dcloudio/uni-app'
import TopAppBar from '../../components/TopAppBar.vue'
import BottomNavBar from '../../components/BottomNavBar.vue'
import IconSearch from '../../components/icons/IconSearch.vue'
import { getKnowledgeEntries } from '@/api/knowledge'

const categories = ['全部', '教务管理', '学生服务', '生活指南']
const categoryIds = [undefined, 1, 2, 3] // 对应分类ID映射

const entries = ref<any[]>([])
const loading = ref(false)
const activeCategory = ref(0)
const searchText = ref('')
const total = ref(0)

// Mock 数据 —— API 无数据时兜底展示
const mockEntries = [
  {
    id: 1,
    categoryId: 1,
    categoryName: '教务管理',
    status: 1,
    title: '2025-2026学年第二学期期末考试日程安排',
    content: '本学期期末考试将于6月18日至7月2日进行。考试地点均在教学楼 A/B 栋。请同学们提前查看各科考试时间和教室安排，携带学生证和准考证参加考试。',
    authorName: '教务处',
    updatedAt: new Date(Date.now() - 86400000).toISOString()
  },
  {
    id: 2,
    categoryId: 2,
    categoryName: '学生服务',
    status: 1,
    title: '校园卡充值与挂失流程指南',
    content: '校园卡可通过微信公众号“智慧校园”在线充值，也可前往一卡通服务中心（行政楼B108）办理。如需挂失，请立即拨打服务热线 400-123-4567 或在小程序中操作。',
    authorName: '学生处',
    updatedAt: new Date(Date.now() - 172800000).toISOString()
  },
  {
    id: 3,
    categoryId: 3,
    categoryName: '生活指南',
    status: 1,
    title: '宿舍报修流程及常见问题解答',
    content: '宿舍设施报修请通过“后勤报修”微信小程序提交，正常工作日 24 小时内响应。紧急情况（漏水、断电）可直接联系楼管或拨打 24 小时紧急维修电话。',
    authorName: '后勤保障处',
    updatedAt: new Date(Date.now() - 259200000).toISOString()
  },
  {
    id: 4,
    categoryId: 1,
    categoryName: '教务管理',
    status: 1,
    title: '转专业申请条件与流程说明',
    content: '符合条件的学生可在每学年第二学期第4周至第6周提交转专业申请。基本条件：GPA ≥ 3.0，无不及格记录，无违纪处分。详细流程请查阅教务系统通知。',
    authorName: '教务处',
    updatedAt: new Date(Date.now() - 604800000).toISOString()
  },
  {
    id: 5,
    categoryId: 3,
    categoryName: '生活指南',
    status: 0,
    title: '校园网络连接指南（WiFi + 有线）',
    content: '校园 WiFi 名称为 YXG-WiFi，使用学号和密码登录。宿舍有线网络需在网络中心网站完成认证。密码重置请携带学生证前往信息中心办理。',
    authorName: '信息中心',
    createdAt: new Date(Date.now() - 432000000).toISOString()
  }
]

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await getKnowledgeEntries({
      categoryId: categoryIds[activeCategory.value],
      title: searchText.value || undefined,
      pageNum: 1,
      pageSize: 20
    })
    const rows = res.rows || []
    entries.value = rows.length > 0 ? rows : mockEntries
    total.value = res.total || rows.length || mockEntries.length
  } catch (e) {
    console.error('加载知识库失败，使用 mock 数据', e)
    entries.value = mockEntries
    total.value = mockEntries.length
  } finally {
    loading.value = false
  }
}

// 切换分类
const switchCategory = (index: number) => {
  activeCategory.value = index
  loadData()
}

// 搜索
const handleSearch = () => {
  loadData()
}

// 跳转到详情
const goToDetail = (id: number) => {
  uni.navigateTo({ url: `/pages/knowledge/detail?id=${id}` })
}

// 获取分类样式
const getCategoryClass = (categoryId?: number) => {
  const map: Record<number, string> = {
    1: 'category-tag--secondary',
    2: 'category-tag--secondary',
    3: 'category-tag--tertiary'
  }
  return map[categoryId || 0] || 'category-tag--secondary'
}

// 获取分类名称
const getCategoryName = (categoryId?: number) => {
  const map: Record<number, string> = {
    1: '教务管理',
    2: '学生服务',
    3: '生活指南'
  }
  return map[categoryId || 0] || '其他'
}

// 获取状态样式
const getStatusClass = (status?: number) => {
  const map: Record<number, string> = {
    0: 'status-dot--draft',
    1: 'status-dot--published',
    2: 'status-dot--draft',
    3: 'status-dot--draft'
  }
  return map[status || 0] || 'status-dot--draft'
}

// 获取状态文字样式
const getStatusTextClass = (status?: number) => {
  const map: Record<number, string> = {
    0: 'status-text--draft',
    1: 'status-text--published',
    2: 'status-text--draft',
    3: 'status-text--draft'
  }
  return map[status || 0] || 'status-text--draft'
}

// 获取状态文字
const getStatusText = (status?: number) => {
  const map: Record<number, string> = {
    0: '草稿',
    1: '已发布',
    2: '审核中',
    3: '已下线'
  }
  return map[status || 0] || '未知'
}

// 获取摘要
const getSummary = (content?: string) => {
  if (!content) return ''
  return content.length > 100 ? content.substring(0, 100) + '...' : content
}

// 格式化时间
const formatTime = (time?: string) => {
  if (!time) return ''
  const date = new Date(time)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  
  // 一小时内
  if (diff < 3600000) {
    const mins = Math.floor(diff / 60000)
    return mins < 1 ? '刚刚' : `${mins}分钟前`
  }
  // 一天内
  if (diff < 86400000) {
    const hours = Math.floor(diff / 3600000)
    return `${hours}小时前`
  }
  // 一周内
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days}天前`
  }
  
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => loadData())
onShow(() => loadData())
</script>

<style lang="scss" scoped>
.knowledge-page {
  min-height: 100vh;
  padding-bottom: 112px;
  background: $background;
}

.main-content {
  position: relative;
  z-index: 1;
  padding-top: 72px;
  padding-left: 20px;
  padding-right: 20px;
}

.section {
  margin-bottom: 24px;
}

// Search Bar
.search-wrapper {
  position: relative;
  height: 56px;
  background: $surface-container;
  border-radius: 16px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
}

.search-input {
  flex: 1;
  height: 100%;
  padding-left: 48px;
  padding-right: 16px;
  background: transparent;
  border: none;
  font-size: 15px;
  color: $on-surface;
  
  &::placeholder {
    color: $on-surface-variant;
    opacity: 0.5;
  }
}

// Tabs
.tabs-section {
  margin-left: -20px;
  margin-right: -20px;
  padding-left: 20px;
  padding-right: 20px;

  :deep(.uni-scroll-view::-webkit-scrollbar) {
    display: none;
  }
  :deep(.uni-scroll-view) {
    scrollbar-width: none;
  }
}

.tabs-scroll {
  white-space: nowrap;
}

.tabs-wrapper {
  display: inline-flex;
  gap: 12px;
  padding-bottom: 8px;
}

.tab-item {
  flex-shrink: 0;
  white-space: nowrap;
  padding: 10px 24px;
  background: $surface-container-low;
  border-radius: 9999px;
  transition: all 0.2s ease;
  
  &:active {
    transform: scale(0.95);
  }
  
  &--active {
    background: $primary;
    box-shadow: 0 8px 16px -4px rgba($primary, 0.2);
    
    .tab-text {
      color: $on-primary;
    }
  }
}

.tab-text {
  font-size: 14px;
  font-weight: 500;
  color: $on-surface-variant;
  white-space: nowrap;
}

// Loading & Empty State
.loading-state,
.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.loading-text,
.empty-text {
  font-size: 14px;
  color: $on-surface-variant;
}

// Knowledge Cards
.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.knowledge-card {
  background: $surface-container-lowest;
  border-radius: 24px;
  padding: 24px;
  transition: all 0.2s ease;
  
  &:active {
    transform: scale(0.98);
    background: $surface-container-low;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.category-tag {
  padding: 4px 12px;
  border-radius: 9999px;
  
  &--secondary {
    background: $secondary-container;
    
    .tag-text {
      color: $on-secondary-container;
    }
  }
  
  &--tertiary {
    background: $tertiary-container;
    
    .tag-text {
      color: $on-tertiary-container;
    }
  }
}

.tag-text {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.status-tag {
  display: flex;
  align-items: center;
  gap: 6px;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  
  &--published {
    background: $primary;
  }
  
  &--draft {
    background: $outline-variant;
  }
}

.status-text {
  font-size: 12px;
  font-weight: 500;
  
  &--published {
    color: $primary;
  }
  
  &--draft {
    color: $on-surface-variant;
  }
}

.card-title {
  display: block;
  font-size: 18px;
  font-weight: 700;
  color: $on-surface;
  line-height: 1.3;
  margin-bottom: 8px;
}

.card-summary {
  display: block;
  font-size: 14px;
  color: $on-surface-variant;
  line-height: 1.6;
  margin-bottom: 16px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid rgba($outline-variant, 0.1);
}

.author-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.avatar-placeholder {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: $surface-container-highest;
}

.author-name {
  font-size: 12px;
  font-weight: 500;
  color: $on-surface-variant;
}

.time-text {
  font-size: 12px;
  color: $on-surface-variant;
  opacity: 0.6;
}
</style>
