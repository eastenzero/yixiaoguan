# Student-App 前端代码结构审计报告

> 生成时间：2026-04-10  
> 项目路径：`apps/student-app/`

---

## Part 1: 代码结构审计

### 1.1 项目技术栈

| 技术类别 | 具体技术 | 版本/说明 |
|---------|---------|----------|
| **前端框架** | Vue | 3.4.21 |
| **跨平台方案** | UniApp (dcloudio) | 3.0.0-4080420251103001 |
| **构建工具** | Vite | 5.2.8 |
| **状态管理** | Pinia | 2.1.7 + pinia-plugin-persistedstate |
| **CSS 方案** | SCSS | sass 1.72.0 |
| **HTTP 客户端** | uni.request (封装) | 自定义 request.ts |
| **Markdown 渲染** | markdown-it | 14.1.1 |
| **国际化** | vue-i18n | 9.1.9 |
| **TypeScript** | TypeScript | 4.9.4 |

**UniApp 目标平台**：H5、微信小程序、支付宝小程序、百度小程序、抖音小程序、QQ小程序、快手小程序、飞书小程序、HarmonyOS、快应用等

---

### 1.2 路由与页面

| 路径 | 组件文件 | 页面说明 | 导航栏样式 |
|------|---------|---------|-----------|
| `/pages/login/index` | `pages/login/index.vue` | 登录页（学号/密码/验证码） | custom |
| `/pages/home/index` | `pages/home/index.vue` | 首页（AI入口/快捷功能） | default |
| `/pages/chat/index` | `pages/chat/index.vue` | AI 对话页（流式聊天） | custom |
| `/pages/chat/history` | `pages/chat/history.vue` | 对话历史列表 | custom |
| `/pages/knowledge/detail` | `pages/knowledge/detail.vue` | 参考资料详情页 | default |
| `/pages/viewer/pdf` | `pages/viewer/pdf.vue` | PDF 文件查看器 | custom |
| `/pages/apply/classroom` | `pages/apply/classroom.vue` | 空教室申请表单 | default |
| `/pages/apply/status` | `pages/apply/status.vue` | 我的申请列表 | default |
| `/pages/apply/detail` | `pages/apply/detail.vue` | 申请详情页 | custom |
| `/pages/services/index` | `pages/services/index.vue` | 服务大厅/事务导办 | custom |
| `/pages/profile/index` | `pages/profile/index.vue` | 个人中心 | default |
| `/pages/questions/index` | `pages/questions/index.vue` | 我的提问/工单列表 | default |

**TabBar 配置**（4个主标签）：
- 首页 (`/pages/home/index`)
- 智能问答 (`/pages/chat/index`)
- 事务导办 (`/pages/services/index`)
- 我的 (`/pages/profile/index`)

---

### 1.3 组件树

```
App.vue (应用根组件)
├── 全局样式导入: theme.scss, utilities.scss
│
├── pages/login/index.vue          # 登录页
│
├── pages/home/index.vue           # 首页
│   ├── BentoCard.vue              # Bento Grid 卡片组件
│   └── LinkCard.vue               # 链接卡片组件
│
├── pages/chat/index.vue           # AI 对话页（核心页面）
│   ├── IconSend.vue               # 发送图标
│   ├── IconCopy.vue               # 复制图标
│   ├── IconCheck.vue              # 勾选图标
│   ├── IconBot.vue                # AI 机器人图标
│   ├── IconUser.vue               # 用户图标
│   ├── IconSparkles.vue           # 闪烁图标
│   └── IconBookOpen.vue           # 书籍图标
│
├── pages/chat/history.vue         # 对话历史
│   ├── IconMessageSquare.vue
│   └── IconPlus.vue
│
├── pages/knowledge/detail.vue     # 知识库详情
│   └── (markdown-it 渲染)
│
├── pages/services/index.vue       # 服务大厅
│   └── IconDoorOpen, IconClipboardList, IconFileSignature,
│       IconGraduationCap, IconFileText, IconHelpCircle,
│       IconCalendar, IconLayoutGrid
│
├── pages/profile/index.vue        # 个人中心
│   └── 大量内联 SVG 图标
│
├── pages/apply/classroom.vue      # 空教室申请
│   ├── IconCalendarDays.vue
│   ├── IconCalendar.vue
│   ├── IconBuilding2.vue
│   ├── IconUser.vue
│   ├── IconGavel.vue
│   └── IconListChecks.vue
│
├── pages/apply/status.vue         # 申请列表
│   ├── StatusBadge.vue            # 状态徽章组件
│   └── IconPlus.vue
│
├── pages/apply/detail.vue         # 申请详情
│   └── 多个图标组件
│
├── pages/viewer/pdf.vue           # PDF 查看器
│   └── web-view 组件
│
└── pages/questions/index.vue      # 我的提问/工单

# 通用组件
components/BentoCard.vue           # Bento 风格卡片
components/LinkCard.vue            # 链接卡片
components/StatusBadge.vue         # 状态徽章
components/CustomTabBar.vue        # 自定义 TabBar（未使用，pages.json 配置的是原生 tabBar）

# 图标组件 (components/icons/)
IconActivity.vue, IconAlignLeft.vue, IconArmchair.vue, IconArrowRight.vue,
IconBell.vue, IconBookOpen.vue, IconBot.vue, IconBuilding2.vue,
IconCalendar.vue, IconCalendarDays.vue, IconCamera.vue, IconCheck.vue,
IconCheckCircle2.vue, IconChevronRight.vue, IconClipboardCheck.vue,
IconClipboardList.vue, IconClock.vue, IconCopy.vue, IconCreditCard.vue,
IconDoorOpen.vue, IconEdit2.vue, IconFileSignature.vue, IconFileText.vue,
IconGavel.vue, IconGlobe.vue, IconGraduationCap.vue, IconHelpCircle.vue,
IconHistory.vue, IconHome.vue, IconInfo.vue, IconLayoutGrid.vue,
IconLibrary.vue, IconLightbulb.vue, IconListChecks.vue, IconLoader2.vue,
IconLogOut.vue, IconMail.vue, IconMessageSquare.vue, IconMic.vue,
IconMinus.vue, IconMonitorPlay.vue, IconPlus.vue, IconSearch.vue,
IconSend.vue, IconShield.vue, IconSparkles.vue, IconStar.vue,
IconTicket.vue, IconUpload.vue, IconUser.vue, IconUsers.vue,
IconWallet.vue, IconWrench.vue
```

