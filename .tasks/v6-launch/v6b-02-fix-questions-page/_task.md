# v6b-02-fix-questions-page

- **parent**: v6-launch
- **status**: pending
- **assignee**: kimi-t3
- **priority**: P0-blocker

## 目标

修复 student-app 的"我的提问"页面两个 bug，使页面能正常加载工单列表并正确跳转。

## Bug 1: status=undefined 参数错误

**现象**: 后端报 `参数[status]要求类型为：'java.lang.Integer'，但输入值为：'undefined'`

**根因**: `apps/student-app/src/api/chat.ts` 的 `getMyEscalations` 函数将 `status: undefined` 直接放入请求参数，UniApp 的 `uni.request` 将其序列化为字符串 `"undefined"` 发送给后端。

**修复**: 在 `getMyEscalations` 中过滤掉值为 `undefined` 的参数。

修改 `apps/student-app/src/api/chat.ts`:
```typescript
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

## Bug 2: navigateTo tabbar page 错误

**现象**: 点击工单卡片跳转时报 `navigateTo:fail can not navigateTo a tabbar page`

**根因**: `apps/student-app/src/pages/questions/index.vue` 的 `goToConversation` 使用 `uni.navigateTo` 跳转到 `pages/chat/index`，但该页面是 tabbar 页面。UniApp 不允许 `navigateTo` 跳转 tabbar 页面。

**修复**: 改用 `uni.switchTab` 跳转，由于 `switchTab` 不支持 query 参数，需要用全局存储传递 `conversationId`。

修改 `apps/student-app/src/pages/questions/index.vue` 的 `goToConversation`:
```typescript
function goToConversation(item: Escalation) {
  // switchTab 不支持 query 参数，通过 storage 传递
  uni.setStorageSync('pendingConversationId', item.conversationId)
  uni.switchTab({
    url: '/pages/chat/index'
  })
}
```

然后在 `apps/student-app/src/pages/chat/index.vue` 的 onShow 或 onLoad 中检查：
```typescript
// 在 onShow 生命周期中检查是否有待加载的会话
const pendingId = uni.getStorageSync('pendingConversationId')
if (pendingId) {
  uni.removeStorageSync('pendingConversationId')
  conversationId.value = Number(pendingId)
  loadConversation(Number(pendingId))
}
```

注意：只在 chat/index.vue 中添加 storage 检查逻辑，不能破坏现有的对话加载流程。

## 修改范围

**允许修改**:
- `apps/student-app/src/api/chat.ts` （仅 getMyEscalations 函数）
- `apps/student-app/src/pages/questions/index.vue` （仅 goToConversation 函数）
- `apps/student-app/src/pages/chat/index.vue` （仅添加 pendingConversationId 检查）

## 验收标准

- AC-1: `getMyEscalations(undefined)` 不再向后端发送 `status=undefined` 参数
- AC-2: "全部" tab 下能正常加载工单列表（无 500 错误）
- AC-3: 点击工单卡片不再报 `navigateTo tabbar page` 错误
- AC-4: 跳转到 chat 页面后能正确加载对应会话
- AC-5: 不破坏现有聊天功能（SSE、来源引用、呼叫老师）

## 禁止

- 不修改 types/chat.ts
- 不修改 pages.json
- 不新增文件
