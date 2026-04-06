# T0 → T1 交接文档 (spec-v5a + spec-v5b)

**日期**: 2026-04-06
**T0**: Cascade (当前窗口)

---

## 任务概览

本轮有 **两个独立 spec**，可以分配给不同的 T1 窗口并行执行：

| Spec | 文件 | 内容 | 预估工时 | 并行安全 |
|------|------|------|----------|----------|
| **v5a** | `.tasks/_spec-v5a-quick-fixes.yaml` | 7 个 UI/Bug 快速修复 | 2-3h | ✅ 与 v5b 无冲突 |
| **v5b** | `.tasks/_spec-v5b-deploy.yaml` | Docker Compose 全栈部署自动化 | 4-6h | ✅ 与 v5a 无冲突 |

---

## spec-v5a: Quick Fixes（7 个任务）

| ID | 任务 | 工作量 | 关键点 |
|----|------|--------|--------|
| F-V5A-01 | 登录页提示文案 | 5min | 改一行文字：`首次登录请使用默认密码` → `初始密码与学号相同` |
| F-V5A-02 | DEBT-V4-01 硬编码颜色 | 15min | 5 处 `#006a64`，推荐 CSS 自定义属性方案 |
| F-V5A-03 | 参考资料卡片样式 | 10min | 灰白冲突，推荐方案 B（浅主题色背景） |
| F-V5A-04 | 历史记录 status=undefined | 15min | `api/chat.ts` 过滤 undefined 参数 |
| F-V5A-05 | 启用验证码 | 15min | Redis 配置 + 确认前端验证码组件存在 |
| F-V5A-06 | 知识详情不可用 | 30min-2h | 推荐方案 B（不调 API，直接用 URL 参数摘要） |
| F-V5A-07 | 首页数据美化 | 1-2h | 替换占位数据为医学院场景数据 |

**注意**: F-V5A-01~04 互不冲突可并行，F-V5A-05 需要 165 服务器操作。

---

## spec-v5b: 部署自动化（5 个模块）

| ID | 任务 | 依赖 | 关键点 |
|----|------|------|--------|
| F-V5B-01 | 前端静态构建 | 无 | `npx uni build -p h5` + `npm run build` |
| F-V5B-02 | 后端 Dockerfile | 无 | 基于 eclipse-temurin:21-jre-alpine，预构建 jar |
| F-V5B-03 | Nginx 反代 | V5B-01 | 端口 80 学生端，81 教师端，SSE 支持 |
| F-V5B-04 | Docker Compose 集成 | V5B-01~03 | 6 个服务，统一网络，健康检查 |
| F-V5B-05 | 部署脚本+文档 | V5B-04 | start-prod.sh + README.md |

**执行顺序**: V5B-01 & V5B-02 并行 → V5B-03 → V5B-04 → V5B-05

**关键风险**:
- `ruoyi-admin.jar` 在 target/ 中，Mutagen 不同步，需 165 上 `mvn package`
- application.yml 数据库地址需改为 Docker 服务名（环境变量覆盖）
- 165 服务器仅 16GB 内存，全容器化预估 4-6GB

---

## 165 服务器信息

- **SSH**: `easten@192.168.100.165`
- **项目路径**: `~/dev/yixiaoguan/`
- **远程执行**: `python collaborative-dev-guide/remote_exec.py dev --file <script.sh>`
- **Docker**: 28.2.2, 用户已在 docker 组
- **现有容器**: yx_postgres(:5432), yx_redis(:6379), yx_ai_service(:8000)
- **现有 Tmux**: backend(:8080), student(:5174), frontend(:5173)

## 测试账号

- 学生: `2524010001 / 2524010001`
- 教师: `liang_s_huli_24 / liangshufeng`

---

## 建议分工

- **T1-A 窗口**: 执行 spec-v5a（纯前端修复，本地即可）
- **T1-B 窗口**: 执行 spec-v5b（需要 165 服务器操作）
- 两个窗口完全独立，无文件冲突
