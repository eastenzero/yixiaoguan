# v6b-01-fix-callteacher 执行报告

## 修改摘要

修复 `apps/student-app/src/pages/chat/index.vue` 中 `handleCallTeacher()` 函数的两个 bug。

## 修改详情

### Bug 1: messageId 修复
- **问题**: 硬编码 `messageId: 0` 导致后端 FK 约束报错
- **修复**: 动态获取最后一条后端消息的 ID
  ```typescript
  // 查找最后一条来自后端的消息（ID 为纯数字）
  const lastRealMsg = [...messages.value].reverse().find(m => /^\d+$/.test(String(m.id)))
  const messageId = lastRealMsg ? Number(lastRealMsg.id) : 0

  if (!messageId) {
    uni.showToast({ title: '请先发送一条消息再呼叫老师', icon: 'none' })
    return
  }
  ```

### Bug 2: 字段名修复
- **问题**: 使用 `reason` 字段，但后端期望 `questionSummary`
- **修复**: 将 `reason: '学生主动呼叫'` 改为 `questionSummary: '学生主动呼叫'`

## 验收标准检查

| 标准 | 状态 |
|------|------|
| AC-1: `handleCallTeacher` 中不再出现 `messageId: 0` | ✅ 已修复 |
| AC-2: `handleCallTeacher` 中不再出现 `reason` 字段，改为 `questionSummary` | ✅ 已修复 |
| AC-3: 当 messages 中没有后端消息时，弹出提示并 return，不发起 API 调用 | ✅ 已修复 |
| AC-4: 不修改任何其他文件 | ✅ 仅修改 index.vue |
| AC-5: 不破坏现有 SSE 流式对话、来源引用等功能 | ✅ 未影响其他功能 |

## 修改文件

- `apps/student-app/src/pages/chat/index.vue` (第 864-914 行)
