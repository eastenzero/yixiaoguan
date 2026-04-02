# Agent 认证状态复用方案

> **适用对象**: AI Agent / Subagent  
> **系统**: 医小管 (YiXiaoGuan)  
> **更新日期**: 2026-04-02

---

## 一、为什么需要状态复用

医小管系统的认证流程具有以下特点：

| 特性 | 说明 | 影响 |
|-----|------|------|
| 验证码验证 | 登录需要输入图形验证码 | AI 无法自动完成 |
| 会话保持 | 登录后使用 JWT Token + Session | 可以复用 |
| Token 有效期 | 通常 24 小时 | 需要定期重新登录 |

**核心问题**: 每次新开 subagent 或新 session 都需要重新走登录流程，包含人工输入验证码的步骤，效率极低。

**解决方案**: 使用 agent-browser 的状态复用功能，一次登录，多次复用。

---

## 二、agent-browser 状态复用方案

### 方案 1: Session Name（最简单，推荐）

使用 `--session-name` 参数让 agent-browser 自动管理状态。

```bash
# ========== 首次创建 Session ==========
# 1. 打开浏览器（指定 session 名称）
agent-browser --session-name yxg-student open http://localhost:5174

# 2. 人工完成登录流程
#    - 输入账号: 4523570155
#    - 输入密码: admin123
#    - 人工输入验证码
#    - 点击登录

# 3. 登录成功后关闭（状态自动保存）
agent-browser close

# ========== 后续任意次数复用 ==========
# 直接打开（自动处于登录状态）
agent-browser --session-name yxg-student open http://localhost:5174/pages/chat/index

# 其他页面同理
agent-browser --session-name yxg-student open http://localhost:5174/pages/home/index
agent-browser --session-name yxg-student open http://localhost:5174/pages/knowledge/index
```

**工作原理**:
- agent-browser 会在本地存储每个 session 的浏览器状态
- 包括 cookies、localStorage、sessionStorage、IndexedDB
- 下次使用相同 session-name 时自动恢复

---

### 方案 2: Profile 模式

使用 `--profile` 参数指定持久化的浏览器配置文件。

```bash
# ========== 首次运行 ==========
# 使用指定 profile 目录
agent-browser --profile ~/.yxg-profile open http://localhost:5174

# 人工完成登录
# ...

# 关闭浏览器
agent-browser close

# ========== 后续运行 ==========
# 使用同一 profile，自动保持登录
agent-browser --profile ~/.yxg-profile open http://localhost:5174
```

**与 Session Name 的区别**:
| 特性 | Session Name | Profile |
|-----|--------------|---------|
| 存储位置 | agent-browser 管理 | 用户指定目录 |
| 适用范围 | 跨命令复用 | 完全独立的浏览器环境 |
| 推荐场景 | 普通测试 | 需要完全隔离的环境 |

---

### 方案 3: State 文件（最灵活）

显式保存和加载状态文件，适合需要版本控制或多环境共享的场景。

```bash
# ========== 保存状态 ==========
# 1. 登录后保存状态
agent-browser state save ./auth/yixiaoguan-student.json

# 2. 关闭浏览器
agent-browser close

# ========== 加载状态 ==========
# 1. 加载之前保存的状态
agent-browser state load ./auth/yixiaoguan-student.json

# 2. 打开网站（自动登录）
agent-browser open http://localhost:5174

# ========== 多环境共享 ==========
# 将状态文件提交到仓库，其他环境可直接使用
agent-browser state load ./auth/yixiaoguan-student.json
agent-browser open http://localhost:5174
```

**状态文件内容示例**:
```json
{
  "cookies": [
    {
      "name": "token",
      "value": "eyJhbGciOiJIUzI1NiIs...",
      "domain": "localhost",
      "path": "/"
    }
  ],
  "origins": [
    {
      "origin": "http://localhost:5174",
      "localStorage": [
        { "name": "userInfo", "value": "{...}" }
      ]
    }
  ]
}
```

---

## 三、多角色测试配置

在医小管系统中，不同角色有不同的权限和功能。建议为每个角色创建独立的 session。

### 推荐的 Session 配置

| 角色 | Session Name | 账号 | State 文件 |
|-----|--------------|------|-----------|
| 学生 | `yxg-student` | 4523570155 | `./auth/student.json` |
| 辅导员 | `yxg-teacher` | cao_p_linchuang_21 | `./auth/teacher.json` |
| 管理员 | `yxg-admin` | admin | `./auth/admin.json` |

### 快速切换脚本示例

```bash
#!/bin/bash
# yxg-login.sh - 快速切换角色

ROLE=$1

if [ "$ROLE" = "student" ]; then
    agent-browser --session-name yxg-student open http://localhost:5174
elif [ "$ROLE" = "teacher" ]; then
    agent-browser --session-name yxg-teacher open http://localhost:5174
elif [ "$ROLE" = "admin" ]; then
    agent-browser --session-name yxg-admin open http://localhost:5174
else
    echo "用法: ./yxg-login.sh [student|teacher|admin]"
fi
```

