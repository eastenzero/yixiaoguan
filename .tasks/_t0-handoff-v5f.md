# T0 → T1 交接文档: spec-v5f PDF 页码裁剪

> 日期: 2026-04-07
> 前置: spec-v5e (closed), DEBT-V5E-01 / DEBT-V5D-02
> Spec: `.tasks/_spec-v5f-pdf-page-slice.yaml`

---

## 目标

"查看原始文件"时，**仅加载 KB 条目对应的 PDF 页范围**（如 3-5 页 / ~200KB），
而非全量 120MB / 182 页。关闭 DEBT-V5E-01 / DEBT-V5D-02。

```
[知识详情页] "查看原始文件"
    │
    ▼  GET /api/materials/slice?file=student-handbook.pdf&start=155&end=158
    │
[AI Service] pypdf → 提取 3 页 → 返回子 PDF (~200KB)
    │
    ▼
[PDF 预览页] 仅加载 3 页
```

---

## 模块 & 分工

| 模块 | 标题 | 负责 | 优先级 | 工时 |
|------|------|------|--------|------|
| F-V5F-01 | KB 条目 frontmatter 页码标注 | T1-A | P1 | 2h |
| F-V5F-02 | 入库 & API 层页码透传 | T1-B | P1 | 1h |
| F-V5F-03 | PDF 页码裁剪后端服务 | T1-B | P1 | 2h |
| F-V5F-04 | 前端对接裁剪 PDF | T1-B | P1 | 1h |

### 执行顺序

```
batch-1 (并行):  F-V5F-01 (T1-A, 页码标注)  ‖  F-V5F-03 (T1-B, 裁剪 API)
batch-2:         F-V5F-02 (T1-B, 入库+API透传, 依赖 F-V5F-01)
batch-3:         F-V5F-04 (T1-B, 前端对接, 依赖 F-V5F-02 + F-V5F-03)
post:            重新入库 + docker compose rebuild ai-service
```

---

## F-V5F-01: KB 条目 frontmatter 页码标注

### 目标

为每个来自 `student-handbook.pdf` 的 KB 条目添加 `page_start` / `page_end`。

### 涉及条目

两组 material_id 指向 student-handbook.pdf:

| material_id | KB 条目范围 | 数量 |
|-------------|------------|------|
| `学生手册-生活服务` | KB-0150 ~ KB-0171 | ~22 |
| `HANDBOOK-2026-001` / `002` | KB-20260324-0138 ~ 0149 | ~12 |

### MinerU 数据

```
knowledge-base/raw/student-handbook-mineru/content_list_v2.json
```

- JSON 数组，每个顶级元素 = 1 页的内容块列表
- 共 **122 逻辑页**（PDF 物理页 182 页，MinerU 可能跳过纯图片/空白页）
- 每个块有 `type` (title/paragraph/list/table) 和 `content`

### 推荐做法

**方案 A: 编写脚本** `scripts/build_page_mapping.py`

```python
"""
1. 加载 content_list_v2.json
2. 为每页提取纯文本（拼接所有块的 text content）
3. 对每个 KB 条目:
   - 读取 .md 正文
   - 提取前 100 字作为 needle
   - 在每页文本中搜索
   - 记录 page_start (首次匹配页) 和 page_end (末次匹配页)
4. 更新 frontmatter
5. 输出 CSV 报告供人工校验
"""
```

⚠️ MinerU 逻辑页 vs PDF 物理页可能有偏移。脚本完成后**必须抽查 3-5 条**:
打开 `student-handbook.pdf`，翻到标注的页码，确认内容匹配。

**方案 B: 手工标注**（兜底）

如果脚本匹配不准，直接手动查 PDF 标注。~34 条约需 1h。

### frontmatter 格式

```yaml
---
material_id: "学生手册-生活服务"
title: "电费缴纳指南"
category: "生活服务"
tags: ["电费", "缴费"]
source: "学生手册-生活服务.md 行 4927-5041"
page_start: 155
page_end: 158
---
```

### AC

- **AC-F01**: 所有 student-handbook 来源 KB 条目有 page_start/page_end
- **AC-F02**: 抽查 3 条，页码与 PDF 实际内容匹配

---

## F-V5F-02: 入库 & API 层页码透传

### batch_ingest_kb.py

在 `ingest_kb_entry()` 的 `base_metadata` 中添加:

```python
base_metadata = {
    ...
    "page_start": metadata.get('page_start', ''),
    "page_end": metadata.get('page_end', ''),
}
```

### knowledge.py API

在 `get_entry()` 返回中添加:

```python
return JSONResponse({
    'code': 0,
    'msg': 'success',
    'data': {
        ...
        'page_start': fm.get('page_start', ''),
        'page_end': fm.get('page_end', ''),
    }
})
```

### AC

- **AC-F03**: `GET /api/knowledge/entries/{id}` 返回 page_start/page_end
- **AC-F04**: ChromaDB chunk metadata 含 page_start/page_end（重新入库后）

---

## F-V5F-03: PDF 页码裁剪后端服务

### 新端点

```
GET /api/materials/slice?file={filename}&start={page}&end={page}
```

| 参数 | 说明 |
|------|------|
| `file` | PDF 文件名，如 `student-handbook.pdf` |
| `start` | 起始页码（1-indexed，含） |
| `end` | 结束页码（1-indexed，含） |

### 响应

- **Content-Type**: `application/pdf`
- **Content-Disposition**: `inline; filename="student-handbook_p155-158.pdf"`
- **Body**: 裁剪后 PDF 二进制

