---
id: "fix-3-deploy-and-e2e-login"
parent: "bugfix-login-userdata"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "high"
foundation: true

scope:
  - "temp/**"
  - ".tasks/bugfix-login-userdata/fix-3-deploy-and-e2e-login/_report.md"

out_of_scope:
  - "services/**"
  - "apps/**"
  - "knowledge-base/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - "scripts/insert_students.sql"
  - "scripts/insert_teachers.sql"
  - "scripts/fix_and_insert.py"

done_criteria:
  L0: "165 数据库执行后 SELECT COUNT(*) FROM yx_user > 0，并在报告中附 SQL 输出"
  L1: "SELECT LEFT(password,4) FROM yx_user LIMIT 5 全部为 $2a$（或等价统计证据）"
  L2: "curl POST http://localhost:8080/login 使用测试账号返回 token；同时 GET /captchaImage 为 captchaEnabled=false"
  L3: "手机浏览器访问 http://192.168.100.165:5174 登录成功并进入首页"

depends_on: ["fix-0-captcha-disabled", "fix-1-generate-userdata-script", "fix-2-fix-and-insert-bcrypt"]
created_at: "2026-04-05 23:40:00"
---

# FIX-3：165 部署执行 + 端到端登录验证

> 完成后，修复后的用户数据在 165 环境成功落库，登录接口与前端登录链路同时验证通过。

## 背景

脚本修复完成后，必须在目标环境完成真实部署与回归验证，才能确认登录阻塞被根治。

## 执行步骤

1. 备份后清理 `yx_user` / `yx_user_role` 旧数据（按可回滚方案）
2. 执行角色初始化与用户数据 SQL
3. 检查 `yx_user` 行数、密码前缀、`status=1` 覆盖情况
4. 验证验证码接口与 `/login` 接口
5. 完成 H5 实机登录验证
6. 记录全部命令、输出摘要与异常分支

## 已知陷阱

- 含 `$2a$` 的 SQL/脚本传输优先使用文件方式，避免引号吞噬
- 必须保留可追溯证据，不可只写“验证通过”
