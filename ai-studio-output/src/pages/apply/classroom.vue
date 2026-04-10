<template>
  <view class="apply-page">
    <view class="hero-section">
      <text class="title">预约申请单</text>
      <text class="subtitle">请如实填写空教室使用需求，审批通过后方可使用。</text>
    </view>

    <view class="form-container">
      <!-- 时间选择 -->
      <view class="form-group">
        <text class="group-title">使用时间</text>
        <view class="form-item">
          <text class="label">使用日期</text>
          <picker mode="date" :value="form.date" @change="onDateChange">
            <view class="picker-value" :class="{ placeholder: !form.date }">
              {{ form.date || '请选择日期' }}
            </view>
          </picker>
        </view>
        <view class="form-row">
          <view class="form-item half">
            <text class="label">开始时间</text>
            <picker mode="time" :value="form.startTime" @change="onStartTimeChange">
              <view class="picker-value" :class="{ placeholder: !form.startTime }">
                {{ form.startTime || '选择时间' }}
              </view>
            </picker>
          </view>
          <view class="form-item half">
            <text class="label">结束时间</text>
            <picker mode="time" :value="form.endTime" @change="onEndTimeChange">
              <view class="picker-value" :class="{ placeholder: !form.endTime }">
                {{ form.endTime || '选择时间' }}
              </view>
            </picker>
          </view>
        </view>
      </view>

      <!-- 教室与人数 -->
      <view class="form-group">
        <text class="group-title">场地信息</text>
        <view class="form-item">
          <text class="label">目标教室</text>
          <picker mode="selector" :range="classrooms" range-key="name" @change="onClassroomChange">
            <view class="picker-value" :class="{ placeholder: !form.classroomId }">
              {{ selectedClassroomName || '请选择教室' }}
            </view>
          </picker>
        </view>
        <view class="form-item">
          <text class="label">预计人数</text>
          <input type="number" v-model="form.peopleCount" placeholder="请输入使用人数" />
        </view>
      </view>

      <!-- 联系与用途 -->
      <view class="form-group">
        <text class="group-title">详细说明</text>
        <view class="form-item">
          <text class="label">联系电话</text>
          <input type="number" v-model="form.phone" placeholder="请输入手机号码" />
        </view>
        <view class="form-item">
          <text class="label">用途说明</text>
          <textarea 
            v-model="form.reason" 
            placeholder="请详细描述使用用途（如：班会、社团活动等）" 
            class="textarea"
          />
        </view>
      </view>

      <!-- 底部信息卡 -->
      <view class="info-card">
        <text class="info-title">申请须知</text>
        <text class="info-text">1. 请至少提前 1 个工作日提交申请。</text>
        <text class="info-text">2. 教室使用期间请保持卫生，爱护公物。</text>
        <text class="info-text">3. 审批流程：辅导员审核 -> 学院审核 -> 教务处备案。</text>
      </view>
    </view>

    <!-- 底部提交按钮 -->
    <view class="bottom-bar">
      <button class="submit-btn" :disabled="isSubmitting" @click="handleSubmit">
        提交申请
      </button>
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getClassroomList, submitApplication } from '@/api/apply'

const form = ref({
  date: '',
  startTime: '',
  endTime: '',
  classroomId: '',
  peopleCount: '',
  phone: '',
  reason: ''
})

const classrooms = ref<any[]>([])
const isSubmitting = ref(false)

const selectedClassroomName = computed(() => {
  const room = classrooms.value.find(c => c.id === form.value.classroomId)
  return room ? room.name : ''
})

const loadClassrooms = async () => {
  try {
    const res = await getClassroomList()
    classrooms.value = res.rows || []
  } catch (error) {
    console.error('Failed to load classrooms', error)
  }
}

onMounted(() => {
  loadClassrooms()
})

