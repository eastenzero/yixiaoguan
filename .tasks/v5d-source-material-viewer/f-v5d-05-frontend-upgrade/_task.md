---
id: "f-v5d-05-frontend-upgrade"
parent: "v5d-source-material-viewer"
type: "feature"
status: "done"
verified_at: "2026-04-07"
verified_by: "T1-L3"
tier: "T3"
priority: "high"
risk: "medium"

scope:
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages/viewer/pdf.vue"    # 新建
  - "apps/student-app/src/pages.json"
out_of_scope:
  - "services/"
  - "deploy/"
  - "apps/student-app/src/api/"
  - "apps/student-app/src/pages/knowledge/"        # 不删除（保留备用）
  - "apps/student-app/src/styles/"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/pages.json"
  - ".tasks/v5d-source-material-viewer/f-v5d-04-api-passthrough/_task.md"

done_criteria:
  L0: |
    apps/student-app/src/pages/viewer/pdf.vue 文件存在
    pages.json 包含 "pages/viewer/pdf" 路由
  L1: |
    本地构建无报错：
    cd apps/student-app && npx uni build -p h5
    → 无 TypeScript/Vue 编译错误
  L2: |
    在 165 服务器上重建 student-app 静态产物：
    source ~/.nvm/nvm.sh && nvm use 24
    npx uni build -p h5
    重启 nginx: docker compose restart nginx
    在手机浏览器：
    - 访问 http://192.168.100.165，登录 2524010001
    - 提问"请假流程"，收到 AI 回复后点击参考资料条目
    - 弹层标题为 material_title（不含 "片段X/N" 后缀）
    - 弹层底部按钮文案为 "查看原始文件"（非 "查看完整资料"）
    - 点击"查看原始文件"跳转 PDF 预览页，能看到 PDF 内容
    - PDF 预览页有返回键
  L3: |
    T1 检查：
    - Source interface 扩展了 material_file_url 和 material_title（可选字段）
    - SSE 解析新增了这两个字段的映射
    - handleSourceClick 逻辑保持降级策略（有 PDF → PDF 预览；无 PDF → 弹层摘要）
    - 按钮遮挡问题已修复（弹层 actions 区域有足够 padding-bottom）
    - 参考资料卡片边框对齐（UI精修）

depends_on: ["f-v5d-04-api-passthrough", "f-v5d-02-nginx-materials-route"]
created_at: "2026-04-06"
---

# F-V5D-05: 前端参考资料交互升级

> 完成后：点击 AI 回复的参考资料 → 弹层显示摘要 + "查看原始文件"按钮；
> 点击按钮 → 跳转 PDF 预览页（web-view 嵌入）；
> 无 PDF 的来源 → 按钮灰显；弹层按钮不再被底栏遮挡。

---

## 变更一：chat/index.vue — 类型定义扩展

**文件**：`apps/student-app/src/pages/chat/index.vue`

### 1a. Source interface（约第 243-249 行）

当前：
```typescript
interface Source {
  entry_id: string
  title: string
  content?: string
  url: string
  score?: number
}
```

改为：
```typescript
interface Source {
  entry_id: string
  title: string
  content?: string
  url: string
  score?: number
  material_file_url?: string
  material_title?: string
}
```

### 1b. sourcePreview ref（约第 269-281 行）

当前：
```typescript
const sourcePreview = ref<{
  visible: boolean
  entryId: string
  title: string
  content: string
  score?: number
}>({
  visible: false,
  entryId: '',
  title: '',
  content: '',
  score: undefined
})
```

改为：
```typescript
const sourcePreview = ref<{
  visible: boolean
  entryId: string
  title: string
  content: string
  score?: number
  materialFileUrl?: string
}>({
  visible: false,
  entryId: '',
  title: '',
  content: '',
  score: undefined,
  materialFileUrl: undefined
})
```

---

## 变更二：SSE 解析 — 新字段映射

**两处** source 映射（约第 478-484 行 和 第 507-513 行），都改为：

当前：
```typescript
pendingSources = data.sources.map((s: any) => ({
  entry_id: s.entry_id || '',
  title: s.title || '未知来源',
  content: s.content || '',
  url: s.url || '',
  score: s.score
}))
```

