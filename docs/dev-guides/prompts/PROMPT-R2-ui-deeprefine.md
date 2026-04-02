# 【提示词 R2】学生端 UI 深度精修 + AI 对话流式升级 + 个人中心

> **状态**：待执行 | **预估工时**：4~6小时
> **前置**：TASK-R1 已完成基础视觉框架，本次在此基础上精修

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**高级移动端交互工程师**，擅长将功能型界面打磨成令人印象深刻的产品。你之前已经完成了 R1 的基础样式重构，对这个项目已经非常熟悉。

---

## 【必读背景材料】

1. `.globalrules`（服务端口和启动方式）
2. `docs/dev-guides/ai-antipatterns.md`（**错题本，必读**）
3. `_references/前端风格/学生移动端/jade_scholar/DESIGN.md`（设计规范）
4. 所有参考截图（`_references/前端风格/学生移动端/_1` 到 `_8`）
5. `apps/student-app/src/pages/chat/index.vue`（当前 AI 对话页完整代码）
6. `apps/student-app/src/pages/home/index.vue`（当前首页代码）
7. `apps/student-app/src/pages/profile/index.vue`（当前个人中心代码，现在只有占位）
8. `apps/student-app/src/stores/user.ts`（用户状态，了解 userInfo 数据结构）
9. `apps/student-app/src/api/chat.ts`（AI 接口封装，了解 aiChat 函数签名）

---

## 【本次任务说明】

**R1 已经完成了什么**：基础色彩体系、tabBar 图标、各页面背景色统一、线条图标替换、输入框 Soft Fields 风格。

**R2 要做的**：在已有基础上进行三个方向的深度升级，放开手脚做——只要你清楚自己在做什么，不必为每行代码请示。

---

## 【任务一：AI 对话页全面升级】（重点中的重点）

这是整个 APP 最核心的功能页，必须做到最好。

### 1.1 流式输出（打字机效果）

当前状态：`callAIService()` 调用的是 `POST /api/chat`（非流式），AI 回复整条出现。

目标：改用 `POST /api/chat/stream`（SSE 流式接口），实现打字机逐字输出效果。

**SSE 接口规范**（来自 `services/ai-service/app/api/chat.py`）：
- 请求：同非流式（`query`、`history`、`use_kb`）
- 响应：`text/event-stream`，每行格式 `data: {"chunk": "文字片段", "is_end": false, "sources": [...]}`
- 结束标记：`"is_end": true`

**实现方案**：
- uni-app H5 环境中，`uni.request` 不支持 SSE/流式读取。请使用 **原生 `fetch` + `ReadableStream`** 来实现：
  ```typescript
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${userStore.token}`
    },
    body: JSON.stringify({ query, history, use_kb: true })
  })
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()
  ```
- 在消息列表中先创建一条**空的 AI 消息**（`content: ''`），然后随着 chunk 到来逐字追加 `content`，触发 Vue 响应式更新
- 每个 chunk 到来后调用 `scrollToBottom()`，保持跟踪最新内容
- 流结束后（`is_end: true`），再调用后端接口把完整的 AI 回复存储到数据库
- **兜底处理**：SSE 解析失败时，回退到普通非流式调用；两者都失败时显示 `"AI 服务暂时不可用，请稍后重试"` 气泡

### 1.2 Markdown 渲染

AI 的回复内容可能包含 Markdown（如 `**加粗**`、`# 标题`、`- 列表`、`> 引用`、`` `代码` ``）。

**实现方案**：
- 安装 `markdown-it`（轻量级 Markdown 解析器）：`npm install markdown-it`
- 对 AI 气泡的内容进行 Markdown → HTML 转换
- 在 uni-app H5 中可以用 `rich-text` 组件渲染 HTML，或者用 `<view v-html="renderedContent">` 替代 `<text>`
- 关键：**只对 AI 和教师的气泡**做 Markdown 渲染；学生气泡保持纯文本

### 1.3 AI 思考动画升级

