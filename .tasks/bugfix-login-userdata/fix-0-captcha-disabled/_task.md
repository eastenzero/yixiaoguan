---
id: "fix-0-captcha-disabled"
parent: "bugfix-login-userdata"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "temp/**"
  - ".tasks/bugfix-login-userdata/fix-0-captcha-disabled/_report.md"

out_of_scope:
  - "scripts/generate_user_data.py"
  - "scripts/fix_and_insert.py"
  - "services/**"
  - "apps/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - "deploy/README.md"

done_criteria:
  L0: "fix-0 的 _report.md 存在，且包含 captchaImage 实际返回 JSON"
  L1: "若使用临时脚本，脚本语法检查通过（bash -n）"
  L2: "165 上执行 curl http://localhost:8080/captchaImage，返回 captchaEnabled=false"
  L3: "验证码门禁已解除，不再阻塞后续 /login 验证"

depends_on: []
created_at: "2026-04-05 23:40:00"
---

# FIX-0：验证码关闭确认（前置）

> 完成后，165 环境登录链路不再被验证码配置误拦截，后续登录验收可稳定复现。

## 背景

根据 T0 诊断，上一轮部署存在 Redis 缓存残留风险，可能导致 `sys.account.captchaEnabled=false` 未生效。若不先确认该门禁，后续账号密码修复将被假性失败掩盖。

## 执行步骤

1. 在 165 检查 `sys_config` 中 `sys.account.captchaEnabled`
2. 若配置正确但返回异常，清理 `captcha_codes:*` 并重启后端
3. 运行 `curl http://localhost:8080/captchaImage`
4. 将命令与输出写入 `_report.md`

## 已知陷阱

- 不要只看数据库配置，必须以接口返回为准
- 缓存清理与后端重启后二次验证不可省略
