# 任务报告: f-v5d-03-chromadb-metadata

STEP-EXECUTED

## 执行摘要

- 执行时间: 2026-04-06T17:26 UTC
- 工作目录: /home/easten/dev/yixiaoguan

## 变更内容

### 变更1: services/ai-service/app/core/chunker.py
- `split()` 方法新增 `title: str = "Document"` 参数
- `split()` 内部调用改为 `_split_by_headings(text, title=title)`
- `_split_by_headings()` 签名新增 `title: str = "Document"` 参数
- 方法体内 `"# Document\n"` 改为 `f"# {title}\n"`

### 变更2: services/ai-service/scripts/batch_ingestion.py
- 新增常量 `MATERIAL_INDEX_PATH`
- 新增函数 `_load_material_index()`
- `process_single_file()` 新增 `material_index: dict = None` 参数
- 新增 `material_id` 查找逻辑，注入 `material_file_url` 和 `material_title`
- `splitter.split()` 调用新增 `title=title` 参数
- `run_batch_ingestion()` 开头加载 material_index 并传入处理函数

## Dry-run 结果

```
总文件数: 77
  ✅ 成功: 77
  ❌ 失败: 0
总 chunks: 933
  ✅ 入库成功: 933 (模拟)
  ❌ 入库失败: 0
总耗时: 0.04 秒
```

## 正式入库结果

```
总文件数: 77
  ✅ 成功: 77
  ❌ 失败: 0
总 chunks: 933
  ✅ 入库成功: 933
  ❌ 入库失败: 0
总耗时: 429.42 秒
```

## material_file_url 注入验证 (L2)

查询 "请假流程" top_k=3 结果：

```
entry=KB-0155-请假销假制度__chunk_5  url=/materials/student-handbook.pdf  mat_title=学生手册（含图片版）
entry=KB-0155-请假销假制度__chunk_6  url=/materials/student-handbook.pdf  mat_title=学生手册（含图片版）
entry=KB-0155-请假销假制度__chunk_7  url=/materials/student-handbook.pdf  mat_title=学生手册（含图片版）
L2 PASS: 3/3 chunks have material_file_url field
```

material_file_url 注入成功 ✅

## STEP-CHECK

| 检查项 | 结果 |
|--------|------|
| L0: _report.md 存在 | PASS |
| L0-REPORT-FORMAT: 含 STEP-EXECUTED | PASS |
| L1-CHUNKER: 无硬编码 "# Document" | PASS |
| L1-INGESTION: 含 material_file_url | PASS |
| L1-INDEX-LOADER: 含 _load_material_index | PASS |
| L2: ChromaDB metadata 字段注入 | PASS (3/3) |

## BLOCKERS

无
