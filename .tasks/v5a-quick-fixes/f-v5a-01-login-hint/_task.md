---
id: "f-v5a-01"
parent: "v5a-quick-fixes"
type: "bugfix"
status: "done"
tier: "T3"
priority: "high"
risk: "low"
foundation: false

scope:
  - "apps/student-app/src/pages/login/index.vue"
out_of_scope:
  - "apps/student-app/src/pages/login/**"
  - "services/**"
  - "scripts/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/login/index.vue"

done_criteria:
  L0: "apps/student-app/src/pages/login/index.vue 存在"
  L1: "grep '初始密码与学号相同' apps/student-app/src/pages/login/index.vue 返回结果"
  L2: "grep -c '首次登录请使用默认密码' apps/student-app/src/pages/login/index.vue 返回 0"
  L3: "登录页底部显示文案为"初始密码与学号相同，登录后请及时修改""

root_cause: "密码策略已由默认密码改为学号即密码（generate_user_data.py 实现），但登录页提示文案未同步更新。"

created_at: "2026-04-06"
completed_at: "2026-04-06"
verified_by: "t2-foreman"
git_commit: "9b9d573"
---

# F-V5A-01: 登录页提示文案修正

> 登录页底部提示文案与实际密码策略一致：显示"初始密码与学号相同，登录后请及时修改"。

## 背景

`generate_user_data.py` 生成的用户数据中，密码为学号本身（BCrypt 哈希）。但登录页当前仍显示旧文案"首次登录请使用默认密码，登录后请修改"，会误导用户。

## 变更详情

- **文件**: `apps/student-app/src/pages/login/index.vue`
- **位置**: template 区域，约 line 66
- **改前**: `首次登录请使用默认密码，登录后请修改`
- **改后**: `初始密码与学号相同，登录后请及时修改`

## 已知陷阱

暂无。本任务为单行文字修改，风险极低。
