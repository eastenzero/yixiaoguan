# 165 服务器 5174 端口调查报告

**调查时间**: 2026-04-06  
**执行者**: T2 (Kiro)  
**调查方式**: 只读探查，无任何修改

---

## 调查结果

### 端口信息

**端口**: 5174  
**状态**: LISTEN  
**进程**: MainThread (pid=2821522)  
**用户**: easten

### 进程详情

**完整命令**:
```bash
node /home/easten/dev/yixiaoguan/apps/student-app/node_modules/.bin/uni -p h5
```

**进程类型**: uni-app H5 开发服务器  
**启动时间**: 2026-04-05  
**CPU 时间**: 0:33  
**内存占用**: 321.6 MB

### 服务功能

**服务名称**: student-app Vite 开发服务器  
**框架**: uni-app + Vite  
**用途**: 学生端 H5 应用开发调试

**配置文件**: `apps/student-app/vite.config.ts`
```typescript
server: {
  port: 5174,
  host: true,
  proxy: {
    '/api/login': { target: 'http://localhost:8080' },
    '/api/chat': { target: 'http://localhost:8000' },
    '/api': { target: 'http://localhost:8080' }
  }
}
```

### HTTP 访问

**URL**: http://192.168.100.165:5174/  
**状态码**: 200 OK  
**认证**: 无（开发服务器，无独立认证）

---

## 账号密码情况

### 结论

**5174 端口本身无账号密码**

**原因**:
1. 这是 Vite 开发服务器，不是独立应用
2. 无独立认证系统
3. 访问控制依赖后端服务（8080 和 8000）

### 相关认证

如需访问学生端功能，需要：

1. **后端认证** (localhost:8080)
   - 登录端点：`/api/login`
   - 验证码：`/api/captchaImage`
   - 用户信息：`/api/getInfo`

2. **测试账号** (如有)
   - 位置：可能在 `.secrets/` 目录
   - 文件：`student-login.json` 或类似

让我检查一下：

---

## 补充调查：测试账号

### 检查 .secrets 目录

**发现文件**:
- `.secrets/student-login.json` - 浏览器状态（token）
- `.secrets/student-login-state.json` - 浏览器状态
- `.secrets/login-state.json` - 浏览器状态

### 测试账号信息

**来源**: `docs/dev-guides/AGENT_LOGIN_GUIDE.md`

| 账号类型 | 用户名 | 密码 | 角色 |
|---------|--------|------|------|
| 学生账号 | 4523570155 | admin123 | 学生 |

**使用方式**:
1. 访问 http://192.168.100.165:5174/
2. 输入用户名：4523570155
3. 输入密码：admin123
4. 输入验证码（数学表达式）
5. 点击登录

---

## 总结

### 5174 端口

**服务类型**: Vite 开发服务器（uni-app H5）  
**认证方式**: 无独立认证，依赖后端 API  
**访问方式**: 直接访问，无需账号密码

### 测试账号

**用户名**: 4523570155  
**密码**: admin123  
**用途**: 学生端功能测试

### 注意事项

1. 5174 是开发服务器，生产环境不使用此端口
2. 测试账号仅用于开发测试，不是真实学生数据
3. 登录需要验证码（数学表达式，如 1+1=?）

---

**T2 签收**: ✅ 调查完成，测试账号已找到
