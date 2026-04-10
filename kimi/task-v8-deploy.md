# T3 任务: v8 DEPLOY — 在本地 Windows 部署 wechat-article-exporter

## 角色
你是医小管知识库自动化工程师。

## 任务目标
在本地 Windows 开发机上通过 Docker 部署 wechat-article-exporter，让用户可以通过浏览器访问 http://localhost:3000 扫码登录。

## ⚠️ 重要说明
- 所有操作在本地 Windows 执行（不是远程服务器）
- PowerShell 中 `curl` 是 `Invoke-WebRequest` 别名，HTTP 测试请用 `curl.exe` 或 `Invoke-WebRequest`
- 如果 Docker 未安装或未运行，先检查并给出提示

## 执行步骤

### Step 1: 检查 Docker 状态
```powershell
docker info 2>&1 | Select-Object -First 5
```
如果 Docker 未运行，输出提示并等待。

### Step 2: 检查端口 3000 是否占用
```powershell
netstat -ano | findstr ":3000"
```
如果端口 3000 被占用，改用 3001。

### Step 3: 创建数据目录
```powershell
New-Item -ItemType Directory -Force -Path "C:\wechat-exporter\.data"
```

### Step 4: 拉取 Docker 镜像
```powershell
docker pull ghcr.io/wechat-article/wechat-article-exporter:latest
```

### Step 5: 启动容器
**如果端口 3000 可用:**
```powershell
docker run -d `
  --restart always `
  --name wechat-article-exporter `
  -e NODE_TLS_REJECT_UNAUTHORIZED=0 `
  -p 3000:3000 `
  -v "C:\wechat-exporter\.data:/app/.data" `
  ghcr.io/wechat-article/wechat-article-exporter:latest
```

**如果端口 3000 被占用，改用 3001:**
```powershell
docker run -d `
  --restart always `
  --name wechat-article-exporter `
  -e NODE_TLS_REJECT_UNAUTHORIZED=0 `
  -p 3001:3000 `
  -v "C:\wechat-exporter\.data:/app/.data" `
  ghcr.io/wechat-article/wechat-article-exporter:latest
```

### Step 6: 等待容器启动（约 5 秒）
```powershell
Start-Sleep -Seconds 5
docker ps | findstr wechat
```

### Step 7: 验证服务可访问
```powershell
# 使用 curl.exe（避免 PowerShell 别名）
curl.exe -s -o $null -w "%{http_code}" http://localhost:3000
```
期望返回 200。

如果 curl.exe 不可用，用 PowerShell 原生方式:
```powershell
(Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing).StatusCode
```

## 输出

将部署结果写入 `kimi/deploy-v8-report.md`:

```markdown
# wechat-article-exporter 部署报告

部署时间: YYYY-MM-DD HH:MM
部署位置: 本地 Windows
访问地址: http://localhost:{PORT}
容器 ID: {CONTAINER_ID}
数据目录: C:\wechat-exporter\.data

## 验收

| 项目 | 结果 |
|------|------|
| docker ps 状态 | Up XX minutes |
| HTTP 状态码 | 200 |
| 数据目录 | 已挂载 |

## 下一步

用户需要：
1. 打开浏览器访问 http://localhost:{PORT}
2. 点击【登录】按钮，用微信扫码
3. 选择一个公众号授权（需要拥有公众号）
4. 登录后在 API 页面复制 auth-key 提供给 T1
```

## 错误处理

**如果镜像拉取失败（网络问题）**:
- 检查是否需要配置 Docker 镜像加速
- 尝试: `docker pull dockerhub.icu/wechat-article/wechat-article-exporter:latest`

**如果容器启动失败**:
- 运行 `docker logs wechat-article-exporter` 查看错误
- 将错误信息写入报告

请开始执行。
