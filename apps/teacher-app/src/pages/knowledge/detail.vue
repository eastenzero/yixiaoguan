<template>
  <view class="knowledge-detail-page">
    <TopAppBar title="知识详情" :showBack="true" action="edit" />

    <view class="main-content animate-fade-up">
      <!-- Hero Section -->
      <view class="hero-section">
        <view class="tags-row">
          <view class="category-tag">
            <text class="tag-text">生活指南</text>
          </view>
          <view class="status-tag">
            <view class="status-dot"></view>
            <text class="status-text">已发布</text>
          </view>
        </view>
        <text class="hero-title">学生电费缴纳指南</text>
        <view class="author-row">
          <view class="author-avatar">
            <IconUser :size="16" color="#612c90" />
          </view>
          <view class="author-info">
            <text class="author-name">系统管理员</text>
            <text class="update-time">最后更新于 2023年10月24日 14:30</text>
          </view>
        </view>
      </view>

      <!-- Body Content -->
      <view class="content-section">
        <!-- Cover Image Placeholder -->
        <view class="cover-placeholder"></view>

        <!-- Section 1 -->
        <text class="section-title">1. 缴纳方式概述</text>
        <text class="paragraph">
          为方便广大在校学生，学校提供了多种电费缴纳途径。目前支持通过校园一卡通、手机银行以及第三方支付平台（微信/支付宝）进行实时充值。
        </text>

        <!-- Section 2 -->
        <text class="section-title">2. 详细操作步骤</text>
        <view class="steps-list">
          <view class="step-item">
            <view class="step-number">
              <text class="step-number-text">01</text>
            </view>
            <view class="step-content">
              <text class="step-title">登录校园小程序</text>
              <text class="step-desc">打开"智慧校园"小程序，进入"生活缴费"模块，选择"电费管理"。</text>
            </view>
          </view>
          <view class="step-item">
            <view class="step-number">
              <text class="step-number-text">02</text>
            </view>
            <view class="step-content">
              <text class="step-title">绑定宿舍信息</text>
              <text class="step-desc">首次使用需输入所在楼栋和宿舍号进行身份校验与余额查询。</text>
            </view>
          </view>
          <view class="step-item">
            <view class="step-number">
              <text class="step-number-text">03</text>
            </view>
            <view class="step-content">
              <text class="step-title">确认并支付</text>
              <text class="step-desc">输入充值金额（单次不少于10元），选择支付方式并完成确认。</text>
            </view>
          </view>
        </view>

        <!-- Section 3 -->
        <text class="section-title">3. 注意事项</text>
        <view class="quote-block">
          <text class="quote-text">"系统每日 23:30 至次日 00:30 为结算维护时间，期间无法进行充值，请避开此时段。"</text>
        </view>
        <text class="paragraph">
          如遇充值成功但电表未及时下发指令的情况，请携带一卡通前往宿舍楼下的自助终端进行补登，或联系后勤保障部服务热线（010-88888888）。
        </text>
      </view>
    </view>

    <!-- Bottom Action Bar -->
    <view class="bottom-action-bar">
      <button class="action-btn action-btn--outline" @click="handleOffline">
        <text class="btn-text">下线</text>
      </button>
      <button class="action-btn action-btn--primary" @click="handleEdit">
        <IconEdit :size="20" color="#f8f0ff" />
        <text class="btn-text">编辑</text>
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import TopAppBar from '../../components/TopAppBar.vue'
import IconUser from '../../components/icons/IconUser.vue'
import IconEdit from '../../components/icons/IconEdit.vue'

const handleOffline = () => {
  uni.showModal({
    title: '确认下线',
    content: '确定要将该知识文档下线吗？',
    success: (res) => {
      if (res.confirm) {
        uni.showToast({ title: '已下线', icon: 'success' })
      }
    }
  })
}

const handleEdit = () => {
  uni.showToast({ title: '进入编辑模式', icon: 'none' })
}
</script>

<style lang="scss" scoped>
@import '../../styles/theme.scss';

.knowledge-detail-page {
  min-height: 100vh;
  background: $surface;
  padding-bottom: 100px;
}

.main-content {
  padding-top: 80px;
  padding-left: 20px;
  padding-right: 20px;
}

// Hero Section
.hero-section {
  margin-bottom: 32px;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
}

.category-tag {
  padding: 4px 12px;
  background: $primary-container;
  border-radius: 9999px;
  
  .tag-text {
    font-size: 11px;
    font-weight: 700;
    color: $on-primary-container;
    letter-spacing: 0.5px;
    text-transform: uppercase;
  }
}

.status-tag {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 4px 12px;
  background: $surface-container;
  border-radius: 9999px;
  
  .status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22c55e;
  }
  
  .status-text {
    font-size: 11px;
    font-weight: 500;
    color: $on-surface-variant;
  }
}

.hero-title {
  display: block;
  font-size: 30px;
  font-weight: 800;
  color: $on-surface;
  line-height: 1.2;
  margin-bottom: 16px;
}

.author-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 8px;
}

.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: $secondary-container;
  display: flex;
  align-items: center;
  justify-content: center;
}

.author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.author-name {
  font-size: 14px;
  font-weight: 600;
  color: $on-surface;
}

.update-time {
  font-size: 12px;
  color: $on-surface-variant;
}

// Content Section
.content-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.cover-placeholder {
  width: 100%;
  aspect-ratio: 16/9;
  background: $surface-container;
  border-radius: 16px;
}

.section-title {
  display: block;
  font-size: 20px;
  font-weight: 700;
  color: $on-surface;
  padding-top: 16px;
}

.paragraph {
  display: block;
  font-size: 14px;
  color: $on-surface-variant;
  line-height: 1.7;
}

// Steps
.steps-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.step-item {
  display: flex;
  gap: 16px;
  padding: 16px;
  background: $surface-container-low;
  border-radius: 16px;
}

.step-number {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: $primary;
  display: flex;
  align-items: center;
  justify-content: center;
}

.step-number-text {
  font-size: 12px;
  font-weight: 700;
  color: $on-primary;
}

.step-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.step-title {
  font-size: 14px;
  font-weight: 700;
  color: $on-surface;
}

.step-desc {
  font-size: 13px;
  color: $on-surface-variant;
  line-height: 1.5;
}

// Quote Block
.quote-block {
  padding: 20px;
  padding-left: 16px;
  background: rgba($primary, 0.05);
  border-left: 4px solid $primary;
  border-radius: 0 16px 16px 0;
}

.quote-text {
  font-size: 14px;
  color: $on-surface-variant;
  font-style: italic;
  line-height: 1.6;
}

// Bottom Action Bar
.bottom-action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 16px 20px;
  padding-bottom: calc(16px + env(safe-area-inset-bottom));
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.04);
}

.action-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  height: 48px;
  border-radius: 9999px;
  border: none;
  font-size: 15px;
  font-weight: 600;
  transition: all 0.2s ease;
  
  &:active {
    transform: scale(0.95);
  }
  
  &::after {
    border: none;
  }
  
  &--outline {
    flex: 1;
    background: transparent;
    border: 1px solid $outline-variant;
    
    .btn-text {
      color: $on-surface;
    }
    
    &:active {
      background: $surface-container-low;
    }
  }
  
  &--primary {
    flex: 2;
    background: linear-gradient(135deg, $primary 0%, $primary-container 100%);
    box-shadow: 0 4px 15px rgba($primary, 0.3);
    
    .btn-text {
      color: $on-primary;
    }
    
    &:active {
      opacity: 0.9;
    }
  }
}

.btn-text {
  font-size: 15px;
  font-weight: 600;
}
</style>
