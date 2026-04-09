# f-v5f-04 前端对接裁剪 PDF - 执行报告

## 任务信息
- **任务ID**: f-v5f-04
- **执行时间**: 2026-04-06
- **修改文件**: `apps/student-app/src/pages/knowledge/detail.vue`

---

## 改动内容

### 1. 添加 pageStart/pageEnd refs（第 64-65 行）
```typescript
const pageStart = ref<number>(0)
const pageEnd = ref<number>(0)
```

### 2. 修改 loadDetail() 成功回调（第 155-156 行）
```typescript
if (data.page_start) pageStart.value = parseInt(String(data.page_start)) || 0
if (data.page_end) pageEnd.value = parseInt(String(data.page_end)) || 0
```

### 3. 替换 openOriginalFile() 函数（第 176-197 行）
```typescript
function openOriginalFile() {
  let pdfUrl: string
  const ttl = encodeURIComponent(
    materialTitle.value || fallbackTitle.value || '原始文件'
  )

  if (pageStart.value > 0 && materialFileUrl.value) {
    const file = materialFileUrl.value.split('/').pop() || ''
    const endPage = pageEnd.value || (pageStart.value + 4)
    pdfUrl = encodeURIComponent(
      '/api/materials/slice?file=' + file + '&start=' + pageStart.value + '&end=' + endPage
    )
  } else if (materialFileUrl.value) {
    pdfUrl = encodeURIComponent(materialFileUrl.value)
  } else {
    return
  }

  uni.navigateTo({
    url: '/pages/viewer/pdf?url=' + pdfUrl + '&title=' + ttl
  })
}
```

---

## BUILD 结果

```
Now using node v24.13.0 (npm v11.6.2)
...
DONE  Build complete.
```

**状态**: BUILD PASS ✓

---

## 关键代码片段确认

| 位置 | 内容 | 状态 |
|------|------|------|
| Line 64-65 | `pageStart` / `pageEnd` refs 定义 | ✓ 已添加 |
| Line 155-156 | page_start/page_end 解析逻辑 | ✓ 已添加 |
| Line 176-197 | `openOriginalFile()` 完整替换 | ✓ 已替换 |

---

## 功能逻辑说明

1. **有页码信息时**: 如果 `pageStart > 0`，构造 `/api/materials/slice?file=xxx&start=N&end=M` URL
2. **默认 endPage 计算**: 如果 `pageEnd` 未设置，使用 `pageStart + 4`（即默认显示5页）
3. **无页码信息时**: 回退到原始行为，直接使用 `materialFileUrl`
4. **无文件 URL 时**: 直接返回，不执行跳转

---

## 无阻塞项

所有步骤执行完成，无阻塞。