---

### 1.4 后端 API 对接清单（⚠️ 重构时必须保留）

#### 认证相关 API (`src/api/auth.ts`)

| 函数 | API 端点 | 方法 | 说明 | 特殊处理 |
|------|---------|------|------|---------|
| `getCaptcha()` | `/api/captchaImage` | GET | 获取验证码图片 | 使用 rawRequest，不走通用封装 |
| `login(params)` | `/api/login` | POST | 用户登录 | 返回 `{ token }`，使用 rawRequest |
| `getUserInfo(token)` | `/api/getInfo` | GET | 获取用户信息 | 返回 `{ user, roles, permissions }` |
| `logout(token)` | `/api/logout` | POST | 退出登录 | 使用 rawRequest |

**⚠️ 重要说明**：RuoYi 框架的认证接口响应格式与业务接口不同，不走 `request.ts` 的通用封装，直接使用 `uni.request`。

#### 聊天相关 API (`src/api/chat.ts`)

| 函数 | API 端点 | 方法 | 说明 | 特殊处理 |
|------|---------|------|------|---------|
| `createConversation(title?)` | `/api/v1/conversations` | POST | 创建新会话 | - |
| `getConversationList(status?, params?)` | `/api/v1/conversations` | GET | 获取会话列表 | 过滤 undefined 参数 |
| `getConversationDetail(id)` | `/api/v1/conversations/${id}` | GET | 获取会话详情 | - |
| `updateConversationTitle(id, title)` | `/api/v1/conversations/${id}/title` | PUT | 更新会话标题 | - |
| `closeConversation(id)` | `/api/v1/conversations/${id}` | DELETE | 关闭会话 | - |
| `getHistory(conversationId)` | `/api/v1/conversations/${id}/messages` | GET | 获取历史消息 | - |
| `getMessagePage(id, params?)` | `/api/v1/conversations/${id}/messages/page` | GET | 分页获取消息 | - |
| `sendMessage(id, params)` | `/api/v1/conversations/${id}/messages` | POST | 发送消息 | `messageType: 1` |
| `callTeacher(params)` | `/api/v1/escalations` | POST | 学生呼叫老师（创建工单） | - |
| `getMyEscalations(status?, params?)` | `/api/v1/escalations/my` | GET | 获取我的工单列表 | - |

#### 知识库相关 API (`src/api/knowledge.ts`)

| 函数 | API 端点 | 方法 | 说明 |
|------|---------|------|------|
| `getKnowledgeEntryFull(entryId)` | `/api/knowledge/entries/${entryId}` | GET | 获取知识条目完整内容 |

#### 申请相关 API (`src/api/apply.ts`)

