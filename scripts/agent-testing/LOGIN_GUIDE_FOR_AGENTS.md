# Agent 登录操作指南

## 背景

系统使用验证码防止自动化登录，Agent 无法自动识别验证码。本指南提供两种解决方案。

---

## 方案一：使用预置账号（推荐）

### 可用测试账号

| 角色 | 用户名 | 密码 | 用途 |
|------|--------|------|------|
| 管理员 | `admin` | `admin123` | 全权限测试 |
| 辅导员 | `cao_p_linchuang_21` | `admin123` | 临床学院2021级辅导员 |
| 辅导员 | `cheng_d_linchuang_22` | `admin123` | 临床学院2022级辅导员 |
| 辅导员 | `yu_j_linchuang_23` | `admin123` | 临床学院2023级辅导员 |

### 登录步骤

1. **访问登录页**
   ```
   http://localhost:5173/login
   ```

2. **填写表单**
   - 用户名：`admin`
   - 密码：`admin123`
   - 验证码：任意输入（如 `1234`）

3. **提交登录**
   - 点击"登 录"按钮

4. **验证登录成功**
   - URL 变为 `/dashboard`
   - 页面显示仪表盘内容

---

## 方案二：状态复用（多 Agent 场景）

### 适用场景
- 需要多个 Agent 同时测试
- 避免每个 Agent 都过验证码

### 操作步骤

#### 步骤 1：人工预登录（1次）

由人类操作员执行：
1. 打开浏览器访问 `http://localhost:5173/login`
2. 使用任意账号登录（如 admin/admin123）
3. 登录成功后，导出认证状态：

```javascript
// 在浏览器控制台执行
(function(){
    const authData = {
        token: localStorage.getItem('token'),
        userInfo: localStorage.getItem('userInfo'),
        timestamp: new Date().toISOString()
    };
    console.log(JSON.stringify(authData, null, 2));
    // 复制输出内容
})();
```

#### 步骤 2：保存状态文件

将复制的 JSON 保存为文件：
```bash
# 保存到项目目录
echo '{"token":"Bearer eyJhbG...","userInfo":"{...}"}' > scripts/agent-testing/auth_state.json
```

#### 步骤 3：Agent 加载状态

每个 Agent 启动时加载状态：
```bash
# 加载认证状态并打开系统
agent-browser --session agent_001 --state ./auth_state.json open http://localhost:5173/dashboard

# 验证已登录
agent-browser --session agent_001 get url
# 期望输出: http://localhost:5173/dashboard
```

---

## 方案三：API 直接登录（后端测试）

### 适用场景
- 纯 API 测试，不经过前端页面
- 需要大量账号并发测试

### 登录接口

```bash
# 1. 获取验证码
curl http://localhost:8080/captchaImage
# 返回: {"uuid":"xxx","code":"200","img":"base64..."}

# 2. 执行登录
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123",
    "code": "1",
    "uuid": "从上一步获取"
  }'
# 返回: {"code":200,"msg":"操作成功","data":{"token":"eyJhbG..."}}
```

### 使用 Token

获取 Token 后，在请求头中添加：
```bash
curl http://localhost:8080/api/v1/escalations/pending \
  -H "Authorization: Bearer eyJhbG..."
```

---

## 常见问题

### Q1: 验证码错误
**原因**：验证码有有效期（通常5分钟）  
**解决**：重新获取验证码

### Q2: 账号锁定
**原因**：连续错误登录  
**解决**：联系管理员解锁或等待30分钟

### Q3: Token 过期
**原因**：Token 有效期通常为24小时  
**解决**：重新登录获取新 Token

---

## 测试数据速查

### 学生账号
- 数量：1,232 个
- 用户名：混淆后的学号（如 `4523570155`）
- 密码：与用户名相同
- 分布：22个学院，4个年级

### 辅导员账号
- 数量：50 个
- 命名规则：`姓氏_首字母_学院_年级`
- 密码：`admin123`
- 权限：仅本学院本年级

---

## 快速测试命令

```bash
# 验证后端服务
curl http://localhost:8080/captchaImage

# 验证前端服务
curl http://localhost:5173

# 登录测试（需要替换uuid和code）
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123","code":"xxx","uuid":"xxx"}'
```
