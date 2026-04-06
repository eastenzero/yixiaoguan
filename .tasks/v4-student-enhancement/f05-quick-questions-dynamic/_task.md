# F-V4-05：快捷问题动态化

## 元信息
- **任务 ID**: F-V4-05
- **优先级**: P1
- **类型**: refactor
- **批次**: batch_2（串行，第 1 个）
- **预计工作量**: 1-2 小时
- **前置依赖**: batch_1 完成
- **后续任务**: F-V4-05-A2

## 目标

将 chat/index.vue 中硬编码的 quickQuestions 数组改为从知识库热门问题动态获取。

## 背景

- 当前 chat/index.vue:269-274 硬编码了 4 条快捷问题
- 无法根据知识库内容动态调整
- 维护成本高

## 范围

### In Scope
- 将 quickQuestions 改为响应式数据
- 实现动态获取逻辑（推荐方案 C：fallback + 远程获取）
- 页面首次加载时异步获取

### Out of Scope
- ai-service 侧新增接口（如需要，单独处理）
- 快捷问题的个性化推荐
- 快捷问题的管理后台

## 技术要点

### 推荐方案 C：Fallback + 远程获取

```typescript
// 默认 fallback 列表
const DEFAULT_QUESTIONS = [
  '如何申请空教室？',
  '奖学金评定标准是什么？',
  '图书馆开放时间？',
  '如何办理请假手续？'
]

const quickQuestions = ref<string[]>(DEFAULT_QUESTIONS)

onMounted(async () => {
  try {
    // 尝试从远程获取（可选实现）
    // const suggestions = await getSuggestions()
    // if (suggestions && suggestions.length > 0) {
    //   quickQuestions.value = suggestions
    // }
  } catch (error) {
    console.warn('获取快捷问题失败，使用默认列表', error)
    // 保持 fallback
  }
})
```

### 可选：新增 API 函数

如果采用方案 A/C，在 api/chat.ts 中新增：

```typescript
export function getSuggestions() {
  return request<string[]>({
    url: '/api/chat/suggestions',
    method: 'GET'
  })
}
```

## 完成标准

### L0: 存在性检查
- 编译无错误
- quickQuestions 不再是纯硬编码常量（const 改为 ref）

### L1: 静态检查
- TypeScript 编译无错误
- quickQuestions 为响应式数据
- 无 ESLint error

### L2: 运行时检查
- H5 预览：快捷问题正常显示（至少 fallback 列表可见）
- 页面加载时不报错
- 点击快捷问题仍可正常发送

### L3: 语义检查
- 快捷问题列表可配置
- 远程获取失败时降级到默认列表

## 文件清单

### 必须修改
- `apps/student-app/src/pages/chat/index.vue` (quickQuestions 定义区域，行 269-274)

### 可能修改
- `apps/student-app/src/api/chat.ts` (如新增 getSuggestions 函数)

### 必须阅读
- 当前 chat/index.vue 的 quickQuestions 使用方式

## 执行提示

1. 将 quickQuestions 从 const 改为 ref
2. 保留当前 4 条问题作为 DEFAULT_QUESTIONS
3. 在 onMounted 中实现获取逻辑（可先用 fallback，预留远程获取接口）
4. 确保点击快捷问题的逻辑不受影响

## 注意事项

- **此任务是 batch_2 的第一个任务**，完成后才能执行 F-V4-05-A2
- 不要修改 chat/index.vue 的其他部分（source-preview、navbar 等）
- 保持代码简洁，优先实现 fallback 方案

## 风险

- 低风险任务
- 即使远程获取失败，fallback 保证功能可用

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: 检查 quickQuestions 是否为 ref
grep -A 5 "quickQuestions" src/pages/chat/index.vue

# L2: 启动 dev server
npm run dev:h5
# 手动测试快捷问题点击
```