| 函数 | API 端点 | 方法 | 说明 |
|------|---------|------|------|
| `getClassroomList(params?)` | `/api/v1/classrooms` | GET | 获取教室列表 |
| `submitApplication(data)` | `/api/v1/classroom-applications` | POST | 提交教室申请 |
| `getMyApplications(userId, params?)` | `/api/v1/classroom-applications` | GET | 获取我的申请列表（使用 applicantId 参数筛选） |
| `getApplicationDetail(id)` | `/api/v1/classroom-applications/${id}` | GET | 获取申请详情 |
| `cancelApplication(id)` | `/api/v1/classroom-applications/${id}/cancel` | PUT | 取消申请 |
| `deleteApplication(id)` | `/api/v1/classroom-applications/${id}` | DELETE | 删除申请 |

#### 通知相关 API (`src/api/notification.ts`)

| 函数 | API 端点 | 方法 | 说明 |
|------|---------|------|------|
| `getNotificationList(pageNum?, pageSize?)` | `/api/v1/notifications` | GET | 获取通知列表 |
| `getUnreadCount()` | `/api/v1/notifications/unread-count` | GET | 获取未读通知数量 |
| `markAsRead(id)` | `/api/v1/notifications/${id}/read` | GET | 标记通知为已读 |

#### ⚠️ SSE 流式聊天实现（核心功能）

**位置**: `pages/chat/index.vue` 第 409-574 行

```typescript
// ===== SSE 流式响应实现（不可修改核心逻辑）=====
async function streamResponse(userContent: string): Promise<string> {
  // 1. 发起 SSE 请求（通过代理转发到 AI 服务 :8000）
  const response = await fetch('/api/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${uni.getStorageSync('token') || ''}`
    },
    body: JSON.stringify({
      query: userContent,
      use_kb: true
    })
  })

  // 2. 使用 ReadableStream 读取数据
  const reader = response.body!.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  let allChunks: string[] = []
  let pendingSources: Source[] = []

  // 3. 解析 SSE 数据格式
  while (true) {
    const { value, done } = await reader.read()
    if (done) break
    const chunk = decoder.decode(value, { stream: true })
    buffer += chunk
    // 处理 data: {...} 格式的行
  }

  // 4. 前端打字机效果
  await playChunks(aiMessage, allChunks, pendingSources)
}
```

**SSE 响应格式**：
```
data: {"chunk": "内容片段", "is_end": false}
data: {"sources": [...], "is_end": false}
data: {"is_end": true}
```

#### 登录鉴权流程（不可修改）

**位置**: 
- `pages/login/index.vue` 第 127-180 行
- `utils/request.ts` 第 12-52 行
- `stores/user.ts`

```typescript
// 1. 登录流程（login/index.vue）
const loginRes = await login({ username, password, code, uuid })
userStore.setToken(loginRes.token)
const userInfoRes = await getUserInfo(loginRes.token)
userStore.setUserInfo({
  id: ruoyiUser.id ?? ruoyiUser.userId,
  username: ruoyiUser.username ?? ruoyiUser.userName,
  realName: ruoyiUser.realName ?? ruoyiUser.nickName ?? ...,
  nickName: ruoyiUser.nickName ?? ruoyiUser.realName,
  avatarUrl: ruoyiUser.avatar,
  email: ruoyiUser.email,
  phone: ruoyiUser.phonenumber,
  roles: userInfoRes.roles,
  permissions: userInfoRes.permissions
})

// 2. Token 存储（stores/user.ts）
const TOKEN_KEY = 'Admin-Token'
const USER_INFO_KEY = 'User-Info'
// 使用 uni.setStorageSync 持久化

// 3. 请求拦截器（utils/request.ts）
if (userStore.token) {
  requestOptions.header['Authorization'] = `Bearer ${token}`
}

// 4. 401 处理（utils/request.ts 第 94-105 行）
case 401:
  userStore.logout()
  uni.reLaunch({ url: '/pages/login/index' })
```

---

### 1.5 状态管理

#### User Store (`src/stores/user.ts`)

| State | 类型 | 说明 | 持久化 |
|-------|------|------|--------|
| `token` | `string` | JWT Token | 是 (uni.setStorageSync) |
| `userInfo` | `UserInfo \| null` | 用户信息 | 是 |

**Getters**:
- `isLoggedIn`: 是否已登录

**Actions**:
- `init()`: 从 Storage 初始化状态
- `setToken(newToken)`: 设置 Token
- `setUserInfo(info)`: 设置用户信息
- `clearAuth()`: 清除登录状态
- `logout()`: 退出登录

#### 全局 Store 结构
```typescript
// stores/index.ts
export const pinia = createPinia()

