---
id: "f-v5b-05-deploy-script"
parent: "v5b-deploy"
type: "feature"
status: "pending"
tier: "T3"
priority: "medium"
risk: "low"

scope:
  - "deploy/start-prod.sh"
  - "deploy/README.md"
out_of_scope:
  - "apps/"
  - "services/"
  - "deploy/docker-compose.yml"
  - "deploy/nginx/"

context_files:
  - ".teb/antipatterns.md"
  - "deploy/docker-compose.yml"
  - ".tasks/v5b-deploy/_task.md"
  - ".tasks/v5b-deploy/f-v5b-01-frontend-build/_task.md"

done_criteria:
  L0: |
    以下两个文件存在：
    deploy/start-prod.sh
    deploy/README.md（内容与旧版不同，包含完整部署步骤）
  L1: |
    bash -n ~/dev/yixiaoguan/deploy/start-prod.sh
    → 无语法错误
  L2: "暂无（功能性验证在 batch-int 覆盖）"
  L3: "T1 检查：脚本包含 .env 检查、前端构建、jar 检测/构建、docker compose up 四个步骤"

depends_on: ["f-v5b-04-compose-integration"]
created_at: "2026-04-06"
---

# F-V5B-05: 一键部署脚本与文档

> 完成后：`deploy/start-prod.sh` 可在 165 服务器从零完成构建到启动的全流程，
> `deploy/README.md` 包含完整可操作的部署说明。

## 背景

deploy/README.md 当前是开发阶段的占位文档，需要替换为真实部署文档。
start-prod.sh 替代旧的 `~/dev/start-dev.sh`。

## start-prod.sh 规格

```bash
#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 步骤1: 检查 .env
[ -f .env ] || { echo "ERROR: 缺少 .env 文件"; exit 1; }

# 步骤2: 构建 student-app
cd "$SCRIPT_DIR/../apps/student-app"
npm install --silent
npx uni build -p h5

# 步骤3: 构建 teacher-web
cd "$SCRIPT_DIR/../apps/teacher-web"
npm install --silent
npm run build-only

# 步骤4: 检查/构建后端 jar
JAR="$SCRIPT_DIR/../services/business-api/ruoyi-admin/target/ruoyi-admin.jar"
if [ ! -f "$JAR" ]; then
    cd "$SCRIPT_DIR/../services/business-api"
    mvn package -DskipTests -q
fi

# 步骤5: Docker Compose
cd "$SCRIPT_DIR"
docker compose build business-api
docker compose up -d

# 步骤6: 状态输出
sleep 30
docker compose ps
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "学生端: http://$SERVER_IP"
echo "教师端: http://$SERVER_IP:81"
```

## README.md 规格

必须包含以下章节：
1. 快速部署（一行命令）
2. 服务架构图（文字版）
3. 前置条件（Docker, Node, JDK 版本要求）
4. 手动步骤（分步说明）
5. 服务管理命令（up/down/logs/rebuild）
6. 访问地址表格

## 已知陷阱

- `set -e` 遇 error 立即退出，确保错误不被忽略
- `npm install --silent` 减少输出但不影响安装
- jar 检测只判断文件是否存在，不验证版本，够用
