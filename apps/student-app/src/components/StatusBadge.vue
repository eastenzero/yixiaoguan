<template>
  <view class="status-badge" :class="statusClass">
    <view v-if="showDot" class="status-dot"></view>
    <text class="status-text">{{ statusText }}</text>
  </view>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  status: number // 0待审批 1已通过 2已拒绝 3已取消 4已过期
  showDot?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showDot: true
})

// 状态映射
const statusMap: Record<number, { text: string; class: string }> = {
  0: { text: '待审批', class: 'status-pending' },
  1: { text: '已通过', class: 'status-approved' },
  2: { text: '已拒绝', class: 'status-rejected' },
  3: { text: '已取消', class: 'status-cancelled' },
  4: { text: '已过期', class: 'status-expired' }
}

const statusText = computed(() => {
  return statusMap[props.status]?.text || '处理中'
})

const statusClass = computed(() => {
  return statusMap[props.status]?.class || 'status-pending'
})
</script>

<style scoped lang="scss">
$primary: #006a64;

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 8rpx;
  padding: 8rpx 20rpx;
  border-radius: 24rpx;
  font-size: 24rpx;
  font-weight: 600;
  transition: all 0.2s ease;
  
  .status-dot {
    width: 12rpx;
    height: 12rpx;
    border-radius: 50%;
    flex-shrink: 0;
  }
  
  .status-text {
    line-height: 1;
  }
  
  // 待审批 - 橙色
  &.status-pending {
    color: #f57c00;
    background: #fff3e0;
    
    .status-dot {
      background-color: #f57c00;
      box-shadow: 0 0 8rpx rgba(245, 124, 0, 0.4);
    }
  }
  
  // 已通过 - MD3 主色
  &.status-approved {
    color: #006565;
    background: rgba(0, 101, 101, 0.1);
    
    .status-dot {
      background-color: #006565;
      box-shadow: 0 0 8rpx rgba(0, 101, 101, 0.4);
    }
  }
  
  // 已拒绝 - 红色
  &.status-rejected {
    color: #d32f2f;
    background: #ffebee;
    
    .status-dot {
      background-color: #d32f2f;
      box-shadow: 0 0 8rpx rgba(211, 47, 47, 0.4);
    }
  }
  
  // 已取消 - 灰色
  &.status-cancelled {
    color: #757575;
    background: rgba(117, 117, 117, 0.1);
    
    .status-dot {
      background-color: #757575;
      box-shadow: 0 0 8rpx rgba(117, 117, 117, 0.4);
    }
  }
  
  // 已过期 - 深灰色
  &.status-expired {
    color: #616161;
    background: rgba(97, 97, 97, 0.1);
    
    .status-dot {
      background-color: #616161;
      box-shadow: 0 0 8rpx rgba(97, 97, 97, 0.4);
    }
  }
}
</style>
