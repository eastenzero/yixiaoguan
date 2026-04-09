---
id: "f-v5f-01"
parent: "v5f-pdf-page-slice"
type: "data-annotation"
status: "pending"
tier: "T3"
dispatch_via: "T2(Kiro) → T3(Kimi)"
priority: "high"
risk: "medium"
depends_on: []

scope:
  - "scripts/build_page_mapping.py (CREATE)"
  - "knowledge-base/entries/first-batch-drafts/KB-0150-*.md ~ KB-0171-*.md (22 files)"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0138.md ~ KB-20260324-0149.md (12 files)"
out_of_scope:
  - "apps/**"
  - "services/**"
  - "deploy/**"
  - "knowledge-base/entries/first-batch-drafts/KB-20260324-0001.md ~ KB-20260324-0137.md (其他条目)"

data_sources:
  mineru_json: "knowledge-base/raw/student-handbook-mineru/content_list_v2.json"
  note: |
    外层数组 = 122 逻辑页（MinerU 跳过图片/空白页，PDF 共 182 物理页）
    每页 = 内层块数组，块类型有 title/paragraph/list/table 等
    内容提取方式：
      title 块: block["content"]["title_content"] 里 type=="text" 的 content 字段
      其他块: 尝试 block["content"] 直接读文本，或 block["content"]["text"]

target_entries:
  group_A:
    count: 22
    pattern: "KB-0150-*.md ~ KB-0171-*.md"
    material_id: "学生手册-生活服务"
    match_strategy: "取正文前 120 字符作 needle，在 MinerU 每页文本中搜索"
  group_B:
    count: 12
    pattern: "KB-20260324-0138.md ~ KB-20260324-0149.md"
    material_id: "HANDBOOK-2026-001 / HANDBOOK-2026-002"
    match_strategy: "取条目 title + 正文前 80 字符作 needle，在 MinerU 每页文本中搜索"

done_criteria:
  L0: "scripts/build_page_mapping.py 存在"
  L1: |
    - 脚本可无错运行: python3 scripts/build_page_mapping.py
    - 在 scripts/ 目录下生成 page_mapping_report.csv（含 entry_id, title, page_start, page_end, match_score, match_snippet）
    - 34 个目标条目全部有 page_start（允许 match_failed=True 的条目用 0 占位）
  L2: |
    - 所有目标条目 frontmatter 已新增 page_start/page_end 字段
    - 执行 grep -l 'page_start' knowledge-base/entries/first-batch-drafts/KB-0150*.md | wc -l 返回 22
    - 执行 grep -l 'page_start' knowledge-base/entries/first-batch-drafts/KB-20260324-0138.md | wc -l 返回 1

report_path: ".tasks/v5f-pdf-page-slice/f-v5f-01-page-annotation/_report.md"
created_at: "2026-04-07"
---

# F-V5F-01: KB 条目 frontmatter 页码标注

## 任务说明

编写一次性脚本 `scripts/build_page_mapping.py`，通过文本匹配自动为
来自 student-handbook.pdf 的 KB 条目标注 `page_start` / `page_end`。

输出 CSV 报告供人工抽查 3-5 条验证页码正确性（RISK-1：逻辑页可能与物理页有偏移）。

## frontmatter 格式示例

修改前:
```yaml
---
material_id: "学生手册-生活服务"
title: "电费缴纳指南"
source: "学生手册-生活服务.md 行 4927-5041"
---
```

修改后:
```yaml
---
material_id: "学生手册-生活服务"
title: "电费缴纳指南"
source: "学生手册-生活服务.md 行 4927-5041"
page_start: 155
page_end: 158
---
```
