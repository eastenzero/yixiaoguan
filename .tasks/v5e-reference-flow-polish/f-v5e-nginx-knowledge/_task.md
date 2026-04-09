---
id: "f-v5e-nginx-knowledge"
parent: "v5e-reference-flow-polish"
type: "config"
status: "pending"
tier: "T3"
dispatch_via: "T2(Kiro) → T3(Kimi)"
priority: "high"
risk: "low"
depends_on: []

scope:
  - "deploy/nginx/conf.d/student.conf"
out_of_scope:
  - "apps/**"
  - "services/**"
  - "deploy/docker-compose.yml"

done_criteria:
  L0: "grep -q 'location /api/knowledge/' ~/dev/yixiaoguan/deploy/nginx/conf.d/student.conf"
  L1: "docker exec yx_nginx nginx -t 返回 test is successful"
  L2: "curl -s -o /dev/null -w '%{http_code}' http://192.168.100.165/api/knowledge/entries/test 返回 404 或 422（非 502/503）"

change:
  file: "deploy/nginx/conf.d/student.conf"
  position: "在 location /api/chat { ... } 块结束后，location /api/ { 之前"
  add: |
    # ── 知识库 API（AI service）──
    location /api/knowledge/ {
        proxy_pass http://ai-service:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

after_change:
  - "docker exec yx_nginx nginx -t"
  - "docker exec yx_nginx nginx -s reload"

report_path: ".tasks/v5e-reference-flow-polish/f-v5e-nginx-knowledge/_report.md"
created_at: "2026-04-07"
---

# f-v5e-nginx-knowledge: 新增 /api/knowledge/ Nginx 路由

> 为 F-V5E-02 知识条目 API 提前配置 Nginx 路由，让 /api/knowledge/ 请求转发到 ai-service:8000。
> 纯配置改动，不依赖 API 代码完成，可与 T1-B 工作并行。
