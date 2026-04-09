---
id: "f-v5d-02"
parent: "v5d-source-material-viewer"
type: "config"
status: "pending"
tier: "T3"
priority: "high"
risk: "low"
foundation: false

depends_on: ["f-v5d-01"]

scope:
  - "deploy/nginx/conf.d/student.conf"
  - "deploy/docker-compose.yml"
out_of_scope:
  - "deploy/nginx/nginx.conf"
  - "apps/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5d-source-material-viewer.yaml"
  - "deploy/nginx/conf.d/student.conf"
  - "deploy/docker-compose.yml"

done_criteria:
  L0: "deploy/nginx/conf.d/student.conf 存在"
  L1: "grep -n 'location /materials/' deploy/nginx/conf.d/student.conf 有结果"
  L2: "在 165 执行 docker compose config --quiet 无错误；且 curl -I http://192.168.100.165/materials/student-handbook.pdf 返回 200/206"
  L3: "浏览器访问 http://192.168.100.165/materials/student-handbook.pdf 可直接预览（非强制下载）"

changes:
  - file: "deploy/nginx/conf.d/student.conf"
    add: |
      location /materials/ {
          alias /usr/share/nginx/html/materials/;
          types {
              application/pdf pdf;
          }
          add_header Content-Disposition inline;
          add_header Cache-Control "public, max-age=86400";
      }
  - file: "deploy/docker-compose.yml"
    add_volume: "- ../deploy/materials:/usr/share/nginx/html/materials:ro"

created_at: "2026-04-06"
---

# F-V5D-02: Nginx 材料静态托管路由

> 暴露 `/materials/` 路由，前端可直接打开原始 PDF。
