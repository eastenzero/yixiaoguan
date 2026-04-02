# Phase 1.1 修复日志：questions.ts 字段适配器

## 执行时间
2026-04-01 16:10:00+08:00

## 任务描述
为 `apps/teacher-web/src/api/questions.ts` 添加字段适配器，解决前后端字段名不匹配问题。

## 发现的问题

### 1. 字段名不匹配
| 后端字段名 | 前端期望字段名 | 处理方式 |
|-----------|--------------|---------|
| `studentRealName` | `studentName` | 直接映射 |
| `teacherRealName` | `teacherName` | 直接映射 |
| `studentClassName` | `studentGrade` + `studentMajor` | 解析拆分 |

### 2. API 未实现
| API 路径 | 后端状态 | 临时解决方案 |
|---------|---------|-------------|
| `GET /api/v1/escalations/stats` | ❌ 未实现 | 返回 mock 数据 |
| `GET /api/v1/questions/ai-cluster-analysis` | ❌ 未实现 | 返回 mock 数据 |

## 修改内容

### 新增类型定义
```typescript
// 后端原始数据结构
interface RawEscalationItem {
  studentRealName?: string
  teacherRealName?: string
  studentClassName?: string
  // ...
}
```

### 新增适配器函数
```typescript
// 解析班级信息
function parseStudentClass(className?: string): { grade?: string; major?: string }

// 单条数据适配
function adaptEscalationItem(raw: RawEscalationItem): EscalationItem

// 分页结果适配
function adaptPageResult<T, R>(raw: PageResult<T>, adapter: (item: T) => R): PageResult<R>
```

### 修改的 API 函数
1. `getQuestionStats()` - 添加 try-catch，失败时返回 mock 数据
2. `getPendingEscalations()` - 添加字段适配
3. `getMyAssignedEscalations()` - 添加字段适配
4. `getEscalationList()` - 添加字段适配
5. `getEscalationDetail()` - 添加字段适配
6. `getAIClusterAnalysis()` - 添加 try-catch，失败时返回 mock 数据

## 向后兼容说明
- 所有函数签名保持不变
- mock 数据包含 `(mock)` 标记，便于识别
- 后端实现后自动切换到真实数据（删除 try-catch 即可）

## 下一步行动
等待用户确认后，继续修改：
1. `approval.ts` - 检查并修复字段适配
2. `knowledge.ts` - 检查并修复字段适配
3. 清理调试代码
4. 生成最终验收报告
