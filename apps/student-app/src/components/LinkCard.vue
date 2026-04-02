<template>
  <view 
    class="link-card"
    :class="{ 'link-card-hover': isHovered }"
    @click="handleClick"
    @touchstart="isHovered = true"
    @touchend="isHovered = false"
  >
    <view class="link-left">
      <view class="link-icon-wrap">
        <component :is="icon" v-if="icon" />
        <svg v-else viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none">
          <circle cx="12" cy="12" r="10"/>
        </svg>
      </view>
      <view class="link-text">
        <text class="link-title">{{ title }}</text>
        <text class="link-subtitle">{{ subtitle }}</text>
      </view>
    </view>
    <view class="link-arrow" :class="{ 'arrow-shift': isHovered }">
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
  icon: Component | (() => Component)
  title: string
  subtitle: string
  href?: string
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: []
}>()

const isHovered = ref(false)

const handleClick = () => {
  if (props.href) {
    // 如果有href，进行页面跳转
    uni.navigateTo({
      url: props.href,
      fail: () => {
        // 如果是tab页面，使用switchTab
        uni.switchTab({ url: props.href })
      }
    })
  }
  emit('click')
}
</script>

<style scoped lang="scss">
$primary: #006a64;
$on-surface: #171d1c;
$on-surface-variant: #5a635f;
$surface-container-low: #eff5f3;

.link-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 32rpx;
  background: #ffffff;
  border-radius: 24rpx;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  
  &:active {
    background: $surface-container-low;
    transform: scale(0.98);
  }
  
  &.link-card-hover {
    background: rgba($primary, 0.02);
  }
}

.link-left {
  display: flex;
  align-items: center;
  gap: 24rpx;
}

.link-icon-wrap {
  width: 64rpx;
  height: 64rpx;
  border-radius: 20rpx;
  background: rgba($primary, 0.08);
  color: $primary;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all 0.2s ease;
  
  .link-card-hover & {
    background: rgba($primary, 0.12);
    transform: scale(1.05);
  }
}

.link-text {
  display: flex;
  flex-direction: column;
  gap: 6rpx;
}

.link-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $on-surface;
  line-height: 1.3;
}

.link-subtitle {
  font-size: 24rpx;
  color: $on-surface-variant;
  line-height: 1.4;
  text-transform: uppercase;
  letter-spacing: 1rpx;
}

.link-arrow {
  width: 48rpx;
  height: 48rpx;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.04);
  color: $on-surface-variant;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  flex-shrink: 0;
  
  &.arrow-shift {
    transform: translateX(8rpx);
    background: rgba($primary, 0.1);
    color: $primary;
  }
}
</style>
