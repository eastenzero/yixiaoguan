# Agent Teams 测试认证指南

## 问题：为什么登录难？

系统使用验证码防止自动化，Agent 难以识别图片验证码。

## 解决方案：状态复用

**核心思路**：人工登录一次 → 保存认证状态 → 所有 Agent 复用该状态

---

## 步骤 1：人工获取认证 Token

### 方法 A：浏览器开发者工具（推荐）

1. 打开浏览器访问 `http://localhost:5173/login`
2. 使用账号登录：
   - 辅导员账号：`cao_p_linchuang_23`
   - 密码：`caopeng`
3. 登录成功后，按 F12 打开开发者工具
4. 进入 Application → Local Storage → `http://localhost:5173`
5. 找到 `token` 字段，复制值（格式如：`Bearer eyJhbG...`）

### 方法 B：API 直接获取（需要验证码豁免）

联系后端开发临时关闭验证码，然后：
```bash
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username":"cao_p_linchuang_23","password":"caopeng","code":"1","uuid":"test"}'
```

---

## 步骤 2：保存认证状态

### 方式 1：agent-browser 状态文件（推荐）

```bash
# 1. 使用获取的 token 创建状态文件
agent-browser --session yixiaoguan_auth open http://localhost:5173

# 2. 在浏览器控制台执行：
# localStorage.setItem('token', 'Bearer eyJhbG...')

# 3. 保存状态
agent-browser --session yixiaoguan_auth state save ./auth_state.json
```

### 方式 2：直接操作 localStorage

创建 `inject_auth.js`：
```javascript
// 在浏览器控制台执行
localStorage.setItem('token', '你的Token');
localStorage.setItem('userInfo', JSON.stringify({
  id: 2001,
  username: 'cao_p_linchuang_23',
  realName: '曹鹏',
  userType: 'teacher'
}));
```

---

## 步骤 3：Agent 复用认证状态

### 启动 Agent 时加载状态

```bash
# 每个 Agent 启动时先加载认证状态
agent-browser --session agent_001 --state ./auth_state.json open http://localhost:5173/dashboard

# 现在 Agent 已登录，直接测试业务
agent-browser --session agent_001 snapshot -i
```

---

## 快速测试脚本

### `test_with_auth.sh` (Bash)

```bash
#!/bin/bash

# 配置
AUTH_STATE="./auth_state.json"
BASE_URL="http://localhost:5173"

# 函数：带认证的 Agent 操作
agent_test() {
    local session_name=$1
    local action=$2
    
    case $action in
        "login")
            agent-browser --session $session_name --state $AUTH_STATE open "$BASE_URL/dashboard"
            ;;
        "questions")
            agent-browser --session $session_name open "$BASE_URL/questions"
            agent-browser --session $session_name wait --load networkidle
            agent-browser --session $session_name snapshot -i
            ;;
        "approval")
            agent-browser --session $session_name open "$BASE_URL/approval"
            agent-browser --session $session_name wait --load networkidle
            agent-browser --session $session_name snapshot -i
            ;;
    esac
}

# 测试示例
agent_test "agent_001" "login"
agent_test "agent_001" "questions"
```

### `test_with_auth.ps1` (PowerShell)

```powershell
# 配置
$AuthState = "./auth_state.json"
$BaseUrl = "http://localhost:5173"

function Test-WithAuth {
    param(
        [string]$SessionName,
        [string]$Action
    )
    
    switch ($Action) {
        "login" {
            agent-browser --session $SessionName --state $AuthState open "$BaseUrl/dashboard"
        }
        "questions" {
            agent-browser --session $SessionName open "$BaseUrl/questions"
            agent-browser --session $SessionName wait --load networkidle
            agent-browser --session $SessionName snapshot -i
        }
        "approval" {
            agent-browser --session $SessionName open "$BaseUrl/approval"
            agent-browser --session $SessionName wait --load networkidle
            agent-browser --session $SessionName snapshot -i
        }
    }
}

# 测试
Test-WithAuth "agent_001" "login"
Test-WithAuth "agent_001" "questions"
```

---

## 备用方案：Mock 登录 API

如果后端支持，可以临时添加一个测试专用的免验证码登录接口：

```java
// 后端添加测试接口（仅开发环境）
@PostMapping("/test-login")
public AjaxResult testLogin(@RequestBody LoginBody loginBody) {
    // 跳过验证码验证
    return loginService.login(loginBody.getUsername(), loginBody.getPassword());
}
```

然后 Agent 使用 `/test-login` 接口获取 Token。

---

## 当前推荐的测试流程

### 阶段 1：人工准备（1次）
1. 人工登录系统
2. 导出 localStorage 中的 token
3. 创建 `auth_state.json`

### 阶段 2：Agent 测试（可重复）
1. 每个 Agent 加载 `auth_state.json`
2. 直接访问业务页面（跳过登录）
3. 执行业务操作测试

---

## 工具脚本

### `extract_token.js`

在浏览器控制台执行，导出当前登录状态：

```javascript
(function(){
    const data = {
        token: localStorage.getItem('token'),
        userInfo: localStorage.getItem('userInfo'),
        timestamp: new Date().toISOString()
    };
    console.log(JSON.stringify(data, null, 2));
    // 复制输出保存为 auth_state.json
})();
```

---

## 常见问题

### Q: Token 过期了怎么办？
A: Token 默认有效期通常 24小时，过期后需要重新人工登录获取。

### Q: 需要测试不同角色的权限？
A: 准备多个状态文件：
- `auth_admin.json` - 管理员
- `auth_teacher.json` - 辅导员
- `auth_student.json` - 学生

### Q: 如何验证 Agent 已登录？
A: 检查页面 URL 或元素：
```bash
agent-browser --session agent_001 get url
# 期望输出: http://localhost:5173/dashboard (不是 /login)
```
