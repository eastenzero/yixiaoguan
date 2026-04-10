# T3 任务: 解压 AI Studio 前端产出 + 校验

## 任务目标
1. 解压 AI Studio 生成的前端重构文件
2. 校验后端对接逻辑是否完整保留
3. 输出校验报告

## 步骤

### Step 1: 解压文件

将压缩包解压到项目目录下的临时文件夹：

```powershell
Expand-Archive -Path "D:\Backup_2025\下载\zip (6).zip" -DestinationPath "C:\Users\Administrator\Documents\code\yixiaoguan\ai-studio-output" -Force
```

解压后查看目录结构：
```powershell
Get-ChildItem -Recurse "C:\Users\Administrator\Documents\code\yixiaoguan\ai-studio-output" | Select-Object FullName, Length
```

### Step 2: 盘点文件

列出解压后的所有文件，与审计报告中的页面清单对比：

**预期文件（12 个页面 + 工具/API/Store 文件）**：

页面文件：
- pages/login/index.vue
- pages/home/index.vue
- pages/chat/index.vue （⚠️ 最关键）
- pages/chat/history.vue
- pages/knowledge/detail.vue
- pages/viewer/pdf.vue
- pages/apply/classroom.vue
- pages/apply/status.vue
- pages/apply/detail.vue
- pages/services/index.vue
- pages/profile/index.vue
- pages/questions/index.vue

工具/API 文件：
- api/auth.ts
- api/chat.ts
- api/apply.ts
- api/notification.ts
- api/knowledge.ts
- utils/request.ts
- stores/user.ts

样式文件：
- styles/theme.scss（或类似）

组件：
- components/BentoCard.vue
- components/LinkCard.vue
- components/StatusBadge.vue
- components/icons/*.vue（45+个图标组件）

记录：哪些文件存在 / 缺失 / 新增。

### Step 3: 关键逻辑校验（⚠️ 最重要）

逐个检查以下关键逻辑是否被完整保留（不是只看有没有函数名，要看实现代码）：

#### 3.1 SSE 流式聊天 (`pages/chat/index.vue`)
检查项：
- [ ] `streamResponse()` 函数存在且逻辑完整
- [ ] `fetch('/api/chat/stream', ...)` POST 请求
- [ ] `ReadableStream` reader 读取循环
- [ ] `decoder.decode(value, { stream: true })` 解码
- [ ] `data: {...}` SSE 格式行解析
- [ ] `playChunks()` 打字机效果函数
- [ ] `allChunks` 增量累加（不是替换）
- [ ] `pendingSources` 来源数据处理
- [ ] `isStreaming` / `isTyping` 状态管理

#### 3.2 登录鉴权 (`pages/login/index.vue`)
检查项：
- [ ] `login({ username, password, code, uuid })` 调用
- [ ] `userStore.setToken(loginRes.token)` 保存
- [ ] `getUserInfo(loginRes.token)` 获取用户信息
- [ ] RuoYi 字段兼容映射（id/userId, username/userName, realName/nickName 等）
- [ ] `uni.switchTab({ url: '/pages/home/index' })` 跳转

#### 3.3 请求拦截器 (`utils/request.ts`)
检查项：
- [ ] Token 注入: `Authorization: Bearer ${token}`
- [ ] `Bearer` 前缀判断（避免重复）
- [ ] 401 处理: `userStore.logout()` + `uni.reLaunch` 跳转登录页
- [ ] HTTP 状态码分层处理（200/401/500 等）

#### 3.4 用户状态管理 (`stores/user.ts`)
检查项：
- [ ] `TOKEN_KEY = 'Admin-Token'` 常量名不变
- [ ] `USER_INFO_KEY = 'User-Info'` 常量名不变
- [ ] `uni.setStorageSync` / `uni.getStorageSync` 持久化
- [ ] `init()` / `setToken()` / `setUserInfo()` / `logout()` 完整

#### 3.5 API 函数完整性
逐个确认所有 API 函数是否存在：
- auth.ts: getCaptcha, login, getUserInfo, logout （4个）
- chat.ts: createConversation, getConversationList, getConversationDetail, updateConversationTitle, closeConversation, getHistory, getMessagePage, sendMessage, callTeacher, getMyEscalations （10个）
- apply.ts: getClassroomList, submitApplication, getMyApplications, getApplicationDetail, cancelApplication, deleteApplication （6个）
- notification.ts: getNotificationList, getUnreadCount, markAsRead （3个）
- knowledge.ts: getKnowledgeEntryFull （1个）

#### 3.6 色彩主题
检查项：
- [ ] 原有青绿色 `#006a64` 是否已替换为紫色系 `#7C3AED`
- [ ] SCSS 变量是否使用紫色色阶
- [ ] 渐变色是否更新为紫色系

### Step 4: 差异总结

对比 AI Studio 产出与原始代码的差异，输出以下维度的评估：

| 维度 | 状态 | 说明 |
|------|------|------|
| 文件完整性 | ✅/⚠️/❌ | 所有页面/组件/API 文件是否齐全 |
| SSE 流式聊天 | ✅/⚠️/❌ | 核心逻辑是否完整 |
| 登录鉴权 | ✅/⚠️/❌ | 登录+Token+401 链路 |
| 请求拦截器 | ✅/⚠️/❌ | request.ts 逻辑 |
| 状态管理 | ✅/⚠️/❌ | Pinia store |
| API 函数 | ✅/⚠️/❌ | 24个 API 函数 |
| 紫色主题 | ✅/⚠️/❌ | 配色替换 |
| 路由路径 | ✅/⚠️/❌ | pages.json 路径不变 |
| UniApp 兼容 | ✅/⚠️/❌ | rpx 单位、uni.* API |

## 输出文件

写入 `kimi/report-v9-review.md`，包含：
1. 解压后文件清单
2. 缺失文件列表（如有）
3. 关键逻辑校验结果（3.1-3.6 每项逐一标注）
4. 差异总结表格
5. 结论：PASS / FAIL / CONDITIONAL PASS（附修复建议）

## 参考
- 审计报告: `kimi/report-v9-frontend-audit.md`
- 原始源码: `apps/student-app/src/`
