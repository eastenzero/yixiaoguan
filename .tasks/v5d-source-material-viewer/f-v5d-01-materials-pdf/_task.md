---
id: "f-v5d-01"
parent: "v5d-source-material-viewer"
type: "data"
status: "pending"
tier: "T3"
priority: "high"
risk: "medium"
foundation: false

scope:
  - "deploy/materials/"
  - "knowledge-base/raw/first-batch-material-index.csv"
out_of_scope:
  - "apps/**"
  - "services/**"
  - "knowledge-base/entries/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5d-source-material-viewer.yaml"
  - ".tasks/_t0-handoff-v5d.md"
  - "knowledge-base/raw/first-batch-material-index.csv"

done_criteria:
  L0: "deploy/materials/ 目录存在，且包含 student-handbook.pdf 与 knowledge-base-v2.pdf"
  L1: "deploy/materials/material-index.json 存在且为合法 JSON（python -m json.tool 校验通过）"
  L2: "material-index.json 至少包含 2 个 key：'学生手册-生活服务' 与任意一个 'MAT-20260323-' 前缀条目"
  L3: "随机打开 2 个 PDF（含 student-handbook.pdf）可正常预览且非损坏文件"

inputs:
  - "MinerU 学生手册 _origin.pdf（Windows 路径见 handoff）"
  - "MinerU 知识库二次修改版 _origin.pdf（Windows 路径见 handoff）"
  - "knowledge-base/raw/原始材料/数据库部分材料/（doc/docx/pdf 等）"
  - "knowledge-base/raw/first-batch-material-index.csv（material_id 映射）"

instructions:
  - step: "复制两份 _origin.pdf 到 deploy/materials/ 并重命名"
    details:
      - "student-handbook.pdf"
      - "knowledge-base-v2.pdf"
  - step: "从 first-batch-material-index.csv 选择 value_level=A 且 processing_action 可转知识/提炼规则后入库 的条目"
  - step: "对 doc/docx 使用 libreoffice headless 转 pdf；pdf 直接复制"
  - step: "生成 material-index.json，覆盖两类 key：学生手册命名空间 + MAT-xxxxx"

notes:
  - "deploy/materials/ 不入 git，请在 _report.md 中列出已生成的文件清单"

created_at: "2026-04-06"
---

# F-V5D-01: 原始材料收集与 PDF 标准化

> 产出 `deploy/materials/` 与 `material-index.json`，供后续 AI metadata 注入与前端打开原件。
