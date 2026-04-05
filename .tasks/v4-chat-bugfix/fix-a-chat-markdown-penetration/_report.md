# FIX-A 执行报告：Chat Markdown 样式穿透修复

## 任务信息
- **任务ID**: fix-a-chat-markdown-penetration
- **关联Bug**: BUG-2 (AI 气泡高度只有一行 — 回复内容被截断)
- **执行时间**: 2026-04-06
- **执行状态**: ✅ 完成

## 问题根因
Vue 3 scoped CSS 会将 `.markdown-body p` 编译为 `.markdown-body p[data-v-xxxxx]`，但 `v-html` 动态插入的 HTML 元素不会携带 `data-v-xxxxx` 属性，导致 `.markdown-body` 下所有子元素样式全部失效，AI 回复气泡高度坍塌为一行。

## 修复方案
将 `.markdown-body` 的所有子元素选择器改为 `:deep()` 穿透写法，使样式能够应用到 v-html 注入的子节点。

## 修改内容

### 文件: `apps/student-app/src/pages/chat/index.vue`

**修改范围**: 第 958-1010 行（.markdown-body 样式块）

**修改方式**: 所有子选择器添加 `:deep()` 包裹

**覆盖元素**: p, h1-h4, ul, ol, li, code, pre, a, blockquote, hr, strong, b

```scss
// 修改前（scoped 样式对 v-html 子节点失效）
.markdown-body {
  p { margin: 0 0 8px 0; }
  h1, h2, h3, h4 { ... }
  // ... 其他子选择器
}

// 修改后（:deep() 穿透生效）
.markdown-body {
  :deep(p) { margin: 0 0 8px 0; }
  :deep(h1), :deep(h2), :deep(h3), :deep(h4) { ... }
  // ... 其他子选择器全部添加 :deep()
}
```

**关键修改片段**（行 963-1010）:
```scss
.markdown-body {
  font-size: 14px;
  line-height: 1.7;
  word-break: break-word;

  :deep(> *:first-child) { margin-top: 0 !important; }
  :deep(> *:last-child)  { margin-bottom: 0 !important; }

  :deep(p) { margin: 0 0 8px 0; &:last-child { margin-bottom: 0; } }

  :deep(strong), :deep(b) { font-weight: 600; color: #006a64; }

  :deep(h1), :deep(h2), :deep(h3), :deep(h4) {
    font-weight: 600;
    margin: 12px 0 6px 0;
    line-height: 1.4;
  }
  :deep(h1) { font-size: 18px; }
  :deep(h2) { font-size: 16px; }
  :deep(h3) { font-size: 15px; }

  :deep(ul), :deep(ol) { margin: 6px 0; padding-left: 20px; }
  :deep(li) { margin: 3px 0; line-height: 1.6; }

  :deep(code) {
    background: rgba(0, 106, 100, 0.1);
    border-radius: 4px;
    padding: 2px 5px;
    font-family: 'Menlo', 'Monaco', monospace;
    font-size: 12px;
    color: #006a64;
  }

  :deep(pre) {
    background: rgba(0, 0, 0, 0.04);
    border-radius: 8px;
    padding: 12px;
    overflow-x: auto;
    margin: 8px 0;
    :deep(code) { background: transparent; padding: 0; color: inherit; }
  }

  :deep(a) { color: $primary-40; text-decoration: underline; }

  :deep(blockquote) {
    border-left: 3px solid rgba(0, 106, 100, 0.4);
    padding-left: 12px;
    margin: 8px 0;
    color: $md-sys-color-on-surface-variant;
  }

  :deep(hr) { border: none; border-top: 1px solid rgba(0,0,0,0.08); margin: 10px 0; }
}
```

## 验证结果

### L0: 代码级验证
- [x] `.markdown-body` 子选择器已全部改为 `:deep()` 穿透写法
- [x] 覆盖元素完整：p, h1-h4, ul, ol, li, code, pre, a, blockquote, hr, strong, b
- [x] 保留现有 `v-html="renderMarkdown(msg.content)"` 渲染路径（未修改 script 逻辑）

### L1: 编译验证
- [x] `npm run build:h5` 编译成功
- [x] 零错误（仅 Sass 废弃警告，与本次修改无关）
- [x] 构建输出：`DONE  Build complete.`

### L2: 逻辑验证
- [x] `<script>` 逻辑层未做任何修改（SSE、来源引用、快捷问题发送逻辑保持不变）
- [x] `pages.json` 未修改

### L3: 运行时验证（待集成测试）
- [ ] [H5] 发送多行问题后 AI 气泡高度自适应
- [ ] 段落/列表/加粗/链接完整显示

## 风险与兜底
- **RISK-1**: 如 `:deep()` 在 uni-app H5 模式下不生效，备选方案是将 `.markdown-body` 样式移至独立的 `<style>`（不加 scoped）块
- **当前状态**: 优先使用 `:deep()`，与 RISK-1 兜底口径一致

## 约束遵守情况
- [x] 仅修改 `apps/student-app/src/pages/chat/index.vue` `<style>` 区域
- [x] 未修改 `<script>` 逻辑层
- [x] 未修改 `pages.json`
- [x] 未涉及 services/, apps/teacher-web/, knowledge-base/, scripts/, docs/
- [x] 仅做当前任务，未顺手修复其他问题

## 后续依赖
- FIX-B (Chat 页面双层导航栏修复) 依赖本任务完成，需串行执行
