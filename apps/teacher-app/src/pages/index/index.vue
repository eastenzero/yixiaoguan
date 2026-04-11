<template>
  <view></view>
</template>
<script setup lang="ts">
import { onLoad } from '@dcloudio/uni-app'
onLoad(() => {
  uni.reLaunch({ url: '/pages/login/index' })
})
</script>
