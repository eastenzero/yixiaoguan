# 教师移动端 (Teacher Mobile App) — UI 生成提示词

> 用途：交给 AI（Claude / Gemini / GPT）一次性生成全部页面的 Vue 3 前端代码。
> 日期：2026-04-11
> 基于：学生端 (student-app) 设计系统 + aether-academic UI 复刻项目 + 教师网页端 (teacher-web) 功能规格

---

## 给 AI 的提示词（从这里开始复制）

---

你是一个专业的前端开发工程师。请为"医小管"（YiXiaoGuan）项目创建一个**教师移动端 H5 应用**的完整前端代码。

### 项目背景

"医小管"是山东第一医科大学的智能校园助手系统。学生端已完成开发（紫色主题、移动优先设计）。现在需要为教师开发一个**竖屏移动端 H5 应用**，让教师在手机上处理学生提问、管理知识库、审批申请等工作。

### 技术栈要求

- **框架**: Vue 3 + Composition API (`<script setup>`)
- **构建**: Vite
- **样式**: Tailwind CSS 3（与 aether-academic 学生端 UI 复刻项目一致）
- **路由**: vue-router 4
- **图标**: Material Symbols Outlined（Google 字体图标，可变字重）
- **字体**: Manrope（西文）+ PingFang SC / Microsoft YaHei（中文）
- **数据**: 全部使用 Mock 数据（不对接真实 API，后续单独嫁接）
- **语言**: TypeScript

### 设计系统（必须严格遵循）

#### 色彩系统 — Material Design 3 紫色主题

```
品牌主色:
  --md-primary:           #630ed4    /* 常用主色（深紫） */
  --md-primary-40:        #7C3AED    /* 标准紫 */
  --md-primary-50:        #8B5CF6    /* 亮紫 */
  --md-primary-60:        #A78BFA    /* 浅亮紫 */
  --md-primary-80:        #DDD6FE    /* 极浅紫 */
  --md-primary-90:        #EDE9FE    /* 淡紫背景 */
  --md-primary-95:        #F5F3FF    /* 近白紫底 */

表面层级 (Surface Container, MD3 Tonal Stacking):
  --md-surface:             #FFFBFF
  --md-surface-container-lowest: #FFFFFF
  --md-surface-container-low:    #F7F2FA
  --md-surface-container:        #F1ECF4
  --md-surface-container-high:   #ECE6F0
  --md-surface-container-highest:#E6E0E9

文字色:
  --md-on-surface:          #1C1B1F    /* 主文字 */
  --md-on-surface-variant:  #49454F    /* 辅助文字 */
  --md-outline:             #79747E    /* 边框/分割线 */
  --md-outline-variant:     #CAC4D0    /* 浅边框 */

语义色:
  --md-success:   #16A34A    /* 绿色-成功/已解决 */
  --md-warning:   #F59E0B    /* 橙色-警告/待处理 */
  --md-error:     #DC2626    /* 红色-错误/紧急 */
  --md-info:      #2563EB    /* 蓝色-信息 */
```

#### Tailwind 扩展配置

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#630ed4',
          40: '#7C3AED',
          50: '#8B5CF6',
          60: '#A78BFA',
          80: '#DDD6FE',
          90: '#EDE9FE',
          95: '#F5F3FF',
        },
        surface: {
          DEFAULT: '#FFFBFF',
          'container-low': '#F7F2FA',
          'container': '#F1ECF4',
          'container-high': '#ECE6F0',
        },
        'on-surface': '#1C1B1F',
        'on-surface-variant': '#49454F',
        outline: '#79747E',
        'outline-variant': '#CAC4D0',
      },
      fontFamily: {
        headline: ['Manrope', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
        body: ['Manrope', 'PingFang SC', 'Microsoft YaHei', 'sans-serif'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
    },
  },
}
```

#### 核心视觉规范

| 属性 | 值 | 说明 |
|------|-----|------|
| 圆角-卡片 | `rounded-3xl` (1.5rem) | 所有卡片统一大圆角 |
| 圆角-按钮 | `rounded-2xl` (1rem) | 药丸形按钮 |
| 圆角-输入框 | `rounded-2xl` (1rem) | 大圆角输入 |
| 圆角-徽章/标签 | `rounded-full` | 完全圆角胶囊 |
| 阴影-卡片 | `shadow-sm` 或无阴影 | 用 surface 层级代替阴影 |
| 毛玻璃-导航 | `backdrop-blur-xl bg-white/80` | 顶部/底部导航栏 |
| 间距-页面横向 | `px-5` (20px) | 统一页面左右边距 |
| 间距-卡片间 | `gap-4` (16px) | 卡片之间间距 |
| 间距-卡片内 | `p-5` (20px) | 卡片内部填充 |
| 底部安全区 | `pb-24` (96px) | 为 BottomNavBar 留空 |
| 触控反馈 | `active:scale-95 transition-transform` | 所有可点击元素 |

#### 动画系统

```css
/* 入场动画 */
@keyframes fadeUpEditorial {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-up { animation: fadeUpEditorial 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) both; }

