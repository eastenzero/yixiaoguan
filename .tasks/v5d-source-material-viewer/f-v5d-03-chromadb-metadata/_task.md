---
id: "f-v5d-03-chromadb-metadata"
parent: "v5d-source-material-viewer"
type: "feature"
status: "done"
verified_at: "2026-04-07"
verified_by: "T1-L3"
tier: "T3"
priority: "high"
risk: "medium"

scope:
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/scripts/batch_ingestion.py"
out_of_scope:
  - "services/ai-service/app/api/"
  - "services/ai-service/app/core/llm_chat.py"
  - "apps/"
  - "deploy/"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/v5d-source-material-viewer/_task.md"
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/scripts/batch_ingestion.py"
  - "deploy/materials/material-index.json"   # T1-A 产出，执行前确认存在

done_criteria:
  L0: |
    chunker.py 第 122-123 行不再出现 "# Document"，
    batch_ingestion.py 包含 material-index.json 加载逻辑
  L1: |
    在 165 服务器上执行重新入库（dry-run 先验证）：
    cd ~/dev/yixiaoguan/services/ai-service
    source venv/bin/activate
    python scripts/batch_ingestion.py --source-dir ../../knowledge-base/raw/first-batch-processing/converted/markdown --dry-run
    → 无报错，每个文件处理 OK
  L2: |
    执行正式入库（非 dry-run）后验证 ChromaDB metadata：
    python -c "
    import sys; sys.path.insert(0, '.')
    from app.core.kb_vectorize import vector_store
    vector_store.initialize()
    results = vector_store.search_similar('请假流程', top_k=3)
    for r in results:
        print(r.entry_id, r.metadata.get('material_file_url', 'MISSING'), r.metadata.get('material_title', 'MISSING'))
    "
    → 有 material_id 对应 PDF 的条目，metadata 含 material_file_url（格式 /materials/xxx.pdf）
    → 无对应 PDF 的条目，material_file_url 为 None 或不存在（不报错）
  L3: |
    T1 检查：
    - chunker.py 修改：_split_by_headings 使用 title 参数而非硬编码 "Document"
    - batch_ingestion.py: 加载路径正确（相对 SERVICE_DIR 定位 deploy/materials/material-index.json）
    - 入库日志中出现 material_file_url 注入成功的记录

depends_on: []
prerequisite: "deploy/materials/material-index.json 必须由 T1-A (F-V5D-01) 先产出"
created_at: "2026-04-06"
---

# F-V5D-03: ChromaDB chunk 元数据补充 material_file_url

> 完成后：重新入库后，ChromaDB 中有 PDF 对应的 chunk metadata 含 material_file_url 字段，
> 无 PDF 对应的 chunk 字段为空（不报错），AI 返回时前端可据此显示"查看原始文件"按钮。

## 前置条件

`deploy/materials/material-index.json` 必须由 T1-A (F-V5D-01) 先完成。
执行前验证：
```bash
ls -lh ~/dev/yixiaoguan/deploy/materials/material-index.json
# 应存在且非空
cat ~/dev/yixiaoguan/deploy/materials/material-index.json | python3 -m json.tool | head -20
```

---

## 变更一：chunker.py 修复虚拟标题

**文件**：`services/ai-service/app/core/chunker.py`

### 修改 `split()` 方法签名（加 title 参数）

当前（约第 55 行）：
```python
def split(
    self,
    text: str,
    source_path: str = "",
    base_metadata: Optional[Dict[str, Any]] = None,
) -> List[TextChunk]:
```

改为：
```python
def split(
    self,
    text: str,
    source_path: str = "",
    base_metadata: Optional[Dict[str, Any]] = None,
    title: str = "Document",
) -> List[TextChunk]:
```

### 修改 `split()` 调用 `_split_by_headings`（约第 80 行）

当前：
```python
sections = self._split_by_headings(text)
```

改为：
```python
sections = self._split_by_headings(text, title=title)
```

### 修改 `_split_by_headings()` 方法签名和行为（约第 114 行）

当前：
```python
def _split_by_headings(self, text: str) -> List[Dict[str, Any]]:
```
```python
        if not text.lstrip().startswith('#'):
            text = "# Document\n" + text
```

改为：
```python
def _split_by_headings(self, text: str, title: str = "Document") -> List[Dict[str, Any]]:
```
```python
        if not text.lstrip().startswith('#'):
            text = f"# {title}\n" + text
```

