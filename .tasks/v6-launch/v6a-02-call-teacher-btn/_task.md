---
id: "v6a-02-call-teacher-btn"
parent: "v6-launch"
type: "feature"
status: "pending"
tier: "T3"
priority: "high"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/chat/index.vue"

out_of_scope:
  - "apps/teacher-web/**"
  - "services/**"
  - "scripts/**"
  - "deploy/**"
  - "apps/student-app/src/api/**"
  - "apps/student-app/src/styles/**"
  - "apps/student-app/src/pages/home/**"
  - "apps/student-app/src/pages/login/**"
  - "apps/student-app/src/pages/profile/**"
  - "apps/student-app/src/pages/services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/api/chat.ts"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "apps/student-app/src/pages/chat/index.vue 中存在 callTeacher 相关函数和按钮模板"
  L1: "grep -q 'callTeacher' apps/student-app/src/pages/chat/index.vue 返回成功"
  L2: "npx uni build --platform h5 (在 apps/student-app 目录) 成功无错误；或至少无 TypeScript/编译错误"
  L3: "聊天页面可见呼叫老师按钮；点击后按钮变为等待状态且不可重复点击；消息列表出现系统提示"

depends_on: []
created_at: "2026-04-11 16:20:00"
---

# 学生端 AI 对话页添加"呼叫老师"按钮

> 聊天页面有一个"呼叫老师"按钮，点击后调用 callTeacher API，按钮变为等待状态，消息列表出现系统提示。

## 背景

`chat.ts` 已定义 `callTeacher(params: CreateEscalationParams)` 接口，但聊天 UI 中没有触发入口。本任务只做 UI 层 + 调用集成。

## 需求

1. **按钮位置**: 在输入框区域左侧添加一个"呼叫老师"图标按钮（参考常见 IM 设计，如输入框左侧的 + 按钮区域）
2. **按钮状态**:
   - 默认: 显示图标 + 文字"呼叫老师"
   - 已呼叫/等待中: 按钮变为"等待老师接入..."（禁用状态，灰色）
   - 通过 `ref` 变量 `teacherCalled` 控制状态
3. **点击流程**:
   - 用户点击 → 设置 `teacherCalled = true`
   - 调用 `callTeacher({ conversationId: currentConversationId, reason: '学生主动呼叫' })`
   - 在消息列表中插入一条系统消息: `{ role: 'system', content: '你已呼叫老师，请稍候...' }`
   - 如果调用失败，恢复按钮状态并提示错误
4. **样式**: 与现有聊天页面风格一致（紫色主题）

## API 参考

```typescript
// apps/student-app/src/api/chat.ts
import { callTeacher } from '@/api/chat'
// callTeacher(params: CreateEscalationParams): Promise<Escalation>
// CreateEscalationParams 需要 conversationId
```

## 已知陷阱

- chat/index.vue 文件较大（~1536行），修改时注意不要影响现有 SSE 流式对话逻辑
- `callTeacher` 的参数类型是 `CreateEscalationParams`，需要检查 `@/types/chat` 中的定义确认字段
- 系统消息的 role 应为 'system'，与 'user' 和 'assistant' 区分，需要在模板中添加系统消息样式