当前的三个点比较简陋。升级为更生动的版本：
- 三个点使用圆形 `<view>` 而非文字 `.`，大小 `12rpx × 12rpx`，颜色 `#006a64`
- 动画：三个圆依次弹跳（`transform: translateY`），间隔 `0.15s`，形成波浪感
- 或者：三个点呈脉冲扩散效果（`scale` 动画）

### 1.4 消息入场动画

每条新消息出现时，加入入场动画：
- AI 消息：从左侧淡入（`opacity: 0` → `1`，`translateX(-10px)` → `0`，duration `0.3s`）
- 学生消息：从右侧淡入（同理 `translateX(10px)` → `0`）
- 动画只在消息~~首次出现时触发，历史记录加载时不触发（通过 `v-show` + 延迟 class 或 transition group 实现）

### 1.5 输入区优化

- 输入框高度自适应（多行输入时自动扩展，最高 `160rpx`）：将 `<input>` 改为 `<textarea>`，监听 `@linechange` 事件调整高度
- 发送按钮激活时加 `scale(1.05)` 微动效
- 空输入状态发送按钮灰色，有内容时平滑过渡至主题色

---

## 【任务二：首页深度重构】

R1 的首页已经完成基础样式，但与参考图（`_8/screen.png`）相比还差得远。参考图的首页非常高级，现在大刀阔斧重构。

### 2.1 顶部欢迎区

参考 `_8/screen.png` 和 `_3/screen.png` 的布局：

- **不再使用实心深色背景块**，改为页面自然渐变底色（`#f0f7f5`）
- 欢迎语：`早上好/下午好/晚上好，[姓名]同学`（根据当前时间动态生成问候语）
- 姓名使用 `52rpx bold #1a2e2b` 大字体，给人强烈的个人化感
- 姓名下方用 `24rpx` 淡色文字显示 `院系·年级`（从 `userStore.userInfo` 读取，如有则显示）
- 右上角用户头像：如果有头像 URL 则显示头像，否则显示姓名首字（主题色圆形背景，白色文字）

### 2.2 AI 搜索入口卡片（新增，重点）

参考 `_8/screen.png` 中那个白色卡片，里面有输入框和话题标签：

在欢迎区下方加一张白色圆角大卡片，内部包含：
- 一个只读的"伪输入框"（`placeholder: 问问 AI 辅导员...`），左侧有机器人小图标，右侧有绑定深绿色圆形的 → 箭头按钮
- 点击这个伪输入框（或箭头按钮）直接跳转 AI 咨询页（`/pages/chat/index`）
- 伪输入框下方有 3 个快捷提问标签（如 `# 空教室申请流程`、`# 如何开证明`、`# 补办学生证`），点击任意一个携带该内容作为初始消息跳入 AI 页

> 注意：这是一个**快捷导航入口**，不是真正的输入框，不需要在首页实现任何输入逻辑

### 2.3 进行中的申请状态卡（动态内容）

参考 `_8/screen.png` 中的绿色"进行中的申请"卡片：
- 如果 `GET /api/v1/classroom-applications?pageSize=1&pageNum=1` 有数据，就显示最新一条申请的状态（浅色圆角卡，主题色左边框或状态 badge）
- 如果没有申请记录，就显示空状态（不显示这块，当成广告位隐藏即可）

### 2.4 快捷服务宫格优化

R1 已经做了线条图标，在此基础上：
- 4 个入口的图标容器增加 `hover` 微动效：按下时 `scale(0.95)`，松开回弹 `scale(1)`，duration `0.15s`
- 图标容器背景颜色区分（轻微色调差异，参考 `_8/screen.png` 中不同入口有不同浅色背景）
- 标题字重从 `normal` 改为 `500`（medium），副标题颜色更淡

### 2.5 首页进入动画

页面进入时，各区块依次从下方淡入（staggered animation）：
- 欢迎区（第 0 批，立即）→ AI 搜索卡（第 1 批，delay 100ms）→ 快捷服务（第 2 批，delay 200ms）→ 通知（第 3 批，delay 300ms）
- 使用 CSS `animation` + `animation-fill-mode: backwards`

---

## 【任务三：个人中心页（从零开始）】

