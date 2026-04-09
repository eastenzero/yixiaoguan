# T0 → T1 交接文档: spec-v5e 参考资料两级导航 + CSS 修复

> 日期: 2026-04-07
> 前置: spec-v5d (completed), v5c push (3397994)
> Spec: `.tasks/_spec-v5e-reference-flow-polish.yaml`

---

## 目标

将"点击参考来源 → 直接打开全量 PDF"的一级跳转，
改为 **两级导航**：

```
点击来源卡片 → [一级] 知识详情页（完整 MD 渲染）
                        ↓ "查看原始文件" 按钮
               [二级] PDF 预览页（相关页码）
```

附带修复 4 项 CSS DEBT。

---

## 模块概览 & T1 分工

| 模块 | 标题 | 负责 | 优先级 | 工时 |
|------|------|------|--------|------|
| F-V5E-01 | CSS/UI 快速修复（4项DEBT） | T1-A | P1 | 1h |
| F-V5E-02 | 知识条目完整内容 API | T1-B | P1 | 2h |
| F-V5E-03 | 前端导航流程重构 | T1-B | P1 | 2h |
| F-V5E-04 | PDF 页码定位 | T1-B | P2 | 3h（可后续） |

### 执行顺序

```
batch-1 (并行):  F-V5E-01 (T1-A, CSS)  ‖  F-V5E-02 (T1-B, API)
batch-2:         F-V5E-03 (T1-B, 前端导航重构, 依赖 F-V5E-02 + F-V5E-01 合并后)
batch-3:         F-V5E-04 (T1-B, PDF 页码, P2 可选)
```

⚠️ **F-V5E-01 和 F-V5E-03 都改 chat/index.vue**，所以 F-V5E-01 必须先合并再启动 F-V5E-03。

---

## F-V5E-01: CSS/UI 快速修复

### 1.1 DEBT-V5D-01 — 参考资料卡片溢出

**文件**: `apps/student-app/src/pages/chat/index.vue`
**位置**: `.source-item` 样式 (约 L1181)

```scss
// 当前
.source-item {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  padding: 8px 10px;
  // ...
}

// 改为
.source-item {
  display: flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  padding: 8px 10px;
  box-sizing: border-box;   // ← 新增
  // ...
}
```

并在 `.message-sources` 添加 `overflow: hidden`。

### 1.2 UI-02 — 弹层底部按钮被遮挡

**文件**: `apps/student-app/src/pages/chat/index.vue`
**位置**: `.source-preview-actions` 样式

```scss
.source-preview-actions {
  // 现有样式...
  padding-bottom: calc(env(safe-area-inset-bottom, 0px) + 16px);  // ← 新增
}
```

### 1.3 UI-01 — 卡片边框/背景色不协调

**文件**: `apps/student-app/src/pages/chat/index.vue`
**位置**: `.source-item` 样式 (约 L1188-1189)

```scss
// 当前
background: #ffffff;
border: 1px solid rgba(0, 106, 100, 0.2);

// 改为
background: rgba(0, 106, 100, 0.04);
border: 1px solid rgba(0, 106, 100, 0.15);
```

### 1.4 #006a64 硬编码清理

将以下文件中的 `#006a64` 替换为 SCSS 变量 `$primary`（已在 theme.scss 定义）：

| 文件 | 处理方式 |
|------|----------|
| `App.vue` | 替换为 `$primary` |
| `components/CustomTabBar.vue` | 替换为 `$primary` |
| `pages/apply/detail.vue` (2处) | 替换为 `$primary` |
| `pages/apply/classroom.vue` | 替换为 `$primary` |
| `pages/apply/status.vue` | 替换为 `$primary` |
| `pages/chat/index.vue` (.back-icon) | 替换为 `$primary` |
| `pages/knowledge/detail.vue` | 替换为 `$primary` |
| `pages/questions/index.vue` | 替换为 `$primary` |
| `pages/viewer/pdf.vue` (.back-icon) | 替换为 `$primary` |
| `styles/theme.scss` | **保留**（这是定义处） |
| `pages.json` | **保留**（原生配置不支持 SCSS 变量，加 `// primary color` 注释） |

