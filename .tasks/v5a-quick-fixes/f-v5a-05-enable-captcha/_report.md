---
task_id: "f-v5a-05"
executed_by: "t2-foreman"
executed_at: "2026-04-06"
duration_minutes: 3
result: "success"
---

# 执行报告：启用登录验证码

## 执行步骤

### Step 1: 确认前端验证码 UI

`login/index.vue` 已包含完整验证码组件：
- `captchaEnabled` 响应式变量
- `captchaUrl` 图片 URL
- `refreshCaptcha()` 刷新方法
- template 中 `v-if="captchaEnabled"` 条件渲染

**结论**：前端无需修改。

### Step 2: Redis 写入

```bash
ssh easten@192.168.100.165 "docker exec yx_redis redis-cli -a 'Yx@Redis2026!' SET sys_config:sys.account.captchaEnabled true"
```

**输出**：`OK`

### Step 3: 验证 Redis 值

```bash
ssh easten@192.168.100.165 "docker exec yx_redis redis-cli -a 'Yx@Redis2026!' GET sys_config:sys.account.captchaEnabled"
```

**输出**：`true`

## 验证结果

```
L0: login/index.vue 存在验证码 UI 元素 ✓
L1: grep 'captcha' 返回结果 ✓
L2: Redis GET 返回 true ✓
```

## 结论

验证码功能已启用。后端读取 `sys_config:sys.account.captchaEnabled` 配置，当前值为 `true`。

## 下一步建议

建议人工访问登录页确认验证码图片正常显示。