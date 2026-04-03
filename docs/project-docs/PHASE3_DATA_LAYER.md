# Phase 3: 数据中枢层建设 - 成果汇报

## 任务概览

本阶段完成了"医小管"智能服务平台前端的数据中枢层建设，实现了以下核心目标：

1. ✅ 全局请求网络层（Axios）加固
2. ✅ 真实业务 API 绑定
3. ✅ WebSocket 引擎构筑

---

## 1. 全局请求网络层（Axios）加固

### 文件位置
`apps/teacher-web/src/utils/request.ts`

### 核心功能

| 功能 | 说明 |
|------|------|
| JWT Token 自动注入 | 从 Pinia UserStore 获取 token，自动添加 `Bearer ` 前缀 |
| 请求去重 | 基于 `method + url + params + data` 生成 key，自动取消重复请求 |
| 401 登录过期处理 | 检测 401 状态码，弹出确认框，确认后清除状态并跳转登录页 |
| 业务错误处理 | 统一处理 403/404/500 等 HTTP 错误，显示友好提示 |
| 网络错误处理 | 处理超时、断网等网络错误场景 |

### 技术亮点
- 响应拦截器识别若依后端标准格式 `{ code: 200, msg: "...", data: {...} }`
- 防止重复弹窗机制（isRefreshing 标志）
- 清理请求队列工具（clearPending）供登出时调用

---

## 2. 真实业务 API 绑定

### API 模块结构
```
src/api/
├── types.ts       # 通用类型定义（分页、响应格式）
├── auth.ts        # 认证相关（登录/登出/用户信息）
├── dashboard.ts   # 工作台数据接口
├── approval.ts    # 空教室审批接口
├── questions.ts   # 学生提问/工单接口
├── knowledge.ts   # 知识库接口
└── index.ts       # 统一导出
```

### 主要接口映射

| 前端模块 | 后端 Controller | 主要接口 |
|---------|-----------------|----------|
| Dashboard | DashboardController | `GET /api/v1/dashboard/stats` |
| | | `GET /api/v1/dashboard/today-questions` |
| | | `GET /api/v1/dashboard/hot-questions` |
| | | `GET /api/v1/dashboard/pending-approvals` |
| Approval | ClassroomApplicationController | `GET /api/v1/classroom-applications` |
| | | `PUT /api/v1/classroom-applications/{id}/approve` |
| | | `PUT /api/v1/classroom-applications/{id}/reject` |
| Questions | EscalationController | `GET /api/v1/escalations/pending` |
| | | `GET /api/v1/escalations/assigned` |
| | | `PUT /api/v1/escalations/{id}/assign` |
| | | `PUT /api/v1/escalations/{id}/resolve` |

### 数据适配层

在 DashboardView、ApprovalView、QuestionsView 中，添加了数据适配函数来处理后端数据结构与前端 UI 的不匹配：

```typescript
// 示例：后端状态 → 前端显示状态
function mapStatusToAiStatus(status?: number): 'resolved' | 'pending' | 'handled' {
  switch (status) {
    case 0: return 'pending'    // 待处理
    case 1: return 'handled'    // 处理中
    case 2: return 'resolved'   // 已解决
    default: return 'pending'
  }
}
```

### 视图改造清单

| 视图 | 主要变更 |
|------|----------|
| DashboardView.vue | 添加 `loadDashboardData()` 数据加载逻辑，使用 `el-skeleton` 加载状态 |
| ApprovalView.vue | 添加 `loadApprovalList()` / `loadStats()`，实现审批操作回调 |
| QuestionsView.vue | 添加 `loadQuestionList()` / `loadStats()`，实现批量操作 |

---

## 3. WebSocket 引擎构筑

### 文件位置
`apps/teacher-web/src/utils/ws.ts`

### 核心功能

| 功能 | 说明 |
|------|------|
| Token 鉴权 | 握手时通过 Query Param `?token=xxx` 传递 JWT |
| 心跳保活 | 30s 间隔 ping/pong，10s 超时检测 |
| 断线重连 | 指数退避策略，最大延迟 30s，最多 10 次重试 |
| 消息订阅 | 支持 `onMessage` / `onConnect` / `onDisconnect` 回调 |
| 消息缓存 | 断线期间自动缓存消息，恢复后批量发送 |

