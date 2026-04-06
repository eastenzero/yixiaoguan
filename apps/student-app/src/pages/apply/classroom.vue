<template>
  <view class="classroom-apply-page">
    <!-- 顶部引导区 -->
    <view class="form-hero">
      <view class="hero-content">
        <text class="hero-title">预约申请单</text>
        <text class="hero-desc">请填写下方表单，我们将根据教学资源占用情况在24小时内完成审核。</text>
      </view>
      <IconCalendarDays size="128" class="hero-bg-icon" />
    </view>

    <!-- 时间选择区 -->
    <view class="form-section">
      <view class="section-header">
        <view class="section-line"></view>
        <IconCalendar size="16" />
        <text class="section-title">时间选择</text>
      </view>
      <view class="section-card">
        <!-- 使用日期 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">使用日期</text>
            <text class="label-required">*</text>
          </view>
          <picker mode="date" :start="minDate" :end="maxDate" :value="form.applyDate" @change="onDateChange">
            <view class="form-picker" :class="{ 'is-empty': !form.applyDate }">
              <text class="picker-text">{{ form.applyDate || '请选择使用日期' }}</text>
              <text class="picker-arrow">›</text>
            </view>
          </picker>
        </view>

        <!-- 开始时间 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">开始时间</text>
            <text class="label-required">*</text>
          </view>
          <picker mode="time" :value="form.startTime" @change="onStartTimeChange">
            <view class="form-picker" :class="{ 'is-empty': !form.startTime }">
              <text class="picker-text">{{ form.startTime || '请选择开始时间' }}</text>
              <text class="picker-arrow">›</text>
            </view>
          </picker>
        </view>

        <!-- 结束时间 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">结束时间</text>
            <text class="label-required">*</text>
          </view>
          <picker mode="time" :value="form.endTime" @change="onEndTimeChange">
            <view class="form-picker" :class="{ 'is-empty': !form.endTime }">
              <text class="picker-text">{{ form.endTime || '请选择结束时间' }}</text>
              <text class="picker-arrow">›</text>
            </view>
          </picker>
        </view>
      </view>
    </view>

    <!-- 教室选择区 -->
    <view class="form-section">
      <view class="section-header">
        <view class="section-line"></view>
        <IconBuilding2 size="16" />
        <text class="section-title">教室选择</text>
      </view>
      <view class="section-card">
        <!-- 教室选择 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">选择教室</text>
            <text class="label-required">*</text>
          </view>
          <picker 
            mode="selector" 
            :range="classroomOptions" 
            :value="classroomIndex"
            @change="onClassroomChange"
          >
            <view class="form-picker" :class="{ 'is-empty': !form.classroomId }">
              <text class="picker-text">{{ selectedClassroomName }}</text>
              <text class="picker-arrow">›</text>
            </view>
          </picker>
        </view>

        <!-- 预计人数 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">预计人数</text>
          </view>
          <input 
            class="form-input" 
            type="number" 
            v-model="form.attendeeCount"
            placeholder="请输入预计使用人数"
            placeholder-class="input-placeholder"
          />
        </view>
      </view>
    </view>

    <!-- 联系信息区 -->
    <view class="form-section">
      <view class="section-header">
        <view class="section-line"></view>
        <IconUser size="16" />
        <text class="section-title">联系信息</text>
      </view>
      <view class="section-card">
        <!-- 联系电话 -->
        <view class="form-item">
          <view class="form-label">
            <text class="label-text">联系电话</text>
          </view>
          <input 
            class="form-input" 
            type="number" 
            v-model="form.contactPhone"
            placeholder="选填，方便联系确认"
            placeholder-class="input-placeholder"
            maxlength="11"
          />
        </view>

        <!-- 用途说明 -->
        <view class="form-item form-item-block">
          <view class="form-label">
            <text class="label-text">用途说明</text>
            <text class="label-required">*</text>
          </view>
          <textarea 
            class="form-textarea" 
            v-model="form.purpose"
            placeholder="请简述申请用途，如：学术交流、学生会会议等..."
            placeholder-class="input-placeholder"
            maxlength="200"
          />
          <text class="textarea-count">{{ form.purpose.length }}/200</text>
        </view>
      </view>
    </view>

    <!-- 提交按钮 -->
    <view class="submit-section">
      <button 
        class="submit-btn" 
        :class="{ 'is-loading': isSubmitting }"
        :disabled="isSubmitting || !isFormValid"
        @click="handleSubmit"
      >
        <text v-if="isSubmitting">提交中...</text>
        <text v-else>提交申请</text>
      </button>
    </view>

    <!-- 底部信息区 -->
    <view class="form-footer">
      <view class="info-card">
        <view class="info-header">
          <IconGavel size="20" color="#006565" />
          <text class="info-title">申请规则</text>
        </view>
        <text class="info-text">1. 至少提前2个工作日申请。\n2. 申请人须负责室内卫生。</text>
      </view>
      <view class="info-card">
        <view class="info-header">
          <IconListChecks size="20" color="#206393" />
          <text class="info-title">审核流程</text>
        </view>
        <text class="info-text">1. 提交申请单。\n2. 院系初审及排课确认。</text>
      </view>
    </view>

    <!-- 底部留白 -->
    <view class="bottom-safe"></view>
  </view>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getClassroomList, submitApplication, type Classroom, type ApplyForm } from '@/api/apply'
