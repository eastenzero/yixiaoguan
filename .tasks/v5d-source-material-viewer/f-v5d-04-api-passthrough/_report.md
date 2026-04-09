# f-v5d-04-api-passthrough 执行报告

## 代码变更说明

### services/ai-service/app/core/llm_chat.py
- `SourceItem` dataclass 新增两个字段：`material_file_url: str = ""` 和 `material_title: str = ""`
- `_build_sources` 方法的 `SourceItem` 构造中追加从 metadata 读取：
  - `material_file_url=r.metadata.get("material_file_url", "")`
  - `material_title=r.metadata.get("material_title", "")`

### services/ai-service/app/api/chat.py
- `SourceItemDTO` 新增两个字段：
  - `material_file_url: str = Field(default="", description="原始材料 PDF 路径，无则为空字符串")`
  - `material_title: str = Field(default="", description="原始材料标题")`
- `_convert_sources` 函数的 `SourceItemDTO` 构造中追加透传：
  - `material_file_url=s.material_file_url`
  - `material_title=s.material_title`

## Docker 重建结果

构建成功：`sha256:93b8c051ac8aa6c373d4eb24d0212e7f0dea5b76a427b9abfc11c51a5919a8ef`
容器重启成功：`yx_ai_service` Up，端口 0.0.0.0:8000->8000/tcp

## curl 验证结果

`material_file_url` 字段存在于 API 响应中：

```json
"material_file_url": "/materials/student-handbook.pdf",
"material_title": "学生手册（含图片版）"
```

## 验收结论

- L0: PASS
- L1-LLMCHAT: PASS（grep 命中 2 处）
- L1-CHATAPI: PASS（grep 命中 2 处）
- L2: PASS — material_file_url 字段存在，值为 `/materials/student-handbook.pdf`
