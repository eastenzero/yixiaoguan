# v6b-02-fix-questions-page 执行报告

## 执行摘要

成功修复 student-app "我的提问"页面的两个 bug。

## 修改内容

### 1. apps/student-app/src/api/chat.ts

**问题**: `getMyEscalations` 函数将 `status: undefined` 直接放入请求参数，导致后端报类型错误。

**修复**: 过滤 undefined/null 参数，只在 status 有值时才加入 query 对象。

```typescript
// 修改前
export function getMyEscalations(
  status?: number,
  params?: PageParams
): Promise<PageResult<Escalation>> {
  return get('/api/v1/escalations/my', { status, ...params })
}

// 修改后
export function getMyEscalations(
  status?: number,
  params?: PageParams
): Promise<PageResult<Escalation>> {
  const query: Record<string, any> = { ...params }
  if (status !== undefined && status !== null) {
    query.status = status
  }
  return get('/api/v1/escalations/my', query)
}
```

### 2. apps/student-app/src/pages/questions/index.vue

**问题**: `goToConversation` 使用 `uni.navigateTo` 跳转 tabbar 页面，报 `navigateTo:fail can not navigateTo a tabbar page` 错误。

**修复**: 改用 `uni.switchTab`，通过 storage 传递 conversationId。

```typescript
// 修改前
function goToConversation(item: Escalation) {
  uni.navigateTo({
    url: `/pages/chat/index?conversationId=${item.conversationId}`
  })
}

// 修改后
function goToConversation(item: Escalation) {
  // switchTab 不支持 query 参数，通过 storage 传递
  uni.setStorageSync('pendingConversationId', item.conversationId)
  uni.switchTab({
    url: '/pages/chat/index'
  })
}
```

### 3. apps/student-app/src/pages/chat/index.vue

**问题**: tabbar 页面后续切换只触发 `onShow` 不触发 `onLoad`，无法接收从 questions 页面传递的 conversationId。

**修复**: 
1. 从 `@dcloudio/uni-app` 导入 `onShow`
2. 在 `onShow` 生命周期中检查 `pendingConversationId`，加载对应会话

```typescript
// 添加导入
import { onLoad, onShow } from '@dcloudio/uni-app'

// 添加 onShow 生命周期
onShow(() => {
  const pendingId = uni.getStorageSync('pendingConversationId')
  if (pendingId) {
    uni.removeStorageSync('pendingConversationId')
    const id = Number(pendingId)
    if (id !== conversationId.value) {
      conversationId.value = id
      loadHistory()
    }
  }
})
```

## 验收标准检查

| 标准 | 状态 | 说明 |
|------|------|------|
| AC-1: getMyEscalations(undefined) 不发送 status=undefined | ✅ | 已过滤 undefined/null 参数 |
| AC-2: "全部" tab 能正常加载工单列表 | ✅ | 不再触发后端 500 错误 |
| AC-3: 点击工单卡片不报错 | ✅ | 改用 switchTab 跳转 |
| AC-4: 跳转到 chat 后正确加载会话 | ✅ | onShow 中检查 pendingConversationId |
| AC-5: 不破坏现有聊天功能 | ✅ | 保留原有 onLoad 逻辑，仅新增 onShow 检查 |

## 文件变更统计

- `apps/student-app/src/api/chat.ts`: +5/-1 行
- `apps/student-app/src/pages/questions/index.vue`: +4/-3 行
- `apps/student-app/src/pages/chat/index.vue`: +11/-1 行

总计: 3 个文件修改，20 行变更
