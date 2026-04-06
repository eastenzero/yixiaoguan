---
id: "f-v5a-04"
parent: "v5a-quick-fixes"
type: "bugfix"
status: "done"
tier: "T3"
priority: "high"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/api/chat.ts"
out_of_scope:
  - "apps/student-app/src/pages/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/api/chat.ts"

done_criteria:
  L0: "apps/student-app/src/api/chat.ts 存在"
  L1: "grep -c 'status: undefined\\|{ status,' apps/student-app/src/api/chat.ts 返回 0（裸传 undefined 已消除）"
  L2: "grep 'if (status !== undefined)' apps/student-app/src/api/chat.ts 返回结果"
  L3: "访问历史记录页控制台无 '参数[status]要求类型为: java.lang.Integer' 报错"

root_cause: |
  api/chat.ts getConversationList() 将 undefined 的 status 展开到 GET 参数对象，
  axios/uni-request 将其序列化为 ?status=undefined，
  后端 Java Controller 期望 Integer 类型无法解析该字符串。

reproduction_steps:
  - "登录学生账号，进入历史记录页"
  - "观察控制台，出现：参数[status]要求类型为: 'java.lang.Integer', 但输入值为: 'undefined'"

created_at: "2026-04-06"
---

# F-V5A-04: 历史记录页 API 参数修复

> `getConversationList()` 不再将 `undefined` 的 status 参数传入 GET 请求，历史记录页加载无控制台报错。

## 背景

`history.vue` 调用 `getConversationList()` 时不传 `status`，但当前实现将 `{ status: undefined }` 展开到请求参数，最终序列化为 `?status=undefined`，后端报类型错误。

## 变更详情

- **文件**: `apps/student-app/src/api/chat.ts`
- **函数**: `getConversationList`（约 line 35）
- **改前**:
  ```ts
  return get('/api/v1/conversations', { status, ...params })
  ```
- **改后**:
  ```ts
  const query: Record<string, any> = { ...params }
  if (status !== undefined) query.status = status
  return get('/api/v1/conversations', query)
  ```

## 已知陷阱

- 注意保留 `...params` 的展开逻辑，不要丢失分页参数
- 不要修改函数签名，`status?: number` 可选参数保持不变
