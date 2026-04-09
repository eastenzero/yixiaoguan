---
id: "f-v5d-04-api-passthrough"
parent: "v5d-source-material-viewer"
type: "feature"
status: "done"
verified_at: "2026-04-07"
verified_by: "T1-L3"
tier: "T3"
priority: "high"
risk: "low"

scope:
  - "services/ai-service/app/core/llm_chat.py"
  - "services/ai-service/app/api/chat.py"
out_of_scope:
  - "services/ai-service/app/core/chunker.py"
  - "services/ai-service/scripts/"
  - "apps/"
  - "deploy/"

context_files:
  - ".teb/antipatterns.md"
  - "services/ai-service/app/core/llm_chat.py"
  - "services/ai-service/app/api/chat.py"
  - "services/ai-service/app/core/kb_vectorize.py"
  - ".tasks/v5d-source-material-viewer/f-v5d-03-chromadb-metadata/_task.md"

done_criteria:
  L0: |
    chat.py SourceItemDTO 包含 material_file_url 和 material_title 字段
    llm_chat.py SourceItem dataclass 包含这两个字段
  L1: |
    在 165 上重启 ai-service 后，curl 验证：
    curl -s -X POST http://192.168.100.165:8000/api/chat \
      -H "Content-Type: application/json" \
      -d '{"query":"请假流程"}' | python3 -m json.tool | grep -A3 '"sources"'
    → sources 数组中的对象包含 material_file_url 字段
    → 有 PDF 对应的 source: material_file_url 值为 "/materials/xxx.pdf"
    → 无 PDF 对应的 source: material_file_url 为 "" 或 null
  L2: "N/A（端到端验证在 batch-int 覆盖）"
  L3: |
    T1 检查：
    - SourceItem dataclass 新增字段有默认值（不破坏已有调用）
    - SourceItemDTO 的 material_file_url 为 Optional[str]（不影响旧前端）
    - _convert_sources 正确传递新字段
    - _build_sources 从 r.metadata 读取而非硬编码

depends_on: ["f-v5d-03-chromadb-metadata"]
created_at: "2026-04-06"
---

# F-V5D-04: AI service 检索结果传递 material_file_url

> 完成后：`/api/chat` 和 `/api/chat/stream` 返回的 sources 列表中，
> 每个 source 包含 material_file_url 和 material_title 字段，前端可直接使用。

## 背景

F-V5D-03 将 `material_file_url` 注入了 ChromaDB chunk metadata。
本任务确保该字段沿着 `SearchResult.metadata → SourceItem → SourceItemDTO → SSE payload` 路径完整透传，不被截断过滤。

---

## 变更一：llm_chat.py — SourceItem dataclass 扩展

**文件**：`services/ai-service/app/core/llm_chat.py`

当前（第 28-34 行）：
```python
@dataclass
class SourceItem:
    """引用来源结构"""
    entry_id: str
    title: str
    content: str
    score: float
```

改为：
```python
@dataclass
class SourceItem:
    """引用来源结构"""
    entry_id: str
    title: str
    content: str
    score: float
    material_file_url: str = ""
    material_title: str = ""
```

---

## 变更二：llm_chat.py — _build_sources 透传 metadata 字段

**文件**：`services/ai-service/app/core/llm_chat.py`

当前（第 151-161 行）：
```python
def _build_sources(self, results: List[SearchResult]) -> List[SourceItem]:
    """将检索结果转换为来源引用列表"""
    return [
        SourceItem(
            entry_id=r.entry_id,
            title=r.metadata.get("title", "未知标题"),
            content=r.content[:500] + "..." if len(r.content) > 500 else r.content,
            score=r.score,
        )
        for r in results
    ]
```

改为：
```python
def _build_sources(self, results: List[SearchResult]) -> List[SourceItem]:
    """将检索结果转换为来源引用列表"""
    return [
        SourceItem(
            entry_id=r.entry_id,
            title=r.metadata.get("title", "未知标题"),
            content=r.content[:500] + "..." if len(r.content) > 500 else r.content,
            score=r.score,
            material_file_url=r.metadata.get("material_file_url", ""),
            material_title=r.metadata.get("material_title", ""),
        )
        for r in results
    ]
```

---

## 变更三：chat.py — SourceItemDTO 扩展 + _convert_sources 透传

**文件**：`services/ai-service/app/api/chat.py`

### 3a. SourceItemDTO 新增字段（约第 43-49 行）

当前：
```python
class SourceItemDTO(BaseModel):
    """引用来源传输对象"""
    entry_id: str = Field(..., description="知识条目 ID")
    title: str = Field(..., description="知识标题")
    content: str = Field(..., description="知识内容摘要")
    score: float = Field(..., description="相似度分数 0-1")
```

改为：
```python
class SourceItemDTO(BaseModel):
    """引用来源传输对象"""
    entry_id: str = Field(..., description="知识条目 ID")
    title: str = Field(..., description="知识标题")
    content: str = Field(..., description="知识内容摘要")
    score: float = Field(..., description="相似度分数 0-1")
    material_file_url: str = Field(default="", description="原始材料 PDF 路径（/materials/xxx.pdf），无则为空字符串")
    material_title: str = Field(default="", description="原始材料标题")
```

### 3b. _convert_sources 透传新字段（约第 85-95 行）

当前：
```python
def _convert_sources(sources: List[SourceItem]) -> List[SourceItemDTO]:
    """将内部 SourceItem 列表转换为 DTO 列表"""
    return [
        SourceItemDTO(
            entry_id=s.entry_id,
            title=s.title,
            content=s.content,
            score=s.score,
        )
        for s in sources
    ]
```

改为：
```python
def _convert_sources(sources: List[SourceItem]) -> List[SourceItemDTO]:
    """将内部 SourceItem 列表转换为 DTO 列表"""
    return [
        SourceItemDTO(
            entry_id=s.entry_id,
            title=s.title,
            content=s.content,
            score=s.score,
            material_file_url=s.material_file_url,
            material_title=s.material_title,
        )
        for s in sources
    ]
```

---

## 重启 ai-service 使改动生效

ai-service 在 Docker Compose 中运行，修改代码后需重新构建镜像：
```bash
cd ~/dev/yixiaoguan/deploy
docker compose build ai-service
docker compose up -d ai-service
```

或者在 Tmux 开发模式（如正在用 venv）：
```bash
# tmux ai-service 窗口中 Ctrl+C 停止，再重启
cd ~/dev/yixiaoguan/services/ai-service
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 已知陷阱

- ChromaDB metadata 中 `material_file_url` 是空字符串 `""` 而非 `None`（F-V5D-03 中已统一处理），直接 `.get("material_file_url", "")` 不会有 KeyError
- SourceItemDTO 新字段有 `default=""`，不影响旧版前端（旧前端忽略未知字段）
- `s.dict()` 在 chat.py SSE 流中被调用（第 222 行），Pydantic model.dict() 自动包含新字段，无需额外修改 SSE 序列化逻辑
