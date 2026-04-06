# F-V4-01：知识详情页 API 对接

## 元信息
- **任务 ID**: F-V4-01
- **优先级**: P0
- **类型**: feature
- **批次**: batch_1（并行）
- **预计工作量**: 1-2 小时
- **前置依赖**: 无

## 目标

knowledge/detail.vue 当前走 fallback（API 404 → 展示 route query 中的摘要）。
后端 GET /api/v1/knowledge/entries/{id} 已实现，需前端对接。

## 背景

- 后端 API 已就绪：`GET /api/v1/knowledge/entries/{id}` (KnowledgeEntryController.getById())
- 前端 api/knowledge.ts 已定义 getKnowledgeEntryDetail 函数，但调用格式可能不正确
- 当前详情页因 API 失败走 fallback 分支，只显示摘要

## 范围

### In Scope
- 修复 getKnowledgeEntryDetail 调用，正确处理 AjaxResult 响应包装
- 成功时渲染完整知识条目（标题 + markdown 正文 + 标签）
- 失败时保留现有 fallback 行为

### Out of Scope
- 后端接口修改
- 其他页面
- 新增功能（如评论、收藏等）

## 技术要点

1. **响应格式处理**：后端返回 AjaxResult 包装，需正确解包
   ```typescript
   // 可能需要的格式
   const response = await getKnowledgeEntryDetail(id)
   const entry = response.data // 或 response.result
   ```

2. **字段映射**：确认后端返回字段名与前端期望一致
   - id / entryId
   - title
   - content (markdown 正文)
   - tags
   - category

3. **Markdown 渲染**：复用已有的 renderMarkdown 函数和 .markdown-body 样式

## 完成标准

### L0: 存在性检查
- TypeScript 编译无错误
- getKnowledgeEntryDetail 函数调用存在于 detail.vue 中

### L1: 静态检查
- getKnowledgeEntryDetail 函数调用格式正确（参数、返回值类型）
- 无 TypeScript 类型错误
- 无 ESLint error

### L2: 运行时检查
- H5 预览：从 AI 回复来源点击进入详情页，显示完整条目内容
- API 成功时显示标题、正文、标签
- API 失败时显示 fallback（摘要）

### L3: 语义检查
- 知识条目内容完整可读
- Markdown 格式正确渲染
- 标签正确显示

## 文件清单

### 必须修改
- `apps/student-app/src/pages/knowledge/detail.vue`
- `apps/student-app/src/api/knowledge.ts` (可能需要调整)

### 必须阅读
- `services/business-api/.../knowledge/controller/KnowledgeEntryController.java` (了解响应格式)
- `apps/student-app/src/pages/chat/index.vue` (了解来源引用跳转逻辑)

## 执行提示

1. 先检查 api/knowledge.ts 中 getKnowledgeEntryDetail 的实现
2. 确认后端响应格式（可用 curl 或浏览器 DevTools 测试）
3. 修改 detail.vue 的 loadDetail 函数，正确解包响应
4. 测试成功和失败两种情况

## 风险

- **RISK-V4-01**: business-api 未运行导致无法测试 L2
  - 缓解：L0-L1 可在无后端情况下通过
  - 详情页应优雅处理 API 失败

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: Lint 检查
npm run lint

# L2: 需要 business-api 运行
# 手动测试：H5 预览 → 智能问答 → 点击来源引用
```