// main.ts 中挂载
app.use(pinia)
```

---

### 1.6 当前样式分析

#### 主色调色值（当前）

**Primary 主色**（青绿色系）：
| 变量名 | 色值 | 用途 |
|--------|------|------|
| `$primary` / `$primary-40` | `#006a64` | 主色 |
| `$primary-10` | `#002020` | 深色 |
| `$primary-20` | `#003735` | - |
| `$primary-30` | `#004f4c` | - |
| `$primary-50` | `#008580` | - |
| `$primary-60` | `#00a29c` | 浅色 |
| `$primary-70` | `#3cbfb9` | - |
| `$primary-80` | `#5edcd4` | - |
| `$primary-90` | `#a0f0ea` | 背景浅色 |
| `$primary-95` | `#d0f8f4` | 背景浅色 |
| `$primary-container` | `#00A79D` | 容器色 |

**Secondary 辅助色**（蓝灰色系）：
- `$secondary-40`: `#52606F`
- `$secondary-90`: `#D6E4F7`

**Tertiary 第三色**（紫色系）：
- `$tertiary-40`: `#69577B`
- `$tertiary-90`: `#F2DCFF`

**Neutral 中性色**（灰度）：
- `$neutral-0` ~ `$neutral-100`: 黑到白完整色阶
- `$neutral-10`: `#1A1C1E`（主要文字）
- `$neutral-50`: `#76777A`（次要文字）
- `$neutral-90`: `#E3E2E6`（边框/背景）

**状态颜色**：
| 状态 | 色值 |
|------|------|
| 成功 | `#006E1C` (success-40) |
| 警告 | `#7A5900` (warning-40) |
| 错误 | `#BA1A1A` (error-40) |
| 待审批 | `#F7BE34` (status-pending) |
| 已通过 | `#4CAF50` (status-approved) |
| 已拒绝 | `#F44336` (status-rejected) |

#### 布局方式

| 布局类型 | 使用场景 |
|---------|---------|
| Flexbox | 主要布局方式，用于列表、卡片、导航等 |
| Grid | 服务矩阵（4列）、统计卡片（2列） |
| Position | 固定定位用于 TabBar、NavBar |
| 百分比/rpx | 响应式尺寸单位（750rpx = 屏幕宽度） |

#### 响应式策略

- **基准宽度**: 375px（iPhone 标准宽度）
- **尺寸单位**: rpx（responsive pixel）
- **安全区域**: 适配刘海屏、底部手势条
  - `env(safe-area-inset-top/bottom/left/right)`
- **状态栏高度**: `var(--status-bar-height, 44px)`

#### 图标库

- **自定义 SVG 图标**: 45+ 个 Vue 单文件图标组件
- **图标风格**: Lucide Icons 风格（线性、2px stroke、圆角）
- **使用方式**: `<component :is="IconXXX" :size="24" :color="'#006a64'" />`

---

### 1.7 静态资源

| 资源类型 | 文件路径 | 说明 |
|---------|---------|------|
| Logo | `src/static/logo.png` | 应用 Logo |
| TabBar 图标 | `src/static/icons/` | home, chat, apply, profile 的 active/inactive 状态 |

**图标清单**：
```
src/static/icons/
├── apply-active.png
├── apply.png
├── chat-active.png
├── chat.png
├── home-active.png
├── home.png
├── profile-active.png
└── profile.png
```

---

### 1.8 技术债与 TODO

| 位置 | 内容 | 优先级 |
|------|------|--------|
| `api/chat.ts` 第 153-156 行 | `// TODO: 后端实现 /api/chat/suggestions 后取消注释` | P2 |
| `pages/chat/index.vue` 第 317 行 | `// TODO: 后端实现 /api/chat/suggestions 后可恢复远程获取` | P2 |
| `pages/chat/index.vue` 第 397 行 | `// TODO: AI 回复持久化需后端提供专用接口` | P1 |
| `pages/chat/index.vue` 第 343-345 行 | `// P1 功能：后续可实现分页加载` | P1 |
| `pages/home/index.vue` 第 350-363 行 | `// 加载最新申请` - 直接使用 uni.request 而非封装 API | P2 |
| `pages/services/index.vue` | 多个功能标记为 `active: false`（开发中） | - |

---

## Part 2: AI Studio Prompt

