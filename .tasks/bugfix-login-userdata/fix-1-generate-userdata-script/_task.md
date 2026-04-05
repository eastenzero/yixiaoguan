---
id: "fix-1-generate-userdata-script"
parent: "bugfix-login-userdata"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "high"
risk: "high"
foundation: true

scope:
  - "scripts/generate_user_data.py"
  - "scripts/insert_students.sql"
  - "scripts/insert_teachers.sql"
  - ".tasks/bugfix-login-userdata/fix-1-generate-userdata-script/_report.md"

out_of_scope:
  - "scripts/fix_and_insert.py"
  - "services/**"
  - "apps/**"
  - "knowledge-base/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - "services/business-api/sql/yx_schema.sql"
  - "scripts/generate_user_data.py"

done_criteria:
  L0: "scripts/generate_user_data.py 可被 ast.parse 解析，且生成 insert_students.sql / insert_teachers.sql"
  L1: "python scripts/generate_user_data.py --help（或 dry-run）执行无异常"
  L2: "生成 SQL 满足：列名与 yx_user 对齐、无 nick_name/dept_name/user_type、password 为 BCrypt（$2a$ 开头）、status=1、student_id/employee_id 正确落列"
  L3: "脚本产物可直接用于 165 部署，不依赖后端二次加密"

depends_on: []
created_at: "2026-04-05 23:40:00"
---

# FIX-1：重写 generate_user_data.py（列名对齐 + BCrypt + 激活状态）

> 完成后，数据生成脚本产出的 SQL 可直接写入 `yx_user`，且密码格式符合 Spring Security BCrypt 校验要求。

## 背景

当前登录阻塞的主根因在 `generate_user_data.py`：列名不匹配 + 明文密码写入。此任务是后续部署与验收的地基任务。

## 执行步骤

1. 校正 SQL 模板列名：`nickname` / `department`，删除 `user_type`
2. 增加 `student_id` / `employee_id` 显式写入
3. 引入 `bcrypt.hashpw()` 预哈希密码并安全写入 SQL
4. 显式写入 `status=1`
5. 同步生成 `yx_role` 与 `yx_user_role` 初始化/关联语句
6. 运行自检并在 `_report.md` 留下实际命令与输出摘要

## 已知陷阱

- `$2a$10$...` 在 shell 中容易被解释，写 SQL 时必须考虑转义与定界
- 不得顺手修改 `services/**`，认证链 Java 代码不在本任务范围
