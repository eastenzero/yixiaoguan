# F-V5B-05: 一键部署脚本与文档 - 执行报告

## 任务状态

- **状态**: ✅ 已完成
- **执行时间**: 2026-04-06
- **执行者**: AI Agent

---

## 交付物清单

### 1. deploy/start-prod.sh ✅

**文件路径**: `deploy/start-prod.sh`

**功能检查**:
- ✅ `set -e` - 遇 error 立即退出
- ✅ 步骤1: .env 文件检查
- ✅ 步骤2: student-app 前端构建 (npm install --silent + npx uni build -p h5)
- ✅ 步骤3: teacher-web 前端构建 (npm install --silent + npm run build-only)
- ✅ 步骤4: 后端 jar 检测/构建
- ✅ 步骤5: docker compose build + up -d
- ✅ 步骤6: 状态输出 + 访问地址

**额外优化**:
- Node 版本自动切换（source ~/.nvm/nvm.sh && nvm use 24），解决 AP-001
- 智能跳过已存在的 node_modules，减少重复安装时间
- jar 存在性检查，避免不必要的 Maven 构建

**语法检查**: ✅ bash -n 通过

### 2. deploy/README.md ✅

**文件路径**: `deploy/README.md`

**内容检查**:
- ✅ 快速部署（一行命令）
- ✅ 服务架构图（文字版 ASCII 架构图）
- ✅ 前置条件（Docker, Node, JDK 版本要求）
- ✅ 手动步骤（分步说明）
- ✅ 服务管理命令（up/down/logs/rebuild 表格）
- ✅ 访问地址表格

**额外内容**:
- 故障排查章节（常见问题及解决）
- 目录结构说明
- 165 服务器具体访问地址

---

## 合规性检查

### 修改范围

- ✅ 仅修改了允许的文件：`deploy/start-prod.sh`, `deploy/README.md`
- ✅ 未触碰禁止修改的文件：apps/, services/, deploy/docker-compose.yml, deploy/nginx/

### Done Criteria

- L0 ✅: 两个文件均存在
- L1 ✅: bash -n 无语法错误
- L2 N/A: 功能性验证在 batch-int 覆盖
- L3 ✅: 脚本包含四个必需步骤
  - .env 检查
  - 前端构建（student-app + teacher-web）
  - jar 检测/构建
  - docker compose up

---

## 新发现的错误模式

无新发现。遵循了 AP-001 关于 Node 版本切换的建议。

---

## 注意事项

1. **Node 版本**: 脚本会自动检测并切换 Node 版本，但首次使用前需确保 Node 24 已安装：
   ```bash
   nvm install 24
   ```

2. **环境变量**: 首次部署前必须创建 .env 文件：
   ```bash
   cp deploy/.env.example deploy/.env
   vim deploy/.env
   ```

3. **WSL 警告**: Windows 环境下执行 bash -n 时出现的 WSL localhost 代理警告不影响脚本功能。

---

## 后续建议

1. 考虑在 batch-int 集成测试中验证脚本在 165 服务器上的实际执行
2. 考虑添加 `--skip-frontend` 等参数支持部分构建
3. 考虑添加 `docker system prune` 清理选项（带确认提示）