```markdown
# 任务：山东第一医科大学学生端 App 前端重构

## 项目概述

医小管 - 山东第一医科大学智慧校园服务平台学生端
- **目标用户**: 在校大学生
- **核心功能**: AI 智能问答、知识库浏览、事务导办、空教室申请
- **重构目标**: 
  1. 主色调从青绿色 → 紫色（契合学校官网和校徽色调）
  2. 提升整体 UI 设计质量
  3. 保持所有现有功能不变

## 技术栈约束（必须严格遵守）

| 技术 | 版本/说明 |
|------|----------|
| 框架 | Vue 3.4.21 (Composition API + `<script setup>`) |
| 跨平台 | UniApp 3.0 |
| 构建工具 | Vite 5.2.8 |
| 状态管理 | Pinia 2.1.7 |
| 样式 | SCSS |
| 尺寸单位 | rpx (750rpx = 屏幕宽度) |
| 类型系统 | TypeScript |

**⚠️ 重要约束**：
- 保持 `<script setup lang="ts">` 写法
- 所有 API 调用逻辑原封不动复制
- 状态管理（Pinia store）保持原有结构
- 页面路由路径不可更改

## 设计要求

### 色彩方案（紫色主题）

参考山东第一医科大学校徽紫色调：

**主色（Primary）**: `#7C3AED`（紫罗兰 600）
| 色阶 | 色值 | 用途 |
|------|------|------|
| Primary-10 | `#2E1065` | 最深色 |
| Primary-20 | `#4C1D95` | - |
| Primary-30 | `#5B21B6` | - |
| **Primary-40** | **`#7C3AED`** | **主色调** |
| Primary-50 | `#8B5CF6` | 高亮 |
| Primary-60 | `#A78BFA` | 浅色 |
| Primary-70 | `#C4B5FD` | 禁用态 |
| Primary-80 | `#DDD6FE` | 浅背景 |
| Primary-90 | `#EDE9FE` | 极浅背景 |
| Primary-95 | `#F5F3FF` | 近白色背景 |

**辅助色系**：
- **Secondary**: `#475569` (Slate 600) - 中性辅助
- **Tertiary**: `#059669` (Emerald 600) - 成功/通过状态
- **Error**: `#DC2626` (Red 600)
- **Warning**: `#D97706` (Amber 600)
- **Success**: `#059669` (Emerald 600)

**背景色系**：
- 页面背景: `#F8FAFC` (Slate 50)
- 卡片背景: `#FFFFFF`
- 次级背景: `#F1F5F9` (Slate 100)
- 边框: `#E2E8F0` (Slate 200)

**文字色系**：
- 主要文字: `#0F172A` (Slate 900)
- 次级文字: `#475569` (Slate 600)
- 辅助文字: `#94A3B8` (Slate 400)
- 反色文字（紫色背景上）: `#FFFFFF`

### UI 风格规范

1. **圆角设计**（现代柔和风格）：
   - 大卡片: `border-radius: 24rpx`
   - 按钮: `border-radius: 48rpx`（药丸形）
   - 小标签: `border-radius: 40rpx`
   - 输入框: `border-radius: 16rpx`

2. **阴影层级**：
   - Elevation-1: `0 2rpx 8rpx rgba(124, 58, 237, 0.06)`
   - Elevation-2: `0 8rpx 24rpx rgba(124, 58, 237, 0.1)`
   - Elevation-3: `0 12rpx 40rpx rgba(124, 58, 237, 0.15)`

3. **间距系统**（8rpx 基准）：
   - xs: 8rpx
   - sm: 16rpx
   - md: 24rpx
   - lg: 32rpx
   - xl: 48rpx

4. **字体**：
   - 系统字体栈: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
   - 标题加粗: 600-700
   - 正文: 400

5. **动画**：
   - 入场动画: `fadeInUp` 0.6s cubic-bezier(0.2, 0.8, 0.2, 1)
   - 阶梯延迟: 0.05s, 0.1s, 0.15s...
   - 按压效果: `transform: scale(0.96)`

6. **移动端优先**：
   - 设计基准: 375px 宽度
   - 安全区域适配: `env(safe-area-inset-*)`

## 页面清单（需重构）

### 1. 登录页 (`pages/login/index.vue`)
- **布局**: 居中卡片式
- **元素**: 
  - 顶部 Logo + "医小管" + "智慧校园服务平台"
  - 输入框: 学号、密码、验证码
  - 验证码图片（点击刷新）
  - 登录按钮（药丸形，紫色渐变）
  - 底部提示: "初始密码与学号相同"
- **背景**: 紫色渐变（从 #7C3AED 到 #A78BFA）

### 2. 首页 (`pages/home/index.vue`)
- **布局**: 垂直堆叠，顶部欢迎区 + AI 输入区 + Bento Grid + 链接列表
- **欢迎区**: 
  - 左: "早上好/下午好/晚上好" + 用户名
  - 右: 状态小卡片（显示进行中的申请数）
- **AI 输入区**: 药丸形搜索条，左侧 AI 徽章，右侧箭头按钮
- **快捷标签**: 横向滚动 pill 标签（奖学金申请、选课指南等）
- **Bento Grid**:
  - 大卡片（跨2列）: 任务指引，紫色渐变背景
  - 下方2个小卡片: 空教室预约、申请进度
