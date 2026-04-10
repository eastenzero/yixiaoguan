# T3 任务: 查看 wechat-article-exporter 代理节点

## Step 1: 访问代理管理页面

```powershell
curl.exe -s http://localhost:3000/dashboard/proxy
```

如果返回 HTML，提取其中的代理节点列表（IP/域名、端口、协议类型）。

## Step 2: 尝试通过 API 获取代理列表

```powershell
curl.exe -s -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/public/v1/proxy
```

```powershell
curl.exe -s -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/proxy
```

## Step 3: 查看 Docker 容器环境变量中是否有代理配置

```powershell
docker inspect wechat-article-exporter 2>$null | python -m json.tool | Select-String -Pattern "proxy|PROXY|ENV" -Context 0,2
```

## 输出

报告：
1. 可用代理节点列表（节点数量、协议、地址）
2. 是否支持通过 API 切换代理
3. 是否支持为单次请求指定代理

请开始执行。
