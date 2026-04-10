# T3 任务: 配置公共代理节点 + 验证可用性

## 目标
将 10 个公共代理节点注入 wechat-article-exporter，实现多节点轮转下载。

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3

## Step 1: 探测代理相关 API 端点

```powershell
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/public/v1/proxies
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/proxies
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/settings
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" http://localhost:3000/api/config
```

## Step 2: 尝试 POST 添加代理

```powershell
curl.exe -s -X POST -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" -H "Content-Type: application/json" `
  -d '{"url":"https://wproxy-01.deno.dev"}' `
  http://localhost:3000/api/public/v1/proxy

curl.exe -s -X POST -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" -H "Content-Type: application/json" `
  -d '{"proxies":["https://wproxy-01.deno.dev","https://wproxy-02.deno.dev"]}' `
  http://localhost:3000/api/settings
```

## Step 3: 检查 .data 目录是否有配置文件

```powershell
Get-ChildItem -Recurse "C:\wechat-exporter\.data" | Select-Object FullName, Length
```

如果有配置文件（.json/.yaml/.toml），读取并查看是否有 proxy 字段，然后追加代理节点。

## Step 4: 测试带代理的下载请求

```powershell
curl.exe -s -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" `
  "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=5&proxy=https://wproxy-01.deno.dev"
```

## 输出

1. 哪些 API 端点响应了（非 HTML fallback）
2. 是否成功添加代理
3. 是否找到配置文件及其路径
4. 带 proxy 参数的请求是否返回正常数据

请开始执行。