/* 阶梯延迟 */
.delay-1 { animation-delay: 50ms; }
.delay-2 { animation-delay: 100ms; }
.delay-3 { animation-delay: 150ms; }
.delay-4 { animation-delay: 200ms; }
```

### 图标使用方式

使用 Material Symbols Outlined 字体图标。在 `index.html` 中引入：

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet" />
```

使用方式：
```html
<span class="material-symbols-outlined">dashboard</span>
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1">favorite</span>
```

### 公共组件（2 个）

#### 1. TopAppBar.vue
- 毛玻璃背景: `backdrop-blur-xl bg-white/80`
- 固定顶部: `fixed top-0 left-0 right-0 z-50`
- 高度: `h-14` (56px)
- 左侧: 返回箭头（仅非首页时显示）
- 中间: 页面标题（font-semibold text-lg）
- 右侧: 可选操作按钮插槽
- 底部: 1px 分割线 `border-b border-outline-variant/30`

#### 2. BottomNavBar.vue
- 毛玻璃背景: `backdrop-blur-xl bg-white/90`
- 固定底部: `fixed bottom-0 left-0 right-0 z-50`
- 高度: `h-16` (64px) + `pb-[env(safe-area-inset-bottom)]`
- 4 个 Tab 项:
  - **工作台** — icon: `dashboard`, 路由: `/`
  - **学生提问** — icon: `forum`, 路由: `/questions`，右上角红色数字徽章（待处理数）
  - **知识库** — icon: `menu_book`, 路由: `/knowledge`
  - **我的** — icon: `person`, 路由: `/profile`
- 激活态: 图标填充 (`FILL 1`) + 主色文字 + 图标下方小圆点指示器
- 未激活: 灰色 `text-on-surface-variant`

### 页面规格（共 7 个页面）

---

#### 页面 1: LoginView.vue — 登录页

**路由**: `/login`
**无** TopAppBar 和 BottomNavBar

**布局**:
- 全屏紫色渐变背景: `bg-gradient-to-br from-primary-40 to-primary`
- 中央白色登录卡片: `bg-white rounded-4xl p-8 mx-6 shadow-2xl`
- 顶部: 品牌 Logo 区域（大图标 + "医小管" + "教师工作台" 副标题）
- 表单:
  - 用户名输入框（icon: person, placeholder: "请输入教师工号"）
  - 密码输入框（icon: lock, placeholder: "请输入密码", 右侧眼睛图标切换可见）
  - "记住我" 复选框
  - 登录按钮: 全宽，紫色渐变 `bg-gradient-to-r from-primary-40 to-primary-50`，白色文字，`rounded-2xl h-12`
- 底部: 版权信息 "山东第一医科大学 · 医小管智能管理系统"

**Mock 数据**: 任意用户名密码点击登录直接跳转到首页

---

#### 页面 2: DashboardView.vue — 工作台首页

**路由**: `/` (默认首页)
**有** TopAppBar（标题: "工作台"，右侧: 通知铃铛图标 + 红点）+ BottomNavBar

**布局 — 从上到下**:

**区块 A — 欢迎横幅**:
- 紫色渐变卡片 `bg-gradient-to-r from-primary-40 to-primary-50 rounded-3xl p-5 text-white`
- 左侧: "早上好，梁老师 👋" + 副标题 "今天有 3 条待处理提问"
- 右侧: 教师头像圆形 `w-12 h-12 rounded-full`

