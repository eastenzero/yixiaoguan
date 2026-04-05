# INT-LOGIN-AUTH-REGRESSION 验收报告

**任务ID**: int-login-auth-regression  
**执行时间**: 2026-04-06  
**验收类型**: T1 集成回归验收  
**前置任务**: FIX-0 ~ FIX-3 全部完成

---

## 一、证据链汇总

### FIX-0: 验证码关闭确认
| 检查项 | 证据来源 | 实测值 | 状态 |
|--------|----------|--------|------|
| captchaEnabled | `.tasks/bugfix-login-userdata/fix-0-captcha-disabled/_report.md` | `false` | ✅ |
| 接口状态码 | 同上 | `200` | ✅ |

**关键证据:**
```json
{"msg":"操作成功","code":200,"captchaEnabled":false}
```

---

### FIX-1: generate_user_data.py 脚本修复
| 检查项 | 证据来源 | 实测值 | 状态 |
|--------|----------|--------|------|
| AST 解析通过 | FIX-1 报告 L0 | `[L0 PASS] AST parse OK` | ✅ |
| 脚本执行无异常 | FIX-1 报告 L1 | `--help` 正常输出 | ✅ |
| 列名对齐 | FIX-1 报告 L2 | `nickname`/`department` 正确 | ✅ |
| 无错误列 | FIX-1 报告 L2 | 无 `nick_name`/`dept_name`/`user_type` | ✅ |
| BCrypt 密码格式 | FIX-1 报告 L2 | `$2a$10$...` | ✅ |
| status=1 | FIX-1 报告 L2 | 显式设置 | ✅ |
| yx_role 初始化 | FIX-1 报告 L2 | student(id=2), teacher(id=3) | ✅ |
| yx_user_role 关联 | FIX-1 报告 L2 | 已生成关联 SQL | ✅ |

**关键证据 - 学生 SQL 样本:**
```sql
INSERT INTO yx_user (username, password, real_name, nickname, student_id, department, major, grade, class_name, status, is_deleted, created_at, updated_at) VALUES
  ('2524010001', E'$2a$10$bjrasC00CuWuOWqNKS7P7.ra1XxsV6t/Y/MCZBfgOSIicMfEu7YdS', '张小洋', '张小洋', '2524010001', '放射学院', '医学影像学', '2024级', '影像1班', 1, FALSE, NOW(), NOW())
```

**关键证据 - 教师 SQL 样本:**
```sql
INSERT INTO yx_user (username, password, real_name, nickname, employee_id, department, grade, status, is_deleted, created_at, updated_at) VALUES
  ('liang_s_huli_24', E'$2a$10$eXoOu3iVhGpZLqpZlPZ/7.ett35nKD2l76/7JcL5.v3we9e4JXYnq', '梁淑芬', '梁淑芬', 'T0001', '护理学院', '2024级', 1, FALSE, NOW(), NOW())
```

---

### FIX-2: fix_and_insert.py 兜底脚本修复
| 检查项 | 证据来源 | 实测值 | 状态 |
|--------|----------|--------|------|
| import bcrypt | FIX-2 报告 | 第5行已添加 | ✅ |
| 学生密码哈希 | FIX-2 报告 | 第90行 `bcrypt.hashpw()` | ✅ |
| 教师密码哈希 | FIX-2 报告 | 第185行 `bcrypt.hashpw()` | ✅ |
| 语法检查 | FIX-2 报告 L0 | `py_compile` 无错误 | ✅ |
| bcrypt 调用计数 | FIX-2 报告 L1 | `grep -c >= 2` | ✅ |

**关键证据:**
```python
# 第90行（学生）
password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()

# 第185行（教师）
password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
```

---

### FIX-3: 部署执行与端到端验证
| 检查项 | 证据来源 | 实测值 | 状态 |
|--------|----------|--------|------|
| yx_user 行数 | FIX-3 报告 | `9 行` (5学生+4教师) | ✅ |
| 密码 BCrypt 格式 | FIX-3 报告 | 全部 `$2a$` 开头 | ✅ |
| status=1 | FIX-3 报告 | 无 `status != 1` 记录 | ✅ |
| yx_user_role 行数 | FIX-3 报告 | `9 行` | ✅ |
| 验证码状态 | FIX-3 报告 API 验证 | `captchaEnabled: false` | ✅ |
| 学生登录 API | FIX-3 报告 | Token 获取成功 | ✅ |
| 教师登录 API | FIX-3 报告 | Token 获取成功 | ✅ |
| 用户信息接口 | FIX-3 报告 | `roles: ["student"]` 正确 | ✅ |

**关键证据 - 数据库验证:**
```sql
SELECT COUNT(*) FROM yx_user;  -- 结果: 9
SELECT LEFT(password,4) FROM yx_user LIMIT 5;  -- 结果: ['$2a$', '$2a$', '$2a$', '$2a$', '$2a$']
SELECT COUNT(*) FROM yx_user_role;  -- 结果: 9
```

**关键证据 - API 登录验证:**
```bash
# 学生账号 2524010001 / 2524010001
POST http://192.168.100.165:8080/login
Response: {"code":200,"token":"eyJhbGciOiJIUzUxMiJ9..."}

# 教师账号 liang_s_huli_24 / liangshufen
POST http://192.168.100.165:8080/login
Response: {"code":200,"token":"eyJhbGciOiJIUzUxMiJ9..."}
```

---

## 二、结构化验收表（对照 T0 Acceptance Criteria）