import { useUserStore } from '@/stores/user'
import IconCalendarDays from '@/components/icons/IconCalendarDays.vue'
import IconCalendar from '@/components/icons/IconCalendar.vue'
import IconBuilding2 from '@/components/icons/IconBuilding2.vue'
import IconUser from '@/components/icons/IconUser.vue'
import IconGavel from '@/components/icons/IconGavel.vue'
import IconListChecks from '@/components/icons/IconListChecks.vue'

const userStore = useUserStore()

// ===== 状态数据 =====
const classrooms = ref<Classroom[]>([])
const classroomIndex = ref(-1)
const isSubmitting = ref(false)
const isLoading = ref(false)

const form = ref<ApplyForm>({
  classroomId: 0,
  applyDate: '',
  startTime: '',
  endTime: '',
  purpose: '',
  attendeeCount: undefined,
  contactPhone: ''
})

// ===== 计算属性 =====

// 教室选择器选项
const classroomOptions = computed(() => {
  return classrooms.value.map(item => `${item.building} ${item.roomNumber}${item.capacity ? ` (${item.capacity}人)` : ''}`)
})

// 选中的教室名称
const selectedClassroomName = computed(() => {
  if (classroomIndex.value < 0 || !classrooms.value[classroomIndex.value]) {
    return '请选择教室'
  }
  const room = classrooms.value[classroomIndex.value]
  return `${room.building} ${room.roomNumber}`
})

// 最小日期（明天）
const minDate = computed(() => {
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  return formatDate(tomorrow)
})

// 最大日期（30天后）
const maxDate = computed(() => {
  const max = new Date()
  max.setDate(max.getDate() + 30)
  return formatDate(max)
})

// 表单是否有效
const isFormValid = computed(() => {
  return (
    form.value.classroomId > 0 &&
    form.value.applyDate &&
    form.value.startTime &&
    form.value.endTime &&
    form.value.purpose.trim().length > 0 &&
    isTimeValid.value
  )
})

// 时间是否有效（结束时间晚于开始时间）
const isTimeValid = computed(() => {
  if (!form.value.startTime || !form.value.endTime) return true
  return form.value.endTime > form.value.startTime
})

// ===== 方法 =====

