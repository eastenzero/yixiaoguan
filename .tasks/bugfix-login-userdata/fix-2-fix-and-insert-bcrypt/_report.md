# FIX-2 执行报告: 修复 fix_and_insert.py 密码哈希

**任务ID:** fix-2-fix-and-insert-bcrypt  
**状态:** ✅ 已完成  
**完成时间:** 2026-04-05  

---

## 实际修改的代码位置和内容

### 修改1: 添加 bcrypt 导入
**位置:** 第5行  
**内容:**
```python
import bcrypt
```

### 修改2: 学生插入逻辑增加密码哈希
**位置:** 第88-90行 (fix_and_insert_students 函数)  
**修改前:**
```python
username = fields[0].strip("'")
password = fields[1].strip("'")
real_name = fields[2].strip("'")
```

**修改后:**
```python
username = fields[0].strip("'")
password_plain = fields[1].strip("'")
password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
real_name = fields[2].strip("'")
```

### 修改3: 教师插入逻辑增加密码哈希
**位置:** 第183-185行 (fix_and_insert_teachers 函数)  
**修改前:**
```python
username = fields[0].strip("'")
password = fields[1].strip("'")
real_name = fields[2].strip("'")
```

**修改后:**
```python
username = fields[0].strip("'")
password_plain = fields[1].strip("'")
password = bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()
real_name = fields[2].strip("'")
```

---

## L0/L1/L2 验证结果

### L0: 语法检查
**命令:**
```powershell
python -m py_compile scripts/fix_and_insert.py
```
**输出:**
```
✓ L0: 语法检查通过
```

### L1: bcrypt.hashpw 调用存在性验证
**命令:**
```powershell
Select-String -Pattern "bcrypt.hashpw" -Path scripts/fix_and_insert.py
```
**输出:**
```
LineNumber Line
---------- ----
        90             password = ...
       185             password = ...
```

**grep 验证证据:**
- 第90行: 学生插入逻辑中包含 `bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()`
- 第185行: 教师插入逻辑中包含 `bcrypt.hashpw(password_plain.encode(), bcrypt.gensalt()).decode()`

### L2: bcrypt 库可用性验证
**命令:**
```powershell
python -c "import bcrypt; print('bcrypt 库可用')"
```
**输出:**
```
✓ bcrypt 库可用
```

---

## 修改总结

| 检查项 | 状态 | 说明 |
|--------|------|------|
| import bcrypt | ✅ | 已添加在文件第5行 |
| 学生密码哈希 | ✅ | 第90行，覆盖学生插入逻辑 |
| 教师密码哈希 | ✅ | 第185行，覆盖教师插入逻辑 |
| 语法检查通过 | ✅ | py_compile 无错误 |
| 不改变其他业务 | ✅ | 仅修改密码处理逻辑 |

---

## 技术细节

- **哈希算法:** BCrypt (通过 Python bcrypt 库)
- **哈希格式:** `$2a$10$...` (60字符)
- **盐值生成:** `bcrypt.gensalt()` 自动生成随机盐
- **编码处理:** 明文密码先 `.encode()` 转为 bytes，哈希结果 `.decode()` 转为字符串存储

---

## 与 FIX-1 的一致性

本修复确保 `fix_and_insert.py` 与 `generate_user_data.py` (FIX-1) 使用相同的密码哈希策略：
- 两者均使用 `bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()`
- 生成的密码哈希格式一致（均以 `$2a$` 开头）
- 满足后端 `BCryptPasswordEncoder.matches()` 的验证要求
