# deploy — 部署配置

本目录存放 Docker Compose 配置和 Nginx 反向代理配置。

## 待建文件

- [ ] `docker-compose.yml` — 本地开发 + 服务器部署统一配置
- [ ] `docker-compose.prod.yml` — 生产环境覆盖配置
- [ ] `nginx/nginx.conf` — Nginx 反向代理配置
- [ ] `.env.example` — 环境变量模板（不含真实值，提交 Git）

## 服务端口规划

| 服务 | 容器内端口 | Nginx 代理路径 |
|---|---|---|
| teacher-web（静态文件） | 80 | `/` |
| student-app（静态文件） | 80 | `/student/` |
| business-api | 8080 | `/api/` |
| ai-service | 8000 | 不对外暴露，仅 business-api 调用 |
| PostgreSQL | 5432 | 不对外暴露 |
| Redis | 6379 | 不对外暴露 |