**区块 B — 统计卡片网格** (2×2 Bento Grid):
- `grid grid-cols-2 gap-3`
- 4 张统计卡片，每张:
  - `bg-surface-container-low rounded-3xl p-4`
  - 顶部: 圆形图标背景 `w-10 h-10 rounded-full bg-primary-90 flex items-center justify-center`
  - 数字: `text-2xl font-bold text-on-surface`
  - 标签: `text-sm text-on-surface-variant`
- 数据:
  | 图标 | 数字 | 标签 | 图标背景色 |
  |------|------|------|-----------|
  | forum | 12 | 今日提问 | bg-primary-90 |
  | priority_high | 3 | 待处理 | bg-red-50 (红色系) |
  | menu_book | 731 | 知识条目 | bg-emerald-50 (绿色系) |
  | task_alt | 5 | 今日审批 | bg-amber-50 (橙色系) |

**区块 C — 待处理提问**:
- 标题行: "待处理提问" + 右侧 "查看全部 →"（点击跳 /questions）
- 3 条提问卡片列表，每张:
  - `bg-white rounded-2xl p-4 border border-outline-variant/20`
  - 第一行: 学生姓名 + 学院标签（`bg-primary-95 text-primary rounded-full px-2 py-0.5 text-xs`）+ 时间 "10分钟前"
  - 第二行: 问题摘要（单行截断 `truncate`）
  - 第三行: 状态标签 + AI 置信度
  - 状态标签样式:
    - 待处理: `bg-amber-50 text-amber-700`
    - 处理中: `bg-blue-50 text-blue-700`
    - 已解决: `bg-emerald-50 text-emerald-700`

**Mock 数据**:
```ts
const questions = [
  { id: 1, studentName: '张小洋', department: '护理学院', question: '请问学校的电费缴纳在哪里操作？完美校园APP上找不到入口', time: '10分钟前', status: 'pending', aiConfidence: 0.32 },
  { id: 2, studentName: '李小辉', department: '临床医学院', question: '教务系统密码忘了怎么重置？', time: '25分钟前', status: 'pending', aiConfidence: 0.15 },
  { id: 3, studentName: '王伟', department: '药学院', question: '图书馆电子资源校外访问VPN怎么设置', time: '1小时前', status: 'processing', aiConfidence: 0.45 },
]
```

**区块 D — 快捷操作** (横向滑动):
- 标题: "快捷操作"
- 横向滚动容器 `flex gap-3 overflow-x-auto pb-2`
- 4 个圆角卡片按钮:
  | 图标 | 文字 | 颜色 |
  |------|------|------|
  | edit_note | 新建知识 | primary |
  | campaign | 发布通知 | blue |
  | bar_chart | 数据报告 | emerald |
  | settings | 系统设置 | gray |

---

#### 页面 3: QuestionsView.vue — 学生提问列表

**路由**: `/questions`
**有** TopAppBar（标题: "学生提问"，右侧: 搜索图标）+ BottomNavBar

**布局**:

**顶部 — 筛选 Tab 栏**:
- 横向滑动药丸形 Tab: `flex gap-2 px-5 py-3 overflow-x-auto`
- Tab 项: 全部(28) | 待处理(3) | 处理中(5) | 已解决(20)
- 激活态: `bg-primary text-white rounded-full px-4 py-2`
- 未激活: `bg-surface-container-low text-on-surface-variant rounded-full px-4 py-2`

**列表 — 提问卡片**:
- 卡片样式同 DashboardView 区块 C
- 额外信息: 每张卡片底部显示 "AI 置信度: 32%" 进度条
  - 进度条: `h-1 rounded-full bg-outline-variant/30`，填充部分根据置信度变色:
    - < 50%: `bg-red-400`
    - 50-80%: `bg-amber-400`
    - > 80%: `bg-emerald-400`
- 点击卡片 → 跳转 `/questions/:id`

**Mock 数据**: 8~10 条提问记录，混合不同状态

---

#### 页面 4: QuestionDetailView.vue — 提问详情（含对话和教师回复）

**路由**: `/questions/:id`
**有** TopAppBar（标题: "提问详情"，返回箭头）
**无** BottomNavBar（底部是回复输入框）

**这是最重要的页面，请特别用心设计。**

**布局 — 从上到下**:

**区块 A — 学生信息卡片**:
- `bg-surface-container-low rounded-3xl p-4 mx-5 mt-4`
- 头像(40px) + 姓名 + 学院/专业 + 年级
- 右侧: 状态标签（待处理/处理中/已解决）