改为：
```typescript
pendingSources = data.sources.map((s: any) => ({
  entry_id: s.entry_id || '',
  title: s.title || '未知来源',
  content: s.content || '',
  url: s.url || '',
  score: s.score,
  material_file_url: s.material_file_url || '',
  material_title: s.material_title || ''
}))
```

---

## 变更三：showSourcePreviewPopup — 存储 materialFileUrl

当前（约第 630-638 行）：
```typescript
function showSourcePreviewPopup(source: Source) {
  sourcePreview.value = {
    visible: true,
    entryId: source.entry_id || '',
    title: source.title || '参考资料',
    content: source.content || '暂未获取到摘要内容，可稍后重试查看详情。',
    score: source.score
  }
}
```

改为：
```typescript
function showSourcePreviewPopup(source: Source) {
  sourcePreview.value = {
    visible: true,
    entryId: source.entry_id || '',
    title: source.material_title || source.title || '参考资料',
    content: source.content || '暂未获取到摘要内容，可稍后重试查看详情。',
    score: source.score,
    materialFileUrl: source.material_file_url || ''
  }
}
```

---

## 变更四：openSourceDetailFromPreview — PDF 优先逻辑

当前（约第 644-661 行）：
```typescript
async function openSourceDetailFromPreview() {
  const source = sourcePreview.value
  if (!source.entryId) {
    closeSourcePreview()
    return
  }
  try {
    await navigateToPage(
      `/pages/knowledge/detail?id=${encodeURIComponent(source.entryId)}&title=${encodeURIComponent(source.title)}&summary=${encodeURIComponent(source.content)}&score=${source.score ?? ''}`
    )
    closeSourcePreview()
  } catch {
    uni.showToast({
      title: '详情页暂不可用',
      icon: 'none'
    })
  }
}
```

改为：
```typescript
async function openSourceDetailFromPreview() {
  const source = sourcePreview.value

  // 优先：有 PDF 链接 → 跳 PDF 预览页
  if (source.materialFileUrl) {
    const pdfUrl = encodeURIComponent(source.materialFileUrl)
    const title = encodeURIComponent(source.title)
    try {
      await navigateToPage(`/pages/viewer/pdf?url=${pdfUrl}&title=${title}`)
      closeSourcePreview()
      return
    } catch {
      // PDF 预览跳转失败，降级到知识详情
    }
  }

  // 降级：无 PDF → 跳知识详情页
  if (!source.entryId) {
    closeSourcePreview()
    return
  }
  try {
    await navigateToPage(
      `/pages/knowledge/detail?id=${encodeURIComponent(source.entryId)}&title=${encodeURIComponent(source.title)}&summary=${encodeURIComponent(source.content)}&score=${source.score ?? ''}`
    )
    closeSourcePreview()
  } catch {
    uni.showToast({
      title: '详情页暂不可用',
      icon: 'none'
    })
  }
}
```

---

## 变更五：弹层模板 — 按钮文案 + 灰显逻辑 + UI精修

**Template 部分**（约第 195-207 行），source-preview-actions：

当前：
```html
<view class="source-preview-actions">
  <button
    v-if="sourcePreview.entryId"
    class="preview-btn preview-btn-primary"
    @click="openSourceDetailFromPreview"
  >
    查看完整资料
  </button>
  <button class="preview-btn preview-btn-ghost" @click="closeSourcePreview">
    知道了
  </button>
</view>
```

改为：
```html
<view class="source-preview-actions">
  <button
    v-if="sourcePreview.entryId || sourcePreview.materialFileUrl"
    class="preview-btn preview-btn-primary"
    :class="{ 'preview-btn-disabled': !sourcePreview.materialFileUrl && !sourcePreview.entryId }"
    :disabled="!sourcePreview.materialFileUrl && !sourcePreview.entryId"
    @click="openSourceDetailFromPreview"
  >
    {{ sourcePreview.materialFileUrl ? '查看原始文件' : '查看参考摘要' }}
  </button>
  <button class="preview-btn preview-btn-ghost" @click="closeSourcePreview">
    知道了
  </button>
</view>
```

---

## 变更六：SCSS 精修 — 按钮遮挡 + 卡片边框

**Style 部分**（约第 833 行之后），在 `.source-preview-actions` 区块：

