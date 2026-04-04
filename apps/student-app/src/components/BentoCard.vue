<template>
  <view 
    class="bento-card"
    :class="[size === 'large' ? 'bento-card-large' : 'bento-card-normal', bgClass]"
    @click="handleClick"
  >
    <view class="bento-content">
      <view class="bento-icon-wrap">
        <component :is="icon" v-if="icon" />
        <svg v-else viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
          <circle cx="12" cy="12" r="10"/>
        </svg>
      </view>
      <view class="bento-text">
        <text class="bento-title">{{ title }}</text>
        <text class="bento-desc">{{ desc }}</text>
      </view>
    </view>
    <view v-if="hasArrow" class="bento-arrow" :class="{ 'arrow-active': isPressed }">
      <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h14" />
        <path d="m12 5 7 7-7 7" />
      </svg>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Component } from 'vue'

interface Props {
  size?: 'large' | 'normal'
  bgClass?: string
  icon: Component | (() => Component)
  title: string
  desc: string
  hasArrow?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  size: 'normal',
  bgClass: 'bg-default',
  hasArrow: false
})

const emit = defineEmits<{
  click: []
}>()

const isPressed = ref(false)

const handleClick = () => {
  isPressed.value = true
  setTimeout(() => {
    isPressed.value = false
  }, 150)
  emit('click')
}
</script>

<style scoped lang="scss">
// 导入主题变量
@import '@/styles/theme.scss';

$on-surface: #171d1c;
$on-surface-variant: #5a635f;
$surface-container-lowest: #ffffff;

.bento-card {
  position: relative;
  border-radius: 24rpx;
  overflow: hidden;
  transition: transform 0.2s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.2s ease;
  
  &:active {
    transform: scale(0.96);
  }
  
  // 默认背景
  &.bg-default {
    background: $surface-container-lowest;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.04);
  }
  
  // 渐变背景 - 任务指引
  &.bg-gradient-primary {
    background: linear-gradient(135deg, rgba($primary, 0.9) 0%, rgba($primary, 0.7) 100%);
    color: #ffffff;
    box-shadow: 0 12rpx 40rpx rgba($primary, 0.25);
  }
  
  // 渐变背景 - 空教室
  &.bg-gradient-teal {
    background: linear-gradient(135deg, $primary-60 0%, $primary-40 100%);
    color: #ffffff;
    box-shadow: 0 12rpx 40rpx rgba($primary-40, 0.25);
  }
  
  // 渐变背景 - 申请进度
  &.bg-gradient-purple {
    background: linear-gradient(135deg, #7B68EE 0%, #5B4BC4 100%);
    color: #ffffff;
    box-shadow: 0 12rpx 40rpx rgba(123, 104, 238, 0.25);
  }
  
  // 纯色背景
  &.bg-surface {
    background: $surface-container-lowest;
    box-shadow: 0 8rpx 32rpx rgba(0, 0, 0, 0.04);
  }
}

// 大尺寸卡片 - 跨列
.bento-card-large {
  padding: 40rpx;
  min-height: 200rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  .bento-content {
    display: flex;
    align-items: center;
    gap: 28rpx;
  }
  
  .bento-icon-wrap {
    width: 80rpx;
    height: 80rpx;
    border-radius: 24rpx;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    backdrop-filter: blur(8rpx);
  }
  
  .bento-text {
    display: flex;
    flex-direction: column;
    gap: 8rpx;
  }
  
  .bento-title {
    font-size: 36rpx;
    font-weight: 700;
    line-height: 1.3;
  }
  
  .bento-desc {
    font-size: 26rpx;
    opacity: 0.9;
    line-height: 1.4;
  }
  
  .bento-arrow {
    width: 56rpx;
    height: 56rpx;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease, background 0.2s ease;
    
    &.arrow-active {
      transform: translateX(8rpx);
      background: rgba(255, 255, 255, 0.3);
    }
  }
}

// 普通尺寸卡片
.bento-card-normal {
  padding: 32rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  
  .bento-content {
    display: flex;
    align-items: center;
    gap: 20rpx;
  }
  
  .bento-icon-wrap {
    width: 64rpx;
    height: 64rpx;
    border-radius: 20rpx;
    background: rgba($primary, 0.1);
    color: $primary;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  // 在渐变背景上的图标样式
  &.bg-gradient-primary,
  &.bg-gradient-teal,
  &.bg-gradient-purple {
    .bento-icon-wrap {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
    }
  }
  
  .bento-text {
    display: flex;
    flex-direction: column;
    gap: 4rpx;
  }
  
  .bento-title {
    font-size: 30rpx;
    font-weight: 600;
    color: $on-surface;
    line-height: 1.3;
  }
  
  .bento-desc {
    font-size: 24rpx;
    color: $on-surface-variant;
    line-height: 1.4;
  }
  
  // 在渐变背景上的文字样式
  &.bg-gradient-primary,
  &.bg-gradient-teal,
  &.bg-gradient-purple {
    .bento-title,
    .bento-desc {
      color: #ffffff;
    }
    .bento-desc {
      opacity: 0.9;
    }
  }
  
  .bento-arrow {
    width: 48rpx;
    height: 48rpx;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.04);
    color: $on-surface-variant;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.2s ease, background 0.2s ease;
    
    &.arrow-active {
      transform: translateX(6rpx);
      background: rgba(0, 0, 0, 0.08);
    }
  }
  
  // 在渐变背景上的箭头样式
  &.bg-gradient-primary,
  &.bg-gradient-teal,
  &.bg-gradient-purple {
    .bento-arrow {
      background: rgba(255, 255, 255, 0.2);
      color: #ffffff;
      
      &.arrow-active {
        background: rgba(255, 255, 255, 0.3);
      }
    }
  }
}
</style>
