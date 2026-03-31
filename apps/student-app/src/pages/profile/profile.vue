<script setup lang="ts">
// TODO: 个人主页 — 学生描述、历史问答记录
</script>

<template>
  <view class="profile-page">
    <text class="title">个人主页</text>
    <text class="subtitle">个人中心（待实现）</text>
  </view>
</template>

<style lang="scss" scoped>
.profile-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;

  .title {
    font-size: 28px;
    font-weight: bold;
    color: #1a7a4a;
    margin-bottom: 12px;
  }

  .subtitle {
    font-size: 16px;
    color: #999;
  }
}
</style>
