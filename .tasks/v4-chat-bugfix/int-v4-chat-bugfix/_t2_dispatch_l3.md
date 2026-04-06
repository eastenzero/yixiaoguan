---
from: T1
to: T2
task: int-v4-chat-bugfix
dispatch_type: L3 补充验收
issued_at: 2026-04-06
status: open
---

# T2 派发：int-v4-chat-bugfix L3 补充验收

## 背景

前序自动化验收（`_report.md`）结论为 **PARTIAL**。以下 4 个 AC 项未达到 PASS 状态，本次派发要求 T2 完成这 4 项的人工 L3 验收并回填最终结论。

## 前置条件

执行前必须确认以下条件满足，否则标注 BLOCKED 并立即回传：

- [ ] `student-app` H5 开发服务已运行（端口 5174）
- [ ] `business-api` 后端服务已运行（端口 8080）
- [ ] `ai-service` AI 服务已运行（端口 8000）

如 `business-api` 无法启动，AC-6 保持 BLOCKED，其余项继续验收。

---

## 验收任务清单

### AC-2：Chat 页面 Markdown 渲染样式（MARGINAL → 目标 PASS）

**操作步骤：**
1. H5 打开 `http://localhost:5174`，登录后进入 chat 页面
2. 发送消息：`请介绍一下学校图书馆的借阅规则`（或任意触发 Markdown 回复的问题）
3. 等待 AI 回复，目视检查回复气泡内容

**通过标准：**
- 回复气泡内 `**加粗**` 文字渲染为 **粗体**（非原始星号）
- `# 标题` 渲染为标题字号（非原始 `#` 字符）
- 列表项渲染为带缩进的列表（非 `- ` 前缀字面量）
- 代码块有背景色区分

**证据要求：** 截图保存至 `.tasks/v4-chat-bugfix/int-v4-chat-bugfix/ac2-chat-markdown.png`

---

### AC-3：Chat 页面无双层导航栏（PENDING → 目标 PASS）

**操作步骤：**
1. H5 打开 chat 页面
2. 目视检查页面顶部导航区域

**通过标准：**
- 顶部仅显示一套导航栏（chat 页面自定义导航栏）
- 无系统默认导航栏与自定义导航栏重叠的双层现象
- 导航栏无异常空白区域或遮挡

**证据要求：** 截图保存至 `.tasks/v4-chat-bugfix/int-v4-chat-bugfix/ac3-navbar.png`

---

### AC-6：登录后用户信息正确显示（BLOCKED → 目标 PASS）

**前置：** 需 `business-api`（8080）运行，否则保持 BLOCKED。

**操作步骤：**
1. H5 打开登录页，使用学生账号登录（如 `2524010001` / `Test@123`）
2. 登录成功后，进入首页或个人信息页
3. 目视检查用户姓名、学号/工号是否正确展示

**通过标准：**
- 显示的姓名与数据库 `real_name` 字段一致（如"张小洋"）
- 无显示 `undefined`、`null` 或空白
- 若存在欢迎语，内容语义正确

**证据要求：** 截图保存至 `.tasks/v4-chat-bugfix/int-v4-chat-bugfix/ac6-userinfo.png`

---

### AC-7：端到端功能回归无退化（PENDING → 目标 PASS）

**操作步骤：** 按以下流程逐步走通，每步确认无异常：

1. **登录**：H5 登录页 → 账号密码登录 → 进入首页（无白屏/报错）
2. **Chat 发消息**：首页 → 进入 chat 页 → 发送一条普通消息 → 收到回复（无报错）
3. **来源跳转**：若 AI 回复包含来源引用，点击来源 → 跳转知识详情页（无白屏）
4. **知识详情页 Fallback**：若详情页触发 fallback 分支，确认 Markdown 内容可读（非原始标记符）
5. **返回**：从详情页返回 chat 页（无崩溃/路由异常）

**通过标准：** 上述 5 步全部无报错、无白屏、无路由异常。

**证据要求：** 截图关键步骤（至少登录成功、chat 收到回复、返回正常），保存至 `.tasks/v4-chat-bugfix/int-v4-chat-bugfix/ac7-e2e-{step}.png`

---

## 回传要求

验收完成后，T2 需执行以下操作：

1. **更新** `_report.md`：将 AC-2/AC-3/AC-6/AC-7 的状态替换为最终结论（PASS / FAIL / BLOCKED），并填写证据截图路径
2. **提交**：`git add` 报告文件及截图，`git commit -m "test(int-v4): L3 manual acceptance AC-2/3/6/7"`
3. **回传 T1**：输出最终 4 项 AC 状态汇总及 commit hash

## 回传格式

```yaml
task: int-v4-chat-bugfix
dispatch_ref: _t2_dispatch_l3.md
ac_results:
  AC-2: PASS | FAIL
  AC-3: PASS | FAIL
  AC-6: PASS | FAIL | BLOCKED
  AC-7: PASS | FAIL
overall: PASS | PARTIAL | FAIL
commit: <hash>
notes: ""
```
