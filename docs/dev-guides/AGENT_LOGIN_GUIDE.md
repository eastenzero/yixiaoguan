# Agent 登录测试指南

> **最后更新**: 2026-04-02  
> **测试账号**: 4523570155 / admin123 (学生账号)  
> **适用系统**: 医小管 - 学术智治系统 (教师端)

---

## 一、前置条件

### 1. 开发服务器启动

确保以下服务已正常运行：

```bash
# 前端服务 (端口 5173)
cd apps/teacher-web
npm run dev

# 后端服务 (端口 8080)
cd services/business-api
# 使用 IDEA 或 mvn spring-boot:run 启动
```

### 2. 测试账号信息

| 账号类型 | 用户名 | 密码 | 角色 |
|---------|--------|------|------|
| 学生账号 | 4523570155 | admin123 | 学生 |
| 辅导员账号 | cao_p_linchuang_21 | admin123 | 辅导员 |
| 管理员账号 | admin | admin123 | 管理员 |

---

## 二、登录步骤详解

### 方法 1: 标准登录流程 (含验证码)

```powershell
# Step 1: 打开登录页面
npx agent-browser open http://localhost:5173/#/login

# Step 2: 获取页面元素快照
npx agent-browser snapshot -i
# 输出示例:
# - heading "学术智治系统" [level=1, ref=e2]
# - textbox "请输入用户名" [ref=e6]
# - textbox "请输入密码" [ref=e7]
# - textbox "请输入验证码" [ref=e8]
# - button "登 录" [ref=e4]

# Step 3: 填写用户名 (使用单引号避免 PowerShell 解析 @)
npx agent-browser fill '@e6' '4523570155'

# Step 4: 填写密码
npx agent-browser fill '@e7' 'admin123'

# Step 5: 截图查看验证码
npx agent-browser screenshot --full
# 验证码类型: 数学表达式 (如 2*9=?)

# Step 6: 填写验证码答案
npx agent-browser fill '@e8' '18'  # 根据实际验证码填写

# Step 7: 点击登录按钮
npx agent-browser click '@e4'

# Step 8: 验证登录成功
npx agent-browser get url
# 期望输出: http://localhost:5173/dashboard
```

### 方法 2: 使用已保存的登录状态

如果之前已保存登录状态，可以直接恢复：

```powershell
# 加载保存的登录状态
npx agent-browser state load '.secrets/login-state.json'
npx agent-browser open http://localhost:5173/#/dashboard

# 验证登录状态
npx agent-browser get url
# 应显示: http://localhost:5173/dashboard
```

### 方法 3: 使用 Session 名称自动保存

```powershell
# 首次登录 (使用 --session-name 自动保存状态)
npx agent-browser --session-name yixiaoguan open http://localhost:5173/#/login
# ... 执行登录流程 ...
npx agent-browser close  # 状态自动保存

# 后续使用 (自动恢复状态)
npx agent-browser --session-name yixiaoguan open http://localhost:5173/#/dashboard
```

---

## 三、验证码处理方法

### 验证码类型识别

系统使用数学表达式验证码，格式为: `数字*数字=?`

**识别技巧**:
1. 截图后仔细观察蓝色扭曲文字
2. 格式为 `a*b=?` 或 `a*b=` (a, b 为个位数)
3. 计算结果并输入纯数字答案

**示例**:
- 看到 `2*9=?` → 输入 `18`
- 看到 `3*7=?` → 输入 `21`
- 看到 `5+3=?` → 输入 `8`

### 如果验证码识别困难

```powershell
# 方法 1: 使用 headed 模式 (可视化窗口)
npx agent-browser --headed open http://localhost:5173/#/login

# 方法 2: 保存验证码图片单独识别
npx agent-browser eval "
const img = document.querySelector('.captcha-img img');
if (img) console.log(img.src);  // 获取 base64 图片数据
"
```

---

## 四、常见问题与解决

### 问题 1: PowerShell 中 @ 符号解析错误

**错误信息**:
```
The variable '$e6' cannot be retrieved because it has not been set.
```

**解决方案**:
使用单引号包裹 ref:
```powershell
npx agent-browser fill '@e6' '4523570155'  # ✅ 正确
npx agent-browser fill @e6 "4523570155"     # ❌ 错误
```

