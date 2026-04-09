---
id: "int-v5d-a"
parent: "v5d-source-material-viewer"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

depends_on: ["f-v5d-01", "f-v5d-02"]

scope:
  - ".tasks/v5d-source-material-viewer/"
out_of_scope:
  - "apps/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5d-source-material-viewer.yaml"
  - ".tasks/_t0-handoff-v5d.md"

done_criteria:
  L0: "f-v5d-01 与 f-v5d-02 均有 _report.md"
  L1: "material-index.json JSON 校验通过；且 student.conf 含 /materials/ location"
  L2: "curl -I http://192.168.100.165/materials/student-handbook.pdf 返回 200/206"
  L3: "在浏览器内可预览 PDF（至少 student-handbook.pdf），且文件内容含图片（截图页可见）"

acceptance_checklist:
  AC-1: "deploy/materials/ 含 student-handbook.pdf + knowledge-base-v2.pdf + material-index.json"
  AC-2: "/materials/student-handbook.pdf 可预览"

created_at: "2026-04-06"
---

# int-v5d-a: T1-A 集成验收

> 只覆盖 T1-A 范围（F-V5D-01/02）：材料 PDF 与 Nginx 静态托管可用。
