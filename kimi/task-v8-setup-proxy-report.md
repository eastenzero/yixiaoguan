# T3 任务报告: 配置公共代理节点 + 验证可用性

## 执行时间
2026-04-10 16:15:00+08:00

## 1. API 端点探测结果

### 测试的端点
| 端点 | 响应状态 | 说明 |
|------|----------|------|
| `GET /api/public/v1/proxies` | ❌ HTML Fallback | 端点不存在 |
| `GET /api/proxies` | ❌ HTML Fallback | 端点不存在 |
| `GET /api/settings` | ❌ HTML Fallback | 端点不存在 |
| `GET /api/config` | ❌ HTML Fallback | 端点不存在 |
| `GET /api/public/v1/proxy` | ❌ HTML Fallback | 端点不存在 |

### 可用的 API 端点 (JSON 响应)
| 端点 | 响应状态 | 说明 |
|------|----------|------|
| `GET /api/public/v1/article` | ✅ 正常 | 支持 `proxy` 参数 |
| `GET /api/public/v1/account` | ✅ 正常 | 支持 `proxy` 参数 |
| `GET /api/public/v1/download` | ✅ 正常 | 支持 `proxy` 参数 |
| `GET /api/public/v1/authkey` | ✅ 正常 | 返回当前 auth-key |

## 2. 代理节点可用性测试

### 原始公共代理节点 (全部不可用)
根据 `config/public-proxy.ts` 配置的 96 个代理节点 (6 个域 × 16 个子域) 全部被 Cloudflare 拦截:

| 域名 | 状态 | 备注 |
|------|------|------|
| `*.worker-proxy.asia` | ❌ 被拦截 | Cloudflare 403 |
| `*.net-proxy.asia` | ❌ 被拦截 | Cloudflare 403 |
| `*.1235566.space` | ❌ 被拦截 | Cloudflare 403 |
| `*.worker-proxy.shop` | ❌ 被拦截 | Cloudflare 403 |
| `*.worker-proxys.cyou` | ❌ 被拦截 | Cloudflare 403 |
| `*.worker-proxy.cyou` | ❌ 被拦截 | Cloudflare 403 |

### wproxy 节点 (全部不可用)
| 节点 | 状态 | 备注 |
|------|------|------|
| `wproxy-01.deno.dev` ~ `wproxy-10.deno.dev` | ❌ 404 | DEPLOYMENT_NOT_FOUND |

### vproxy 节点 (部分可用)
| 节点 | 状态 | 测试响应 |
|------|------|----------|
| `https://vproxy-01.deno.dev` | ✅ 可用 | `{"origin": "34.16.131.219"}` |
| `https://vproxy-02.deno.dev` | ✅ 可用 | `{"origin": "34.50.175.32"}` |
| `vproxy-03.deno.dev` ~ `vproxy-06.deno.dev` | ❌ 404 | DEPLOYMENT_NOT_FOUND |
| `vproxy-01.jooooock.workers.dev` | ❌ 错误 | error code: 1042 |
| `vproxy-02.jooooock.workers.dev` | ❌ 错误 | error code: 1042 |

## 3. 配置文件创建

创建了代理配置文件:
- **路径**: `C:\wechat-exporter\.data\config\proxies.json`
- **内容**:
```json
{
  "proxies": [
    "https://vproxy-01.deno.dev",
    "https://vproxy-02.deno.dev"
  ],
  "updated_at": "2026-04-10T16:15:00+08:00",
  "source": "manual_test_verified"
}
```

## 4. 带代理的 API 请求测试

### 测试命令
```powershell
# 使用 vproxy-01 获取文章列表
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" `
  -H "Accept: application/json" `
  "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=5&proxy=https://vproxy-01.deno.dev"

# 使用 vproxy-02 获取文章列表
curl.exe -s -X GET -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" `
  -H "Accept: application/json" `
  "http://localhost:3000/api/public/v1/article?fakeid=Mzg3ODMyNjg1Nw==&begin=0&count=5&proxy=https://vproxy-02.deno.dev"
```

### 测试结果
| 代理 | 状态 | 响应 |
|------|------|------|
| vproxy-01 | ✅ 成功 | 返回 5 篇文章 |
| vproxy-02 | ✅ 成功 | 返回 5 篇文章 |

## 5. 容器信息

| 项目 | 值 |
|------|-----|
| 容器名称 | wechat-article-exporter |
| 镜像 | ghcr.io/wechat-article/wechat-article-exporter:latest |
| 版本 | v2.3.15 |
| 端口映射 | 0.0.0.0:3000->3000/tcp |
| 数据卷 | C:\wechat-exporter\.data:/app/.data |

### 环境变量
| 变量 | 值 |
|------|-----|
| NODE_TLS_REJECT_UNAUTHORIZED | 0 |
| NODE_ENV | production |
| HOST | 0.0.0.0 |
| PORT | 3000 |

## 6. 结论与建议

### 当前可用代理
仅 **2 个**代理节点可用:
1. `https://vproxy-01.deno.dev`
2. `https://vproxy-02.deno.dev`

### API 使用方式
wechat-article-exporter 支持通过 `proxy` 查询参数为单次请求指定代理:
```
GET /api/public/v1/article?proxy=https://vproxy-01.deno.dev&...
GET /api/public/v1/download?proxy=https://vproxy-01.deno.dev&...
```

### 建议
1. **公共代理不稳定**: 大部分公共代理已被 Cloudflare 拦截或下线
2. **推荐私有代理**: 按照官方文档搭建私有代理节点
3. **代理轮换**: 仅有的 2 个可用代理需要轮换使用以避免频率限制
4. **监控代理状态**: 建议定期测试代理可用性

### 下一步行动
1. ✅ 配置文件已创建: `C:\wechat-exporter\.data\config\proxies.json`
2. ⚠️ 需要搭建私有代理节点以保证稳定性
3. ⚠️ 需要实现代理轮换逻辑