注意：替换前确认文件已 `@import '@/styles/theme.scss'`，否则需添加导入。

### AC 验收

- AC-E01: 卡片不溢出
- AC-E02: 弹层按钮完全可见
- AC-E03: 卡片背景色协调
- AC-E04: 除 pages.json/theme.scss 外，无 #006a64 硬编码

---

## F-V5E-02: 知识条目完整内容 API

### 端点

```
GET /api/knowledge/entries/{entry_id}
```

### 逻辑

1. 接收 `entry_id`（chunk ID 或 base entry ID 均可）
   - chunk ID: `"KB-0150-电费缴纳指南__chunk_0"`
   - base ID: `"KB-0150-电费缴纳指南"`
2. 提取 base_entry_id: `entry_id.split("__chunk_")[0]`
3. **推荐方案**: 直接读取 knowledge-base 的 .md 文件
   - 文件路径规则: 在 `knowledge-base/entries/` 下递归搜索 `{base_entry_id}.md`
   - 解析 frontmatter (YAML) + body (Markdown)
   - 从 frontmatter 提取 material_id
   - 用 material_id 查 `deploy/materials/material-index.json` → 得到 PDF 路径
4. **备选方案**: ChromaDB 聚合
   - query all chunks with ID prefix = base_entry_id
   - 排序 + 拼接 → 完整文档
   - 从 metadata 取 material_file_url

