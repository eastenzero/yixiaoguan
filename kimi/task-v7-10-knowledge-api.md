# 任务: F-V7-10 知识库 API 对接

## 目标状态
教师端知识库列表和详情页从 Mock 数据切换到真实 Knowledge API。

## 后端 API 端点（已验证存在）

路由前缀: `/api/v1/knowledge/entries`

| 方法 | 路径 | 说明 | 参数 |
|------|------|------|------|
| GET | / | 分页查询知识条目 | categoryId?, status?, title?, pageNum, pageSize |
| GET | /{id} | 知识条目详情 | - |
| POST | /draft | 保存草稿 | Body: YxKnowledgeEntry |
| POST | /{id}/submit | 发起提审 | - |
| POST | /{id}/offline | 下线条目 | - |
| DELETE | /{id} | 软删除 | - |

分类 API: `/api/v1/knowledge/categories`
| GET | / | 分类列表 | - |

### 响应格式（若依 AjaxResult）
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "total": 96,
    "rows": [
      {
        "id": 1,
        "title": "学生电费缴纳指南",
        "content": "...",
        "categoryId": 3,
        "categoryName": "生活指南",
        "status": 1,
        "authorId": 15,
        "authorName": "梁淑芬",
        "createdAt": "2026-03-15T10:00:00",
        "updatedAt": "2026-04-01T14:30:00"
      }
    ]
  }
}
```

### 状态枚举（推测，需容错）
- 0 = 草稿
- 1 = 已发布
- 2 = 审核中
- 3 = 已下线

## 执行步骤

### 步骤 1: 新建 src/api/knowledge.ts

创建 `apps/teacher-app/src/api/knowledge.ts`

必须先读取: `apps/teacher-app/src/utils/request.ts`

```typescript
import request from '@/utils/request'

// 分页查询知识条目
export function getKnowledgeEntries(params?: {
  categoryId?: number
  status?: number
  title?: string
  pageNum?: number
  pageSize?: number
}) {
  return request({
    url: '/api/v1/knowledge/entries',
    method: 'get',
    params: {
      pageNum: 1,
      pageSize: 10,
      ...params
    }
  })
}

// 获取知识条目详情
export function getKnowledgeDetail(id: number) {
  return request({
    url: `/api/v1/knowledge/entries/${id}`,
    method: 'get'
  })
}

// 获取分类列表
export function getCategories() {
  return request({
    url: '/api/v1/knowledge/categories',
    method: 'get'
  })
}

// 下线条目
export function offlineEntry(id: number) {
  return request({
    url: `/api/v1/knowledge/entries/${id}/offline`,
    method: 'post'
  })
}
```

### 步骤 2: 修改 knowledge/index.vue — 接入真实数据

读取现有文件: `apps/teacher-app/src/pages/knowledge/index.vue`

修改点:
1. 导入:
```typescript
import { getKnowledgeEntries } from '@/api/knowledge'
import { onShow } from '@dcloudio/uni-app'
```

2. 状态:
```typescript
const entries = ref<any[]>([])
const loading = ref(false)
const activeCategory = ref<number | undefined>(undefined) // undefined=全部
const searchText = ref('')
const total = ref(0)
```

3. 加载函数:
```typescript
const loadData = async () => {
  loading.value = true
  try {
    const res = await getKnowledgeEntries({
      categoryId: activeCategory.value,
      title: searchText.value || undefined,
      pageNum: 1,
      pageSize: 20
    })
    entries.value = res.data?.rows || res.rows || []
    total.value = res.data?.total || res.total || 0
  } catch (e) {
    console.error('加载知识库失败', e)
  } finally {
    loading.value = false
  }
}
```

4. 分类切换:
```typescript
const switchCategory = (catId?: number) => {
  activeCategory.value = catId
  loadData()
}
```

5. 搜索:
```typescript
const handleSearch = () => {
  loadData()
}
```

6. 生命周期:
```typescript
onMounted(() => loadData())
onShow(() => loadData())
```

7. 模板:
   - 用 `v-for="item in entries"` 替换硬编码卡片
   - 标题: `item.title`
   - 分类: `item.categoryName`（如果有）或根据 `item.categoryId` 映射
   - 状态: 根据 `item.status` 显示（0=草稿, 1=已发布）
   - 摘要: `item.content`（截取前100字）或 `item.summary`
   - 作者: `item.authorName`
   - 时间: 格式化 `item.updatedAt` 或 `item.createdAt`
   - 点击: `uni.navigateTo({ url: '/pages/knowledge/detail?id=' + item.id })`
   - 空状态: 无数据时显示提示

8. 分类标签: 暂保留硬编码的4个标签（全部/教务管理/学生服务/生活指南），点击时传对应 categoryId

### 步骤 3: 修改 knowledge/detail.vue — 接入真实数据

读取现有文件: `apps/teacher-app/src/pages/knowledge/detail.vue`

修改点:
1. 导入:
```typescript
import { getKnowledgeDetail, offlineEntry } from '@/api/knowledge'
import { onLoad } from '@dcloudio/uni-app'
```

2. 状态:
```typescript
const entry = ref<any>(null)
const loading = ref(false)
const entryId = ref(0)
```

3. 加载:
```typescript
onLoad((options: any) => {
  entryId.value = Number(options?.id || 0)
  if (entryId.value) loadDetail()
})

