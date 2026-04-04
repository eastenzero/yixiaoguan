<template>
  <view class="services-page">
    <!-- 毛玻璃 NavBar -->
    <view class="glass-navbar">
      <view class="navbar-content">
        <text class="navbar-title">服务大厅</text>
      </view>
    </view>

    <!-- Header 区 -->
    <view class="page-hero">
      <text class="hero-label">Service Hall</text>
      <text class="hero-title">服务大厅</text>
      <text class="hero-subtitle">高效处理您的校园行政事务</text>
    </view>

    <!-- 服务矩阵 Grid -->
    <view class="services-section">
      <view class="services-grid">
        <view
          v-for="service in services"
          :key="service.name"
          class="service-card"
          :class="{ 'service-active': service.active, 'service-placeholder': !service.active }"
          @click="handleServiceClick(service)"
        >
          <view class="service-icon-wrapper">
            <component
              :is="service.iconComponent"
              :size="28"
              :color="service.active ? 'var(--primary-color)' : '#76777A'"
            />
          </view>
          <text class="service-name">{{ service.name }}</text>
        </view>
      </view>
    </view>

    <!-- 底部留白 -->
    <view class="bottom-safe"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, shallowRef } from 'vue'
import IconDoorOpen from '@/components/icons/IconDoorOpen.vue'
import IconClipboardList from '@/components/icons/IconClipboardList.vue'
import IconFileSignature from '@/components/icons/IconFileSignature.vue'
import IconGraduationCap from '@/components/icons/IconGraduationCap.vue'
import IconFileText from '@/components/icons/IconFileText.vue'
import IconHelpCircle from '@/components/icons/IconHelpCircle.vue'
import IconCalendar from '@/components/icons/IconCalendar.vue'
import IconLayoutGrid from '@/components/icons/IconLayoutGrid.vue'

interface Service {
  name: string
  iconComponent: any
  active: boolean
  path?: string
}

const services = ref<Service[]>([
  {
    name: '空教室申请',
    iconComponent: shallowRef(IconDoorOpen),
    active: true,
    path: '/pages/apply/classroom'
  },
  {
    name: '我的申请',
    iconComponent: shallowRef(IconClipboardList),
    active: true,
    path: '/pages/apply/status'
  },
  {
    name: '请假销假',
    iconComponent: shallowRef(IconFileSignature),
    active: false
  },
  {
    name: '学籍管理',
    iconComponent: shallowRef(IconGraduationCap),
    active: false
  },
  {
    name: '证明开具',
    iconComponent: shallowRef(IconFileText),
    active: false
  },
  {
    name: '心理服务',
    iconComponent: shallowRef(IconHelpCircle),
    active: false
  },
  {
    name: '缓考申请',
    iconComponent: shallowRef(IconCalendar),
    active: false
  },
  {
    name: '更多',
    iconComponent: shallowRef(IconLayoutGrid),
    active: false
  }
])

function handleServiceClick(service: Service) {
  if (service.active && service.path) {
    uni.navigateTo({ url: service.path })
  } else {
    uni.showToast({
      title: '功能开发中，敬请期待',
      icon: 'none',
      duration: 2000
    })
  }
}
</script>

<style scoped lang="scss">
// 导入主题变量
@use '@/styles/theme.scss' as *;

.services-page {
  min-height: 100vh;
  background: $md-sys-color-background;
  --primary-color: #{$primary};
}

// 毛玻璃 NavBar
.glass-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border-bottom: none;
  padding-top: var(--status-bar-height, 44px);
}

.navbar-content {
  height: 88rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 32rpx;
}

.navbar-title {
  font-size: 34rpx;
  font-weight: 600;
  color: $neutral-10;
}

// Header 区
.page-hero {
  padding: calc(var(--status-bar-height, 44px) + 120rpx) 40rpx 48rpx;
  background: $md-sys-color-background;
}

.hero-label {
  display: block;
  font-size: 24rpx;
  font-weight: 500;
  color: $primary-60;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 12rpx;
}

.hero-title {
  display: block;
  font-size: 52rpx;
  font-weight: 700;
  color: $neutral-10;
  margin-bottom: 16rpx;
}

.hero-subtitle {
  display: block;
  font-size: 28rpx;
  color: $neutral-50;
}

// 服务矩阵区
.services-section {
  padding: 0 32rpx;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20rpx;
}

.service-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32rpx 16rpx;
  border-radius: $radius-xl;
  background: $md-sys-color-surface-container-lowest;
  transition: all 0.2s ease;
}

.service-active {
  background: $md-sys-color-surface-container-lowest;
  box-shadow: $md-sys-elevation-1;
  
  &:active {
    transform: scale(0.96);
    box-shadow: $md-sys-elevation-2;
  }
}

.service-placeholder {
  background: $md-sys-color-surface-container-low;
  opacity: 0.85;
  
  &:active {
    transform: scale(0.98);
  }
}

.service-icon-wrapper {
  width: 64rpx;
  height: 64rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16rpx;
  border-radius: $radius-lg;
  background: $md-sys-color-surface-container-low;
}

.service-active .service-icon-wrapper {
  background: $primary-90;
}

.service-name {
  font-size: 24rpx;
  font-weight: 500;
  color: $neutral-10;
  text-align: center;
  line-height: 1.3;
}

.service-placeholder .service-name {
  color: $neutral-50;
}

// 底部留白
.bottom-safe {
  height: 40rpx;
}
</style>