const onDateChange = (e: any) => form.value.date = e.detail.value
const onStartTimeChange = (e: any) => form.value.startTime = e.detail.value
const onEndTimeChange = (e: any) => form.value.endTime = e.detail.value
const onClassroomChange = (e: any) => {
  const index = e.detail.value
  form.value.classroomId = classrooms.value[index].id
}

const handleSubmit = async () => {
  if (!form.value.date || !form.value.startTime || !form.value.endTime || !form.value.classroomId || !form.value.reason) {
    uni.showToast({ title: '请填写完整信息', icon: 'none' })
    return
  }

  isSubmitting.value = true
  try {
    await submitApplication(form.value)
    uni.showToast({ title: '提交成功', icon: 'success' })
    setTimeout(() => {
      uni.navigateBack()
    }, 1500)
  } catch (error) {
    console.error('Submit failed', error)
    uni.showToast({ title: '提交失败', icon: 'none' })
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped lang="scss">
@import '@/styles/theme.scss';

.apply-page {
  min-height: 100vh;
  background: $bg-page;
  padding-bottom: calc(120rpx + env(safe-area-inset-bottom));
}

.hero-section {
  background: linear-gradient(135deg, $primary-40 0%, $primary-60 100%);
  padding: 64rpx $spacing-md 80rpx;
  color: $text-inverse;

  .title {
    font-size: 48rpx;
    font-weight: 700;
    display: block;
    margin-bottom: $spacing-xs;
  }

  .subtitle {
    font-size: 28rpx;
    opacity: 0.9;
  }
}

.form-container {
  margin-top: -40rpx;
  padding: 0 $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.form-group {
  background: $bg-card;
  border-radius: $radius-lg;
  padding: $spacing-md;
  box-shadow: $elevation-1;
  animation: $animation-fade-in-up;

  .group-title {
    font-size: 32rpx;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: $spacing-md;
    display: block;
  }

  .form-row {
    display: flex;
    gap: $spacing-md;
  }

  .form-item {
    margin-bottom: $spacing-md;

    &.half {
      flex: 1;
    }

    &:last-child {
      margin-bottom: 0;
    }

    .label {
      font-size: 28rpx;
      color: $text-secondary;
      margin-bottom: 8rpx;
      display: block;
    }

    input, .picker-value {
      height: 88rpx;
      background: $bg-secondary;
      border-radius: $radius-md;
      padding: 0 $spacing-md;
      font-size: 28rpx;
      color: $text-primary;
      display: flex;
      align-items: center;
      box-sizing: border-box;

      &.placeholder {
        color: $text-tertiary;
      }
    }

    .textarea {
      width: 100%;
      height: 200rpx;
      background: $bg-secondary;
      border-radius: $radius-md;
      padding: $spacing-md;
      font-size: 28rpx;
      color: $text-primary;
      box-sizing: border-box;
    }
  }
}

.info-card {
  background: $primary-95;
  border-radius: $radius-lg;
  padding: $spacing-md;
  border: 1px solid $primary-80;
  animation: $animation-fade-in-up;
  animation-delay: 0.2s;
  animation-fill-mode: both;

  .info-title {
    font-size: 28rpx;
    font-weight: 600;
    color: $primary-40;
    margin-bottom: 8rpx;
    display: block;
  }

  .info-text {
    font-size: 24rpx;
    color: $text-secondary;
    line-height: 1.6;
    display: block;
  }
}

.bottom-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: $bg-card;
  padding: $spacing-sm $spacing-md;
  padding-bottom: calc($spacing-sm + env(safe-area-inset-bottom));
  box-shadow: 0 -4rpx 16rpx rgba(0, 0, 0, 0.05);

  .submit-btn {
    height: 88rpx;
    border-radius: $radius-pill;
    background: linear-gradient(90deg, $primary-40 0%, $primary-50 100%);
    color: $text-inverse;
    font-size: 32rpx;
    font-weight: 600;
    display: flex;
    align-items: center;
    justify-content: center;

    &:active {
      transform: scale(0.98);
    }

    &[disabled] {
      opacity: 0.6;
    }
  }
}
</style>