**区块 B — AI 对话记录**（关键区域）:
- 标题: "AI 对话记录" + 对话时间
- 消息气泡列表（滚动区域 `flex-1 overflow-y-auto`）:
  
  **学生消息气泡**:
  - 右对齐
  - `bg-primary-90 text-on-surface rounded-2xl rounded-tr-md px-4 py-3 max-w-[80%] ml-auto`
  
  **AI 回复气泡**:
  - 左对齐
  - `bg-white text-on-surface rounded-2xl rounded-tl-md px-4 py-3 max-w-[80%] border border-outline-variant/20`
  - 左上角: AI 头像小圆 + "医小管AI"
  - 如果 AI 无法回答，显示拒答消息（红色边框）:
    `bg-red-50 border border-red-200 rounded-2xl px-4 py-3`
    "很抱歉，医小管目前尚未学习到相关说明，请咨询您的辅导员或相关负责老师。"
  
  **系统消息**:
  - 居中灰色文字 `text-center text-sm text-on-surface-variant py-2`
  - 如: "学生已呼叫老师 — 14:32"

  **教师消息气泡**（如果教师已回复）:
  - 左对齐
  - `bg-primary/10 text-on-surface rounded-2xl rounded-tl-md px-4 py-3 max-w-[80%] border border-primary/20`
  - 左上角: 教师头像 + "梁老师"
  - 与 AI 气泡用不同背景色区分

**区块 C — 操作区（固定底部）**:
- 如果状态是"待处理":
  - 大按钮: "接单处理" `bg-primary text-white w-full rounded-2xl h-12`
- 如果状态是"处理中"（已接单）:
  - 输入框 + 发送按钮（类似聊天输入）:
  - `fixed bottom-0 left-0 right-0 bg-white/90 backdrop-blur-xl border-t border-outline-variant/30 p-4`
  - 输入框: `bg-surface-container-low rounded-2xl px-4 py-3 flex-1`
  - 发送按钮: `bg-primary rounded-full w-10 h-10 flex items-center justify-center ml-2`
  - 输入框上方: 快捷回复建议 Tag（横向滚动）
    - "已为您查询到相关信息" / "请到XX部门咨询" / "稍后为您详细解答"
- 如果状态是"已解决":
  - 显示解决信息: "已由 梁老师 于 2026-04-11 14:35 回复解决"

**Mock 数据**:
```ts
const conversation = {
  student: { name: '张小洋', department: '护理学院', major: '护理学', grade: '2024级', avatar: '' },
  status: 'pending', // pending | processing | resolved
  messages: [
    { role: 'student', content: '请问学校的电费缴纳在哪里操作？完美校园APP上找不到入口', time: '14:20' },
    { role: 'ai', content: '很抱歉，医小管目前尚未学习到相关说明，请咨询您的辅导员或相关负责老师。', time: '14:20', isRefusal: true, confidence: 0.32 },
    { role: 'system', content: '学生已呼叫老师', time: '14:21' },
  ],
  escalation: { createdAt: '2026-04-11 14:21', reason: 'AI 无法回答' },
}
```

---

#### 页面 5: KnowledgeView.vue — 知识库管理

**路由**: `/knowledge`
**有** TopAppBar（标题: "知识库"，右侧: "+" 添加按钮）+ BottomNavBar

**布局**:

**顶部 — 搜索栏**:
- `mx-5 mt-3`
- 搜索输入框: `bg-surface-container-low rounded-2xl px-4 py-3 w-full` + 搜索图标

**分类 Tab**:
- 横向药丸 Tab: 全部 | 教务管理 | 学生服务 | 生活指南 | 校园信息
- 样式同 QuestionsView 筛选栏

**知识列表**:
- 卡片式列表，每张:
  - `bg-white rounded-2xl p-4 border border-outline-variant/20 mx-5 mb-3`
  - 标题: `text-base font-semibold text-on-surface` (单行截断)
  - 摘要: `text-sm text-on-surface-variant mt-1` (两行截断 `line-clamp-2`)
  - 底部: 分类标签 + 状态标签 + 更新时间
  - 状态标签:
    - 已发布: `bg-emerald-50 text-emerald-700`
    - 草稿: `bg-gray-100 text-gray-600`
    - 审核中: `bg-amber-50 text-amber-700`

