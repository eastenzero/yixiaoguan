# 任务: F-V7-09 工单/提问 API 对接

## 目标状态
教师端提问列表和详情页从 Mock 数据切换到真实 Escalation API，教师可查看待处理工单、接单、回复。

## 后端 API 端点（已验证存在）

路由前缀: `/api/v1/escalations`

| 方法 | 路径 | 说明 | 参数 |
|------|------|------|------|
| GET | /pending | 待处理工单列表 | pageNum, pageSize |
| GET | /assigned | 教师已接工单 | status?, pageNum, pageSize |
| GET | /{id} | 工单详情 | - |
| PUT | /{id}/assign | 教师接单(0→1) | - |
| PUT | /{id}/resolve | 回复解决(1→2) | Body: { teacherReply } |

### 响应格式（若依 AjaxResult）
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "total": 10,
    "rows": [
      {
        "id": 1,
        "conversationId": 1,
        "messageId": 2,
        "studentId": 10,
        "teacherId": null,
        "questionSummary": "请问学校的电费缴纳在哪里操作？",
        "status": 0,
        "priority": 1,
        "triggerType": 1,
        "teacherReply": null,
        "resolvedAt": null,
        "createdAt": "2026-04-10T14:30:00",
        "studentRealName": "张小洋",
        "studentClassName": "护理2023-1班",
        "teacherRealName": null
      }
    ]
  }
}
```

### 状态枚举
- 0 = 待处理
- 1 = 处理中
- 2 = 已解决
- 3 = 已关闭

## 执行步骤

### 步骤 1: 新建 src/api/escalation.ts

创建 `apps/teacher-app/src/api/escalation.ts`

必须先读取: `apps/teacher-app/src/utils/request.ts`（了解 request 函数签名）

```typescript
import request from '@/utils/request'

// 获取待处理工单列表
export function getPendingEscalations(pageNum = 1, pageSize = 10) {
  return request({
    url: '/api/v1/escalations/pending',
    method: 'get',
    params: { pageNum, pageSize }
  })
}

// 获取教师已接工单列表
export function getAssignedEscalations(status?: number, pageNum = 1, pageSize = 10) {
  return request({
    url: '/api/v1/escalations/assigned',
    method: 'get',
    params: { status, pageNum, pageSize }
  })
}

// 获取工单详情
export function getEscalationDetail(id: number) {
  return request({
    url: `/api/v1/escalations/${id}`,
    method: 'get'
  })
}

// 教师接单
export function assignEscalation(id: number) {
  return request({
    url: `/api/v1/escalations/${id}/assign`,
    method: 'put'
  })
}

// 教师回复解决
export function resolveEscalation(id: number, teacherReply: string) {
  return request({
    url: `/api/v1/escalations/${id}/resolve`,
    method: 'put',
    data: { teacherReply }
  })
}
```

### 步骤 2: 修改 questions/index.vue — 接入真实数据

读取现有文件: `apps/teacher-app/src/pages/questions/index.vue`

修改点:
1. 导入 API 函数:
```typescript
import { getPendingEscalations, getAssignedEscalations } from '@/api/escalation'
```

2. 将 mock 数据替换为响应式状态:
```typescript
const questions = ref<any[]>([])
const loading = ref(false)
const activeTab = ref(0)  // 0=全部, 1=待处理, 2=处理中, 3=已解决
const total = ref(0)
```

3. 加载数据函数:
```typescript
const loadData = async () => {
  loading.value = true
  try {
    let res: any
    if (activeTab.value === 1) {
      // 待处理 = pending (status=0, 未分配)
      res = await getPendingEscalations(1, 20)
    } else {
      // 全部/处理中/已解决 = assigned (带 status 筛选)
      const statusMap: Record<number, number | undefined> = {
        0: undefined, // 全部
        2: 1,         // 处理中
        3: 2          // 已解决
      }
      res = await getAssignedEscalations(statusMap[activeTab.value], 1, 20)
    }
    questions.value = res.data?.rows || res.rows || []
    total.value = res.data?.total || res.total || 0
  } catch (e) {
    console.error('加载工单失败', e)
  } finally {
    loading.value = false
  }
}
```

4. Tab 切换时重新加载:
```typescript
const switchTab = (index: number) => {
  activeTab.value = index
  loadData()
}
```

5. 在 `onMounted` 和 `onShow` 中调用 `loadData()`

6. 模板中: 用 `v-for="item in questions"` 替换硬编码卡片，绑定真实字段:
   - 学生姓名: `item.studentRealName`
   - 班级: `item.studentClassName`
   - 提问内容: `item.questionSummary`
   - 状态: 根据 `item.status` 显示对应文字和颜色
   - 时间: 格式化 `item.createdAt`
   - 点击跳转: `uni.navigateTo({ url: '/pages/questions/detail?id=' + item.id })`

7. 空状态: 当 `questions.length === 0` 且 `!loading` 时，显示"暂无工单"提示

8. Tab 计数: 暂时移除括号中的数字（因为需要多次 API 调用获取各状态计数，可后续优化），或保留但不显示动态数字

### 步骤 3: 修改 questions/detail.vue — 接入真实数据

读取现有文件: `apps/teacher-app/src/pages/questions/detail.vue`

修改点:
1. 导入:
```typescript
import { getEscalationDetail, assignEscalation, resolveEscalation } from '@/api/escalation'
import { onLoad } from '@dcloudio/uni-app'
```

2. 状态:
```typescript
const escalation = ref<any>(null)
const loading = ref(false)
const escalationId = ref(0)
const replyText = ref('')
const submitting = ref(false)
```

3. 加载详情:
```typescript
onLoad((options: any) => {
  escalationId.value = Number(options?.id || 0)
  if (escalationId.value) {
    loadDetail()
  }
})