- **官方链接区**: 教务管理、图书馆、学生邮箱（LinkCard 样式）
- **通知 Banner**: 底部提醒横幅

### 3. AI 对话页 (`pages/chat/index.vue`) ⚠️ 核心页面
- **布局**: 全屏，顶部自定义导航栏 + 消息列表 + 底部输入区
- **导航栏**: 居中标题 "医小管"，右侧历史按钮
- **消息列表**:
  - 空状态: AI 图标 + 欢迎语 + 快捷问题 chips
  - 用户消息: 右侧，白色背景，圆角气泡
  - AI 消息: 左侧，AI 头像 + 名称 + 紫色浅色背景气泡
  - 支持 Markdown 渲染（引用、列表、代码块）
  - 参考资料展开（可点击查看详情）
  - 时间戳 + 复制按钮
- **输入区**: 
  - 底部固定
  - 圆角输入框 + 发送按钮（紫色背景）
  - 快捷问题横向滚动条
- **参考资料预览弹层**: 半屏弹窗，显示来源详情

### 4. 对话历史 (`pages/chat/history.vue`)
- **布局**: 列表页，顶部导航栏 + 会话卡片列表
- **导航栏**: 紫色渐变背景，标题 "对话历史"
- **会话卡片**: 
  - 标题 + 状态标签（已关闭/进行中/教师介入）
  - 时间 + 消息数量
  - 点击跳转对应会话
- **空状态**: 图标 + "还没有对话记录" + 开始新对话按钮
- **FAB**: 右下角悬浮新建按钮

### 5. 服务大厅 (`pages/services/index.vue`)
- **布局**: 顶部毛玻璃导航 + Hero 区 + 统计卡片 + 服务矩阵
- **导航栏**: 毛玻璃效果，标题 "服务大厅"
- **Hero 区**: 英文标签 + 中文标题 + 副标题
- **统计卡片**: 2列网格，紫色渐变背景，显示进行中的申请数、待处理通知
- **服务矩阵**: 4列网格，图标 + 名称
  - 已启用: 空教室申请、我的申请
  - 未启用: 请假销假、学籍管理、证明开具等（灰色态）

### 6. 个人中心 (`pages/profile/index.vue`)
- **布局**: 垂直滚动，多卡片组合
- **头部身份区**: 
  - 左: "已认证身份"徽章 + 用户名 + 院系年级
  - 右: 大头像（紫色渐变背景）
- **功能矩阵**: 2列，问答历史、申请进度
- **Bento Grid 卡片**:
  - 学期进度: 进度条 + 待办提醒
  - AI 助手历史: 最近对话列表
  - 常用服务: 课表、成绩、一卡通
- **设置分组**: 消息通知、系统设置、服务反馈、帮助中心、关于
- **底部**: 退出登录按钮 + 版本信息

### 7. 空教室申请 (`pages/apply/classroom.vue`)
- **布局**: 表单页，Hero 区 + 分组表单
- **Hero 区**: 紫色渐变，标题 "预约申请单" + 说明文字
- **表单分组**: 
  - 时间选择（日期、开始时间、结束时间）
  - 教室选择（picker）、预计人数
  - 联系电话、用途说明（textarea）
- **提交按钮**: 底部固定，药丸形紫色按钮
- **底部信息卡**: 申请规则、审核流程

### 8. 我的申请 (`pages/apply/status.vue`)
- **布局**: 列表页，Hero 区 + 新建按钮 + 申请卡片列表
- **Hero 区**: 紫色渐变，标题 "我的申请"
- **申请卡片**:
  - 顶部步骤指示器（已提交→审核中→已完成）
  - 教室名称 + 状态标签 + 时间段
  - 用途、人数、联系信息
  - 审批意见展开区
  - 底部: 申请时间 + 取消按钮（仅待审批状态）
- **空状态**: 无申请时的引导

### 9. 申请详情 (`pages/apply/detail.vue`)
- **布局**: 详情页，Hero 区 + 步骤卡片 + 时间线
- **Hero 区**: 教室名称 + 脉冲指示器 + 当前状态
- **步骤卡片**: 4步流程可视化（已提交→审核中→待补充→已通过）
- **申请信息摘要**: 申请编号、提交时间
- **审批历史时间线**: 图标 + 标题 + 时间 + 描述 + 意见引用
- **辅助信息**: 预计处理时间、帮助中心入口
- **操作按钮**: 联系审批人、修改申请

### 10. 我的提问 (`pages/questions/index.vue`)
- **布局**: 列表页，筛选标签 + 工单卡片列表
- **筛选标签**: 全部、待处理、处理中、已解决
- **工单卡片**:
  - 状态标签 + 创建时间
  - 问题摘要（2行截断）
  - 会话 ID、处理老师分配状态