---

## 四、验证登录状态

在使用保存的 session 或加载状态后，应该验证是否真正处于登录状态。

### 方法 1: 检查 URL

```bash
agent-browser get url
```

**预期结果**:
- ✅ 已登录: `http://localhost:5174/pages/home/index` 或其他内页
- ❌ 未登录: `http://localhost:5174`（跳转回登录页）

### 方法 2: 检查页面内容

```bash
agent-browser snapshot -i
```

查看截图或文本输出：
- ✅ 已登录: 显示用户信息、菜单导航
- ❌ 未登录: 显示登录表单、验证码输入框

### 方法 3: 检查 LocalStorage

```bash
agent-browser evaluate "localStorage.getItem('token')"
```

**预期结果**:
- ✅ 已登录: 返回 JWT token 字符串
- ❌ 未登录: 返回 `null`

### 自动化验证脚本

```bash
# verify-auth.sh - 验证登录状态

URL=$(agent-browser get url)
if echo "$URL" | grep -q "/login\|/pages/index"; then
    echo "❌ 未登录或已过期"
    exit 1
else
    echo "✅ 已登录: $URL"
    exit 0
fi
```

---

## 五、故障排除

### Session 过期怎么办

**现象**: 复用 session 后被重定向到登录页

**原因**: Token 过期或 Session 被服务器清除

**解决**:
```bash
# 1. 删除过期 session
agent-browser session delete yxg-student

# 2. 重新登录（首次登录流程）
agent-browser --session-name yxg-student open http://localhost:5174
# ... 人工输入验证码完成登录 ...
agent-browser close

# 3. 后续可正常复用
agent-browser --session-name yxg-student open http://localhost:5174/pages/chat/index
```

### 如何清除状态重新登录

```bash
# 删除指定 session
agent-browser session delete yxg-student

# 或者删除所有 sessions
agent-browser session list
agent-browser session delete --all

# 如果使用 state 文件，直接删除文件
rm ./auth/yixiaoguan-student.json
```

### 验证码刷新问题

**现象**: 验证码图片加载失败或不显示

**解决**:
```bash
# 刷新页面重新加载验证码
agent-browser reload

# 或者点击"换一张"按钮
agent-browser click "text='换一张'"
```

### Session 冲突

**现象**: 多个 agent 同时使用同一个 session name

**解决**: 为每个 agent 使用独立的 session name
```bash
# Agent 1
agent-browser --session-name yxg-student-1 open http://localhost:5174

# Agent 2
agent-browser --session-name yxg-student-2 open http://localhost:5174
```

---

## 六、最佳实践

### 1. 首次登录流程标准化

```bash
# init-session.sh - 初始化所有角色的 sessions

echo "=== 初始化学生 Session ==="
agent-browser --session-name yxg-student open http://localhost:5174
echo "请人工完成学生账号登录..."
read -p "按回车继续..."
agent-browser close

echo "=== 初始化辅导员 Session ==="
agent-browser --session-name yxg-teacher open http://localhost:5174
echo "请人工完成辅导员账号登录..."
read -p "按回车继续..."
agent-browser close

echo "=== 初始化管理员 Session ==="
agent-browser --session-name yxg-admin open http://localhost:5174
echo "请人工完成管理员账号登录..."
read -p "按回车继续..."
agent-browser close

echo "=== 所有 Session 初始化完成 ==="
```

### 2. 定期更新 Session

建议每天或每次长时间测试前更新 session：

```bash
# 检查 session 是否有效
if ! agent-browser --session-name yxg-student get url | grep -q "home"; then
    echo "Session 已过期，需要重新登录"
    agent-browser session delete yxg-student
    # ... 重新登录流程
fi
```

### 3. 文档化 Session 信息

在团队内共享 session 配置：

```markdown
## 可用 Session

| Session Name | 角色 | 最后更新 | 状态 |
|-------------|------|---------|------|
| yxg-student | 学生 | 2026-04-02 | ✅ 有效 |
| yxg-teacher | 辅导员 | 2026-04-02 | ✅ 有效 |
| yxg-admin | 管理员 | 2026-04-02 | ⚠️ 待更新 |
```

---

## 七、总结

| 方案 | 复杂度 | 推荐场景 |
|-----|-------|---------|
| Session Name | ⭐ 低 | 大多数测试场景，强烈推荐 |
| Profile 模式 | ⭐⭐ 中 | 需要完全隔离的浏览器环境 |
| State 文件 | ⭐⭐⭐ 高 | 需要版本控制或多环境共享 |

**核心原则**: 一次人工登录，多次自动复用，避免重复输入验证码。

---

**相关文档**: [AGENT_LOGIN_GUIDE.md](./AGENT_LOGIN_GUIDE.md) - 登录测试操作指南
