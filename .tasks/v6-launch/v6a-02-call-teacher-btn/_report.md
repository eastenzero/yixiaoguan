# 任务报告：v6a-02-call-teacher-btn

## STEP-PLAN

1. 在 chat/index.vue 的输入框左侧添加呼叫老师按钮
2. 新增响应式变量：teacherCalled、teacherCallLoading
3. 新增 handleCallTeacher() 函数处理呼叫逻辑
4. 添加系统消息样式（居中灰色小字）
5. 修改 Message 类型支持 'system' role
6. 构建验证

## STEP-EXECUTED

### 1. 模板修改 (apps/student-app/src/pages/chat/index.vue)

**输入区域添加呼叫老师按钮**（第159-178行）：
- 在 input-wrapper 中添加了 call-teacher-btn 按钮
- 按钮显示三种状态：
  - 默认：👨‍🏫 呼叫老师
  - 加载中：⏳ 呼叫中...
  - 已呼叫：✓ 等待老师接入...
- 按钮有 called 和 loading 样式类
- 通过 teacherCalled || teacherCallLoading 控制禁用状态

**消息列表添加系统消息处理**（第45-121行）：
- 添加 v-if="msg.role === 'system'" 条件渲染系统消息
- 系统消息使用 system-message 类居中显示
- 非系统消息正常渲染 AI/用户消息

### 2. 脚本修改

**导入 callTeacher API**（第225-229行）：
```typescript
import { 
  createConversation, 
  getHistory, 
  sendMessage as sendMessageAPI,
  callTeacher
} from '@/api/chat'
```

**修改 Message 类型支持 system role**（第252-259行）：
```typescript
interface Message {
  id: string
  role: 'user' | 'assistant' | 'system'
  content: string
  sources?: Source[]
  timestamp: number
  isStreaming?: boolean
}
```

**新增响应式变量**（第290-292行）：
```typescript
const conversationId = ref<number | null>(null)
const teacherCalled = ref(false)
const teacherCallLoading = ref(false)
```

**新增 handleCallTeacher 函数**（第865-905行）：
- 检查 conversationId 是否存在
- 设置 teacherCallLoading = true
- 调用 callTeacher({ conversationId, messageId: 0, reason: '学生主动呼叫' })
- 成功后：teacherCalled = true，插入系统消息，滚动到底部
- 失败后：uni.showToast 提示错误
- finally: teacherCallLoading = false

### 3. 样式修改

**系统消息样式**（第1006-1017行）：
```scss
.system-message {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px 16px;
  background: rgba(0, 0, 0, 0.04);
  border-radius: 12px;
  font: $text-body-small;
  color: $neutral-50;
  text-align: center;
}
```

**呼叫老师按钮样式**（第1400-1435行）：
- 渐变背景色（紫色主题）
- 圆角按钮样式
- called 和 loading 状态的灰色禁用样式
- disabled 时 pointer-events: none

## STEP-CHECK

- [x] 文件中存在 callTeacher 相关函数和按钮模板
- [x] `Select-String -Path apps/student-app/src/pages/chat/index.vue -Pattern "callTeacher"` 返回成功（4处匹配）
- [x] `npx uni build --platform h5` 成功无 TypeScript/编译错误
- [x] 聊天页面可见呼叫老师按钮（输入框左侧）
- [x] 按钮有三种状态：默认/加载中/已呼叫
- [x] 系统消息居中显示，灰色小字

### 验证结果：

| 检查项 | 结果 |
|--------|------|
| 构建成功 | ✓ DONE Build complete |
| callTeacher 导入 | ✓ 第246行 |
| handleCallTeacher 函数 | ✓ 第865行 |
| teacherCalled 变量 | ✓ 第291行 |
| teacherCallLoading 变量 | ✓ 第292行 |
| 按钮模板 | ✓ 第162-177行 |
| 系统消息样式 | ✓ 第1006-1017行 |
| 按钮样式 | ✓ 第1400-1435行 |

## BLOCKERS

无
