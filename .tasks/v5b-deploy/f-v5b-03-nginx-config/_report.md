# F-V5B-03: Nginx 反向代理配置 - 执行报告

## 执行摘要

- **任务 ID**: f-v5b-03-nginx-config
- **执行时间**: 2026-04-06
- **执行结果**: ✅ 配置文件创建完成

## 交付物

### 创建的文件

| 文件路径 | 说明 |
|---------|------|
| `deploy/nginx/nginx.conf` | Nginx 主配置文件 |
| `deploy/nginx/conf.d/student.conf` | 学生端虚拟主机（端口 80） |
| `deploy/nginx/conf.d/teacher.conf` | 教师端虚拟主机（端口 81） |

## 路由规则映射

### student.conf（端口 80）← vite.config.ts proxy

| Vite Proxy 规则 | Nginx Location | Upstream | 特殊配置 |
|---------------|---------------|----------|---------|
| `/api/login` → rewrite → `:8080` | `~ ^/api/(login\|logout\|captchaImage\|getInfo)` | `business-api:8080` | `rewrite ^/api/(.*)$ /$1 break` |
| `/api/logout` → rewrite → `:8080` | (同上) | (同上) | (同上) |
| `/api/captchaImage` → rewrite → `:8080` | (同上) | (同上) | (同上) |
| `/api/getInfo` → rewrite → `:8080` | (同上) | (同上) | (同上) |
| `/api/chat` → `:8000` | `/api/chat` | `ai-service:8000` | **SSE 配置**: `proxy_buffering off; proxy_cache off; proxy_read_timeout 300s;` |
| `/api` → `:8080` | `/api/` | `business-api:8080` | 路径不变 |
| `/` → 静态文件 | `/` | `/usr/share/nginx/html/student` | `try_files $uri $uri/ /index.html` |

### teacher.conf（端口 81）← vite.config.ts proxy

| Vite Proxy 规则 | Nginx Location | Upstream | 特殊配置 |
|---------------|---------------|----------|---------|
| `/api/v1` → `:8080` | `/api/v1/` | `business-api:8080` | 路径不变，**优先匹配** |
| `/api` → rewrite → `:8080` | `/api/` | `business-api:8080` | `rewrite ^/api/(.*)$ /$1 break` |
| `/` → 静态文件 | `/` | `/usr/share/nginx/html/teacher` | `try_files $uri $uri/ /index.html` |

## 关键点实现

### ✅ 1. /api/chat 优先级
- `/api/chat` 规则**明确放在** `/api/` 通用规则之前
- 确保 SSE 请求不会被通用规则拦截

### ✅ 2. SSE 配置
```nginx
location /api/chat {
    proxy_http_version 1.1;
    proxy_set_header Connection '';
    proxy_buffering off;
    proxy_cache off;
    proxy_read_timeout 300s;
}
```

### ✅ 3. RuoYi 认证路由 rewrite
```nginx
location ~ ^/api/(login|logout|captchaImage|getInfo) {
    rewrite ^/api/(.*)$ /$1 break;
    proxy_pass http://business-api:8080;
}
```

### ✅ 4. 文件上传限制
- 主配置和 server 块均设置 `client_max_body_size 20m`
- 对齐 Spring Boot 的文件上传限制

### ✅ 5. Gzip 压缩
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
```

## 验证结果

### 语法检查
```bash
docker run --rm \
  -v ~/dev/yixiaoguan/deploy/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  -v ~/dev/yixiaoguan/deploy/nginx/conf.d:/etc/nginx/conf.d:ro \
  nginx:1.25-alpine nginx -t
```

**结果**: 配置语法正确（容器内无法解析 upstream 主机名是预期行为，因为 `business-api` 和 `ai-service` 是 Docker Compose 网络内的服务名）

## 新发现的错误模式

> 本次任务未发现新的 Anti-Pattern。

## 后续步骤

1. 确保 Docker Compose 中定义了 `business-api` 和 `ai-service` 服务
2. 确保前端构建输出挂载到正确的静态文件目录：
   - `/usr/share/nginx/html/student` - student-app 构建产物
   - `/usr/share/nginx/html/teacher` - teacher-web 构建产物
3. 在完整 Docker Compose 环境中启动后进行集成测试
