---
id: "bugfix-login-userdata"
parent: ""
type: "bugfix"
status: "pending"
tier: "T1"
priority: "high"
risk: "high"
foundation: true

scope:
  - "scripts/generate_user_data.py"
  - "scripts/fix_and_insert.py"
  - "scripts/insert_students.sql"
  - "scripts/insert_teachers.sql"
  - ".tasks/bugfix-login-userdata/**"
  - "temp/**"

out_of_scope:
  - "services/business-api/**"
  - "services/ai-service/**"
  - "apps/**"
  - "knowledge-base/**"
  - "docs/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - "services/business-api/sql/yx_schema.sql"
  - "services/business-api/ruoyi-framework/src/main/java/com/ruoyi/framework/web/service/UserDetailsServiceImpl.java"
  - "services/business-api/ruoyi-framework/src/main/java/com/ruoyi/framework/web/service/SysPasswordService.java"

done_criteria:
  L0: "fix-0/fix-1/fix-2/fix-3/int-login-auth-regression 五个子任务目录均产出 _report.md"
  L1: "FIX-1 和 FIX-2 对应脚本通过静态检查（ast.parse 或 py_compile）"
  L2: "FIX-3 与集成任务报告包含实际命令证据：captchaEnabled=false、yx_user password 前缀为 $2a$、/login 返回 token"
  L3: "165 学生端 H5 使用测试账号登录成功并进入首页，登录阻塞解除"

depends_on: []
created_at: "2026-04-05 23:40:00"

batches:
  - name: "batch-0"
    tasks: ["fix-0-captcha-disabled"]
    parallel: false
  - name: "batch-1"
    tasks: ["fix-1-generate-userdata-script", "fix-2-fix-and-insert-bcrypt"]
    parallel: true
    depends_on: "batch-0"
  - name: "batch-2"
    tasks: ["fix-3-deploy-and-e2e-login"]
    depends_on: "batch-1"
  - name: "batch-3"
    tasks: ["int-login-auth-regression"]
    depends_on: "batch-2"
---

# 登录阻塞修复：用户数据生成链路重建

> 完成后，`yx_user` 中的学生/教师账号可被认证链正确识别，密码以 BCrypt 存储，验证码不再误拦截，学生端登录流程可在 165 环境端到端通过。

## 背景

T0 规格已确认根因集中在数据层与部署层，而非前后端业务代码：

- `generate_user_data.py` 列名与 `yx_user` 表结构不一致（致命）
- 生成与修复脚本均存在明文密码写入（致命）
- 历史测试数据落在 `sys_user`，而认证链查询 `yx_user`（致命）
- 验证码配置可能被 Redis 缓存污染（高风险）

本任务按地基优先执行：先确保验证码门禁放通，再修脚本，再做 165 部署与回归验收。

## 批次门禁

| Batch | 任务 | 并行 | 门禁条件 |
|---|---|---|---|
| batch-0 | fix-0-captcha-disabled | 否 | 无 |
| batch-1 | fix-1-generate-userdata-script + fix-2-fix-and-insert-bcrypt | 是 | batch-0 PASS |
| batch-2 | fix-3-deploy-and-e2e-login | 否 | batch-1 全部 PASS |
| batch-3 | int-login-auth-regression | 否 | batch-2 PASS |

## 已知陷阱

- `remote_exec.py` 传输包含 `$2a$...` 的内容存在转义风险，优先 `--file` 或先落地脚本再执行
- `yx_user.status` 默认值是 `2`，插入时必须显式 `status=1`
- `yx_role` / `yx_user_role` 可能缺失，部署步骤必须补齐并验收
