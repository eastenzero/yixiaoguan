# T3 委托任务：INT-V4-FINAL L2 功能验收

**委托人**: T1-Integrator（窗口 2）  
**执行人**: T3 Executor  
**委托时间**: 2026-04-06  
**优先级**: P0

---

## 任务目标

完成 INT-V4-FINAL 的阶段 2（功能验收 L2），验证以下 AC 的实际功能：
- AC-1: 知识详情页
- AC-3: 会话历史
- AC-4: 统计卡片
- AC-6: 来源弹层 Markdown
- AC-7: Chat 集成
- AC-10: 回归测试

---

## 前置条件

### 测试环境状态 ✅
- PostgreSQL: 运行中（健康）
- Redis: 运行中（健康）
- AI Service: 运行中（entry_count: 1059）
- business-api: 运行中（http://localhost:8080，Terminal ID: 29）
- student-app: 运行中（http://localhost:5175，Terminal ID: 30）

### 阶段 1 完成情况 ✅
- AC-2: 标记为 ⚠️ PASS WITH DEBT（不阻塞发布）
- AC-5: ✅ PASS（快捷问题动态化）
- AC-8: ✅ PASS（KB entry_count = 1059）
- AC-9: ✅ PASS（防幻觉指标达标）
- AC-10: ⚠️ 已知问题（type-check，不阻塞发布）

### 阻塞性问题修复 ✅
- login/index.vue 的 $primary 变量问题已修复（第 297 行改为 #006a64）

---

## 执行步骤

### Step 1: 登录应用

**方法 1（推荐）**: 使用登录状态文件
```powershell
agent-browser state load .secrets/student-login-state.json
agent-browser open http://localhost:5175
```

**方法 2**: 手动登录
```powershell
agent-browser open http://localhost:5175
agent-browser snapshot -i
agent-browser fill @e1 "452357015"  # 学号
agent-browser fill @e2 "123456"     # 密码
agent-browser fill @e3 "1234"       # 验证码（可能已禁用）
# 点击登录按钮
```

**注意**: 根据任务报告，验证码应该已被禁用，但 UI 仍显示验证码字段。如果登录失败，请检查后端配置。

---

### Step 2: 验证 AC-1（知识详情页）

**测试步骤**:
1. 导航到智能问答页面
2. 发送问题："如何申请空教室？"
3. 等待 AI 回复
4. 点击回复中的来源引用（有 entryId 的来源）
5. 验证跳转到知识详情页
6. 验证显示完整条目（标题、正文、标签）

**预期结果**: ✅
- 详情页正确显示
- Markdown 格式正确渲染
- 标签显示正确

**验证命令**:
```powershell
agent-browser snapshot -i
agent-browser get text body
agent-browser screenshot ac1-knowledge-detail.png
```

---

### Step 3: 验证 AC-3（会话历史）

**测试步骤**:
1. 在智能问答页面，点击导航栏"历史记录"按钮（📋 图标）
2. 验证跳转到会话历史页
3. 验证显示历史会话列表（或空状态）
4. 点击"新建对话"按钮
5. 验证创建新会话并跳转到对话页

**预期结果**: ✅
- 历史页功能正常
- UI 与 chat 页面风格统一
- 新建对话功能正常

**验证命令**:
```powershell
agent-browser snapshot -i
agent-browser screenshot ac3-chat-history.png
```

---

### Step 4: 验证 AC-4（统计卡片）

**测试步骤**:
1. 导航到事务导办页面
2. 验证顶部显示统计卡片区域
3. 验证显示"进行中的申请"数量
4. 验证显示"待处理通知"数量（可为 0 或 mock）

**预期结果**: ✅
- 统计卡片正确显示
- 数据获取失败时显示 "--"

**验证命令**:
```powershell
agent-browser snapshot -i
agent-browser screenshot ac4-services-stats.png
```

---

### Step 5: 验证 AC-6（来源弹层 Markdown）

**测试步骤**:
1. 在智能问答页面，发送问题
2. 等待 AI 回复
3. 点击来源引用（无 entryId 的来源，触发弹层）
4. 验证弹层内容 Markdown 正确渲染（粗体、列表、标题等）

**预期结果**: ✅
- 弹层内容格式化显示
- 无原始 Markdown 标记裸露

