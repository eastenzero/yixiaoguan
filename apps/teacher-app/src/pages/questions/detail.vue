<template>
  <view class="question-detail-page">
    <TopAppBar title="提问详情" showBack />

    <scroll-view scroll-y class="main-content">
      <!-- Student Info Card -->
      <view class="student-card animate-fade-up delay-1">
        <view class="avatar-wrapper">
          <view class="avatar-placeholder"></view>
          <view class="online-indicator"></view>
        </view>
        <view class="student-meta">
          <view class="student-header">
            <text class="student-name">张小洋</text>
            <view class="status-tag">
              <text class="status-text">待处理</text>
            </view>
          </view>
          <text class="student-info-text">护理学院 · 2023级本科</text>
        </view>
      </view>

      <!-- Chat History -->
      <view class="chat-section">
        <!-- Student Message -->
        <view class="message-wrapper student-message animate-fade-up delay-2">
          <view class="message-bubble student-bubble">
            <text class="message-text student-text">请问学校的电费缴纳在哪里操作？我看校微中心没找到入口，宿舍快停电了有点急，麻烦老师指路一下。</text>
          </view>
          <text class="message-time">14:30</text>
        </view>

        <!-- AI Response (Refusal) -->
        <view class="message-wrapper ai-message animate-fade-up delay-3">
          <view class="ai-avatar">
            <IconBot :size="24" color="#702ae1" />
          </view>
          <view class="ai-content">
            <view class="message-bubble ai-bubble">
              <view class="red-indicator"></view>
              <text class="message-text ai-text">很抱歉，医小管目前尚未学习到关于"校微中心电费缴纳入口"的相关说明。系统提示可能在"智慧校园"APP的"后勤服务"模块中进行。已为您呼叫人工老师处理。</text>
            </view>
            <text class="message-time">14:31</text>
          </view>
        </view>

        <!-- System Message -->
        <view class="system-message animate-fade-up delay-4">
          <view class="system-badge">
            <IconBell :size="16" color="#5d5b5f" />
            <text class="system-text">学生已呼叫老师 — 14:32</text>
          </view>
        </view>
      </view>

      <!-- Bottom padding for fixed action bar -->
      <view class="bottom-padding"></view>
    </scroll-view>

    <!-- Fixed Bottom Action Bar -->
    <view class="action-bar animate-fade-up delay-5">
      <view class="action-button" @click="handleAccept">
        <IconUserCheck :size="24" color="#f8f0ff" />
        <text class="action-text">接单处理</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
import TopAppBar from '../../components/TopAppBar.vue'
import { IconBot, IconBell, IconUserCheck } from '../../components/icons'

const handleAccept = () => {
  uni.showToast({
    title: '已接单',
    icon: 'success'
  })
}
</script>

<style lang="scss" scoped>
@import '../../styles/theme.scss';

.question-detail-page {
  min-height: 100vh;
  background: $surface;
}

.main-content {
  padding-top: 80px;
  padding-left: 16px;
  padding-right: 16px;
  padding-bottom: 120px;
  height: 100vh;
  box-sizing: border-box;
}

// Student Card
.student-card {
  background: $surface-container-lowest;
  border-radius: 24px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 32px;
}

.avatar-wrapper {
  position: relative;
}

.avatar-placeholder {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: $surface-container;
  border: 2px solid rgba($primary, 0.1);
}

.online-indicator {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 16px;
  height: 16px;
  background: #22c55e;
  border: 2px solid white;
  border-radius: 50%;
}

.student-meta {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.student-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.student-name {
  font-size: 20px;
  font-weight: 700;
  color: $on-surface;
}

.status-tag {
  padding: 4px 12px;
  background: $primary-container;
  border-radius: 9999px;

  .status-text {
    font-size: 12px;
    font-weight: 700;
    color: $on-primary-container;
  }
}

.student-info-text {
  font-size: 14px;
  color: $on-surface-variant;
}

// Chat Section
.chat-section {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

// Message Wrapper
.message-wrapper {
  display: flex;
  flex-direction: column;
}

.student-message {
  align-items: flex-end;
}

.ai-message {
  flex-direction: row;
  align-items: flex-start;
  gap: 12px;
}

// AI Avatar
.ai-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: $secondary-container;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.ai-content {
  display: flex;
  flex-direction: column;
  flex: 1;
}

// Message Bubbles
.message-bubble {
  max-width: 85%;
  padding: 16px;
  position: relative;
  overflow: hidden;
}

.student-bubble {
  background: $primary;
  border-radius: 16px 16px 0 16px;
  box-shadow: 0 8px 24px -4px rgba($primary, 0.12);
  align-self: flex-end;
}

.ai-bubble {
  background: white;
  border: 1px solid rgba($error, 0.2);
  border-radius: 16px 16px 16px 0;
  max-width: 90%;
}

.red-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: $error;
}

.message-text {
  font-size: 14px;
  line-height: 1.6;
}

.student-text {
  color: $on-primary;
}

.ai-text {
  color: $on-surface;
  padding-left: 8px;
}

.message-time {
  font-size: 10px;
  color: $on-surface-variant;
  margin-top: 8px;
  padding-left: 4px;
}

// System Message
.system-message {
  display: flex;
  justify-content: center;
}

.system-badge {
  display: flex;
  align-items: center;
  gap: 8px;
  background: $surface-container;
  border-radius: 9999px;
  padding: 6px 16px;
}

.system-text {
  font-size: 12px;
  font-weight: 500;
  color: $on-surface-variant;
}

// Bottom padding
.bottom-padding {
  height: 40px;
}

// Action Bar
.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 24px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  z-index: 50;
}

.action-button {
  height: 56px;
  border-radius: 9999px;
  background: linear-gradient(135deg, $primary, $primary-container);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 12px 32px -4px rgba($primary, 0.2);
  transition: transform 0.2s ease;

  &:active {
    transform: scale(0.95);
  }
}

.action-text {
  font-size: 18px;
  font-weight: 700;
  color: $on-primary;
}

// Animation delays
.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }
.delay-5 { animation-delay: 0.5s; }
</style>
