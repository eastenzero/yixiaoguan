# F-V4-05-A2：来源弹层 Markdown 渲染

## 元信息
- **任务 ID**: F-V4-05-A2
- **优先级**: P1
- **类型**: bugfix
- **批次**: batch_2（串行，第 2 个）
- **预计工作量**: 0.5-1 小时
- **前置依赖**: F-V4-05
- **后续任务**: F-V4-06

## 目标

source-preview 弹层当前用 `<text>{{ content }}</text>` 渲染来源摘要，导致 markdown 符号裸露。修改为 v-html + markdown 渲染。

## 背景

- spec-v3 遗留技术债 DEBT-V3-04
- 当前来源弹层显示原始 markdown 标记（**粗体**、# 标题等）
- 用户体验差

## 范围

### In Scope
- 修改 source-preview 弹层的内容渲染方式
- 使用 v-html="renderMarkdown(content)"
- 添加 :deep() 样式穿透（复用 .markdown-body 样式）

### Out of Scope
- 其他文件
- renderMarkdown 函数逻辑（已有）
- 弹层的其他功能（关闭、动画等）

## 技术要点

1. **模板修改**（chat/index.vue 行 183-184）：
   ```vue
   <!-- 修改前 -->
   <text class="source-preview-content">{{ currentSource.content }}</text>
   
   <!-- 修改后 -->
   <view 
     class="source-preview-content markdown-body" 
     v-html="renderMarkdown(currentSource.content)"
   ></view>
   ```

2. **样式穿透**（source-preview 区域）：
   ```scss
   .source-preview-content {
     // 复用 markdown-body 样式
     :deep(p) {
       margin: 0 0 8px 0;
     }
     :deep(ul), :deep(ol) {
       margin: 8px 0;
       padding-left: 20px;
     }
     :deep(strong), :deep(b) {
       font-weight: bold;
     }
     // ... 其他 markdown 元素
   }
   ```

3. **复用已有函数**：
   - renderMarkdown 函数已在 chat/index.vue 中定义
   - .markdown-body 样式已在 spec-v4-chat-bugfix 中修复（:deep() 穿透）

## 完成标准

### L0: 存在性检查
- 编译无错误
- source-preview-content 使用 v-html 而非 {{ }}

### L1: 静态检查
- TypeScript 编译无错误
- source-preview-content 包含 markdown-body class
- 样式使用 :deep() 穿透

### L2: 运行时检查
- H5 预览：来源弹层内 markdown 正确渲染
- 粗体、列表、标题等格式正确显示
- 无样式丢失

### L3: 语义检查
- 来源摘要可读性提升
- 格式化内容与原始 markdown 语义一致

## 文件清单

### 必须修改
- `apps/student-app/src/pages/chat/index.vue` (template 行 183-184, CSS source-preview 区域)

### 必须阅读
- chat/index.vue 中的 renderMarkdown 函数
- chat/index.vue 中的 .markdown-body 样式（spec-v4-chat-bugfix 已修复）

## 执行提示

1. 找到 source-preview-content 的模板代码（行 183-184）
2. 将 `<text>{{ content }}</text>` 改为 `<view v-html="renderMarkdown(content)"></view>`
3. 添加 markdown-body class
4. 在 CSS 中为 .source-preview-content 添加 :deep() 样式穿透
5. 测试弹层显示效果

## 注意事项

- **此任务依赖 F-V4-05 完成**，必须在 F-V4-05 之后执行
- **此任务完成后才能执行 F-V4-06**
- 不要修改 chat/index.vue 的其他部分
- 复用已有的 renderMarkdown 函数和 .markdown-body 样式

## 风险

- 低风险任务
- :deep() 穿透在 spec-v4-chat-bugfix 中已验证可用

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: 检查 v-html 使用
grep -A 3 "source-preview-content" src/pages/chat/index.vue

# L2: 启动 dev server
npm run dev:h5
# 手动测试：发送问题 → 点击来源引用 → 查看弹层内容
```
