---
id: "bugfix-login-auth"
parent: ""
type: "bugfix"
status: "superseded_by_spec-bugfix-login-userdata"
tier: "T3"
priority: "high"
risk: "high"
foundation: true

scope:
  - "scripts/generate_user_data.py"
  - "scripts/fix_and_insert.py"
  - "scripts/insert_students.sql"
  - "scripts/insert_teachers.sql"

out_of_scope:
  - "services/**"
  - "apps/**"
  - "knowledge-base/**"
  - "docs/**"

context_files:
  - ".teb/antipatterns.md"
  - "services/business-api/sql/yx_schema.sql"
  - "services/business-api/ruoyi-framework/src/main/java/com/ruoyi/framework/web/service/UserDetailsServiceImpl.java"
  - "services/business-api/ruoyi-framework/src/main/java/com/ruoyi/framework/web/service/SysPasswordService.java"
  - "services/business-api/ruoyi-common/src/main/java/com/ruoyi/common/utils/SecurityUtils.java"

done_criteria:
  L0: "scripts/generate_user_data.py 存在且可被 python -c 'import ast; ast.parse(open(...).read())' 解析"
  L1: "python scripts/generate_user_data.py --help 或 dry-run 不报错（无需实际 Excel 源文件时可 mock）"
  L2: "生成的 insert_students.sql 满足：(a) INSERT 列名与 yx_schema.sql 的 yx_user 表完全一致；(b) password 字段值以 $2a$ 开头（BCrypt 格式）；(c) 无 nick_name/dept_name/user_type 等不存在的列"
  L3: "在 165 服务器执行生成的 SQL 后，使用测试账号通过 POST /login 接口成功获取 token"

depends_on: []
created_at: "2026-04-05 23:00:00"

reproduction_steps:
  - "手机浏览器访问 http://192.168.100.165:5174 学生端登录页"
  - "输入任意已知账号（如 4523570155）和对应密码"
  - "点击登录 → 失败（用户不存在 或 密码不匹配）"

root_cause: |
  三层叠加导致所有账号均无法登录：

  Bug-1（致命）：generate_user_data.py 生成的 SQL 列名与 yx_user 实际表结构不匹配
    - SQL 使用: nick_name, dept_name, user_type
    - 实际表列: nickname, department, （无 user_type 列）
    - 后果: PostgreSQL INSERT 报错 "column does not exist"，yx_user 表零行数据
    - 定位: scripts/generate_user_data.py 第 165-180 行 SQL 模板
    - 证据: yx_schema.sql 第 7-33 行 CREATE TABLE yx_user 定义

  Bug-2（致命）：密码以明文存储，BCrypt 校验永远不通过
    - generate_user_data.py 第 168-169 行: password = obfuscated_id（明文）
    - 认证链末端 SysPasswordService.matches() 调用 BCryptPasswordEncoder.matches(raw, stored)
    - BCryptPasswordEncoder.matches("明文", "明文") 永远返回 false（非法 BCrypt 格式）
    - 定位: scripts/generate_user_data.py 第 168-169 行
    - 证据: SecurityUtils.java matchesPassword 方法；SysPasswordService.java validate 方法

  Bug-3（致命）：旧测试账号插入了 sys_user 表，但认证链查 yx_user 表
    - 165 服务器上手动插入的 4523570155/admin123 和 2024010001/admin123 在 sys_user 表
    - 定制后的 UserDetailsServiceImpl.loadUserByUsername() 查 yx_user 表
    - 定位: UserDetailsServiceImpl.java 第 45 行 userService.selectUserByUsername

  附加：fix_and_insert.py 修复了 Bug-1（列名映射），但未修复 Bug-2（密码仍为明文）

affected_modules:
  - "scripts/generate_user_data.py — 根源文件"
  - "scripts/insert_students.sql — 产物（列名错误 + 明文密码）"
  - "scripts/insert_teachers.sql — 产物（同上）"
  - "scripts/fix_and_insert.py — 部分修复但遗漏密码哈希"
  - "165 PostgreSQL yx_user 表 — 当前大概率零行或明文密码数据"
  - "学生端登录（全阻塞）"
  - "教师端登录（若走 yx_user 则同样阻塞）"

fix_direction: |
  1. 修复 generate_user_data.py：
     a) SQL 模板列名对齐 yx_schema.sql：nick_name→nickname, dept_name→department, 删除 user_type
     b) 在生成 SQL 前对密码做 BCrypt 哈希（引入 Python bcrypt 库）
     c) 哈希结果以 $2a$10$... 格式写入 SQL 的 password 字段

  2. 修复 fix_and_insert.py：
     a) 在 INSERT 前对 password 字段做 BCrypt 哈希
     b) 当前第 88 行 password = fields[1].strip("'") 后增加 bcrypt.hashpw() 调用

  3. 重新生成 insert_students.sql 和 insert_teachers.sql（由修复后的 generate_user_data.py 产出）

  4. 部署执行（超出 T3/Kimi CLI 能力范围，需单独安排）：
     a) 在 165 服务器执行修复后的 SQL 或 fix_and_insert.py
     b) 验证 yx_user 行数 > 0 且 password 以 $2a$ 开头
     c) curl POST /login 验证端到端登录

regression_test: |
  - generate_user_data.py 的单元测试：生成的 SQL 列名必须为 yx_schema.sql 中定义的列
  - generate_user_data.py 的单元测试：password 字段值必须匹配 $2a$10$ 正则
  - 端到端：测试账号能通过 /login API 获取 token
---

# 登录认证全链路修复

> 修复后，generate_user_data.py 生成的用户数据 SQL 能正确插入 yx_user 表，
> 且密码以 BCrypt 哈希存储，学生/教师可通过学号+默认密码成功登录。

## 背景

学生端部署到 165 服务器后，所有账号均无法登录。T0 诊断发现数据生成脚本
（generate_user_data.py）与实际数据库表结构存在列名不匹配和密码格式错误两个根因。
这是地基级 bug——用户认证不通，所有业务功能均不可用。

## 已知陷阱

1. **remote_exec.py 引号丢失**：通过 remote_exec.py --file 传输含单引号的 bash/SQL 脚本时，
   单引号会被吞掉。快速验证脚本因此 BLOCKED。全盘修复后的 SQL 文件部署到 165 时需注意此问题。

2. **yx_user.status 默认值为 2（未激活）**：INSERT 时必须显式设置 status=1，
   否则 UserDetailsServiceImpl 会拒绝登录（status==0 || status==2 → 停用/未激活）。

3. **yx_role 和 yx_user_role 可能为空**：fix_and_insert.py 有初始化 yx_role 的逻辑
   （student=2, teacher=3），但需确认 165 数据库中这些记录是否存在。
   UserDetailsServiceImpl.loadUserByUsername 会 LEFT JOIN yx_user_role 和 yx_role。

4. **BCrypt 哈希含 $ 符号**：生成的 SQL 中 $2a$10$... 在 bash 环境下会被解释为变量，
   需要用单引号包裹或转义。在 PostgreSQL 中可使用 E'' 或 $$ 定界符。
