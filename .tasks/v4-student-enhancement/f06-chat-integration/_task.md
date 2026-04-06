# F-V4-06：Chat 页面集成增强

## 元信息
- **任务 ID**: F-V4-06
- **优先级**: P0
- **类型**: feature
- **批次**: batch_2（串行，第 3 个，最终集成）
- **预计工作量**: 3-4 小时
- **前置依赖**: F-V4-01, F-V4-03, F-V4-05, F-V4-05-A2

## 目标

将 B1/B2/A2 相关的 chat/index.vue 改动统一集成。此任务是 chat/index.vue 的唯一写入者（batch_2 阶段）。

## 背景

- F-V4-01 已完成知识详情页 API 对接
- F-V4-03 已完成会话历史页面
- F-V4-05 已完成快捷问题动态化
- F-V4-05-A2 已完成来源弹层 markdown 渲染
- 现在需要在 chat 页面集成所有功能

## 范围

### In Scope
1. **历史导航按钮**：navbar 区域增加"历史记录"入口
2. **来源点击闭环**：handleSourceClick 优先跳知识详情页
3. **会话持久化集成**：
   - sendMessage 时如无 conversationId 则先 createConversation
   - AI 回复完成后保存 user+AI 消息到后端
   - onLoad 时如有 conversationId 参数则加载历史消息
4. **快捷问题集成**：在 onMounted 中调用获取建议问题（如 F-V4-05 实现了远程获取）

### Out of Scope
- history.vue 页面本身（由 F-V4-03 完成）
- knowledge/detail.vue（由 F-V4-01 完成）
- 会话删除/归档功能

## 技术要点

### 1. 历史导航按钮

```vue
<template>
  <view class="navbar">
    <text class="title">医小管</text>
    <!-- 新增历史按钮 -->
    <view class="nav-actions">
      <view class="history-btn" @click="goToHistory">
        <text class="icon">📋</text>
      </view>
    </view>
  </view>
</template>

<script setup lang="ts">
const goToHistory = () => {
  uni.navigateTo({
    url: '/pages/chat/history'
  })
}
</script>
```

### 2. 来源点击闭环

```typescript
const handleSourceClick = (source: any) => {
  // 优先跳知识详情页
  if (source.entryId) {
    uni.navigateTo({
      url: `/pages/knowledge/detail?id=${source.entryId}`
    })
    return
  }
  
  // 降级：弹层显示摘要
  if (source.content) {
    currentSource.value = source
    showSourcePreview.value = true
    return
  }
  
  // 兜底：外链
  if (source.url) {
    // #ifdef H5
    window.open(source.url, '_blank')
    // #endif
    // #ifndef H5
    uni.navigateTo({
      url: `/pages/webview/index?url=${encodeURIComponent(source.url)}`
    })
    // #endif
  }
}
```

### 3. 会话持久化

```typescript
import { 
  createConversation, 
  getHistory, 
  sendMessage as sendMessageAPI 
} from '@/api/chat'

const conversationId = ref<number | null>(null)

// 页面加载时
onLoad((options: any) => {
  if (options.conversationId) {
    conversationId.value = parseInt(options.conversationId)
    loadHistory()
  }
})

// 加载历史消息
const loadHistory = async () => {
  try {
    const history = await getHistory(conversationId.value!)
    messages.value = history.data || []
  } catch (error) {
    console.error('加载历史消息失败:', error)
  }
}

// 发送消息时
const sendMessage = async () => {
  // 如果没有 conversationId，先创建会话
  if (!conversationId.value) {
    try {
      const conv = await createConversation({ 
        title: userInput.value.slice(0, 20) 
      })
      conversationId.value = conv.data.id
    } catch (error) {
      console.error('创建会话失败:', error)
      // 继续执行，不阻塞对话
    }
  }
  
  // 发送消息到 AI
  // ... 现有逻辑 ...
  
  // AI 回复完成后保存到后端
  if (conversationId.value) {
    try {
      await sendMessageAPI(conversationId.value, {
        role: 'user',
        content: userInput.value
      })
      await sendMessageAPI(conversationId.value, {
        role: 'assistant',
        content: aiResponse
      })
    } catch (error) {
      console.error('保存消息失败:', error)
      // 不影响前端显示
    }
  }
}
```

## 完成标准

### L0: 存在性检查
- 编译无错误
- navbar 包含历史入口按钮
- handleSourceClick 包含 entryId 判断逻辑
- 会话持久化相关代码存在

### L1: 静态检查
- TypeScript 编译无错误
- 无 ESLint error
- API 调用格式正确

### L2: 运行时检查
- H5 预览：点击历史按钮跳转到历史页
- 来源点击跳转详情页（有 entryId 时）
- 来源点击显示弹层（无 entryId 时）
- 发送消息不报错

### L3: 语义检查（需 business-api 运行）
- 发送消息后刷新页面，消息从后端恢复
- 从历史页进入会话，历史消息正确加载
- 来源引用跳转到知识详情页，内容完整显示

## 文件清单

### 必须修改
- `apps/student-app/src/pages/chat/index.vue`

### 必须阅读
- `apps/student-app/src/api/chat.ts` (会话/消息 API)
- `apps/student-app/src/pages/chat/history.vue` (F-V4-03 产出)
- `apps/student-app/src/pages/knowledge/detail.vue` (F-V4-01 产出)

## 执行提示

1. 先添加历史导航按钮（navbar 区域）
2. 修改 handleSourceClick 逻辑（优先跳详情页）
3. 实现会话持久化逻辑：
   - onLoad 加载历史
   - sendMessage 创建会话
   - AI 回复后保存消息
4. 测试各个功能点
5. 集成测试

## 注意事项

- **此任务是 batch_2 的最后一个任务**，是 chat/index.vue 的最终集成
- **必须在 F-V4-01, F-V4-03, F-V4-05, F-V4-05-A2 全部完成后执行**
- 会话持久化失败不应阻塞前端对话功能
- 优雅处理所有 API 失败情况

## 风险

- **RISK-V4-01**: business-api 未运行导致会话 API 不可用
  - 缓解：L0-L2 可在无后端情况下通过
  - 会话持久化失败不影响前端对话
- **RISK-V4-02**: 改动面大，需重点 review
  - 缓解：分步实现，逐个功能点测试

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: Lint 检查
npm run lint

# L2: 启动 dev server
npm run dev:h5
# 手动测试：
# 1. 点击历史按钮 → 跳转历史页
# 2. 发送问题 → 点击来源 → 跳转详情页
# 3. 发送消息 → 刷新页面 → 消息恢复（需后端）
```