// 格式化日期为 YYYY-MM-DD
function formatDate(date: Date): string {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// 加载教室列表
async function loadClassrooms() {
  isLoading.value = true
  try {
    const res = await getClassroomList({ status: 1, pageSize: 100 })
    classrooms.value = res.rows || []
    if (classrooms.value.length === 0) {
      uni.showToast({
        title: '暂无可申请教室',
        icon: 'none'
      })
    }
  } catch (error) {
    console.error('加载教室列表失败', error)
    uni.showToast({
      title: '教室列表加载失败',
      icon: 'none'
    })
  } finally {
    isLoading.value = false
  }
}

// 教室选择变更
function onClassroomChange(e: any) {
  classroomIndex.value = e.detail.value
  const room = classrooms.value[classroomIndex.value]
  if (room) {
    form.value.classroomId = room.id
  }
}

// 日期选择变更
function onDateChange(e: any) {
  form.value.applyDate = e.detail.value
}

// 开始时间选择变更
function onStartTimeChange(e: any) {
  form.value.startTime = e.detail.value
  // 如果结束时间早于开始时间，清空结束时间
  if (form.value.endTime && form.value.endTime <= e.detail.value) {
    form.value.endTime = ''
    uni.showToast({
      title: '请重新选择结束时间',
      icon: 'none'
    })
  }
}

// 结束时间选择变更
function onEndTimeChange(e: any) {
  const endTime = e.detail.value
  if (form.value.startTime && endTime <= form.value.startTime) {
    uni.showToast({
      title: '结束时间必须晚于开始时间',
      icon: 'none'
    })
    return
  }
  form.value.endTime = endTime
}

// 提交表单
async function handleSubmit() {
  if (!isFormValid.value) {
    if (!isTimeValid.value) {
      uni.showToast({
        title: '结束时间必须晚于开始时间',
        icon: 'none'
      })
    } else {
      uni.showToast({
        title: '请填写完整信息',
        icon: 'none'
      })
    }
    return
  }

  // 手机号格式校验（如果有填）
  if (form.value.contactPhone && !/^1[3-9]\d{9}$/.test(form.value.contactPhone)) {
    uni.showToast({
      title: '请输入正确的手机号',
      icon: 'none'
    })
    return
  }

  isSubmitting.value = true
  uni.showLoading({ title: '提交中...' })

  try {
    const submitData: ApplyForm = {
      ...form.value,
      attendeeCount: form.value.attendeeCount ? Number(form.value.attendeeCount) : undefined,
      purpose: form.value.purpose.trim()
    }
    
    await submitApplication(submitData)
    
    uni.hideLoading()
    uni.showModal({
      title: '提交成功',
      content: '您的申请已提交，请耐心等待审批结果',
      showCancel: false,
      success: () => {
        // 跳转到我的申请页
        uni.switchTab({
          url: '/pages/apply/status'
        })
      }
    })
  } catch (error) {
    uni.hideLoading()
    console.error('提交申请失败', error)
    // 错误已在 request.ts 中统一提示
  } finally {
    isSubmitting.value = false
  }
}

// ===== 生命周期 =====
onMounted(() => {
  loadClassrooms()
})
</script>

<style scoped lang="scss">
page {
  background-color: #f0f7f5;
}

// 颜色变量（遵循设计规范）
$primary: #006a64;
$primary-container: #8bf2e8;
$on-primary: #ffffff;
$on-primary-container: #00201d;
$surface: #f0f7f5;
$surface-container-low: #eff5f3;
$surface-container-lowest: #ffffff;
$surface-container-highest: rgba(0, 106, 100, 0.06);
$on-surface: #171d1c;
$on-surface-variant: #3f4947;
$outline-variant: #bec9c6;

.classroom-apply-page {
  min-height: 100vh;
  background: $surface;
  padding: 24rpx;
}

// 顶部引导区
.form-hero {
  position: relative;
  background: linear-gradient(135deg, $primary, $primary-container);
  border-radius: 24rpx;
  padding: 40rpx 32rpx;
  margin-bottom: 32rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 16rpx rgba(0, 106, 100, 0.15);
}

.hero-content {
  position: relative;
  z-index: 1;
}

.hero-title {
  display: block;
  font-size: 40rpx;
  font-weight: 700;
  color: $on-primary;
  margin-bottom: 12rpx;
}

.hero-desc {
  display: block;
  font-size: 28rpx;
  color: rgba($on-primary, 0.9);
  line-height: 1.5;
  max-width: 70%;
}

.hero-bg-icon {
  position: absolute;
  right: -20rpx;
  bottom: -20rpx;
  opacity: 0.1;
  color: $on-primary;
}

// 表单分区
.form-section {
  margin-bottom: 32rpx;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 16rpx;
  margin-bottom: 20rpx;
  padding: 0 8rpx;
}

.section-line {
  width: 6rpx;
  height: 32rpx;
  background: linear-gradient(180deg, $primary, $primary-container);
  border-radius: 4rpx;
}

.section-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $on-surface;
}