找到或添加：
```scss
.source-preview-actions {
  display: flex;
  gap: 8px;
  padding: 12px 16px;
  padding-bottom: max(12px, env(safe-area-inset-bottom, 12px));  // 修复底栏遮挡
  border-top: 1px solid $md-sys-color-outline-variant;
  
  .preview-btn {
    flex: 1;
    height: 44px;
    border-radius: $radius-lg;
    font: $text-label-large;
    display: flex;
    align-items: center;
    justify-content: center;   // 修复按钮文字居中
    text-align: center;
  }
  
  .preview-btn-primary {
    background: $primary;
    color: #ffffff;
    border: none;
  }
  
  .preview-btn-ghost {
    background: transparent;
    color: $primary;
    border: 1px solid $primary;
  }
  
  .preview-btn-disabled {
    background: $md-sys-color-outline-variant;
    color: $md-sys-color-on-surface-variant;
    pointer-events: none;
  }
}
```

对 `.source-item`（参考资料卡片条目）也做对齐修复：
```scss
.source-item {
  display: flex;
  align-items: center;
  padding: 10px 12px;
  border-radius: $radius-md;
  border: 1px solid $md-sys-color-outline-variant;  // 统一边框颜色
  background: $md-sys-color-surface;                 // 统一背景色
  margin-bottom: 6px;
  gap: 6px;
  cursor: pointer;
  
  &:active {
    background: $md-sys-color-surface-variant;
  }
}
```

---

## 新建文件：pages/viewer/pdf.vue

**路径**：`apps/student-app/src/pages/viewer/pdf.vue`

```vue
<template>
  <view class="pdf-viewer-page">
    <view class="navbar">
      <view class="back-btn" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <text class="title">{{ pageTitle }}</text>
    </view>
    <web-view class="pdf-frame" :src="pdfSrc" />
  </view>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { onLoad } from '@dcloudio/uni-app'

const pdfSrc = ref('')
const pageTitle = ref('原始文件')

onLoad((options: any) => {
  if (options?.url) {
    pdfSrc.value = decodeURIComponent(options.url)
  }
  if (options?.title) {
    pageTitle.value = decodeURIComponent(options.title)
  }
})

function goBack() {
  uni.navigateBack()
}
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

.pdf-viewer-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  height: 100dvh;
  background: $md-sys-color-background;
}

.navbar {
  display: flex;
  align-items: center;
  height: 44px;
  padding-top: var(--status-bar-height, 44px);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  flex-shrink: 0;
  padding-left: 8px;
  padding-right: 16px;
  gap: 8px;

  .back-btn {
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: $radius-md;
    
    &:active {
      background: rgba(0, 0, 0, 0.06);
    }
    
    .back-icon {
      font-size: 20px;
      color: $primary;
    }
  }

  .title {
    flex: 1;
    font: $text-title-medium;
    color: $md-sys-color-on-background;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.pdf-frame {
  flex: 1;
  width: 100%;
}
</style>
```

---

## pages.json — 注册新路由

在 `pages` 数组中，`pages/knowledge/detail` 条目之后添加：
```json
{
  "path": "pages/viewer/pdf",
  "style": {
    "navigationBarTitleText": "原始文件",
    "navigationStyle": "custom"
  }
}
```

---

## 已知陷阱

- **RISK-4（H5 web-view 限制）**: H5 环境下 `<web-view>` 是模拟实现，使用 `<iframe>` 渲染 PDF 时某些移动端浏览器（尤其 iOS Safari）可能无法内嵌。若预览空白，降级提示文案："如无法预览，请长按复制链接到浏览器打开"
- `env(safe-area-inset-bottom)` 在非 iOS 设备返回 0，加 `max(12px, ...)` 确保最小间距
- PDF URL 格式为 `/materials/xxx.pdf`（相对路径），在 H5 环境下会自动拼接当前 host。`pdfSrc` 会是 `http://192.168.100.165/materials/xxx.pdf`，Nginx 已配置 Content-Disposition: inline，可内嵌显示
- uni-app H5 build 时 `<web-view>` 编译为 `<iframe>`，`src` 属性有效
- SCSS 精修区不要改动 `$primary` 变量（已在 `@import '@/styles/theme.scss'` 中定义），直接用即可