const loadDetail = async () => {
  loading.value = true
  try {
    const res = await getKnowledgeDetail(entryId.value)
    entry.value = res.data || res
  } catch (e) {
    uni.showToast({ title: '加载失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
```

4. 下线操作:
```typescript
const handleOffline = async () => {
  try {
    await offlineEntry(entryId.value)
    uni.showToast({ title: '已下线', icon: 'success' })
    loadDetail()
  } catch (e: any) {
    uni.showToast({ title: e?.message || '操作失败', icon: 'none' })
  }
}
```

5. 模板:
   - Hero区: 绑定 `entry.categoryName`, `entry.title`, `entry.authorName`, `entry.updatedAt`
   - 正文: 显示 `entry.content`（可能是 markdown 或纯文本）
   - 底部"下线"按钮 → `handleOffline()`
   - 底部"编辑"按钮 → 暂时 `uni.showToast({ title: '编辑功能开发中', icon: 'none' })`
   - 加载中状态

## 允许修改的文件
- `apps/teacher-app/src/api/knowledge.ts`（新建）
- `apps/teacher-app/src/pages/knowledge/index.vue`（修改）
- `apps/teacher-app/src/pages/knowledge/detail.vue`（修改）

## 禁止修改的文件
- `apps/teacher-app/src/api/auth.ts`
- `apps/teacher-app/src/api/escalation.ts`
- `apps/teacher-app/src/utils/request.ts`
- `apps/teacher-app/src/stores/**`
- `apps/teacher-app/src/components/**`
- `apps/teacher-app/src/styles/**`
- `apps/teacher-app/src/pages/login/**`
- `apps/teacher-app/src/pages/dashboard/**`
- `apps/teacher-app/src/pages/questions/**`
- `apps/teacher-app/src/pages/profile/**`
- `apps/teacher-app/src/pages.json`
- `apps/teacher-app/package.json`
- `apps/student-app/**`
- `services/**`

## 硬约束
- 使用项目已有的 request 封装
- 不改任何已有文件（auth.ts, request.ts, escalation.ts）
- API 返回空数组要显示空状态
- detail 页通过 URL query `id` 接收
- 保留原有 SCSS 样式

## 完成标准
- L0: knowledge.ts 存在且导出 4 个函数
- L1: knowledge/index.vue 导入 API 函数，使用 v-for 渲染
- L2: knowledge/detail.vue 有下线按钮绑定真实 API

## 报告
写入: `.tasks/v7-teacher-app/f-v7-10-knowledge-api/_report.md`
仅输出: STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