**验证命令**:
```powershell
agent-browser snapshot -i
agent-browser screenshot ac6-source-preview-markdown.png
```

---

### Step 6: 验证 AC-7（Chat 集成）

**测试步骤**:
1. 在智能问答页面，验证导航栏有"历史记录"按钮
2. 点击历史按钮，验证跳转到历史页
3. 返回对话页，发送问题
4. 点击来源引用（有 entryId），验证跳转到详情页
5. 返回对话页，刷新页面
6. 验证消息从后端恢复（需要 business-api）

**预期结果**: ✅
- 所有集成功能正常工作
- 会话持久化正常

**验证命令**:
```powershell
agent-browser snapshot -i
agent-browser screenshot ac7-chat-integration.png
```

---

### Step 7: 验证 AC-10（回归测试）

**测试步骤**:
1. 登录功能正常
2. 首页个性化问候正常
3. 事务导办功能正常
4. 个人中心功能正常
5. SSE 流式回复正常
6. 复制按钮正常

**预期结果**: ✅
- 所有已有功能无回归

**验证命令**:
```powershell
# 遍历所有主要页面
agent-browser open http://localhost:5175/#/pages/index/index
agent-browser screenshot ac10-home.png
agent-browser open http://localhost:5175/#/pages/services/index
agent-browser screenshot ac10-services.png
agent-browser open http://localhost:5175/#/pages/profile/index
agent-browser screenshot ac10-profile.png
```

---

## 输出要求

### 1. 更新验收报告

在 `.tasks/v4-student-enhancement/int-v4-final/_report.md` 中更新以下内容：

**每个 AC 的验证结果**:
```markdown
### AC-X: [名称]
**状态**: ✅ PASS / ❌ FAIL / ⚠️ PARTIAL

**L2 验证**: [详细结果]
- 测试步骤 1: ✅ / ❌
- 测试步骤 2: ✅ / ❌
- ...

**截图**: ac-x-[描述].png

**问题**（如有）:
- [问题描述]
```

### 2. 记录问题

如发现问题，在报告的"问题清单"中添加：
```markdown
| ISSUE-XX | [描述] | [严重性] | [相关任务] | ⏳ 待修复 | [建议] |
```

### 3. 截图文件

保存所有截图到：`.tasks/v4-student-enhancement/int-v4-final/screenshots/`

---

## 决策点

### 如果登录失败
- 检查 business-api 是否正常运行
- 检查验证码是否真的已禁用
- 尝试使用不同的登录凭据
- 如果无法解决，记录问题并通知 T1

### 如果 AC 验证失败
- 记录详细的失败信息（错误消息、截图）
- 判断严重性（阻塞 / 非阻塞）
- 在报告中标记状态
- 通知 T1 决策是否需要修复

### 如果发现新问题
- 在问题清单中记录
- 判断是否与本次任务相关
- 判断是否阻塞发布

---

## 完成标准

- [ ] 所有 6 个 AC（AC-1, AC-3, AC-4, AC-6, AC-7, AC-10）已验证
- [ ] 验收报告已更新（每个 AC 的 L2 验证结果）
- [ ] 所有截图已保存
- [ ] 问题清单已更新（如有新问题）
- [ ] 通知 T1 验收完成

---

## 参考资料

- 任务文档: `.tasks/v4-student-enhancement/int-v4-final/_task.md`
- 验收报告: `.tasks/v4-student-enhancement/int-v4-final/_report.md`
- T2 验收报告: 
  - `.tasks/v4-student-enhancement/_fc1_t2_verification.md`
  - `.tasks/v4-student-enhancement/_fc2_t2_verification.md`
- 登录凭据: `.secrets/student-login.json`
- 登录状态: `.secrets/student-login-state.json`

---

## 注意事项

1. **端口变化**: student-app 现在运行在 5175（而非 5174），因为 5174 被占用
2. **已修复问题**: login/index.vue 的 $primary 变量已修复，页面应该可以正常加载
3. **已知问题**: type-check 有全局问题，不影响本次验收
4. **技术债**: AC-2 主题色统一未完全完成，但已决策不阻塞发布

---

**委托完成后，请通知 T1-Integrator（窗口 2）！** 🚀
