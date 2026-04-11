# v6b-01-fix-callteacher

- **parent**: v6-launch
- **status**: pending
- **assignee**: kimi-t3
- **priority**: P0-blocker

## 目标

修复 `handleCallTeacher()` 函数中的两个 bug，使呼叫老师功能能正确创建工单。

## 当前 Bug

1. **messageId: 0** — 后端 yx_escalation.message_id 有 FK 约束引用 yx_message(id)，传 0 直接报 500
2. **reason 字段名错误** — 前端传 `reason`，但 `CreateEscalationParams` 定义的是 `questionSummary`，后端也期望 `questionSummary`

## 修改范围

**仅允许修改**: `apps/student-app/src/pages/chat/index.vue`

## 具体修复

### Bug 1: messageId

在 `handleCallTeacher()` 中，将 `messageId: 0` 改为使用对话中最后一条**来自后端的消息**的 ID。

逻辑：
```
const lastRealMsg = [...messages.value].reverse().find(m => /^\d+$/.test(String(m.id)))
const messageId = lastRealMsg ? Number(lastRealMsg.id) : 0
```

如果 messageId 仍为 0（没有任何历史消息），应该阻止调用并提示用户先发送至少一条消息：
```
if (!messageId) {
  uni.showToast({ title: '请先发送一条消息再呼叫老师', icon: 'none' })
  return
}
```

### Bug 2: 字段名

将 `reason: '学生主动呼叫'` 改为 `questionSummary: '学生主动呼叫'`

## 验收标准

- AC-1: `handleCallTeacher` 中不再出现 `messageId: 0`
- AC-2: `handleCallTeacher` 中不再出现 `reason` 字段，改为 `questionSummary`
- AC-3: 当 messages 中没有后端消息时，弹出提示并 return，不发起 API 调用
- AC-4: 不修改任何其他文件
- AC-5: 不破坏现有 SSE 流式对话、来源引用等功能

## 禁止

- 不要修改 `@/api/chat.ts`
- 不要修改 `@/types/chat.ts`
- 不要修改其他 .vue 文件
- 不要新增文件
