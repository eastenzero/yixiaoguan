---
id: "rework-01-pdf-supplement"
parent: "v5d-source-material-viewer"
type: "rework"
status: "pending"
tier: "T3"
dispatch_via: "T2(Kiro) → T3(Kimi)"
priority: "high"
risk: "low"

depends_on: []

scope:
  - "deploy/materials/"
out_of_scope:
  - "apps/**"
  - "services/**"
  - "knowledge-base/entries/**"
  - "deploy/nginx/**"
  - "deploy/docker-compose.yml"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_t0-handoff-v5d.md"
  - ".tasks/v5d-materials/f-v5d-01-materials-collection/_report.md"

background: |
  Batch-1 的 F-V5D-01 以 .md 格式替代 .pdf 交付，不满足 spec-v5d AC-1/AC-2 的核心要求。
  本返工任务目标：在 165 服务器上将 deploy/materials/ 补齐为 PDF 格式原件。

done_criteria:
  L0: "ls ~/dev/yixiaoguan/deploy/materials/ 显示 student-handbook.pdf 与 knowledge-base-v2.pdf"
  L1: "python3 -m json.tool ~/dev/yixiaoguan/deploy/materials/material-index.json 输出合法 JSON，且 filename 字段后缀为 .pdf"
  L2: "curl -s -o /dev/null -w '%{http_code}' http://192.168.100.165/materials/student-handbook.pdf 返回 200 或 206"
  L3: "浏览器访问 http://192.168.100.165/materials/student-handbook.pdf 可直接预览 PDF（非下载）"

instructions:
  - step: "1. 检查 pandoc 是否可用"
    cmd: "which pandoc || echo 'not found'"
  - step: "2a. 若 pandoc 可用 → 转换现有 .md 为 .pdf"
    cmd: |
      cd ~/dev/yixiaoguan/deploy/materials
      pandoc student-handbook.md -o student-handbook.pdf --pdf-engine=wkhtmltopdf 2>/dev/null \
        || pandoc student-handbook.md -o student-handbook.pdf 2>/dev/null
      pandoc knowledge-base-v2.md -o knowledge-base-v2.pdf 2>/dev/null
  - step: "2b. 若 pandoc 不可用 → 用 python 生成最小 PDF（占位，等 Windows scp 上传覆盖）"
    cmd: |
      python3 -c "
      # 生成最小合规 PDF（纯文本内容，浏览器可预览）
      import os
      for name, title in [('student-handbook.pdf','学生手册'), ('knowledge-base-v2.pdf','知识库')]:
          pdf_content = f'''%PDF-1.4
      1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj
      2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj
      3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj
      4 0 obj<</Length 44>>stream
      BT /F1 16 Tf 72 750 Td ({title} - 待更新) Tj ET
      endstream endobj
      5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj
      xref
      0 6
      0000000000 65535 f
      0000000009 00000 n
      0000000058 00000 n
      0000000115 00000 n
      0000000274 00000 n
      0000000369 00000 n
      trailer<</Size 6/Root 1 0 R>>
      startxref
      441
      %%EOF'''
          with open(os.path.join('/root/dev/yixiaoguan/deploy/materials', name), 'w') as f:
              f.write(pdf_content)
          print(f'Created {name}')
      "
  - step: "3. 更新 material-index.json — filename 改为 .pdf，format 改为 pdf"
    cmd: |
      python3 - <<'PYEOF'
      import json, os
      path = os.path.expanduser('~/dev/yixiaoguan/deploy/materials/material-index.json')
      with open(path) as f:
          idx = json.load(f)
      for m in idx.get('materials', []):
          if m.get('filename', '').endswith('.md'):
              m['filename'] = m['filename'].replace('.md', '.pdf')
          m['format'] = 'pdf'
      with open(path, 'w', encoding='utf-8') as f:
          json.dump(idx, f, ensure_ascii=False, indent=2)
      print('material-index.json updated')
      PYEOF
  - step: "4. 修复文件权限"
    cmd: "chmod 644 ~/dev/yixiaoguan/deploy/materials/*.pdf ~/dev/yixiaoguan/deploy/materials/material-index.json"
  - step: "5. 确认 Nginx 容器已挂载 materials 目录"
    cmd: "docker exec yx_nginx ls /usr/share/nginx/html/materials/ 2>/dev/null || docker exec yx_nginx ls /usr/share/nginx/materials/ 2>/dev/null"

report_path: ".tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_report.md"

created_at: "2026-04-07"
---

# rework-01-pdf-supplement: F-V5D-01 返工 — 补齐 PDF 原件

> Batch-1 以 .md 代替 .pdf 交付，本任务在 165 服务器上将 `deploy/materials/` 补齐为 PDF。
>
> **优先尝试 pandoc 转换**；pandoc 不可用时生成最小合规 PDF 作为占位，并在报告中标注
> "需从 Windows scp 上传完整版 PDF" 供 T1 知晓。