### 实现要点

1. **新文件**: `services/ai-service/app/api/materials.py`

2. **依赖**: `requirements.txt` 添加 `pypdf>=4.0`

3. **PDF 文件路径**: AI service 已挂载 `./materials:/app/materials:ro`
   ```python
   _MATERIALS_DIR = Path('/app/materials')
   if not _MATERIALS_DIR.exists():
       _MATERIALS_DIR = Path(__file__).parent.parent.parent.parent.parent / 'deploy' / 'materials'
   ```

4. **安全**:
   - `file` 参数禁止含 `/` `\` `..` → 防路径穿越
   - 单次最多 20 页 → 防全量下载绕过
   - 简单内存缓存（最多 50 个切片）

5. **注册路由** in `main.py`:
   ```python
   from app.api.materials import router as materials_router
   app.include_router(materials_router)
   ```

6. **Nginx 路由** in `student.conf`（与 /api/knowledge/ 同级）:
   ```nginx
   location /api/materials/ {
       proxy_pass http://ai-service:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

### 参考实现

见 spec 文件 `_spec-v5f-pdf-page-slice.yaml` 中 F-V5F-03 的完整代码示例。

### AC

- **AC-F05**: `GET /api/materials/slice?file=student-handbook.pdf&start=1&end=3` → 3 页 PDF
- **AC-F06**: 返回文件 < 2MB（原始 120MB）
- **AC-F07**: `file=../etc/passwd` → 400

---

## F-V5F-04: 前端对接裁剪 PDF

### knowledge/detail.vue 变更

1. **新增 ref**:
   ```typescript
   const pageStart = ref<number>(0)
   const pageEnd = ref<number>(0)
   ```

2. **loadDetail() 成功回调中**:
   ```typescript
   pageStart.value = parseInt(data.page_start) || 0
   pageEnd.value = parseInt(data.page_end) || 0
   ```

3. **openOriginalFile() 改为**:
   ```typescript
   function openOriginalFile() {
     let pdfUrl: string
     const ttl = encodeURIComponent(
       materialTitle.value || fallbackTitle.value || '原始文件'
     )

     if (pageStart.value > 0 && materialFileUrl.value) {
       // 有页码 → 裁剪 API
       const file = materialFileUrl.value.split('/').pop() || ''
       const end = pageEnd.value || (pageStart.value + 4)
       pdfUrl = encodeURIComponent(
         `/api/materials/slice?file=${file}&start=${pageStart.value}&end=${end}`
       )
     } else if (materialFileUrl.value) {
       // 无页码 → 降级全量
       pdfUrl = encodeURIComponent(materialFileUrl.value)
     } else {
       return
     }

     uni.navigateTo({
       url: '/pages/viewer/pdf?url=' + pdfUrl + '&title=' + ttl
     })
   }
   ```

### viewer/pdf.vue

无需改动，`web-view` 的 `src` 直接接受裁剪 API 的 URL。

### AC

- **AC-F08**: 有页码 → 请求裁剪 API → 加载 < 2MB
- **AC-F09**: 无页码 → 降级全量（现有行为不回退）
- **AC-F10**: PDF 预览页正常显示裁剪后内容

---

## 部署步骤（按顺序）

1. F-V5F-01 完成后，push KB 条目 frontmatter 变更
2. F-V5F-03 完成后，rebuild ai-service:
   ```bash
   cd ~/dev/yixiaoguan/deploy
   docker compose build ai-service
   docker compose up -d ai-service
   ```
3. F-V5F-02 完成后，重新入库:
   ```bash
   cd ~/dev/yixiaoguan
   python scripts/batch_ingest_kb.py --yes
   ```
4. 更新 nginx conf 并 reload:
   ```bash
   docker compose exec nginx nginx -s reload
   ```
5. F-V5F-04 完成后，rebuild 前端:
   ```bash
   cd ~/dev/yixiaoguan/apps/student-app
   npm run build
   ```

---

## 服务器信息

- **IP**: 192.168.100.165
- **SSH**: easten@192.168.100.165
- **项目路径**: ~/dev/yixiaoguan/
- **端口**: AI service 8000, business-api 8080, frontend 5173/5174
- **测试账号**: 2524010001 / 2524010001

---

## 风险

| ID | 描述 | 应对 |
|----|------|------|
| RISK-1 | MinerU 逻辑页 vs PDF 物理页偏移 (122 vs 182) | 脚本输出报告 + 人工抽查 |
| RISK-2 | pypdf 加载 120MB PDF 延迟 | 缓存切片结果 |
| RISK-3 | H5 web-view 加载 API URL | 确保用绝对 URL 或相对 URL 可达 |

---

## AC 汇总

| AC | 项目 | 模块 |
|----|------|------|
| AC-F01 | KB 条目有 page_start/page_end | F-V5F-01 |
| AC-F02 | 页码抽查正确 | F-V5F-01 |
| AC-F03 | knowledge API 返回页码 | F-V5F-02 |
| AC-F04 | ChromaDB metadata 含页码 | F-V5F-02 |
| AC-F05 | 裁剪 API 返回子 PDF | F-V5F-03 |
| AC-F06 | 子 PDF < 2MB | F-V5F-03 |
| AC-F07 | 路径穿越拦截 | F-V5F-03 |
| AC-F08 | 前端使用裁剪 API | F-V5F-04 |
| AC-F09 | 无页码时降级 | F-V5F-04 |
| AC-F10 | 预览页正常显示 | F-V5F-04 |