### 问题 2: 验证码过期/错误

**现象**: 点击登录后仍停留在登录页

**解决方案**:
1. 重新截图获取新验证码
2. 确保在验证码刷新后 30 秒内完成输入
3. 验证码为数学表达式，注意计算正确

### 问题 3: Ref 失效

**现象**: `Unknown ref: e6`

**解决方案**:
页面 DOM 变化后需要重新获取 snapshot:
```powershell
npx agent-browser snapshot -i  # 重新获取最新的 refs
```

### 问题 4: 无法连接服务器

**错误信息**:
```
net::ERR_CONNECTION_REFUSED
```

**解决方案**:
1. 检查前端服务是否启动 `npm run dev`
2. 检查后端服务是否启动
3. 确认 URL 正确: `http://localhost:5173/#/login`

---

## 五、会话保持方法

### 保存登录状态

```powershell
# 登录成功后保存状态
npx agent-browser state save '.secrets/my-login.json'
```

### 恢复登录状态

```powershell
# 下次直接恢复
npx agent-browser state load '.secrets/my-login.json'
npx agent-browser open http://localhost:5173/#/dashboard
```

### 验证登录状态

```powershell
# 检查 localStorage 中的 token
npx agent-browser eval "localStorage.getItem('token')"

# 检查 Cookie
npx agent-browser eval "document.cookie"
```

---

## 六、验证登录成功的方法

### 方法 1: 检查 URL

```powershell
npx agent-browser get url
# 登录前: http://localhost:5173/login
# 登录后: http://localhost:5173/dashboard
```

### 方法 2: 检查页面元素

```powershell
npx agent-browser snapshot -i
# 登录成功后会看到:
# - heading "工作台概览" [level=1, ref=e1]
# - link "学生提问" [ref=e5]
# - link "空教室审批" [ref=e6]
```

### 方法 3: 检查 localStorage

```powershell
npx agent-browser eval "localStorage.getItem('token')"
# 登录成功后应返回 JWT token 字符串
```

---

## 七、完整登录脚本模板

```powershell
# 医小管系统自动登录脚本
# 用法: 复制到 PowerShell 执行

$USERNAME = "4523570155"
$PASSWORD = "admin123"
$LOGIN_URL = "http://localhost:5173/#/login"

Write-Host "Step 1: 打开登录页面..."
npx agent-browser open $LOGIN_URL
Start-Sleep -Seconds 2

Write-Host "Step 2: 获取页面元素..."
$SNAPSHOT = npx agent-browser snapshot -i 2>&1

Write-Host "Step 3: 填写用户名..."
npx agent-browser fill '@e6' $USERNAME

Write-Host "Step 4: 填写密码..."
npx agent-browser fill '@e7' $PASSWORD

Write-Host "Step 5: 请查看验证码..."
npx agent-browser screenshot --annotate
$CAPTCHA = Read-Host "请输入验证码答案 (数学表达式结果)"

Write-Host "Step 6: 填写验证码..."
npx agent-browser fill '@e8' $CAPTCHA

Write-Host "Step 7: 点击登录..."
npx agent-browser click '@e4'

Start-Sleep -Seconds 3

Write-Host "Step 8: 验证登录结果..."
$URL = npx agent-browser get url 2>&1
if ($URL -like "*/dashboard") {
    Write-Host "✅ 登录成功! URL: $URL" -ForegroundColor Green
    
    # 保存登录状态
    npx agent-browser state save '.secrets/login-state.json'
    Write-Host "✅ 登录状态已保存" -ForegroundColor Green
} else {
    Write-Host "❌ 登录失败,当前 URL: $URL" -ForegroundColor Red
}
```

---

## 八、相关文件

| 文件 | 说明 |
|------|------|
| `.secrets/login-state.json` | 保存的登录状态 |
| `docs/test-reports/PENDING_ISSUES_REPORT.md` | 系统问题汇总 |

---

## 九、注意事项

1. **验证码刷新**: 每次点击登录失败后，验证码会自动刷新
2. **会话超时**: 登录状态通常保持 24 小时，超时后需要重新登录
3. **端口占用**: 确保 5173 和 8080 端口未被其他程序占用
4. **状态文件安全**: `.secrets/login-state.json` 包含敏感信息，已添加到 `.gitignore`
