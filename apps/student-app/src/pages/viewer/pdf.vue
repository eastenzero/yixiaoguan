<template>
  <view class="pdf-viewer-page">
    <view class="navbar">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">&#8592;</text>
      </view>
      <text class="title">{{ pageTitle }}</text>
    </view>
    <web-view class="pdf-frame" :src="pdfSrc" />
  </view>
</template>
<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'
const pdfSrc = ref('')
const pageTitle = ref('原始文件')
onLoad((options: any) => {
  if (options?.url) pdfSrc.value = decodeURIComponent(options.url)
  if (options?.title) pageTitle.value = decodeURIComponent(options.title)
})
function goBack() { uni.navigateBack() }
</script>
<style lang="scss" scoped>
@import '@/styles/theme.scss';
.pdf-viewer-page { display: flex; flex-direction: column; height: 100vh; height: 100dvh; }
.navbar { display: flex; align-items: center; height: 44px; padding-top: var(--status-bar-height, 44px); background: rgba(255,255,255,0.95); flex-shrink: 0; padding-left: 8px; padding-right: 16px; gap: 8px; }
.back-btn { width: 40px; height: 40px; display: flex; align-items: center; justify-content: center; }
.back-icon { font-size: 20px; color: $primary; }
.title { flex: 1; font-size: 16px; font-weight: 500; color: #1c1b1f; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pdf-frame { flex: 1; width: 100%; }
</style>
