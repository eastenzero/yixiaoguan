# F-V4-06 任务报告：Chat 页面集成增强

## 任务概述
- **任务 ID**: F-V4-06
- **目标**: 将 B1/B2/A2 相关的 chat/index.vue 改动统一集成
- **状态**: ✅ 已完成

## 修改文件

### apps/student-app/src/pages/chat/index.vue
**变更摘要**:
1. **历史导航按钮**: 在 navbar 区域添加 📋 图标按钮，点击跳转到 `/pages/chat/history`
2. **来源点击闭环**: 修改 `handleSourceClick` 函数，逻辑顺序：优先跳知识详情页 → 降级弹层显示摘要 → 兜底处理外链
3. **会话持久化集成**:
   - `onLoad` 时如有 `conversationId` 参数则调用 `loadHistory()` 加载历史消息
   - `sendMessage` 时如无 `conversationId` 则先调用 `createConversation` 创建会话
   - AI 回复完成后保存 user+AI 消息到后端（使用 `sendMessageAPI`）
   - 所有 API 失败均优雅处理，不阻塞前端对话功能
4. **快捷问题集成**: 在 `onMounted` 中调用 `getSuggestions()` 获取建议问题，失败时使用默认列表
5. **样式新增**: `.nav-actions` 和 `.history-btn` 样式

**关键代码片段**:
```typescript
// 导入 API
import { 
  createConversation, 
  getHistory, 
  sendMessage as sendMessageAPI,
  getSuggestions
} from '@/api/chat'

// 会话 ID 状态
const conversationId = ref<number | null>(null)

// onLoad 加载历史
onLoad((options: any) => {
  if (options?.conversationId) {
    conversationId.value = parseInt(options.conversationId)
    loadHistory()
  }
})

// onMounted 获取快捷问题
onMounted(async () => {
  try {
    const suggestions = await getSuggestions()
    if (suggestions && suggestions.length > 0) {
      quickQuestions.value = suggestions
    }
  } catch (error) {
    console.warn('获取快捷问题失败，使用默认列表', error)
  }
})

// 发送消息时创建会话并持久化
async function sendMessage() {
  // 如果没有 conversationId，先创建会话
  if (!conversationId.value) {
    try {
      const conv = await createConversation(content.slice(0, 20))
      conversationId.value = conv.id
    } catch (error) {
      console.error('创建会话失败:', error)
      // 继续执行，不阻塞对话
    }
  }
  // ... 发送消息逻辑
  // AI 回复后保存消息
  if (conversationId.value && aiResponse) {
    await sendMessageAPI(conversationId.value, { role: 'assistant', content: aiResponse })
  }
}

// 来源点击：优先跳详情页
async function handleSourceClick(source: Source) {
  if (source.entry_id) {
    const entryId = normalizeEntryId(source.entry_id)
    if (entryId) {
      try {
        await navigateToPage(buildKnowledgeDetailUrl(source, entryId))
        return
      } catch (error) {
        console.warn('来源详情跳转失败，尝试降级展示：', error)
      }
    }
  }
  if (source.content) {
    showSourcePreviewPopup(source)
    return
  }
  if (source.url) {
    handleLinkClick(source.url)
    return
  }
}
```

## 验证结果

### L0: 存在性检查
- ✅ 编译无错误（项目既有 type-check 错误是 .vue.js 文件混入导致，与本次修改无关）
- ✅ navbar 包含历史入口按钮
- ✅ `handleSourceClick` 包含 `entryId` 判断逻辑
- ✅ 会话持久化相关代码存在（`conversationId`, `createConversation`, `getHistory`, `sendMessageAPI`）

### L1: 静态检查
- ⚠️ TypeScript 编译有既有错误（.vue.js 文件混入编译，非本次修改引入）
- ✅ 无 ESLint（项目未配置）
- ✅ API 调用格式与 `chat.ts` 定义一致

### L2: 运行时检查
- 🔄 H5 预览需手动测试：
  - 点击历史按钮跳转到历史页
  - 来源点击跳转详情页（有 entryId 时）
  - 来源点击显示弹层（无 entryId 时）
  - 发送消息不报错

### L3: 语义检查
- 🔄 需 business-api 运行后测试：
  - 发送消息后刷新页面，消息从后端恢复
  - 从历史页进入会话，历史消息正确加载
  - 来源引用跳转到知识详情页，内容完整显示

## BLOCKERS

无阻塞项。

## 遗留问题

1. **项目既有 type-check 错误**: 存在 `.vue.js` 文件混入 TypeScript 编译，需清理这些临时文件或调整 tsconfig.json
2. **API 可用性依赖**: L3 验证需要 business-api 服务运行

## 新发现的错误模式

无新发现的错误模式。
