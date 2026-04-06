# F-V4-03：聊天历史记录

## 元信息
- **任务 ID**: F-V4-03
- **优先级**: P0
- **类型**: feature
- **批次**: batch_1（并行）
- **预计工作量**: 3-4 小时
- **前置依赖**: 无

## 目标

新建会话历史列表页，对接已有后端 API，实现对话持久化。

## 背景

- 后端会话/消息 API 已全部实现（ConversationController）
- 前端 api/chat.ts 已定义全部 API 函数，但页面层尚未调用
- 当前 chat 页面无历史记录功能，刷新后对话丢失

## 范围

### In Scope
1. 新建 pages/chat/history.vue — 会话历史列表页
   - 调用 getConversationList() 展示历史会话
   - 每条显示：标题（或首条消息摘要）、最后消息时间、消息数
   - 点击进入对应会话，加载历史消息
   - "新建对话"按钮，调用 createConversation()
   - 空状态提示
2. pages.json 注册新路由

### Out of Scope
- chat/index.vue 修改（由 F-V4-06 统一处理）
- 搜索/删除/归档会话（后续迭代）
- 会话持久化逻辑集成（由 F-V4-06 处理）

## 技术要点

1. **API 调用**：
   ```typescript
   import { getConversationList, createConversation } from '@/api/chat'
   
   // 获取会话列表
   const conversations = await getConversationList()
   
   // 新建会话
   const newConv = await createConversation({ title: '新对话' })
   ```

2. **路由跳转**：
   ```typescript
   // 点击会话进入对话页
   uni.navigateTo({
     url: `/pages/chat/index?conversationId=${conv.id}`
   })
   ```

3. **UI 设计参考**：
   - 列表项卡片式布局
   - teal 渐变标题栏（与 chat 页面风格统一）
   - 空状态：友好提示 + "开始新对话"按钮

4. **数据展示**：
   - 标题：conversation.title 或首条消息摘要（截取前 20 字）
   - 时间：formatTime(conversation.updatedAt)
   - 消息数：conversation.messageCount

## 完成标准

### L0: 存在性检查
- 编译无错误
- pages/chat/history.vue 文件存在
- pages.json 包含新路由

### L1: 静态检查
- pages.json 包含 `pages/chat/history` 路由配置
- TypeScript 编译无错误
- 无 ESLint error

### L2: 运行时检查
- H5 预览：会话历史页渲染正常
- 空状态或已有会话列表可见
- "新建对话"按钮可点击（即使 API 失败也应有 UI 反馈）

### L3: 语义检查（需 business-api 运行）
- 会话列表正确显示历史会话
- 点击会话可跳转到对话页
- 新建对话功能正常

## 文件清单

### 必须创建
- `apps/student-app/src/pages/chat/history.vue` (新建)

### 必须修改
- `apps/student-app/src/pages.json` (新增路由)

### 必须阅读
- `apps/student-app/src/api/chat.ts` (API 函数定义)
- `apps/student-app/src/pages/chat/index.vue` (UI 风格参考)
- `services/business-api/.../conversation/controller/ConversationController.java` (API 响应格式)

## UI 结构参考

```vue
<template>
  <view class="history-page">
    <!-- 导航栏 -->
    <view class="navbar">
      <text class="title">对话历史</text>
    </view>
    
    <!-- 会话列表 -->
    <view class="conversation-list" v-if="conversations.length > 0">
      <view 
        class="conversation-item" 
        v-for="conv in conversations" 
        :key="conv.id"
        @click="enterConversation(conv.id)"
      >
        <view class="conv-title">{{ conv.title || '未命名对话' }}</view>
        <view class="conv-meta">
          <text class="time">{{ formatTime(conv.updatedAt) }}</text>
          <text class="count">{{ conv.messageCount }} 条消息</text>
        </view>
      </view>
    </view>
    
    <!-- 空状态 -->
    <view class="empty-state" v-else>
      <text class="empty-text">还没有对话记录</text>
      <button class="new-btn" @click="createNew">开始新对话</button>
    </view>
    
    <!-- 新建按钮（固定底部） -->
    <view class="fab">
      <button class="fab-btn" @click="createNew">+</button>
    </view>
  </view>
</template>
```

## 执行提示

1. 先创建基础页面结构和样式
2. 实现 API 调用逻辑（优雅处理失败）
3. 实现路由跳转
4. 测试空状态和有数据两种情况
5. 在 pages.json 注册路由

## 风险

- **RISK-V4-01**: business-api 未运行导致会话 API 不可用
  - 缓解：L0-L2 可在无后端情况下通过（代码层验证）
  - 会话列表页应优雅处理 API 失败（显示空状态而非报错）

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: 检查路由注册
cat src/pages.json | grep -A 5 "chat/history"

# L2: 启动 dev server
npm run dev:h5
# 手动访问 http://localhost:5174/#/pages/chat/history
```
