---
id: "v5b-deploy"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

batches:
  - name: "batch-1"
    tasks: ["f-v5b-01-frontend-build", "f-v5b-02-backend-dockerfile"]
    parallel: true
    status: "done"
    verified_at: "2026-04-06"
    note: "两任务写入路径完全不重叠，可并行"
  - name: "batch-2"
    tasks: ["f-v5b-03-nginx-config"]
    depends_on: "batch-1"
    status: "done"
    verified_at: "2026-04-06"
    note: "Nginx 路径设计需确认前端产物目录结构"
  - name: "batch-3"
    tasks: ["f-v5b-04-compose-integration"]
    depends_on: "batch-2"
  - name: "batch-4"
    tasks: ["f-v5b-05-deploy-script"]
    depends_on: "batch-3"
  - name: "batch-int"
    tasks: ["int-v5b-deploy"]
    depends_on: "batch-4"

created_at: "2026-04-06"
---

# spec-v5b: Docker Compose 全栈部署自动化

> 完成后：在 165 服务器执行 `docker compose up -d` 即可一键启动全部 5 个服务，
> 浏览器访问 `http://192.168.100.165` 可正常使用学生端登录和 AI 对话。

## 背景

spec-v4 已签收。当前各服务散落在 Tmux 中手动维护，不具备自动恢复能力。
目标：方案 B 级部署自动化——前端静态构建 + Nginx 反代 + 全服务 Docker Compose 编排。

## 已知陷阱（T3 必读）

- **RISK-1**: `services/business-api/ruoyi-admin/target/` 被 Mutagen 排除同步，165 上需先确认 jar 是否存在（`ls -lh ~/dev/yixiaoguan/services/business-api/ruoyi-admin/target/ruoyi-admin.jar`），不存在则在 165 上 `mvn package -DskipTests`
- **RISK-2**: `application-druid.yml` 硬编码 `localhost:5432`，不能直接改文件（破坏开发环境），必须通过 docker-compose environment 的 Spring env var 覆盖：`SPRING_DATASOURCE_DRUID_MASTER_URL`
- **RISK-3（已确认）**: 165 服务器默认 Node 18.19.1，Vite 8 确定无法运行，需先切换：`source ~/.nvm/nvm.sh && nvm use 24`，再执行 `npm run build-only`（跳过 vue-tsc）。见 AP-001
- **RISK-4**: student-app 多个页面 style 块有本地 SCSS 变量但缺少 `$primary` 定义（没有 `@import '@/styles/theme.scss'`），已知文件：`pages/questions/index.vue`、`pages/apply/classroom.vue`（其他页面执行时按需检查）。修复方式：在对应 style 块的本地变量区加一行 `$primary: #006a64;`
