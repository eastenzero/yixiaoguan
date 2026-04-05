---
id: "fix-2-fix-and-insert-bcrypt"
parent: "bugfix-login-userdata"
type: "bugfix"
status: "pending"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "scripts/fix_and_insert.py"
  - ".tasks/bugfix-login-userdata/fix-2-fix-and-insert-bcrypt/_report.md"

out_of_scope:
  - "scripts/generate_user_data.py"
  - "services/**"
  - "apps/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - "scripts/fix_and_insert.py"

done_criteria:
  L0: "scripts/fix_and_insert.py 存在且可 ast.parse"
  L1: "文件中存在 bcrypt.hashpw 调用，覆盖学生与教师两段插入逻辑"
  L2: "python -m py_compile scripts/fix_and_insert.py 通过，且脚本运行入口不抛 ImportError"
  L3: "该脚本补写的数据与 FIX-1 生成数据在密码策略上完全一致（均为 BCrypt）"

depends_on: []
created_at: "2026-04-05 23:40:00"
---

# FIX-2：修复 fix_and_insert.py 密码哈希

> 完成后，`fix_and_insert.py` 不再写入明文密码，作为兜底数据修复脚本可安全复用。

## 背景

该脚本已处理列名映射，但仍在关键路径写入明文密码，导致认证链 `BCryptPasswordEncoder.matches` 恒失败。需补齐与 FIX-1 一致的哈希策略。

## 执行步骤

1. 在学生插入逻辑中增加 `bcrypt.hashpw()`
2. 在教师插入逻辑中同步增加 `bcrypt.hashpw()`
3. 检查依赖导入、编码与字符串处理
4. 运行语法检查并记录证据

## 已知陷阱

- 仅修密码哈希，不改其他业务流程
- 不允许把哈希逻辑写成不可复用的临时分支
