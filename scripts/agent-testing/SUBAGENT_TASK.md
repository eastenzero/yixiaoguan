# Subagent 测试任务说明

## 前置条件（必须完成）

由于登录有验证码，Subagent 无法自动完成登录。需要你先人工准备认证状态。

## 准备步骤

### 1. 人工登录获取 Token

打开浏览器，访问：`http://localhost:5173/login`

使用以下账号登录：
```
用户名: cao_p_linchuang_23
密码: caopeng
```

### 2. 导出 Token

登录成功后，在浏览器控制台（F12）执行：

```javascript
(function(){
    const token = localStorage.getItem('token');
    const userInfo = localStorage.getItem('userInfo');
    const data = { token, userInfo, timestamp: new Date().toISOString() };
    console.log(JSON.stringify(data, null, 2));
})();
```

复制输出的 JSON，保存为 `scripts/agent-testing/auth_state.json`

### 3. 验证状态文件

```bash
cd scripts/agent-testing
ls -la auth_state.json
```

确认文件存在且大小 > 100 bytes。

---

## Subagent 任务分配

### Agent 1：核心业务流验证

**任务**：验证三大业务页面是否正常加载

```powershell
# 执行精简验证脚本
cd scripts/agent-testing
.\quick_test.ps1
```

**期望结果**：
- ✅ 登录成功（无需验证码）
- ✅ 学生提问页面显示数据
- ✅ 空教室审批页面显示数据
- ✅ 知识库页面显示数据
- ✅ 4 张截图文件生成

**成功标准**：4/4 页面正常加载

---

### Agent 2：提问工单操作

**任务**：模拟辅导员处理提问工单

```powershell
# 步骤 1：加载认证状态
agent-browser --session agent2 --state ./auth_state.json open http://localhost:5173/questions

# 步骤 2：截图查看列表
agent-browser --session agent2 screenshot --full ./agent2_list.png

# 步骤 3：点击第一个工单（如果有）
# agent-browser --session agent2 click @e??  # 根据 snapshot 结果

# 步骤 4：截图详情页
agent-browser --session agent2 screenshot --full ./agent2_detail.png
```

**期望结果**：
- 提问列表有数据（>0条）
- 能进入工单详情
- 截图证明流程通顺

---

### Agent 3：空教室审批操作

**任务**：模拟辅导员审批教室申请

```powershell
# 步骤 1：加载认证状态
agent-browser --session agent3 --state ./auth_state.json open http://localhost:5173/approval

# 步骤 2：截图查看待审批列表
agent-browser --session agent3 screenshot --full ./agent3_list.png

# 步骤 3：选中第一个申请
# agent-browser --session agent3 click @e??

# 步骤 4：截图详情
agent-browser --session agent3 screenshot --full ./agent3_detail.png
```

**期望结果**：
- 待审批列表有数据
- 能查看申请详情
- 审批按钮可操作

---

## 失败处理

如果某个 Agent 失败：

1. **检查认证状态**
   ```powershell
   agent-browser --session agentX get url
   # 如果显示 /login，说明状态失效，需要重新人工登录
   ```

2. **检查服务状态**
   ```powershell
   curl http://localhost:5173
   curl http://localhost:8080
   ```

3. **重置 Agent 会话**
   ```powershell
   agent-browser --session agentX close
   # 重新执行
   ```

---

## 测试结果汇总

所有 Agent 完成后，请提交：

1. 各 Agent 的截图文件
2. 成功/失败标记
3. 遇到的问题描述

---

## 提示

- 认证状态（auth_state.json）有效期约 24 小时
- 如果过期，需要重新人工登录获取
- 多个 Agent 可以共用同一个状态文件
