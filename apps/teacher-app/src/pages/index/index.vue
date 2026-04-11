<template>
  <view class="container">
    <text class="title">医小管教师端</text>
    <text class="subtitle">项目初始化成功</text>
  </view>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: $surface;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: $primary;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: $on-surface-variant;
}
</style>
