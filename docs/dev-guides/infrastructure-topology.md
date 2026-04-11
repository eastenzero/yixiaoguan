# 医小管 — 基础设施拓扑

> 最后更新：2026-04-11

## 设备总览

| 角色 | 地址 | OS | 硬件 | 用途 |
|------|------|----|------|------|
| **Windows 主力机** | 192.168.100.209 | Windows | i7-14600K / 32GB | 代码编辑、Git、Windsurf IDE |
| **Ubuntu 开发服务器** | 192.168.100.165 | Ubuntu 24.04 | i5-8665U / 16GB / 128GB SSD | 全栈运行、测试平台 |
| **NAS (Gitea)** | 192.168.100.176:13000 | — | — | Git 仓库托管，自动镜像到 GitHub |
| **阿里云公网服务器** | 60.205.205.99 | Alibaba Cloud Linux 3 | — | nginx 反向代理，公网入口 |

## 网络拓扑

```
                    ┌─────────────────────────────────────┐
                    │        公网 (Internet)               │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │  阿里云 60.205.205.99                │
                    │  nginx 反向代理                       │
                    │  :8174 → 学生端   :8173 → 教师端      │
                    └──────────────┬──────────────────────┘
                                   │ EasyTier VPN
                                   │ 10.77.0.10 ↔ 10.77.0.2
                                   │ ~18ms 延迟
                    ┌──────────────▼──────────────────────┐
                    │  165 开发服务器 192.168.100.165       │
                    │  Docker + Tmux 全栈                   │
                    └──────────────┬──────────────────────┘
                                   │ LAN
                    ┌──────────────▼──────────────────────┐
                    │  Windows 主力机 192.168.100.209       │
                    │  Mutagen 单向同步 → 165               │
                    └─────────────────────────────────────┘
```

## 165 开发服务器详情

### 连接方式

```bash
ssh easten@192.168.100.165
# sudo 密码: ZhaYeFan05.07.14
```

### 软件环境

- JDK 21, Maven 3.8.7, Docker 28.2.2, Node 18.19.1, Python 3.12, Tmux
- 项目路径: `~/dev/yixiaoguan/`
- pip 镜像: 必须指定 `-i https://pypi.tuna.tsinghua.edu.cn/simple`

### Docker 容器（持久运行）

| 容器名 | 镜像 | 端口 | 说明 |
|--------|------|------|------|
| yx_postgres | postgres:16-alpine | 5432 | 数据库，42 张表 |
| yx_redis | redis:7-alpine | 6379 | 缓存 |
| yx_business_api | 自构建 (Spring Boot) | 8080 | 若依后端 |
| yx_nginx | nginx:1.25-alpine | 80 (学生端), 81 (教师端) | 静态资源 + 反向代理 |

### Tmux 会话（非 Docker 服务）

| 会话名 | 端口 | 说明 |
|--------|------|------|
| ai-service | 8000 | FastAPI + ChromaDB, venv 虚拟环境 |
| student | 5174 | student-app Vite dev server |
| frontend | 5173 | teacher-web Vite dev server |
| backend | 8080 | (备用) 直接跑 Spring Boot jar |

> **注意**: ai-service 运行在宿主机 tmux 而非 Docker。nginx 配置中使用
> `host.docker.internal:8000` 访问它（docker-compose.yml 中 nginx 服务配置了
> `extra_hosts: ["host.docker.internal:host-gateway"]`）。

### 一键启动

```bash
bash ~/dev/start-dev.sh
```

### 手动启动

```bash
# 基础设施
cd ~/dev/yixiaoguan/deploy && sudo docker compose up -d postgres redis

# 后端 (Docker)
docker compose up -d business-api

# AI 服务 (tmux: ai-service)
cd ~/dev/yixiaoguan/services/ai-service
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000

# 学生端 dev (tmux: student)
cd ~/dev/yixiaoguan/apps/student-app
npx uni -p h5

# 教师端 dev (tmux: frontend)
cd ~/dev/yixiaoguan/apps/teacher-web
npm run dev

# 生产 nginx
docker compose up -d nginx
```

## 165 上的访问地址

| 服务 | Dev 地址 | 生产地址 (Docker nginx) |
|------|----------|----------------------|
| 学生端 | http://192.168.100.165:5174 | http://192.168.100.165 (:80) |
| 教师端 | http://192.168.100.165:5173 | http://192.168.100.165:81 |
| 后端 API | http://192.168.100.165:8080 | 同左 (Docker) |
| AI 服务 | http://192.168.100.165:8000/docs | 同左 (Tmux) |

## 公网访问地址

| 服务 | 公网 URL | 转发目标 |
|------|----------|----------|
| 学生端 | http://60.205.205.99:8174 | → 10.77.0.10:80 (Docker nginx) |
| 教师端 | http://60.205.205.99:8173 | → 10.77.0.10:81 (Docker nginx) |

### 阿里云 nginx 配置

- 配置文件: `/etc/nginx/conf.d/yixiaoguan-proxy.conf`
- 本地备份: `deploy/public-proxy/yixiaoguan-proxy.conf`
- 安全组: 8173/8174 已放行

## Mutagen 文件同步

- 方向: **Windows → 165 单向同步**
- 排除: `node_modules/`, `target/`, `venv/`
- 状态检查: `mutagen sync list`
- 已知问题: ai-service venv 目录有 72 个权限相关的 transition problems，不影响前端/后端代码同步

## 生产构建发布流程

```bash
# 1. 本地编辑代码 (Windows) → Mutagen 自动同步到 165

# 2. 在 165 上构建学生端
cd ~/dev/yixiaoguan/apps/student-app
npx uni build -p h5
# 输出到 dist/build/h5/，nginx 容器已挂载此目录

# 3. 重启 nginx 使新构建生效
cd ~/dev/yixiaoguan/deploy
docker restart yx_nginx

# 4. 清浏览器缓存验证
# LAN: http://192.168.100.165
# 公网: http://60.205.205.99:8174 (Ctrl+Shift+R 硬刷新)
```

## 测试账号

### 学生账号 (yx_user 表, role_id=2)

| 用户名 | 密码 | 姓名 |
|--------|------|------|
| 2524010001 | 2524010001 | 张小洋 |
| 2021010002 | 2021010002 | 李小辉 |
| 2024010103 | 2024010103 | 王伟 |
| 2024410004 | 2024410004 | 刘芳 |
| 2024010003 | 2024010003 | 陈静 |

### 教师账号 (yx_user 表, role_id=3)

| 用户名 | 密码 | 姓名 |
|--------|------|------|
| liang_s_huli_24 | liangshufeng | 梁淑芬 |
| deng_p_linchuang_24 | dengping | 邓平 |
| cheng_d_fangshe_24 | chengdan | 程丹 |

> 密码规则: 学生=学号, 教师=姓名全拼。BCrypt $2a$ 哈希。

## 关键配置文件索引

| 文件 | 说明 |
|------|------|
| `deploy/docker-compose.yml` | Docker 服务编排 |
| `deploy/.env` | 数据库/Redis/DashScope 密钥 |
| `deploy/nginx/conf.d/student.conf` | 学生端 nginx (反代 + SPA) |
| `deploy/nginx/conf.d/teacher.conf` | 教师端 nginx |
| `services/ai-service/.env` | AI 服务环境变量 |
| `apps/student-app/vite.config.ts` | 学生端 Vite 配置 |
| `apps/teacher-web/.env.development` | 教师端 API 地址 |
