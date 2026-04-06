---
id: "f-v5a-05"
parent: "v5a-quick-fixes"
type: "feature"
status: "done"
tier: "T3"
priority: "medium"
risk: "medium"
foundation: false

scope:
  - "apps/student-app/src/pages/login/index.vue"
out_of_scope:
  - "services/**"
  - "apps/student-app/src/pages/**"
  - "scripts/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/login/index.vue"

done_criteria:
  L0: "login/index.vue 中存在验证码相关 UI 元素（captchaImage 或类似）"
  L1: "grep 'captcha' apps/student-app/src/pages/login/index.vue 有结果"
  L2: "curl -s http://192.168.100.165:8080/captchaImage | grep -q 'captchaEnabled.*true' && echo PASS || echo FAIL"
  L3: "访问登录页可见算术验证码图片；输入正确验证码+正确账号密码登录成功；验证码错误有提示"

execution:
  step1:
    desc: "确认 login/index.vue 已有验证码 UI（若依标准模板通常已内置）"
    action: "读取 login/index.vue，检查是否有 captchaImage 相关代码"
  step2:
    desc: "在 165 服务器执行 Redis 写入启用验证码"
    command: "ssh easten@192.168.100.165 \"docker exec yx_redis redis-cli -a 'Yx@Redis2026!' SET sys_config:sys.account.captchaEnabled true\""
    fallback: "若 Redis Key 不生效，改查 PostgreSQL sys_config 表：UPDATE sys_config SET config_value='true' WHERE config_key='sys.account.captchaEnabled'"
  step3:
    desc: "验证 /captchaImage 接口返回 captchaEnabled=true"
    command: "curl -s http://192.168.100.165:8080/captchaImage"

created_at: "2026-04-06"
---

# F-V5A-05: 启用登录验证码

> 165 服务器登录页显示算术验证码，验证码功能正常（正确可登录，错误有提示）。

## 背景

当前 captchaEnabled=false（曾在 bugfix-login 阶段关闭以便测试）。demo 演示前需启用以增强安全感。

## 变更详情

**服务器操作**（非代码变更）：
```bash
docker exec yx_redis redis-cli -a 'Yx@Redis2026!' SET sys_config:sys.account.captchaEnabled true
```

**前端确认**：检查 `login/index.vue` 是否已有验证码组件。若已有则无需代码修改；若无则参考若依标准登录页补充 captchaImage UI。

## 已知陷阱

- Redis Key 格式须与后端 `CacheConstants` 定义一致，若不生效可检查后端日志中实际读取的 key 名
- 若后端缓存了旧配置，重启 Spring Boot 进程可清除
- 165 服务器 SSH 用户 `easten`，sudo 密码 `ZhaYeFan05.07.14`