- **空状态**: 引导去提问

### 11. 知识库详情 (`pages/knowledge/detail.vue`)
- **布局**: 内容页，Hero 卡片 + 内容区
- **Hero 卡片**: 紫色渐变，标题 + 条目编号 + 相关度 + 分类
- **标签区**: 知识标签 pill 列表
- **内容区**: Markdown 渲染正文
- **查看原始文件按钮**: 如有 PDF 则显示

### 12. PDF 查看器 (`pages/viewer/pdf.vue`)
- **布局**: 全屏，顶部导航栏 + web-view
- **导航栏**: 返回按钮 + 标题

## ⚠️ 必须保留的后端对接逻辑（不可修改）

### 1. 登录鉴权逻辑

**文件**: `src/pages/login/index.vue`

```typescript
// ⚠️ 不可修改 - 登录流程
const handleLogin = async () => {
  // 1. 登录获取 token
  const loginRes = await login({
    username: form.username.trim(),
    password: form.password,
    code: form.code.trim(),
    uuid: form.uuid
  })
  
  // 2. 保存 token
  userStore.setToken(loginRes.token)
  
  // 3. 获取用户信息（兼容字段映射）
  const userInfoRes = await getUserInfo(loginRes.token)
  const ruoyiUser = userInfoRes.user
  userStore.setUserInfo({
    id: ruoyiUser.id ?? ruoyiUser.userId,
    username: ruoyiUser.username ?? ruoyiUser.userName,
    realName: ruoyiUser.realName ?? ruoyiUser.nickName ?? ruoyiUser.username ?? ruoyiUser.userName,
    nickName: ruoyiUser.nickName ?? ruoyiUser.realName,
    avatarUrl: ruoyiUser.avatar,
    email: ruoyiUser.email,
    phone: ruoyiUser.phonenumber,
    roles: userInfoRes.roles,
    permissions: userInfoRes.permissions
  })
  
  // 4. 跳转首页
  uni.switchTab({ url: '/pages/home/index' })
}
```

### 2. SSE 流式聊天逻辑

**文件**: `src/pages/chat/index.vue` 第 409-574 行

```typescript
// ⚠️ 不可修改 - SSE 流式响应核心逻辑
async function streamResponse(userContent: string): Promise<string> {
  isStreaming.value = true
  isTyping.value = true

  // 创建 AI 消息占位
  const aiMessage: Message = {
    id: `assistant-${Date.now()}`,
    role: 'assistant',
    content: '',
    sources: [],
    timestamp: Date.now(),
    isStreaming: true
  }

  try {
    // 发起 SSE 请求
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${uni.getStorageSync('token') || ''}`
      },
      body: JSON.stringify({
        query: userContent,
        use_kb: true
      })
    })

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let buffer = ''
    let allChunks: string[] = []
    let pendingSources: Source[] = []

    // 读取流数据
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      const chunk = decoder.decode(value, { stream: true })
      buffer += chunk
      // 解析 data: {...} 格式的行...
    }

    // 打字机效果播放
    await playChunks(aiMessage, allChunks, pendingSources)
    
  } catch (error) {
    // 错误处理...
  } finally {
    isStreaming.value = false
    isTyping.value = false
  }
}
```

### 3. 请求拦截器与 Token 注入

**文件**: `src/utils/request.ts`

```typescript
// ⚠️ 不可修改 - Token 注入逻辑
export function request<T = any>(options: UniApp.RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const userStore = useUserStore()
    
    // 构建请求配置
    const requestOptions: UniApp.RequestOptions = {
      ...options,
      header: {
        'Content-Type': 'application/json',
        ...options.header
      },
      success: (res) => handleResponse(res, resolve, reject, userStore),
      fail: (err) => handleError(err, reject)
    }
    
    // 注入 JWT Token
    if (userStore.token) {
      const token = userStore.token.startsWith('Bearer') 
        ? userStore.token 
        : `Bearer ${userStore.token}`
      requestOptions.header = {
        ...requestOptions.header,
        'Authorization': token
      }
    }
    
    uni.request(requestOptions)
  })
}

// ⚠️ 不可修改 - 401 处理
function handleBusinessError(data, reject, userStore) {
  switch (data.code) {
    case 401:
      uni.showToast({ title: data.msg || '登录已过期', icon: 'none' })
      userStore.logout()
      setTimeout(() => {
        uni.reLaunch({ url: '/pages/login/index' })
      }, 1500)
      break
    // ...
  }
}
```

### 4. 用户状态管理

**文件**: `src/stores/user.ts`

```typescript
// ⚠️ 不可修改 - Storage Key 与持久化逻辑
const TOKEN_KEY = 'Admin-Token'
const USER_INFO_KEY = 'User-Info'