### 响应格式

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "entry_id": "KB-0150-电费缴纳指南",
    "title": "电费缴纳指南",
    "content": "## 电费缴纳指南\n\n### 缴费方式\n完美校园APP...",
    "material_file_url": "/materials/student-handbook.pdf",
    "material_title": "学生手册（含图片版）",
    "chunk_count": 3,
    "metadata": {
      "category": "生活服务",
      "tags": ["电费", "缴费"]
    }
  }
}
```

错误: 404 `{ "code": 404, "msg": "条目不存在" }`

### 文件

- **新建**: `services/ai-service/app/api/knowledge.py`
- **修改**: `services/ai-service/app/main.py` (注册路由)

### Nginx 路由

当前 `student.conf` 已有 `/api/` → `business-api:8080` 的通用规则。
新的 `/api/knowledge/` 需要路由到 AI service (`ai-service:8000`)。

在 `student.conf` 中 `/api/chat` 规则之后、通用 `/api/` 之前添加:

```nginx
# ── 知识库 API（AI service）──
location /api/knowledge/ {
    proxy_pass http://ai-service:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### 知识库文件结构

```
knowledge-base/entries/
├── 入学与学籍/
│   ├── KB-0150-电费缴纳指南.md
│   └── ...
├── 事务申请与审批/
│   └── ...
└── first-batch-drafts/
    └── ...
```

每个 .md 文件格式:
```markdown
---
title: "电费缴纳指南"
material_id: "学生手册-生活服务"
tags: ["电费", "缴费"]
...
---

## 电费缴纳指南

正文内容...
```

### AC 验收

- AC-E05: `GET /api/knowledge/entries/KB-0150-电费缴纳指南` 返回完整 MD
- AC-E06: `GET /api/knowledge/entries/KB-0150-电费缴纳指南__chunk_0` 同样工作
- AC-E07: 返回 `material_file_url` 字段

---

## F-V5E-03: 前端导航流程重构

### chat/index.vue 变更

#### 3.1 handleSourceClick 重构

```typescript
// 当前（有问题）:
async function handleSourceClick(source: Source) {
  if (source.entry_id) {
    const entryId = normalizeEntryId(source.entry_id)  // ← 转数字，字符串 ID 永远失败
    if (entryId) { ... }
  }
  // 降级弹层
}

// 改为:
async function handleSourceClick(source: Source) {
  if (source.entry_id) {
    const baseEntryId = extractBaseEntryId(source.entry_id)
    if (baseEntryId) {
      try {
        await navigateToPage(
          '/pages/knowledge/detail?entry_id=' + encodeURIComponent(baseEntryId)
          + '&title=' + encodeURIComponent(source.title || '')
          + '&summary=' + encodeURIComponent((source.content || '').slice(0, 300))
          + '&score=' + (source.score ?? '')
          + '&material_file_url=' + encodeURIComponent(source.material_file_url || '')
          + '&material_title=' + encodeURIComponent(source.material_title || '')
        )
        return
      } catch (error) {
        console.warn('知识详情跳转失败，降级弹层:', error)
      }
    }
  }
  // 降级: 弹层显示摘要
  if (source.content) { showSourcePreviewPopup(source); return }
  if (source.url) { handleLinkClick(source.url); return }
}

function extractBaseEntryId(rawEntryId: string): string {
  if (!rawEntryId) return ''
  return rawEntryId.split('__chunk_')[0]
}
```

#### 3.2 简化 openSourceDetailFromPreview

弹层中的 "查看详细资料" 按钮: 跳知识详情页（而非直接跳 PDF）

```typescript
async function openSourceDetailFromPreview() {
  const source = sourcePreview.value
  const baseEntryId = extractBaseEntryId(source.entryId)
  if (baseEntryId) {
    try {
      await navigateToPage(
        '/pages/knowledge/detail?entry_id=' + encodeURIComponent(baseEntryId)
        + '&title=' + encodeURIComponent(source.title)
        + '&summary=' + encodeURIComponent(source.content)
        + '&score=' + (source.score ?? '')
        + '&material_file_url=' + encodeURIComponent(source.materialFileUrl || '')
      )
      closeSourcePreview()
      return
    } catch {}
  }
  closeSourcePreview()
}
```

#### 3.3 弹层按钮文字

```vue
<!-- 当前: {{ sourcePreview.materialFileUrl ? '查看原始文件' : '查看参考摘要' }} -->
<!-- 改为: 统一 -->
查看详细资料
```

### knowledge/detail.vue 变更

#### 3.4 onLoad 接收 entry_id 为字符串

```typescript
// 当前: entryId.value = parseEntryId(options?.id)  // 转数字
// 改为:
const entryIdStr = ref<string>('')
const materialFileUrl = ref<string>('')
const materialTitle = ref<string>('')

onLoad((options) => {
  entryIdStr.value = decodeText(options?.entry_id || options?.id || '')
  fallbackTitle.value = decodeText(options?.title)
  fallbackSummary.value = decodeText(options?.summary)
  fallbackScore.value = parseScore(options?.score)
  materialFileUrl.value = decodeText(options?.material_file_url)
  materialTitle.value = decodeText(options?.material_title)
  loadDetail()
})
```

#### 3.5 loadDetail 调用新 API

```typescript
import { getKnowledgeEntryFull } from '@/api/knowledge'

async function loadDetail() {
  if (!entryIdStr.value) {
    loadFailed.value = true
    isLoading.value = false
    return
  }
  try {
    const data = await getKnowledgeEntryFull(entryIdStr.value)
    if (data) {
      entry.value = {
        title: data.title,
        content: data.content,
        // 其他字段按需映射
      } as any
      materialFileUrl.value = data.material_file_url || materialFileUrl.value
      materialTitle.value = data.material_title || materialTitle.value
      loadFailed.value = false
    } else {
      loadFailed.value = true
    }
  } catch {
    loadFailed.value = true
  }
  isLoading.value = false
}
```

#### 3.6 "查看原始文件" 按钮

在模板中，正文区下方添加:

```vue
<button
  v-if="materialFileUrl"
  class="view-original-btn"
  @click="openOriginalFile"
>
  查看原始文件
</button>
```

```typescript
function openOriginalFile() {
  const url = encodeURIComponent(materialFileUrl.value)
  const title = encodeURIComponent(materialTitle.value || displayTitle.value)
  uni.navigateTo({ url: '/pages/viewer/pdf?url=' + url + '&title=' + title })
}
```

### api/knowledge.ts 变更

```typescript
import { request } from '@/utils/request'

export async function getKnowledgeEntryFull(entryId: string) {
  try {
    const res = await request.get(`/api/knowledge/entries/${encodeURIComponent(entryId)}`)
    if (res.data?.code === 0) {
      return res.data.data
    }
    return null
  } catch {
    return null
  }
}
```

### AC 验收

- AC-E08: 点击参考资料卡片 → 跳转知识详情页
- AC-E09: 知识详情页展示完整 KB 条目 Markdown（非碎片）
- AC-E10: 知识详情页有 "查看原始文件" 按钮 → PDF 预览
- AC-E11: API 失败时降级显示 chunk 摘要

---

## F-V5E-04: PDF 页码定位（P2, 可后续）

本轮 MVP: 如果页码数据不可用，先跳过此模块。
PDF 入口已从聊天页移至知识详情页，用户体验已显著改善。

如果实施:
1. PDF URL 改为: `/materials/student-handbook.pdf#page=42`
2. 浏览器内置 PDF 阅读器支持 `#page=N` fragment
3. 页码数据来源: chunk metadata 中的 `page_start` 字段

---

## 服务器信息

- IP: 192.168.100.165
- SSH: easten@192.168.100.165
- 项目路径: ~/dev/yixiaoguan/
- 端口: AI service 8000, business-api 8080, 前端 5173/5174
- 测试账号: 2524010001 / 2524010001

## 全局 AC 汇总

| AC | 项目 | 模块 | 优先级 |
|----|------|------|--------|
| AC-E01 | 卡片不溢出 | F-V5E-01 | P1 |
| AC-E02 | 弹层按钮可见 | F-V5E-01 | P1 |
| AC-E03 | 卡片背景色协调 | F-V5E-01 | P1 |
| AC-E04 | 硬编码清理 | F-V5E-01 | P1 |
| AC-E05 | API 返回完整 MD | F-V5E-02 | P1 |
| AC-E06 | chunk ID 提取 base ID | F-V5E-02 | P1 |
| AC-E07 | API 返回 material_file_url | F-V5E-02 | P1 |
| AC-E08 | 来源 → 知识详情页 | F-V5E-03 | P1 |
| AC-E09 | 详情页完整 MD | F-V5E-03 | P1 |
| AC-E10 | "查看原始文件" 按钮 | F-V5E-03 | P1 |
| AC-E11 | API 失败降级 | F-V5E-03 | P1 |
| AC-E12 | PDF #page=N | F-V5E-04 | P2 |
| AC-E13 | PDF 自动滚动 | F-V5E-04 | P2 |

---

## T0 最终验收 (2026-04-07)

### 验收结论：**PASS**（附 P2 遗留）

| AC | 项目 | 结果 | 备注 |
|----|------|------|------|
| AC-E01 | 卡片不溢出 | ✅ PASS | T1-A commit 365139b |
| AC-E02 | 弹层按钮可见 | ✅ PASS | T1-A commit 365139b |
| AC-E03 | 卡片背景色协调 | ✅ PASS | T1-A commit 365139b |
| AC-E04 | #006a64 硬编码清理 | ✅ PASS | T1-A commit 365139b |
| AC-E05 | API 返回完整 MD | ✅ PASS | T1-B |
| AC-E06 | chunk ID → base ID | ✅ PASS | T1-B |
| AC-E07 | API 返回 material_file_url | ✅ PASS | T1-B |
| AC-E08 | 来源 → 知识详情页 | ✅ PASS | T0 人工确认 |
| AC-E09 | 详情页完整 MD | ✅ PASS | T0 人工确认 |
| AC-E10 | "查看原始文件" 按钮 | ✅ PASS | T0 人工确认 |
| AC-E11 | API 失败降级 | ✅ PASS | T0 人工确认 |
| AC-E12 | PDF #page=N | ⏭ P2 DEBT | 合并 DEBT-V5D-02，下轮迭代 |
| AC-E13 | PDF 自动滚动 | ⏭ P2 DEBT | 同上 |

### T1 交付记录

| commit | 任务 | 内容 |
|--------|------|------|
| 365139b | F-V5E-01 | CSS 4 项修复（溢出/遮挡/配色/硬编码） |
| 957028f | nginx-knowledge | /api/knowledge/ → ai-service:8000 路由 |
| — | F-V5E-02 | 知识条目完整内容 API |
| — | F-V5E-03 | 前端导航流程重构 |

### 遗留 DEBT

- **DEBT-V5E-01 / DEBT-V5D-02**: PDF 页码定位（#page=N 或 pypdf 切片）→ 下轮迭代

### spec-v5e 状态: **CLOSED ✅**
