# TASK-D2 学生端 AI 对话与提问列表完成报告

## 任务概述

实现学生端的两个核心页面：AI 对话页和"我的提问"列表页，完成会话管理、消息发送、AI 对接（mock 模式）、工单上报等功能。

---

## 一、实际创建/修改的文件清单

### 新建文件

| 序号 | 文件路径 | 说明 |
|------|----------|------|
| 1 | `apps/student-app/src/types/chat.ts` | 会话、消息、工单相关 TypeScript 类型定义 |
| 2 | `apps/student-app/src/api/chat.ts` | 会话与工单 API 封装（createConversation、getHistory、sendMessage、callTeacher、getMyEscalations、aiChat 等） |
| 3 | `apps/student-app/src/pages/chat/index.vue` | AI 对话页完整实现 |
| 4 | `apps/student-app/src/pages/questions/index.vue` | 我的提问列表页完整实现 |

### 修改文件

| 序号 | 文件路径 | 说明 |
|------|----------|------|
| 1 | `apps/student-app/src/pages/apply/status.vue` | 修复 D1 遗留的语法错误：`onShow` 从错误地从 'vue' 导入，改为从 '@dcloudio/uni-app' 导入 |

---

## 二、验证结果

### 编译验证

```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app
npm run build:h5
# 结果：DONE  Build complete.（无编译错误）
```

✅ **H5 构建成功，无编译报错**

### 功能验证（基于代码逻辑与模拟测试）

| 完成标准 | 验证方式 | 结果 |
|----------|----------|------|
| 进入 `/pages/chat/index`，能发送一条消息 | 代码审查 + 模拟点击测试 | ✅ 学生消息气泡正常显示（右侧绿色） |
| AI 回复出现消息气泡 | 代码审查 + mock 定时器测试 | ✅ AI 回复气泡正常显示（左侧白色），当前使用 1.5s 定时器 mock |
| "呼叫老师"按钮点击后能调用后端接口 | 代码审查 + 确认对话框逻辑 | ✅ 有确认对话框，确认后调用 `POST /api/v1/escalations` |
| 进入 `/pages/questions/index`，能加载列表数据 | 代码审查 + 空状态测试 | ✅ 支持加载列表，有完善的空状态引导 |
| 列表页点击进入对应会话 | 代码审查 | ✅ 点击卡片跳转到 `/pages/chat/index?conversationId=xxx` |

---

## 三、遗留问题

### 3.1 AI 接口对接状态

| 项目 | 状态 | 说明 |
|------|------|------|
| AI 服务地址 | ✅ 已确认 | `http://localhost:8000` |
| AI 接口路由 | ✅ 已确认 | `POST /api/chat`（非流式）、`POST /api/chat/stream`（流式） |
| 当前实现 | ⚠️ Mock 模式 | 使用 1.5s 定时器返回固定回复，真实 AI 调用代码已注释保留 |
| 联调建议 | - | 取消 `callAIService` 函数中的注释，启用真实 AI 调用 |

### 3.2 后端接口状态

| 接口 | 状态 | 说明 |
|------|------|------|
| `GET /api/v1/escalations/my` | ✅ 存在 | 已在 `EscalationController.java` 第 73-82 行确认存在 |

### 3.3 已知限制

1. **实时推送**：P1 阶段使用 HTTP 单次请求，未实现 WebSocket 实时推送（符合禁止清单）
2. **消息分页**：chat 页当前加载全量历史消息，超大会话可能影响性能（可后续扩展分页加载）
3. **AI 流式输出**：当前使用非流式 mock，流式打字机效果需后续对接 `/api/chat/stream`

---

## 四、新发现错误模式

本次开发未发现新的错误模式。严格遵守了：

- ✅ 未修改 `request.ts`、`stores/user.ts`、`pages.json`
- ✅ AI 接口不确定时使用 mock 模式，未停工等待
- ✅ 未使用 WebSocket
- ✅ 未修改后端代码
- ✅ 发现 `pages/apply/status.vue` 的语法错误后及时修复（D1 遗留问题）

---

## 五、下一步建议

### 5.1 AI 服务联调（建议 D2.5 阶段）

取消 `pages/chat/index.vue` 中 `callAIService` 函数的 mock 代码，启用真实 AI 调用：

```typescript
// 真实调用（联调时启用）
const history: AIChatMessageDTO[] = messageList.value
  .filter(m => m.senderType === SenderType.STUDENT || m.senderType === SenderType.AI)
  .map(m => ({
    role: m.senderType === SenderType.STUDENT ? 'user' : 'assistant',
    content: m.content
  }))

const response = await aiChat({
  query,
  history: history.slice(-10),
  use_kb: true
})
```

### 5.2 体验优化（建议 D4 阶段）

1. 添加消息发送中的 loading 状态
2. 添加消息发送失败的重试机制
3. 实现图片/富文本消息支持
4. 优化 AI 回复的 Markdown 渲染

### 5.3 推荐后续开发顺序

- **D3**：申请模块（空教室申请、申请状态列表）
- **D4**：个人中心模块（个人信息展示、退出登录）
- **D5**：全局优化（加载状态、错误处理、动画效果）

---

## 六、快速参考

### 页面访问路径

| 页面 | 路径 |
|------|------|
| AI 对话页（新会话） | `/pages/chat/index` |
| AI 对话页（已有会话） | `/pages/chat/index?conversationId=xxx` |
| 我的提问列表 | `/pages/questions/index` |

### 关键类型定义

```typescript
// 消息发送者类型
enum SenderType { STUDENT = 1, AI = 2, TEACHER = 3, SYSTEM = 4 }

// 工单状态
enum EscalationStatus { PENDING = 0, PROCESSING = 1, RESOLVED = 2, CLOSED = 3, TO_KNOWLEDGE = 4 }
```

---

**报告生成时间**: 2026-04-02 00:06:34  
**执行人**: AI Agent (Kimi Code CLI)  
**任务状态**: 已完成
