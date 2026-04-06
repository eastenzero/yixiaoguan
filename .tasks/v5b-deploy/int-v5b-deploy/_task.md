---
id: "int-v5b-deploy"
parent: "v5b-deploy"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "medium"

scope:
  - ".tasks/v5b-deploy/int-v5b-deploy/_report.md"
out_of_scope:
  - "apps/"
  - "services/"
  - "deploy/"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/v5b-deploy/_task.md"
  - ".tasks/_spec-v5b-deploy.yaml"

done_criteria:
  L0: "docker compose ps 输出 5 个服务，全部 Up 或 healthy"
  L1: |
    以下 curl 均返回预期结果（在 165 服务器执行）：
    curl -s -o /dev/null -w "%{http_code}" http://localhost/              → 200
    curl -s -o /dev/null -w "%{http_code}" http://localhost/api/captchaImage → 200
    curl -s -o /dev/null -w "%{http_code}" http://localhost:81/           → 200
  L2: |
    SSE 流式测试（需先登录获取 token）：
    curl -s -N -H "Authorization: Bearer <token>" \
      http://localhost/api/chat/stream?query=你好 | head -c 200
    → 返回 data: 前缀的 SSE 事件，不卡死
  L3: |
    T1 人工验收（需在手机或浏览器中操作）：
    AC-1: 浏览器访问 http://192.168.100.165 → 学生端登录页正常显示
    AC-2: 使用 2524010001/2524010001 登录成功
    AC-3: 发送 AI 问题，收到流式回复（非一行截断）
    AC-4: 点击参考资料条目，跳转或显示摘要
    AC-5: 访问 http://192.168.100.165:81 → 教师端首页正常显示
    AC-6: docker compose down → docker compose up -d → 数据不丢失（yx_user 表仍有数据）

depends_on: ["f-v5b-05-deploy-script"]
created_at: "2026-04-06"
---

# int-v5b-deploy: 全栈部署集成验收

> 完成后：全部 AC 通过，可签收 spec-v5b，向 T0 提交完成汇报。

## 验收项一览

| AC | 内容 | 验证方式 | 预期 |
|----|------|---------|------|
| AC-1 | 学生端首页可访问 | 浏览器/curl | HTTP 200，登录页渲染正常 |
| AC-2 | 登录功能正常 | 浏览器 | 2524010001 登录成功进入首页 |
| AC-3 | AI 流式对话 | 浏览器 | 消息气泡逐字渲染，非一次性显示 |
| AC-4 | 参考资料跳转 | 浏览器 | 点击后有内容展示 |
| AC-5 | 教师端可访问 | 浏览器/curl | HTTP 200，教师端页面渲染 |
| AC-6 | 数据持久化 | docker down/up | 用户数据不丢失 |

## 验收前置检查

```bash
# 在 165 服务器执行
cd ~/dev/yixiaoguan/deploy
docker compose ps                          # 全部 healthy
docker compose logs business-api --tail=5  # 无 ERROR
docker compose logs ai-service --tail=5    # 无 ERROR
docker compose logs nginx --tail=5         # 无 ERROR
```

## 验收报告模板

执行后在本目录创建 `_report.md`，格式参考 `.teb/templates/_report.template.md`。
结论行必须包含：`PASS` 或 `PARTIAL` 或 `FAIL`。
