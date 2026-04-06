<template>
  <view class="custom-tab-bar">
    <view 
      v-for="tab in tabs" 
      :key="tab.key"
      class="tab-item"
      :class="{ 'tab-active': current === tab.key }"
      @click="handleSwitchTab(tab.key)"
    >
      <view class="tab-icon-wrap">
        <component :is="tab.icon" :size="current === tab.key ? 22 : 24" :color="current === tab.key ? 'var(--color-primary, #006a64)' : '#5a635f'" />
      </view>
      <text class="tab-label">{{ tab.label }}</text>
    </view>
  </view>
</template>

<script setup lang="ts">
import IconHome from './icons/IconHome.vue'
import IconBot from './icons/IconBot.vue'
import IconLayoutGrid from './icons/IconLayoutGrid.vue'
import IconUser from './icons/IconUser.vue'

interface Props {
  current: 'home' | 'assistant' | 'services' | 'profile'
}

defineProps<Props>()

const emit = defineEmits<{
  'switch-tab': [key: 'home' | 'assistant' | 'services' | 'profile']
}>()

const tabs = [
  { key: 'home' as const, label: '首页', icon: IconHome },
  { key: 'assistant' as const, label: '智能问答', icon: IconBot },
  { key: 'services' as const, label: '事务导办', icon: IconLayoutGrid },
  { key: 'profile' as const, label: '我的', icon: IconUser }
]

const handleSwitchTab = (key: 'home' | 'assistant' | 'services' | 'profile') => {
  emit('switch-tab', key)
}
</script>

<style scoped lang="scss">
@use '@/styles/theme.scss' as *;

$on-surface-variant: #5a635f;
$surface-container-lowest: #ffffff;

.custom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: calc(120rpx + env(safe-area-inset-bottom, 0));
  padding-bottom: env(safe-area-inset-bottom, 0);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 48rpx 48rpx 0 0;
  box-shadow: 0px -4rpx 20rpx rgba(0, 106, 100, 0.08);
  display: flex;
  align-items: center;
  justify-content: space-around;
  z-index: 999;
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8rpx;
  padding: 16rpx 32rpx;
  border-radius: 24rpx;
  transition: all 0.25s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  
  &:active {
    transform: scale(0.92);
  }
  
  &.tab-active {
    background: rgba($primary, 0.1);
    transform: scale(0.9);
    
    .tab-label {
      color: $primary;
      font-weight: 600;
    }
  }
}

.tab-icon-wrap {
  width: 48rpx;
  height: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
}

.tab-label {
  font-size: 22rpx;
  color: $on-surface-variant;
  line-height: 1;
  transition: all 0.2s ease;
}
</style>
