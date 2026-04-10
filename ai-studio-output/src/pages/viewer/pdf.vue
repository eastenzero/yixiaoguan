<template>
  <view class="pdf-viewer-page">
    <view class="navbar">
      <view class="back-btn" @click="goBack">
        <text class="icon">←</text>
      </view>
      <text class="title">{{ title }}</text>
    </view>
    
    <web-view v-if="url" :src="url" class="web-view"></web-view>
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const url = ref('')
const title = ref('文件预览')

onLoad((options: any) => {
  if (options.url) {
    url.value = decodeURIComponent(options.url)
  }
  if (options.title) {
    title.value = decodeURIComponent(options.title)
  }
})

const goBack = () => {
  uni.navigateBack()
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.pdf-viewer-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.navbar {
  height: 88rpx;
  padding-top: var(--status-bar-height, 44rpx);
  background: $primary-40;
  display: flex;
  align-items: center;
  position: relative;
  
  .back-btn {
    position: absolute;
    left: $spacing-md;
    width: 64rpx;
    height: 64rpx;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .icon {
      font-size: 40rpx;
      color: $text-inverse;
    }
    
    &:active {
      opacity: 0.7;
    }
  }
  
  .title {
    flex: 1;
    text-align: center;
    font-size: 36rpx;
    font-weight: 600;
    color: $text-inverse;
    padding: 0 100rpx;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.web-view {
  flex: 1;
  width: 100%;
}
</style>
