---
id: "v6a-03-batch-accounts"
parent: "v6-launch"
type: "feature"
status: "pending"
tier: "T3"
priority: "high"
risk: "low"
foundation: false

scope:
  - "scripts/generate_user_data.py"

out_of_scope:
  - "apps/**"
  - "services/**"
  - "deploy/**"
  - "scripts/batch_ingest*.py"
  - "scripts/run_eval.py"

context_files:
  - ".teb/antipatterns.md"
  - "scripts/generate_user_data.py"

done_criteria:
  L0: "scripts/generate_user_data.py 中 generate_test_data() 函数返回 ≥ 25 个学生记录"
  L1: "python -m py_compile scripts/generate_user_data.py 成功无错误"
  L2: "python scripts/generate_user_data.py --test --dry-run 运行成功，输出显示学生数 ≥ 25、教师数 ≥ 8"
  L3: "新增账号学号格式合理（2024/2025开头10位），不与现有5个学生账号冲突，教师用户名格式统一"

depends_on: []
created_at: "2026-04-11 16:20:00"
---

# 批量生成内测测试账号

> `generate_user_data.py --test` 模式可生成 ≥ 25 个学生 + ≥ 8 个教师测试账号，密码规则不变。

## 背景

当前仅 5 个学生 + 4 个教师测试账号。内测需要更多账号以模拟真实使用场景。

## 需求

1. 修改 `generate_test_data()` 函数，从 5 个测试学生扩展到 **≥ 25 个**
2. 新增学生账号要求:
   - 学号: 2024/2025 开头的 10 位数字，每个唯一
   - 姓名: 使用真实感的中文姓名（可用现有 COMMON_NAMES 池）
   - 学院: 覆盖至少 5 个不同学院（使用 DEPT_CODES 中的学院名）
   - 专业/年级/班级: 真实感填写
3. 教师账号:
   - 由 `generate_teachers()` 从学院+年级组合自动生成
   - 新增学生覆盖更多学院+年级组合后，教师数量自然增长到 ≥ 8
4. 密码规则不变:
   - 学生密码 = 混淆后学号（username 本身）
   - 教师密码 = 姓名全拼音
   - 所有密码 BCrypt $2a$ 哈希

## 现有账号（禁止冲突）

学生: 2524010001, 2021010002, 2024010103, 2024410004, 2024010003
教师: liang_s_huli_24, xie_s_yaoxue_24, deng_p_linchuang_24, cheng_d_fangshe_24

## 已知陷阱

- `random.seed(42)` 确保可重复性，不要改变种子值
- 脚本依赖 pandas, bcrypt, pypinyin 库，不要添加新依赖
- 不要修改 `generate_sql_students()` 和 `generate_sql_teachers()` 的 SQL 生成逻辑
- 只改 `generate_test_data()` 函数体