// 卡片式表单容器
.section-card {
  background: $surface-container-lowest;
  border-radius: 24rpx;
  padding: 40rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.06);
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 16rpx;
  margin-bottom: 32rpx;

  &:last-child {
    margin-bottom: 0;
  }
}

.form-item-block {
  // 用途说明占满宽度
}

.form-label {
  display: flex;
  align-items: center;
  gap: 8rpx;
}

.label-text {
  font-size: 30rpx;
  font-weight: 500;
  color: $on-surface;
}

.label-required {
  font-size: 30rpx;
  color: #ef4444;
}

// 输入框样式（Soft Fields）
.form-input {
  height: 88rpx;
  background: $surface-container-highest;
  border-radius: 16rpx;
  padding: 0 24rpx;
  font-size: 30rpx;
  color: $on-surface;
  border: none;
  outline: none;
  transition: box-shadow 0.2s ease;
  
  &:focus {
    box-shadow: 0 0 0 2px rgba(0, 168, 150, 0.2);
  }
}

.input-placeholder {
  color: $outline-variant;
  font-size: 28rpx;
}

// 选择器样式
.form-picker {
  height: 88rpx;
  background: $surface-container-highest;
  border-radius: 16rpx;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: none;
}

.picker-text {
  font-size: 30rpx;
  color: $on-surface;
}

.form-picker.is-empty .picker-text {
  color: $outline-variant;
  font-size: 28rpx;
}

.picker-arrow {
  font-size: 36rpx;
  color: $on-surface-variant;
  transform: rotate(90deg);
}

// 文本域样式
.form-textarea {
  width: auto;
  height: 200rpx;
  background: $surface-container-highest;
  border-radius: 16rpx;
  padding: 24rpx;
  font-size: 30rpx;
  color: $on-surface;
  line-height: 1.6;
  border: none;
  outline: none;
  transition: box-shadow 0.2s ease;
  
  &:focus {
    box-shadow: 0 0 0 2px rgba(0, 168, 150, 0.2);
  }
}

.textarea-count {
  font-size: 24rpx;
  color: $on-surface-variant;
  text-align: right;
}

// 提交区域
.submit-section {
  padding: 24rpx 0;
  margin-bottom: 24rpx;
}

.submit-btn {
  width: 100%;
  height: 96rpx;
  background: linear-gradient(135deg, $primary, $primary-container);
  border-radius: 48rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32rpx;
  font-weight: 600;
  color: $on-primary;
  border: none;
  box-shadow: 0 8rpx 24rpx rgba(0, 106, 100, 0.25);
  
  &:disabled {
    opacity: 0.5;
  }
  
  &.is-loading {
    opacity: 0.8;
  }
  
  &:active {
    opacity: 0.9;
    transform: translateY(2rpx);
  }
}

// 底部信息区
.form-footer {
  display: flex;
  flex-direction: column;
  gap: 24rpx;
  margin-bottom: 24rpx;
}

.info-card {
  background: $surface-container-lowest;
  border-radius: 20rpx;
  padding: 28rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
}

.info-header {
  display: flex;
  align-items: center;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.info-title {
  font-size: 30rpx;
  font-weight: 600;
  color: $on-surface;
}

.info-text {
  font-size: 28rpx;
  color: $on-surface-variant;
  line-height: 1.8;
  white-space: pre-line;
}

.bottom-safe {
  height: 40rpx;
}
</style>
