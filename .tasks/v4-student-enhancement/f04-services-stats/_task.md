# F-V4-04：事务导办统计卡片

## 元信息
- **任务 ID**: F-V4-04
- **优先级**: P2
- **类型**: feature
- **批次**: batch_1（并行）
- **预计工作量**: 1-2 小时
- **前置依赖**: 无

## 目标

services/index.vue 顶部添加统计概览卡片区域，显示用户申请和通知数量。

## 背景

- 事务导办页面当前只有功能入口列表
- 缺少用户个人数据概览
- 后端 getMyApplications API 已实现

## 范围

### In Scope
1. "进行中的申请"数量 — 调用 getMyApplications 统计 status=处理中 的数量
2. "待处理通知"数量 — 预留位，当前显示 0 或 mock
3. 数据获取失败时显示 "--" 而非报错

### Out of Scope
- 新增后端接口
- 通知 API 对接（后端通知模块暂未前端化）
- 点击卡片跳转详情（后续迭代）

## 技术要点

1. **API 调用**：
   ```typescript
   import { getMyApplications } from '@/api/apply'
   import { useUserStore } from '@/stores/user'
   
   const userStore = useUserStore()
   const userId = userStore.userInfo.id
   
   // 获取进行中的申请数量
   const res = await getMyApplications(userId, { status: '处理中' })
   const pendingCount = res.data?.length || 0
   ```

2. **错误处理**：
   ```typescript
   try {
     const count = await fetchPendingCount()
     pendingApplications.value = count
   } catch (error) {
     pendingApplications.value = '--' // 失败时显示占位符
   }
   ```

3. **UI 设计**：
   - 卡片式布局，两列网格
   - 数字大号显示，标签小号
   - 与现有页面风格统一（teal 主题）

## 完成标准

### L0: 存在性检查
- 编译无错误
- services/index.vue 包含统计卡片组件

### L1: 静态检查
- TypeScript 编译无错误
- 无 ESLint error
- 统计卡片 DOM 结构存在

### L2: 运行时检查
- H5 预览：事务导办页顶部显示统计区域
- 显示两个统计项（进行中的申请、待处理通知）
- API 失败时显示 "--" 而非崩溃

### L3: 语义检查（需 business-api 运行）
- 进行中的申请数量准确
- 数据刷新正常

## 文件清单

### 必须修改
- `apps/student-app/src/pages/services/index.vue`

### 必须阅读
- `apps/student-app/src/api/apply.ts` (getMyApplications API)
- `apps/student-app/src/stores/user.ts` (用户信息)

## UI 结构参考

```vue
<template>
  <view class="services-page">
    <!-- 统计卡片区域 -->
    <view class="stats-section">
      <view class="stat-card">
        <text class="stat-number">{{ pendingApplications }}</text>
        <text class="stat-label">进行中的申请</text>
      </view>
      <view class="stat-card">
        <text class="stat-number">{{ pendingNotifications }}</text>
        <text class="stat-label">待处理通知</text>
      </view>
    </view>
    
    <!-- 原有功能入口列表 -->
    <view class="service-list">
      <!-- ... -->
    </view>
  </view>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMyApplications } from '@/api/apply'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const pendingApplications = ref<number | string>('--')
const pendingNotifications = ref<number | string>(0) // 预留

onMounted(async () => {
  try {
    const userId = userStore.userInfo.id
    if (!userId) return
    
    const res = await getMyApplications(userId, { status: '处理中' })
    pendingApplications.value = res.data?.length || 0
  } catch (error) {
    console.error('获取统计数据失败:', error)
    pendingApplications.value = '--'
  }
})
</script>

<style lang="scss" scoped>
.stats-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  padding: 16px;
}

.stat-card {
  background: linear-gradient(135deg, #006a64 0%, #008c82 100%);
  border-radius: 12px;
  padding: 20px;
  color: white;
  text-align: center;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  display: block;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  opacity: 0.9;
}
</style>
```

## 执行提示

1. 在 services/index.vue 顶部添加统计卡片区域
2. 实现数据获取逻辑（优雅处理失败）
3. 样式与现有页面保持一致
4. 测试有数据和无数据两种情况

## 风险

- 低风险任务
- API 失败已有降级方案（显示 "--"）
- 通知数量当前为 mock，不影响功能

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: Lint 检查
npm run lint

# L2: 启动 dev server
npm run dev:h5
# 手动访问事务导办页面
```