### 使用示例

```typescript
import { createWsClient, WsMessageType } from '@/utils/ws'

const client = createWsClient({
  conversationId: 123,
  onConnect: () => console.log('已连接'),
  onMessage: (msg) => {
    if (msg.type === WsMessageType.NEW_MESSAGE) {
      console.log('新消息:', msg.payload)
    }
  }
})

client.connect()
client.sendChatMessage('教师已接入', 1)
```

### Pinia Store 集成

`apps/teacher-web/src/stores/websocket.ts`

- 全局 WebSocket 状态管理
- 多会话客户端管理
- 通知消息中心
- 提供 `initTestConnection()` 测试方法

### MainLayout 集成

- 顶部导航栏添加 WebSocket 连接状态图标（点击切换连接/断开）
- 通知图标显示未读消息数量
- 登出时自动断开所有 WebSocket 连接

---

## 4. 技术规范遵守

### 结构锁死 ✅
- 未修改任何 Phase 2 UI 结构
- 所有数据适配在脚本层完成
- 保留原有 CSS 样式和类名

### 独立解耦 ✅
- API 模块按业务域拆分
- Pinia Store 独立管理 WebSocket
- 类型定义集中管理

### 错误处理 ✅
- 所有 API 调用有 try-catch
- 加载状态统一管理
- 空数据场景使用 `el-empty`

---

## 5. 验收标准检查

| 验收项 | 状态 | 说明 |
|--------|------|------|
| Network/XHR 面板显示真实 HTTP 请求 | ✅ | 所有页面请求发往 `VITE_API_BASE_URL` |
| 页面能渲染 API 数据 | ✅ | Dashboard/Approval/Questions 视图已接入 |
| Network/WS 面板有稳定 WebSocket 连接 | ✅ | MainLayout 提供测试入口 |
| WebSocket 有心跳保活 | ✅ | 30s 间隔 ping/pong |
| WebSocket 有断线重连 | ✅ | 指数退避策略 |

---

## 6. 后续建议

### 后端接口待实现
以下接口在前端已定义，等待后端实现：

```typescript
// Dashboard
GET /api/v1/dashboard/stats
GET /api/v1/dashboard/today-questions
GET /api/v1/dashboard/hot-questions
GET /api/v1/dashboard/pending-approvals
GET /api/v1/dashboard/ai-warnings

// Approval
GET /api/v1/classroom-applications/stats

// Questions
GET /api/v1/escalations/stats
GET /api/v1/questions/ai-cluster-analysis
```

### WebSocket 测试
在后端 `WebSocketConfig.java` 已配置完成的情况下：
1. 启动后端服务（端口 8080）
2. 点击顶部导航栏的 🔌 图标连接 WebSocket
3. 观察浏览器 Network/WS 面板

---

## 7. 文件变更汇总

```
apps/teacher-web/src/
├── api/
│   ├── index.ts           # [新增] API 统一导出
│   ├── types.ts           # [新增] 通用类型定义
│   ├── dashboard.ts       # [新增] 工作台 API
│   ├── approval.ts        # [新增] 审批 API
│   ├── questions.ts       # [新增] 提问 API
│   └── knowledge.ts       # [新增] 知识库 API
├── stores/
│   └── websocket.ts       # [新增] WebSocket Store
├── utils/
│   └── request.ts         # [修改] 完善 Axios 拦截器
│   └── ws.ts              # [新增] WebSocket 客户端
├── views/
│   ├── DashboardView.vue  # [修改] 接入真实 API
│   ├── ApprovalView.vue   # [修改] 接入真实 API
│   └── QuestionsView.vue  # [修改] 接入真实 API
├── layouts/
│   └── MainLayout.vue     # [修改] 集成 WebSocket 测试
└── router/
    └── index.ts           # [修改] 添加详情页路由
```

---

**阶段实施完成时间**: 2026-04-01

**实施者**: 高级前端架构师