---

## 变更二：batch_ingestion.py 注入 material_file_url

**文件**：`services/ai-service/scripts/batch_ingestion.py`

### Step 1：在文件顶部（常量区）添加 material-index.json 加载逻辑

在 `DEFAULT_SOURCE_DIR` 定义之后（约第 44 行后），添加：
```python
# ── material-index.json 路径（T1-A 产出）──
MATERIAL_INDEX_PATH = SERVICE_DIR.parent.parent / "deploy" / "materials" / "material-index.json"

def _load_material_index() -> dict:
    """加载原始材料映射索引，文件不存在时返回空字典"""
    if not MATERIAL_INDEX_PATH.exists():
        print(f"[警告] material-index.json 不存在: {MATERIAL_INDEX_PATH}，material_file_url 将不注入")
        return {}
    with open(MATERIAL_INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### Step 2：在 `run_batch_ingestion()` 开头加载索引

在 `run_batch_ingestion()` 函数（约第 296 行）中，`report = BatchReport()` 之后，添加：
```python
    # 加载 material-index.json 映射表
    material_index = _load_material_index()
    print(f"[材料索引] 加载完成，共 {len(material_index)} 条映射")
```

将 `material_index` 传入 `process_single_file`：
```python
# 原调用（约第 365 行）：
result = process_single_file(file_path, splitter, dry_run)

# 改为：
result = process_single_file(file_path, splitter, dry_run, material_index=material_index)
```

### Step 3：修改 `process_single_file()` 函数签名

当前：
```python
def process_single_file(
    file_path: Path,
    splitter: MarkdownTextSplitter,
    dry_run: bool = False,
) -> IngestionResult:
```

改为：
```python
def process_single_file(
    file_path: Path,
    splitter: MarkdownTextSplitter,
    dry_run: bool = False,
    material_index: dict = None,
) -> IngestionResult:
```

### Step 4：在 `process_single_file()` 中提取 material_id 并注入 URL

在 `title` 提取之后（约第 206 行后），在 `base_metadata = {...}` 之前，添加：
```python
        # 提取 material_id 和 PDF 映射
        material_id = metadata.get('material_id', '')
        material_info = (material_index or {}).get(material_id, {}) if material_id else {}
        material_pdf = material_info.get('pdf', '')
        material_file_url = f"/materials/{material_pdf}" if material_pdf else None
        material_title_from_index = material_info.get('title', '')
```

修改 `chunk_metadata` 合并（约第 246 行），在合并字典末尾加入新字段：
```python
            chunk_metadata = {
                **chunk.metadata,
                "chunk_index": chunk.index,
                "total_chunks": len(chunks),
                "source_file": str(file_path.name),
                # F-V5D-03: 原件 PDF 链接（无对应 PDF 时为 None）
                "material_file_url": material_file_url,
                "material_title": material_title_from_index or title,
            }
```

### Step 5：将 title 传给 splitter.split()（用于 chunker 修复）

修改 splitter 调用（约第 221 行）：
```python
# 原：
chunks = splitter.split(
    text=body_content,
    source_path=str(file_path),
    base_metadata=base_metadata,
)
# 改为：
chunks = splitter.split(
    text=body_content,
    source_path=str(file_path),
    base_metadata=base_metadata,
    title=title,
)
```

---

## 入库命令（完成后在 165 执行）

```bash
cd ~/dev/yixiaoguan/services/ai-service
source venv/bin/activate

# 先 dry-run 确认无报错
python scripts/batch_ingestion.py \
  --source-dir ../../knowledge-base/raw/first-batch-processing/converted/markdown \
  --dry-run

# 确认 OK 后正式入库（会覆盖已有条目）
python scripts/batch_ingestion.py \
  --source-dir ../../knowledge-base/raw/first-batch-processing/converted/markdown
```

---

## 已知陷阱

- `MATERIAL_INDEX_PATH` 相对路径：`SERVICE_DIR` 是 `services/ai-service/`，往上两级到项目根，再进 `deploy/materials/material-index.json`
- material_id 可能为空字符串或缺失 key → 代码中用 `if material_id` 防空
- ChromaDB metadata 值不支持 `None`，若 material_file_url 为 None 应改为空字符串 `""`，或者在注入前判断：`"material_file_url": material_file_url or ""`
