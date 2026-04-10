# Google Stitch 设计稿生成提示词

> 使用说明：将以下内容粘贴到 Google Stitch，生成与项目 1:1 对齐的 UI 设计稿。
> 生成后导出 ZIP（参考图+HTML/CSS），用于 Gemini CLI 实现。

---

## Prompt（直接复制到 Stitch）

Design a mobile app UI for "医小管" (YiXiaoGuan) — a smart campus assistant for Shandong First Medical University students.

### Brand & Theme
- **Primary color**: Deep academic purple (#7C3AED), with gradient variations (#5B21B6 → #8B5CF6)
- **Style**: Modern, clean, professional — suitable for a medical university
- **Corners**: Large rounded corners (16-24px)
- **Cards**: Elevated white cards with subtle purple-tinted shadows
- **Typography**: Chinese-first, clean sans-serif
- **Base width**: 375px (iPhone standard), mobile-only

### Color Palette
- Primary: #7C3AED (purple-600)
- Primary Light: #EDE9FE (purple-50)
- Primary Dark: #5B21B6 (purple-700)
- Background: #F8FAFC (slate-50)
- Card: #FFFFFF
- Text Primary: #0F172A (slate-900)
- Text Secondary: #64748B (slate-500)
- Success: #059669
- Warning: #D97706
- Error: #DC2626

### App Structure — 4 Tab Navigation Bar (bottom)
Tab icons with labels:
1. 🏠 **首页** (Home)
2. 💬 **智能问答** (AI Chat)
3. 🏢 **事务导办** (Services)
4. 👤 **我的** (Profile)

---

## Screen 1: Login Page (登录页)
- Full-screen purple gradient background (#5B21B6 → #8B5CF6)
- Centered white card with rounded corners
- Top: App logo (a simple academic-style icon) + "医小管" title + "智慧校园服务平台" subtitle
- Form fields (stacked vertically):
  - 学号 (Student ID) — text input with user icon
  - 密码 (Password) — password input with lock icon
  - 验证码 (Captcha) — text input + captcha image on the right (clickable to refresh)
- Large purple gradient button: "登录" (Login)
- Bottom small text: "初始密码与学号相同"
- No tab bar on this screen

## Screen 2: Home Page (首页) — Tab 1
- **Top welcome section**:
  - Left: Greeting "下午好，[用户名]" with date
  - Right: Small notification bell icon with badge count
- **AI search bar** (prominent, pill-shaped):
  - Left: Purple AI sparkle icon + "有什么可以帮你的？" placeholder
  - Right: Arrow send button
  - Below: Horizontal scrollable quick-ask tags/chips:
    "奖学金政策" "选课指南" "图书馆开放" "校园卡充值" "成绩查询"
- **Feature grid** (Bento-style cards):
  - Large card (full width): "AI 智能助手" — purple gradient bg, sparkle icon, subtitle "随时为你解答校园疑问"
  - Two small cards side by side:
    - "空教室预约" — calendar icon, show count "可预约 12 间"
    - "我的申请" — clipboard icon, show status "2 项进行中"
- **Quick links section** (title: "常用服务"):
  - List items with icon + title + arrow:
    - 📚 教务管理系统 (external link)
    - 📖 图书馆 (external link)
    - 📧 学生邮箱 (external link)
    - 🌐 学校官网 (external link)
- **Notification banner** at bottom (if any unread):
  - Purple-tinted background, bell icon + "你有 3 条未读通知"

## Screen 3: AI Chat Page (智能问答) — Tab 2
- **Custom navigation bar**: 
  - Center: "医小管" title
  - Right: History icon (clock) to view past conversations
  - Frosted glass/translucent background effect
- **Empty state** (when no messages):
  - Large purple gradient AI avatar/icon (centered)
  - "你好！我是医小管智能助手" welcome text
  - "我可以帮你解答校园生活中的各种问题" subtitle
  - Quick question chips grid (2 columns):
    "图书馆几点开门？"
    "怎么申请奖学金？"
    "校园卡怎么补办？"
    "选课有什么注意事项？"
- **Chat state** (with messages):
  - User message: Right-aligned, purple gradient bubble, white text, rounded corners (top-left, top-right, bottom-left rounded, bottom-right small)
  - AI message: Left-aligned, white/light-purple bubble, dark text
    - Top: Small AI avatar + "医小管" name label
    - Content: Supports rich text (bold, lists, quotes)
    - Bottom: Timestamp + copy button
  - **Source citations** (below AI message):
    - White card with left purple border
    - "📖 参考资料" header
    - Expandable list: source title + relevance score + click to view
  - AI typing indicator: Three pulsing dots
- **Bottom input area** (fixed):
  - Pill-shaped input field: "输入你的问题..." placeholder
  - Right: Purple send button (arrow icon)
  - Above input: Horizontal scrollable quick-question chips

## Screen 4: Chat History (对话历史)
- **Navigation bar**: Purple gradient background, "对话历史" title, back arrow
- **Conversation list** (cards):
  - Each card:
    - Title (first message or auto-generated title)
    - Status badge: 进行中(green) / 已关闭(gray) / 教师介入(orange)
    - Last message time + message count
    - Right arrow
  - Cards have subtle hover/press effect
- **Empty state**: Chat bubble icon + "还没有对话记录" + "开始新对话" button
- **FAB** (floating action button): Bottom-right, purple circle, plus icon — start new conversation

## Screen 5: Services Page (事务导办) — Tab 3
Design this as a **service portal / workbench** page, inspired by enterprise WeChat workbench style — categorized service entries with icons, linking to both in-app pages and external systems.

- **Navigation bar**: Frosted glass effect, "服务大厅" title
- **Hero section**: 
  - Purple gradient background card
  - "CAMPUS SERVICES" small English label
  - "校园服务中心" Chinese title
  - "一站式办理校园事务" subtitle

- **Section 1: "快捷入口"** (top row, 4 icons, prominent style with slightly larger icons):
  - 🏫 校(院)主页 (external link — placeholder)
  - 🌐 信息门户 (external link — placeholder)
  - 🏢 网上服务大厅 (external link — placeholder)
  - 🔔 统一消息平台 (external link — placeholder)
  Note: These 4 entries are placeholders that will link to the school's actual enterprise WeChat / official portal URLs. Design them as clickable cards with icon + label.

- **Section 2: "校园服务"** (4-column grid, purple-tinted circle icons):
  - Active items (colorful icons, clickable):
    - 🚪 空教室申请 (in-app → /pages/apply/classroom)
    - 📋 我的申请 (in-app → /pages/apply/status)
    - 🔧 网上报修 (external link — placeholder)
    - � 接诉即办 (external link — placeholder)
  - Active items (external links — placeholders):
    - 📢 辅导员通知 (external link — placeholder)
    - 🎓 学术讲座 (external link — placeholder)
    - 📺 直播山一大 (external link — placeholder)
    - 📸 证件照采集 (external link — placeholder)

- **Section 3: "查询服务"** (4-column grid):
  - 📅 学生课表 (external link — placeholder)
  - � 成绩查询 (external link — placeholder)
  - 📚 图书馆 (external link → library website)
  - 📧 学生邮箱 (external link — placeholder)

- **Section 4: "个人"** (4-column grid):
  - �️ 个人日程 (external link — placeholder)
  - ❓ 我的提问 (in-app → /pages/questions/index)

- **Design note**: External link items should show a small "↗" external link indicator on the icon corner. Placeholder items should look fully functional in the design (not grayed out) — the actual URLs will be configured later during development.

## Screen 6: Profile Page (我的) — Tab 4
- **Header section** (purple gradient background):
  - Left: "已认证身份" badge + 用户真名 + "计算机科学与技术学院 2023级"
  - Right: Large circular avatar with purple border
- **Quick stats** (2 columns, white cards):
  - "问答历史" — count + chat icon
  - "我的申请" — count + clipboard icon
- **Info cards** (Bento-style):
  - "学期进度" card: Progress bar (84% complete), "距离期末还有 23 天"
  - "AI 助手" card: Recent conversation preview, "继续对话" button
- **Settings list** (grouped):
  - Group 1: 消息通知, 系统设置
  - Group 2: 服务反馈, 帮助中心, 关于医小管
  - Each item: icon + label + right chevron
- **Bottom**: Red "退出登录" button + "医小管 v1.0.0" version text

## Screen 7: Classroom Booking Form (空教室申请)
- **Navigation bar**: Back arrow + "空教室预约"
- **Hero card**: Purple gradient, "预约申请单" title, calendar icon
- **Form sections** (white cards with section headers):
  - Section "时间信息":
    - 日期选择 (date picker)
    - 开始时间 (time picker)
    - 结束时间 (time picker)
  - Section "教室信息":
    - 教室选择 (dropdown/picker showing building + room)
    - 预计人数 (number input)
  - Section "申请信息":
    - 联系电话 (phone input)
    - 用途说明 (textarea, multi-line)
- **Bottom fixed**: Large purple "提交申请" button
- **Info card** at bottom: "申请规则" — processing time, rules reminder

## Screen 8: My Applications (我的申请)
- **Navigation bar**: Back arrow + "我的申请"
- **Hero section**: Purple gradient, "我的申请" title + total count
- **Filter tabs**: 全部 / 待审批 / 已通过 / 已拒绝
- **Application cards** (list):
  - Each card:
    - Top: Room name + Status badge (待审批=yellow, 已通过=green, 已拒绝=red)
    - Step indicator: ① 已提交 → ② 审核中 → ③ 已完成 (visual progress)
    - Details: Date, time range, purpose, headcount
    - Bottom: Submit time + Cancel button (only for pending)
- **Empty state**: Clipboard icon + "暂无申请记录" + "去预约" button
- **FAB**: Purple plus button — new application

## Screen 9: Application Detail (申请详情)
- **Hero section**: Room name prominently, status with pulsing indicator
- **Progress card**: 4-step horizontal progress bar
  - ① 已提交 ✓ → ② 审核中 (current, pulsing) → ③ 待补充 → ④ 已通过
- **Info summary card**: 
  - Application ID, submit time, room, date, time, headcount, purpose
- **Approval timeline** (vertical):
  - Each node: Icon + title + timestamp + description
  - "申请已提交" — check icon, green
  - "审核中" — clock icon, orange
  - If rejected: "审核未通过" — x icon, red, with quoted reason
- **Bottom actions**: "联系审批人" button + "修改申请" button

## Screen 10: My Questions / Tickets (我的提问)
- **Navigation bar**: Back arrow + "我的提问"
- **Filter tabs**: 全部 / 待处理 / 处理中 / 已解决
- **Ticket cards**:
  - Status badge (待处理=orange, 处理中=blue, 已解决=green)
  - Question summary (2 lines, truncated)
  - Creation time
  - Teacher assignment status
- **Empty state**: Question mark icon + "还没有提问记录" + "去提问" button

## Screen 11: Knowledge Detail (知识库详情)
- **Hero card**: Purple gradient background
  - Knowledge entry title (large)
  - Entry ID badge: "KB-20260410-0051"
  - Relevance score: "相关度 92%"
  - Category tag: "教务管理"
- **Tags section**: Horizontal pill tags (e.g., "选课", "学分", "培养方案")
- **Content area**: 
  - Rendered markdown content (headings, lists, bold text, quotes)
  - Clean typography, good line spacing
- **Bottom button** (if PDF available): "查看原始文件" button

## Screen 12: PDF Viewer
- Simple full-screen layout
- Top navigation bar: back arrow + document title
- Full-screen PDF/web-view content area

---

### Design Notes
- All screens should feel cohesive with consistent purple theme
- Use subtle animations concepts: cards appear with fade-up effect
- Shadows should have slight purple tint: rgba(124, 58, 237, 0.08)
- Active tab in bottom navigation: filled purple icon + purple label
- Inactive tab: outline gray icon + gray label
- All interactive elements should show pressed state (slightly darker)
- Chinese text throughout, professional academic tone
