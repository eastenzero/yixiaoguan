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
            class="search-input" 
            placeholder="搜索知识文档、指南或规章..." 
            type="text"
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
              @click="activeCategory = index"
            >
              <text class="tab-text">{{ tab }}</text>
            </view>
          </view>
        </scroll-view>
      </view>

      <!-- Knowledge List -->
      <view class="knowledge-list">
        <!-- Card 1 -->
        <view 
          class="knowledge-card animate-fade-up delay-3"
          @click="goToDetail(1)"
        >
          <view class="card-header">
            <view class="category-tag category-tag--secondary">
              <text class="tag-text">教务管理</text>
            </view>
            <view class="status-tag">
              <view class="status-dot status-dot--published"></view>
              <text class="status-text status-text--published">已发布</text>
            </view>
          </view>
          <text class="card-title">2024年春季学期排课调整指南</text>
          <text class="card-summary">本指南详细说明了本学期教务排课的最新变更，包括多媒体教室申请流程、跨学院选修课的时间协调机制以及调课申请的截止日期...</text>
          <view class="card-footer">
            <view class="author-info">
              <view class="avatar-placeholder"></view>
              <text class="author-name">教务处 · 李老师</text>
            </view>
            <text class="time-text">2小时前</text>
          </view>
        </view>

        <!-- Card 2 -->
        <view 
          class="knowledge-card animate-fade-up delay-4"
          @click="goToDetail(2)"
        >
          <view class="card-header">
            <view class="category-tag category-tag--tertiary">
              <text class="tag-text">生活指南</text>
            </view>
            <view class="status-tag">
              <view class="status-dot status-dot--draft"></view>
              <text class="status-text status-text--draft">草稿</text>
            </view>
          </view>
          <text class="card-title">校园智慧卡充值与挂失常见问题解答</text>
          <text class="card-summary">针对近期学生反映的校园卡在线充值延迟及丢失补办手续繁杂的问题，后勤管理处整理了这份最新的FAQ手册供查阅...</text>
          <view class="card-footer">
            <view class="author-info">
              <view class="avatar-placeholder"></view>
              <text class="author-name">后勤处 · 王助理</text>
            </view>
            <text class="time-text">昨天 14:20</text>
          </view>
        </view>

        <!-- Card 3 -->
        <view 
          class="knowledge-card animate-fade-up delay-5"
          @click="goToDetail(3)"
        >
          <view class="card-header">
            <view class="category-tag category-tag--secondary">
              <text class="tag-text">学生服务</text>
            </view>
            <view class="status-tag">
              <view class="status-dot status-dot--published"></view>
              <text class="status-text status-text--published">已发布</text>
            </view>
          </view>
          <text class="card-title">毕业生离校手续一站式办理流程 (2024版)</text>
          <text class="card-summary">为了方便毕业生更快捷地完成离校手续，今年我们将全面采用线上预审模式。请同学们在离校前15天内完成以下步骤...</text>
          <view class="card-footer">
            <view class="author-info">
              <view class="avatar-placeholder"></view>
              <text class="author-name">学生处 · 赵处长</text>
            </view>
            <text class="time-text">2024-03-12</text>
          </view>
        </view>
      </view>
    </view>

    <BottomNavBar :current="2" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import TopAppBar from '../../components/TopAppBar.vue'
import BottomNavBar from '../../components/BottomNavBar.vue'
import IconSearch from '../../components/icons/IconSearch.vue'

const categories = ['全部', '教务管理', '学生服务', '生活指南']
const activeCategory = ref(0)

const goToDetail = (id: number) => {
  uni.navigateTo({ url: `/pages/knowledge/detail?id=${id}` })
}
</script>

<style lang="scss" scoped>
@import '../../styles/theme.scss';

.knowledge-page {
  min-height: 100vh;
  padding-bottom: 112px;
  background: $background;
}

.main-content {
  padding-top: 80px;
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
  overflow: hidden;
}

.tabs-scroll {
  white-space: nowrap;
}

.tabs-wrapper {
  display: flex;
  gap: 12px;
  padding-bottom: 8px;
}

.tab-item {
  padding: 10px 24px;
  background: $surface-container-low;
  border-radius: 9999px;
  transition: all 0.2s ease;
  
  &:active {
    transform: scale(0.95);
  }
  
  &--active {
    background: $primary;
    box-shadow: 0 4px 15px rgba($primary, 0.3);
    
    .tab-text {
      color: $on-primary;
    }
  }
}

.tab-text {
  font-size: 14px;
  font-weight: 500;
  color: $on-surface-variant;
}

// Knowledge Cards
.knowledge-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
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
