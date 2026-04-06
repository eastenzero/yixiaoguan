#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 步骤1: 检查 .env
if [ ! -f .env ]; then
    echo "ERROR: 缺少 .env 文件，请从 .env.example 复制并修改"
    exit 1
fi

# 加载 .env 中的 NODE_VERSION（如果存在）
set -a
source .env 2>/dev/null || true
set +a

# 检查 Node 版本并切换（RISK-3 / AP-001）
if [ -f ~/.nvm/nvm.sh ]; then
    source ~/.nvm/nvm.sh
    NODE_VERSION="${NODE_VERSION:-24}"
    echo ">>> 切换到 Node $NODE_VERSION..."
    nvm use "$NODE_VERSION" || { echo "ERROR: Node $NODE_VERSION 不可用，请先安装"; exit 1; }
fi

echo "========================================"
echo "医小管 - 一键部署脚本"
echo "========================================"

# 步骤2: 构建 student-app
echo ">>> 构建 student-app..."
cd "$SCRIPT_DIR/../apps/student-app"
if [ ! -d node_modules ]; then
    npm install --silent
else
    echo "    node_modules 已存在，跳过 npm install"
fi
npx uni build -p h5
echo "    ✓ student-app 构建完成"

# 步骤3: 构建 teacher-web
echo ">>> 构建 teacher-web..."
cd "$SCRIPT_DIR/../apps/teacher-web"
if [ ! -d node_modules ]; then
    npm install --silent
else
    echo "    node_modules 已存在，跳过 npm install"
fi
npm run build-only
echo "    ✓ teacher-web 构建完成"

# 步骤4: 检查/构建后端 jar
echo ">>> 检查后端 jar..."
JAR="$SCRIPT_DIR/../services/business-api/ruoyi-admin/target/ruoyi-admin.jar"
if [ ! -f "$JAR" ]; then
    echo "    jar 不存在，开始构建..."
    cd "$SCRIPT_DIR/../services/business-api"
    mvn package -DskipTests -q
    echo "    ✓ 后端 jar 构建完成"
else
    echo "    ✓ 后端 jar 已存在，跳过构建"
fi

# 步骤5: Docker Compose
echo ">>> 启动 Docker Compose..."
cd "$SCRIPT_DIR"
docker compose build business-api
docker compose up -d

# 步骤6: 状态输出
echo "========================================"
echo ">>> 等待服务启动（30秒）..."
sleep 30

echo ""
echo "========================================"
echo "服务状态:"
echo "========================================"
docker compose ps

SERVER_IP=$(hostname -I | awk '{print $1}')
echo ""
echo "========================================"
echo "访问地址:"
echo "========================================"
echo "学生端: http://$SERVER_IP"
echo "教师端: http://$SERVER_IP:81"
echo "API 接口: http://$SERVER_IP:8080"
echo "========================================"
