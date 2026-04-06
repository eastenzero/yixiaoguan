---
id: "f-v5b-03-nginx-config"
parent: "v5b-deploy"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"

scope:
  - "deploy/nginx/"
out_of_scope:
  - "apps/"
  - "services/"
  - "deploy/docker-compose.yml"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/vite.config.ts"
  - "apps/teacher-web/vite.config.ts"
  - ".tasks/v5b-deploy/_task.md"
  - ".tasks/v5b-deploy/f-v5b-01-frontend-build/_task.md"

done_criteria:
  L0: |
    以下三个文件存在：
    deploy/nginx/nginx.conf
    deploy/nginx/conf.d/student.conf
    deploy/nginx/conf.d/teacher.conf
  L1: |
    在 165 服务器上执行（仅验证 nginx 语法，无需启动）：
    docker run --rm \
      -v ~/dev/yixiaoguan/deploy/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
      -v ~/dev/yixiaoguan/deploy/nginx/conf.d:/etc/nginx/conf.d:ro \
      nginx:1.25-alpine nginx -t
    → 输出 "syntax is ok" 和 "test is successful"
  L2: "暂无（运行时验证在 batch-int 集成测试覆盖）"
  L3: |
    T1 检查路由规则与 vite.config.ts proxy 规则一一对应：
    - /api/login|logout|captchaImage|getInfo → strip /api → business-api:8080
    - /api/chat → ai-service:8000（含 SSE 配置）
    - /api/ → business-api:8080（路径不变）
    - / → student-app 静态文件（SPA fallback）
    teacher.conf 对应 teacher-web 的 proxy 规则

depends_on: ["f-v5b-01-frontend-build", "f-v5b-02-backend-dockerfile"]
created_at: "2026-04-06"
---

# F-V5B-03: Nginx 反向代理配置

> 完成后：`deploy/nginx/` 目录包含完整 Nginx 配置，
> `docker run nginx -t` 语法检查通过。

## 背景

需要 Nginx 在生产环境中替代 Vite dev server 的 proxy 功能，
同时托管前端静态文件。

## 路由规则规格

规则必须与 `apps/student-app/vite.config.ts` 的 proxy 配置**完全对应**：

### student.conf（端口 80）

```
静态文件根目录: /usr/share/nginx/html/student
SPA fallback: try_files $uri $uri/ /index.html

路由（优先级从高到低）：
1. ~ ^/api/(login|logout|captchaImage|getInfo)
   → rewrite 去掉 /api 前缀 → proxy_pass http://business-api:8080
2. /api/chat
   → proxy_pass http://ai-service:8000
   → SSE 配置：proxy_http_version 1.1; proxy_set_header Connection '';
               proxy_buffering off; proxy_cache off; proxy_read_timeout 300s;
3. /api/
   → proxy_pass http://business-api:8080（路径不变）
4. /
   → 静态文件 + SPA fallback
```

### teacher.conf（端口 81）

对应 `apps/teacher-web/vite.config.ts` proxy 规则：
```
1. /api/v1/ → proxy_pass http://business-api:8080（路径不变）
2. /api/    → rewrite 去掉 /api 前缀 → proxy_pass http://business-api:8080
3. /        → 静态文件 + SPA fallback
```

### nginx.conf（主配置）

标准结构：`include /etc/nginx/conf.d/*.conf;`，开启 gzip。

## 已知陷阱

- `/api/chat` 规则**必须**放在通用 `/api/` 规则之前，否则 Nginx 先匹配通用规则
- SSE（Server-Sent Events）需要 `proxy_buffering off` 否则流式响应卡死
- RuoYi 认证路由（`/login` 等）无 `/api` 前缀，但前端以 `/api/login` 调用，Nginx 需 rewrite
- `client_max_body_size 20m;` 对齐 Spring Boot 的文件上传限制
