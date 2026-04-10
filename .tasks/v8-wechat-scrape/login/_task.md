# LOGIN — 用户手动扫码登录

**所属**: v8-wechat-scrape / PHASE 1
**优先级**: P0
**执行者**: 👤 用户（人工步骤）
**预估工时**: 5 分钟
**依赖**: DEPLOY

## 任务目标

用户通过微信扫码登录 wechat-article-exporter，生成 auth-key 供后续 API 调用。

## 用户操作步骤

1. 浏览器打开 `http://localhost:3000`
2. 点击【登录】按钮
3. 用微信扫描二维码
4. 选择一个**公众号**（订阅号或服务号，不能选小程序）进行授权
5. 登录成功后，进入 API 页面复制 **auth-key**
6. 将 auth-key 告知 T1

## 前提条件

需要拥有一个微信公众号（订阅号即可，免费注册）：  
https://mp.weixin.qq.com/cgi-bin/registermidpage?action=index

## 注意事项

- auth-key 有效期 **4 天**，过期需重新扫码
- 登录不会影响公众号内容，仅借用接口权限

## 验收标准

- AC-LOG-01: 登录成功，页面显示已登录状态
- AC-LOG-02: auth-key 已提供给 T1
