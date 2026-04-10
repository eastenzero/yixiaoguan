# wechat-article-exporter 部署报告

部署时间: 2026-04-10 13:08
部署位置: 本地 Windows
访问地址: http://localhost:3000
容器 ID: ef20a86aeece
数据目录: C:\wechat-exporter\.data

## 验收

| 项目 | 结果 |
|------|------|
| docker ps 状态 | Up 17 seconds |
| HTTP 状态码 | 200 |
| 数据目录 | 已挂载 |

## 下一步

用户需要：
1. 打开浏览器访问 http://localhost:3000
2. 点击【登录】按钮，用微信扫码
3. 选择一个公众号授权（需要拥有公众号）
4. 登录后在 API 页面复制 auth-key 提供给 T1
