# F-V7-09 工单API对接 - 执行报告

## STEP-PLAN

1. 创建 `apps/teacher-app/src/api/escalation.ts` - 工单API模块
2. 修改 `apps/teacher-app/src/pages/questions/index.vue` - 提问列表接入真实数据
3. 修改 `apps/teacher-app/src/pages/questions/detail.vue` - 提问详情接入真实数据，实现接单和回复功能
4. 修改 `apps/teacher-app/src/pages/dashboard/index.vue` - 待处理提问使用真实数据

## STEP-EXECUTED

### STEP 1: 创建 escalation.ts API 模块 ✓

**文件**: `apps/teacher-app/src/api/escalation.ts`

导出5个API函数:
- `getPendingEscalations(pageNum, pageSize)` - 获取待处理工单列表
- `getAssignedEscalations(status?, pageNum, pageSize)` - 获取教师已接工单列表
- `getEscalationDetail(id)` - 获取工单详情
- `assignEscalation(id)` - 教师接单 (status 0→1)
- `resolveEscalation(id, teacherReply)` - 教师回复解决 (status 1→2)

### STEP 2: 修改 questions/index.vue ✓

**变更点**:
- 添加 API 导入: `getPendingEscalations`, `getAssignedEscalations`
- 将 mock 数据替换为响应式状态: `questions`, `loading`, `activeTab`, `total`
- 实现 `loadData()` 函数，根据 Tab 切换调用不同 API
  - Tab 1(待处理): 调用 `getPendingEscalations()`
  - Tab 0/2/3(全部/处理中/已解决): 调用 `getAssignedEscalations(status)`
- 实现 `switchTab()` 函数，切换时重新加载数据
- 添加 `formatTime()` 时间格式化函数
- 更新状态映射 `getStatusText()` 支持数字状态 (0=待处理, 1=处理中, 2=已解决, 3=已关闭)
- 模板中使用 `v-for="item in questions"` 渲染真实数据
- 绑定真实字段: `studentRealName`, `studentClassName`, `questionSummary`, `createdAt`
- 添加 Loading 状态和 Empty 状态提示
- 移除 Tab 中的计数括号（简化实现，避免多次 API 调用）
- 在 `onMounted` 和 `onShow` 中调用 `loadData()` 实现页面刷新

### STEP 3: 修改 questions/detail.vue ✓

**变更点**:
- 添加 API 导入: `getEscalationDetail`, `assignEscalation`, `resolveEscalation`
- 添加 `onLoad` 从 `@dcloudio/uni-app` 导入
- 添加状态: `escalation`, `loading`, `escalationId`, `replyText`, `submitting`
- 实现 `loadDetail()` 加载工单详情
- 实现 `handleAssign()` 接单操作，成功后刷新状态
- 实现 `handleResolve()` 回复解决操作，验证非空后提交
- 添加 `formatTime()` 时间格式化函数
- 更新状态标签样式，支持 4 种状态
- 底部操作栏根据状态动态显示:
  - status=0: 显示"接单处理"按钮 → 调用 `handleAssign()`
  - status=1: 显示回复输入框 + "回复并解决"按钮 → 调用 `handleResolve()`
  - status=2: 显示"已解决"文字（灰色，不可点击）
  - status=3: 显示"已关闭"
- 添加教师回复气泡显示（当 `teacherReply` 存在时）
- 添加 Loading 状态显示

### STEP 4: 修改 dashboard/index.vue ✓

**变更点**:
- 添加 API 导入: `getPendingEscalations`
- 添加状态: `pendingQuestions`, `loading`
- 添加计算属性 `pendingCount` 显示待处理数量
- 实现 `loadPendingQuestions()` 加载待处理提问列表（限制5条）
- 添加 `formatTime()` 时间格式化函数
- 更新 `getStatusText()` 支持数字状态
- 模板中待处理提问列表使用 `v-for` 渲染真实数据
- 绑定真实字段: `studentRealName`, `studentClassName`, `questionSummary`, `createdAt`, `status`
- 添加 Loading 状态和 Empty 状态提示
- 欢迎横幅中的待处理数量改为动态显示 `pendingCount`
- 在 `onMounted` 和 `onShow` 中调用 `loadPendingQuestions()`

## STEP-CHECK

### L0 检查: escalation.ts 存在且导出 5 个函数 ✓
```
✓ getPendingEscalations
✓ getAssignedEscalations
✓ getEscalationDetail
✓ assignEscalation
✓ resolveEscalation
```

### L1 检查: questions/index.vue 导入了 API 函数，使用 v-for 渲染 ✓
```
✓ 导入: import { getPendingEscalations, getAssignedEscalations } from '@/api/escalation'
✓ 使用 v-for="item in questions" 渲染列表
✓ 调用真实 API: loadData() 中根据 Tab 调用不同接口
```

### L2 检查: questions/detail.vue 有接单和回复两个操作按钮 ✓
```
✓ 接单按钮: status=0 时显示，调用 handleAssign()
✓ 回复按钮: status=1 时显示，调用 handleResolve()
✓ 两种操作都有 loading 状态和错误提示
```

## 修改文件汇总

| 文件 | 操作 | 说明 |
|------|------|------|
| apps/teacher-app/src/api/escalation.ts | 新建 | 工单API模块，导出5个函数 |
| apps/teacher-app/src/pages/questions/index.vue | 修改 | 接入真实数据，支持Tab切换加载 |
| apps/teacher-app/src/pages/questions/detail.vue | 修改 | 详情页+接单+回复功能 |
| apps/teacher-app/src/pages/dashboard/index.vue | 修改 | 待处理提问使用真实数据 |

## BLOCKERS

无阻塞项，所有步骤已按计划完成。