| 验收项 | 预期值 | 实测值 | 证据来源 | 状态 |
|--------|--------|--------|----------|------|
| **AC-1: yx_user 学生数据** | 行数 > 0 | 5 行 | FIX-3 报告 | ✅ PASS |
| **AC-1: yx_user 教师数据** | 行数 > 0 | 4 行 | FIX-3 报告 | ✅ PASS |
| **AC-2: password BCrypt 格式** | 全部以 `$2a$` 开头 | 9/9 符合 | FIX-3 报告 | ✅ PASS |
| **AC-3: yx_role student** | id=2 存在 | 存在 | FIX-1 报告 | ✅ PASS |
| **AC-3: yx_role teacher** | id=3 存在 | 存在 | FIX-1 报告 | ✅ PASS |
| **AC-4: yx_user_role 关联** | 学生和教师均有角色 | 9 行关联 | FIX-3 报告 | ✅ PASS |
| **AC-5: 验证码关闭** | `captchaEnabled=false` | `false` | FIX-0/3 报告 | ✅ PASS |
| **AC-6: POST /login 获取 token** | 测试学号+密码成功 | 学生/教师均成功 | FIX-3 报告 | ✅ PASS |
| **AC-7: H5 前端登录** | 手机浏览器登录成功并进入首页 | API 验证通过，前端依赖 APP 部署状态 | FIX-3 报告 | ⚠️ PARTIAL |
| **AC-8: generate_user_data.py 可复用** | AST 通过，可正常执行 | AST OK，--help 正常 | FIX-1 报告 | ✅ PASS |
| **AC-8: fix_and_insert.py 可复用** | AST 通过，bcrypt 调用存在 | AST OK，2处 hash 调用 | FIX-2 报告 | ✅ PASS |

---

## 三、证据路径清单

| 证据类型 | 文件路径 |
|----------|----------|
| FIX-0 验证码关闭证据 | `.tasks/bugfix-login-userdata/fix-0-captcha-disabled/_report.md` |
| FIX-1 脚本修复证据 | `.tasks/bugfix-login-userdata/fix-1-generate-userdata-script/_report.md` |
| FIX-2 兜底脚本证据 | `.tasks/bugfix-login-userdata/fix-2-fix-and-insert-bcrypt/_report.md` |
| FIX-3 部署验证证据 | `.tasks/bugfix-login-userdata/fix-3-deploy-and-e2e-login/_report.md` |
| T0 规格来源 | `.tasks/_spec-bugfix-login-userdata.yaml` |
| 生成脚本产物 | `scripts/insert_students.sql` |
| 生成脚本产物 | `scripts/insert_teachers.sql` |
| 修复后的脚本 | `scripts/generate_user_data.py` |
| 修复后的脚本 | `scripts/fix_and_insert.py` |

---

## 四、最终 L3 语义判定

### 判定结果: **PARTIAL**

### 判定依据:

**✅ 已达成项 (10/11):**
1. 数据库层面：`yx_user` 表 9 行数据（5学生+4教师）✅
2. 密码格式：全部 9 个用户密码以 `$2a$` 开头（BCrypt）✅
3. 角色表：`yx_role` 已初始化 student(id=2) 和 teacher(id=3) ✅
4. 角色关联：`yx_user_role` 9 行关联记录 ✅
5. 用户状态：全部用户 `status=1`（激活）✅
6. 验证码关闭：`captchaEnabled=false` 生效 ✅
7. API 登录：学生账号（2524010001）POST /login 成功获取 token ✅
8. API 登录：教师账号（liang_s_huli_24）POST /login 成功获取 token ✅
9. 用户角色接口：`/getInfo` 正确返回 `roles: ["student"]` ✅
10. 脚本可复用性：`generate_user_data.py` 和 `fix_and_insert.py` 均通过 AST 验证 ✅

**⚠️ 部分达成项 (1/11):**
11. **H5 前端登录验证（手机浏览器）**: API 层已验证通过，但实机 H5 页面访问 `http://192.168.100.165:5174` 需要前端应用（student-app）正确部署后才能完成。

---

## 五、阻塞点与返工建议

### 当前阻塞点
| 阻塞点 | 严重程度 | 说明 |
|--------|----------|------|
| H5 前端实机验证 | LOW | API 已通，需确认 student-app 部署状态 |

### 返工建议
**无需返工** - 登录认证链路的核心阻塞已解除：

1. **数据库层**: 用户数据已正确插入，密码格式符合 BCrypt 要求
2. **API 层**: `/login` 接口已验证可用，JWT Token 正常发放
3. **认证链路**: 从 captcha 验证 → 用户查询 → 密码校验 → Token 生成 全链路畅通

**建议后续操作:**
- 确认 `apps/student-app` 或对应前端服务已部署到 `192.168.100.165:5174`
- 使用手机浏览器访问 `http://192.168.100.165:5174` 完成最终 E2E 验证
- 一旦前端部署完成，AC-7 自动转为 PASS，整体状态可提升为 **PASS**

---

## 六、STEP 汇总

| 步骤 | 内容 | 状态 |
|------|------|------|
| **STEP-PLAN** | 读取 6 份规格/报告文件，提取证据，对照 T0 acceptance_criteria 逐条验证 | ✅ 完成 |
| **STEP-EXECUTED** | 证据提取与结构化汇总，生成验收表 | ✅ 完成 |
| **STEP-CHECK** | 11 项验收标准：10 PASS + 1 PARTIAL | ✅ 完成 |
| **BLOCKERS** | H5 前端验证依赖 APP 部署状态，API 层已验证通过 | ⚠️ 低风险 |

---

## 七、结论

**登录认证 Bugfix 验收状态: PARTIAL**

- 后端认证链路 **已完全修复**
- 数据库用户数据 **已正确部署**
- API 登录接口 **已验证可用**
- H5 前端验证 **待 APP 部署完成后确认**

**放行建议**: 
- 后端开发可解除阻塞，继续进行 spec-v4 相关功能开发
- 前端/H5 验证建议在 24 小时内补充完成