**Mock 数据**: 8~10 条知识条目，涵盖不同分类和状态

---

#### 页面 6: KnowledgeDetailView.vue — 知识详情/编辑

**路由**: `/knowledge/:id`
**有** TopAppBar（标题: "知识详情"，返回箭头，右侧: 编辑图标）
**无** BottomNavBar

**布局**:
- Hero 区: 标题 + 分类标签 + 状态 + 创建时间/更新时间
- 正文: Markdown 渲染区域（`prose` 类）
- 底部操作栏:
  - 草稿状态: "提交审核" 按钮
  - 已发布: "下线" / "编辑" 按钮
  - 审核中: "审核通过" / "退回修改" 按钮（仅审核人员可见）

---

#### 页面 7: ProfileView.vue — 个人中心

**路由**: `/profile`
**有** TopAppBar（标题: "我的"）+ BottomNavBar

**布局**:

**区块 A — 个人信息卡片**:
- 紫色渐变背景卡片（同 Dashboard 欢迎横幅风格）
- 头像(64px) + 姓名 + 职称 + 所属学院
- 教师工号

**区块 B — 工作统计** (横向 3 格):
- `grid grid-cols-3 gap-3 mx-5`
- | 数字 | 标签 |
  |------|------|
  | 156 | 累计处理 |
  | 42 | 本月审批 |
  | 28 | 知识入库 |

**区块 C — 设置列表**:
- 标准列表样式，每行:
  - `flex items-center justify-between px-5 py-4 border-b border-outline-variant/10`
  - 左侧: 图标 + 文字
  - 右侧: 箭头 / Switch 开关
- 列表项:
  | 图标 | 文字 | 右侧 |
  |------|------|------|
  | notifications | 消息通知 | Switch 开关 |
  | volume_up | 声音提醒 | Switch 开关 |
  | smart_toy | AI 自动回复 | Switch 开关 + 说明文字 "置信度>90%自动回复" |
  | lock | 修改密码 | 箭头 → |
  | info | 关于系统 | 箭头 → |
  | logout | 退出登录 | 红色文字，无箭头 |

### 项目文件结构

```
teacher-mobile/
├── public/
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── TopAppBar.vue
│   │   └── BottomNavBar.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   ├── QuestionsView.vue
│   │   ├── QuestionDetailView.vue
│   │   ├── KnowledgeView.vue
│   │   ├── KnowledgeDetailView.vue
│   │   └── ProfileView.vue
│   ├── router/
│   │   └── index.ts
│   ├── App.vue
│   ├── main.ts
│   └── style.css          ← Tailwind directives + 自定义动画
├── index.html              ← 引入 Google Fonts (Manrope + Material Symbols)
├── tailwind.config.js
├── postcss.config.js
├── tsconfig.json
├── vite.config.ts
└── package.json
```

### 关键设计原则

1. **移动端优先**: 所有布局针对 375px~428px 宽度优化
2. **大圆角 + 毛玻璃**: 现代感，与学生端视觉统一
3. **紫色品牌调性**: 传递智慧/学术/专业感
4. **呼吸感**: 充足的间距（px-5, gap-4），不要拥挤
5. **入场动画**: 所有页面使用 `animate-fade-up` + 阶梯延迟
6. **触控反馈**: 所有可点击元素加 `active:scale-95 transition-transform`
7. **状态清晰**: 用颜色编码区分状态（绿=已解决，橙=待处理，蓝=处理中，红=紧急）
8. **内容层级**: 用 Surface Container 层级代替阴影来区分内容层级
9. **安全区适配**: 底部导航考虑 `env(safe-area-inset-bottom)`

### 特别注意

- **不要使用任何 UI 组件库**（如 Element Plus、Vant 等），全部用 Tailwind CSS 手写
- 确保所有页面都有对应的 mock 数据，页面打开即可看到完整效果
- 聊天气泡要区分四种角色: 学生（右侧紫底）、AI（左侧白底）、教师（左侧淡紫底）、系统（居中灰色）
- QuestionDetailView 是最核心的页面，交互最复杂，请重点打磨
- 颜色使用 Tailwind 自定义色彩，不要硬编码 hex 值到模板中

请生成所有文件的完整代码，确保 `npm install && npm run dev` 即可运行。