当前 `pages/profile/index.vue` 只有一个"功能开发中"占位和退出登录按钮。参考 `_7/screen.png` 构建完整的个人中心页。

### 3.1 顶部用户信息区

- 页面背景 `#f0f7f5`
- 顶部显示用户信息：
  - 大号姓名 `44rpx bold`
  - 院系·年级（次色文字）
  - 右侧头像（圆角正方形，`140rpx × 140rpx`，如无则显示首字母）
  - "已认证学生" badge（主题色浅背景，带 ✓ 图标）

### 3.2 快速数据入口（2 列宫格）

参考 `_7/screen.png` 中的"问答历史"和"收藏内容"双列卡片：

- 左：**问答历史**（图标 + 文字 + 副标题"记录您的所有咨询"，点击跳转 `/pages/questions/index`）
- 右：**申请进度**（图标 + 文字 + 副标题"查看最新状态"，点击跳转 `/pages/apply/status`）

### 3.3 设置列表区

参考 `_7/screen.png` 中的"服务与支持"列表：

白色卡片，内部列表项：
```
🔔 消息通知    3条未读    >
📝 意见反馈   帮助我们改进  >
⚙️ 账号设置   隐私、安全   >
```
每行左侧图标（主题色背景圆形）+ 标题 + 副标题，右侧箭头（淡色）。

> 这些条目当前不需要实际功能，点击时 `uni.showToast({ title: '功能开发中', icon: 'none' })` 即可。

### 3.4 退出登录

改为底部全宽红色 pill 按钮，保留现有的 `handleLogout` 函数（不改 script 逻辑）。

### 3.5 页脚引言

底部居中放一句淡色引言，参考 `_7/screen.png`：
```
"博学而笃志，切问而近思。"
医小管 1.0 · 校园数字化实验室
```

---

## 【全局要求：动效品质】

你非常擅长动效，以下是对本次项目的动效期望：

1. **按钮按压反馈**：所有可点击元素 `active` 态有 `scale(0.97)` 或 `opacity(0.85)` 反馈，duration `0.1s`
2. **页面切换**：uni-app tabBar 切换自带动画，不需要额外处理
3. **卡片悬停/点击**：不需要悬停（移动端），但按压时要有即时视觉反馈
4. **列表项**：个人中心列表项按压时背景轻微变深（`rgba(0,0,0,0.04)`）
5. **骨架屏**（可选加分项）：如果首页或个人中心有异步数据加载，可以加一个简单的骨架屏（灰色矩形占位，有shimmer动画）

---

## 【硬性约束——不能违反的红线】

以下内容**不能动**：

| 禁止操作 | 原因 |
|---------|------|
| 修改 `stores/user.ts` | 已固化，其他页面依赖 |
| 修改 `utils/request.ts` | 统一请求层 |
| 修改 `pages.json` 的路由 `pagePath` | 路由不能改 |
| 修改后端任何文件 | 纯前端任务 |
| 在 `<script>` 里改动 chat.vue 中非 AI 相关的函数（goBack、handleCallTeacher、saveTitle 等） | 只改 callAIService 和相关的流式逻辑 |

---

## 【你的工作方式】

本次任务你**可以自主执行**，不需要每步请示。但有一个强制检查点：

**完成任务一（AI 对话页）后，必须简短汇报一次**，说明流式输出的实现方式和 Markdown 渲染方案，然后自主继续完成任务二和三。

---

## 【完成汇报文件（必须交付）】

满足全部目标后，写入：  
`docs/test-reports/completion-reports/TASK-R2-ui-deeprefine-report.md`

报告包含：
1. **任务标识**（时间精确到秒）
2. **修改的文件清单**（路径 + 改动摘要）
3. **流式输出实现方案说明**（技术细节）
4. **Markdown 渲染方案说明**
5. **验收结果**（逐条 ✅/❌）
6. **新发现错误模式**（若有）

写完报告后回复：**"深度精修任务 R2 完成并停止。"**

---

**现在请开始阅读背景材料，然后直接执行。遇到不确定的技术问题可以先实现一个可工作的版本，再酌情优化。**