const loadDetail = async () => {
  loading.value = true
  try {
    const res = await getEscalationDetail(escalationId.value)
    escalation.value = res.data || res
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
```

4. 接单操作:
```typescript
const handleAssign = async () => {
  submitting.value = true
  try {
    await assignEscalation(escalationId.value)
    uni.showToast({ title: '接单成功', icon: 'success' })
    loadDetail() // 刷新状态
  } catch (e: any) {
    uni.showToast({ title: e?.message || '接单失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
```

5. 回复解决:
```typescript
const handleResolve = async () => {
  if (!replyText.value.trim()) {
    uni.showToast({ title: '请输入回复内容', icon: 'none' })
    return
  }
  submitting.value = true
  try {
    await resolveEscalation(escalationId.value, replyText.value)
    uni.showToast({ title: '回复成功', icon: 'success' })
    loadDetail()
  } catch (e: any) {
    uni.showToast({ title: e?.message || '回复失败', icon: 'none' })
  } finally {
    submitting.value = false
  }
}
```

6. 模板:
   - 学生信息区: 绑定 `escalation.studentRealName`, `escalation.studentClassName`
   - 状态标签: 根据 `escalation.status` 动态显示
   - 提问内容: `escalation.questionSummary`
   - 底部操作栏:
     - status=0: 显示"接单处理"按钮 → `handleAssign()`
     - status=1: 显示回复输入框 + "回复并解决"按钮 → `handleResolve()`
     - status=2: 显示"已解决"文字（灰色，不可点击）
   - 加载中: `v-if="loading"` 显示 loading 状态
   - 教师回复: 如果 `escalation.teacherReply` 存在，显示教师回复气泡

### 步骤 4: 修改 dashboard/index.vue — 待处理提问用真实数据

读取现有文件: `apps/teacher-app/src/pages/dashboard/index.vue`

修改点:
1. 导入 `getPendingEscalations`
2. 添加 `pendingQuestions` ref 和 `loadPending()` 函数
3. 在 onMounted/onShow 中加载
4. 模板中"待处理提问"列表区用 `v-for` 替换硬编码
5. "查看全部"链接 → `uni.switchTab({ url: '/pages/questions/index' })`
6. 统计数字暂保留 mock（因为没有专门的统计 API）

## 允许修改的文件
- `apps/teacher-app/src/api/escalation.ts`（新建）
- `apps/teacher-app/src/pages/questions/index.vue`（修改）
- `apps/teacher-app/src/pages/questions/detail.vue`（修改）
- `apps/teacher-app/src/pages/dashboard/index.vue`（修改）

## 禁止修改的文件
- `apps/teacher-app/src/api/auth.ts`
- `apps/teacher-app/src/utils/request.ts`
- `apps/teacher-app/src/stores/**`
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/knowledge/**`
- `apps/teacher-app/src/pages/profile/**`
- `apps/teacher-app/src/pages.json`
- `apps/teacher-app/package.json`
- `apps/student-app/**`
- `services/**`

## 硬约束
- API 函数必须使用项目已有的 `request` 封装
- 不改 request.ts 或 auth.ts
- 若 API 返回空数组，要显示空状态提示而非崩溃
- detail 页面通过 URL query 参数 `id` 接收工单 ID
- 保留原有的 SCSS 样式，只修改 `<script setup>` 和 `<template>`

## 完成标准
- L0: escalation.ts 存在且导出 5 个函数
- L1: questions/index.vue 导入了 API 函数，使用 v-for 渲染
- L2: questions/detail.vue 有接单和回复两个操作按钮

## 报告
写入: `.tasks/v7-teacher-app/f-v7-09-escalation-api/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
