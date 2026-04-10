# DEPLOY — Docker 部署 wechat-article-exporter

**所属**: v8-wechat-scrape / PHASE 1
**优先级**: P0
**执行者**: Kimi
**预估工时**: 0.5h
**依赖**: 无

## 任务目标

在本地 Windows 开发机上通过 Docker 部署 wechat-article-exporter，使用户能在浏览器中访问扫码登录页。

## 执行步骤

1. 检查 Docker 是否运行 (`docker info`)
2. 拉取镜像: `ghcr.io/wechat-article/wechat-article-exporter:latest`
3. 创建数据目录: `C:/wechat-exporter/.data`
4. 启动容器（端口 3000）
5. 验证 `http://localhost:3000` 可访问

## 输出文件

`kimi/deploy-v8-report.md` — 记录部署结果（容器ID、端口、数据目录）

## 验收标准

- AC-DEP-01: `docker ps` 显示容器状态 Up
- AC-DEP-02: `curl http://localhost:3000` 返回 HTTP 200
- AC-DEP-03: 数据目录已挂载