export const useUserStore = defineStore('user', () => {
  const token = ref<string>('')
  const userInfo = ref<UserInfo | null>(null)
  
  const init = () => {
    const storedToken = uni.getStorageSync(TOKEN_KEY)
    const storedUserInfo = uni.getStorageSync(USER_INFO_KEY)
    if (storedToken) token.value = storedToken
    if (storedUserInfo) userInfo.value = JSON.parse(storedUserInfo)
  }
  
  const setToken = (newToken: string) => {
    token.value = newToken
    uni.setStorageSync(TOKEN_KEY, newToken)
  }
  
  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
    uni.setStorageSync(USER_INFO_KEY, JSON.stringify(info))
  }
  
  const logout = () => {
    token.value = ''
    userInfo.value = null
    uni.removeStorageSync(TOKEN_KEY)
    uni.removeStorageSync(USER_INFO_KEY)
  }
  
  return { token, userInfo, isLoggedIn, init, setToken, setUserInfo, logout }
})
```

### 5. API 函数清单（完整保留）

**认证 API** (`src/api/auth.ts`):
- `getCaptcha()` → GET `/api/captchaImage`
- `login(params)` → POST `/api/login`
- `getUserInfo(token)` → GET `/api/getInfo`
- `logout(token)` → POST `/api/logout`

**聊天 API** (`src/api/chat.ts`):
- `createConversation(title?)` → POST `/api/v1/conversations`
- `getConversationList(status?, params?)` → GET `/api/v1/conversations`
- `getHistory(conversationId)` → GET `/api/v1/conversations/${id}/messages`
- `sendMessage(id, params)` → POST `/api/v1/conversations/${id}/messages`
- `callTeacher(params)` → POST `/api/v1/escalations`
- `getMyEscalations(status?, params?)` → GET `/api/v1/escalations/my`

**申请 API** (`src/api/apply.ts`):
- `getClassroomList(params?)` → GET `/api/v1/classrooms`
- `submitApplication(data)` → POST `/api/v1/classroom-applications`
- `getMyApplications(userId, params?)` → GET `/api/v1/classroom-applications`
- `getApplicationDetail(id)` → GET `/api/v1/classroom-applications/${id}`
- `cancelApplication(id)` → PUT `/api/v1/classroom-applications/${id}/cancel`

**通知 API** (`src/api/notification.ts`):
- `getNotificationList(pageNum?, pageSize?)` → GET `/api/v1/notifications`
- `getUnreadCount()` → GET `/api/v1/notifications/unread-count`

**知识库 API** (`src/api/knowledge.ts`):
- `getKnowledgeEntryFull(entryId)` → GET `/api/knowledge/entries/${entryId}`

## 事务导办页面特别说明

`pages/services/index.vue` 是服务入口页面，只负责跳转：

**已启用功能**（可点击跳转）：
- 空教室申请 → `/pages/apply/classroom`
- 我的申请 → `/pages/apply/status`

**未启用功能**（显示"功能开发中"提示）：
- 请假销假
- 学籍管理
- 证明开具
- 心理服务
- 缓考申请

**外部链接入口**（可选添加）：
- 企业微信入口（如有 URL）
- 学校官网: `https://www.sdfmu.edu.cn`

## 输出要求

1. **文件格式**: 完整的 Vue SFC 文件（`.vue`）
2. **Script 写法**: `<script setup lang="ts">`
3. **样式**: `<style scoped lang="scss">`
4. **功能保留**: 
   - 所有 API 调用代码原样复制（标注"不可修改"的部分）
   - 所有状态管理逻辑保留
   - 所有路由跳转路径不变
   - SSE 流式聊天完整保留
   - Markdown 渲染保留
5. **配色替换**: 
   - 将原有的青绿色（#006a64 等）替换为紫色系（#7C3AED 等）
   - 保持原有的透明度、渐变比例不变
6. **图标**: 可复用现有的 SVG 图标组件
7. **布局**: 保持原有页面结构和组件层级

## 验证清单

重构完成后，请确认以下功能正常：
- [ ] 登录/退出流程正常
- [ ] 获取验证码显示正常
- [ ] AI 对话流式响应正常
- [ ] 对话历史列表加载正常
- [ ] 空教室申请表单提交正常
- [ ] 申请列表和详情查看正常
- [ ] 知识库参考资料查看正常
- [ ] Token 过期自动跳转登录页
```

---

**报告生成完成**  
**输出文件**: `kimi/report-v9-frontend-audit.md`
