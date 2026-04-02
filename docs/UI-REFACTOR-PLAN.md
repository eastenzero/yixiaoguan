# 学生移动端 UI 改造计划

> 目标：将现有 uni-app 项目界面风格完全对齐参考项目（React/Tailwind 样例）
> 技术栈：Vue 3 + uni-app + SCSS（保持现有栈，仅改造样式）

---

## 一、设计系统对齐

### 1.1 颜色变量统一

将现有 SCSS 变量与参考项目的 MD3 颜色系统对齐：

```scss
// src/uni.scss 或新建 src/styles/theme.scss
// Primary (Teal)
$primary: #006565;
$primary-container: #008080;
$on-primary: #ffffff;
$on-primary-container: #e3fffe;
$primary-fixed: #93f2f2;
$primary-fixed-dim: #76d6d5;

// Secondary (Blue)
$secondary: #206393;
$secondary-container: #90c9ff;
$on-secondary: #ffffff;
$on-secondary-container: #035584;
$secondary-fixed: #cee5ff;
$secondary-fixed-dim: #96ccff;

// Tertiary (Orange/Brown)
$tertiary: #8b4823;
$tertiary-container: #a96039;
$on-tertiary: #ffffff;
$on-tertiary-container: #fff9f7;
$tertiary-fixed: #ffdbcb;
$tertiary-fixed-dim: #ffb692;

// Surface
$surface: #f6faf9;
$surface-dim: #d7dbda;
$surface-bright: #f6faf9;
$surface-variant: #dfe3e2;
$on-surface: #181c1c;
$on-surface-variant: #3e4949;

// Surface Containers
$surface-container-lowest: #ffffff;
$surface-container-low: #f0f4f3;
$surface-container: #ebefee;
$surface-container-high: #e5e9e8;
$surface-container-highest: #dfe3e2;

// Outline
$outline: #6e7979;
$outline-variant: #bdc9c8;

// Error
$error: #ba1a1a;
$error-container: #ffdad6;
$on-error: #ffffff;
$on-error-container: #93000a;

// Background
$background: #f6faf9;
$on-background: #181c1c;

// Inverse
$inverse-surface: #2c3131;
$inverse-on-surface: #edf2f1;
$inverse-primary: #76d6d5;
```

### 1.2 字体系统

```scss
// 字体家族
$font-headline: "Plus Jakarta Sans", "Noto Sans SC", "PingFang SC", sans-serif;
$font-body: "Inter", "Noto Sans SC", "PingFang SC", sans-serif;
$font-label: "Inter", "Noto Sans SC", "PingFang SC", sans-serif;
```

### 1.3 阴影与圆角

```scss
// 阴影（参考 Tailwind 的 shadow 值转换）
$shadow-sm: 0 2rpx 8rpx rgba(0, 0, 0, 0.04);
$shadow-md: 0 8rpx 24rpx rgba(0, 0, 0, 0.06);
$shadow-lg: 0 12rpx 32rpx rgba(0, 106, 106, 0.08);
$shadow-xl: 0 16rpx 48rpx rgba(0, 106, 106, 0.12);

// 圆角
$radius-sm: 12rpx;
$radius-md: 20rpx;
$radius-lg: 24rpx;
$radius-xl: 32rpx;
$radius-2xl: 48rpx;
$radius-full: 9999rpx;
```

### 1.4 通用工具类

```scss
// src/styles/utilities.scss

// 滚动条隐藏
.scrollbar-hide {
  &::-webkit-scrollbar { display: none; }
  -ms-overflow-style: none;
  scrollbar-width: none;
}

// 文本截断
.line-clamp-1 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

// 入场动画
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(40rpx); }
  to { opacity: 1; transform: translateY(0); }
}

.staggered-1 { animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.1s; }
.staggered-2 { animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.2s; }
.staggered-3 { animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.3s; }
.staggered-4 { animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.4s; }
.staggered-5 { animation: fadeUp 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) backwards; animation-delay: 0.5s; }
```

---

## 二、页面改造详情

### 2.1 首页 (pages/home/index.vue)

#### 视觉结构对比

| 现有布局 | 参考布局 | 改造动作 |
|---------|---------|---------|
| 背景渐变洗刷 | 纯白背景 + 顶部渐变 | 对齐参考：移除大面积渐变，改为顶部小范围渐变 |
| 大排版欢迎区 | 紧凑型欢迎区 + 状态卡片 | 添加"当前活跃申请"状态小卡片 |
| AI Hero 卡片（圆角较小） | AI 输入条（圆角极大） | 改为圆角全满的药丸形输入条 |
| 标签横向滚动 | 标签横向滚动 | 保持，但样式改为圆角 pill |
| 四宫格服务矩阵 | Bento Grid（2x2 + 跨列卡片） | 改为 Bento Grid：任务指引跨2列，下方两个卡片 |
| 通知列表 | 官方校园链接卡片列表 | 改为带图标 + 英文副标题的链接卡片 |

#### 具体改造点

1. **欢迎区改造**
   ```vue
   <!-- 新增：状态摘要小卡片 -->
   <view class="status-mini-card" @click="goToApplyStatus">
     <view class="pulse-dot"></view>
     <text class="status-text">当前活跃申请: {{ activeCount }}</text>
   </view>
   ```

2. **AI 输入区改造**
   - 改为药丸形（rounded-full）
   - 左侧 AI 标识改为文字徽章
   - 右侧箭头按钮改为圆形发送按钮
   - 添加阴影：shadow-[0px_12px_32px_rgba(0,106,106,0.08)]

3. **服务矩阵 → Bento Grid**
   ```vue
   <view class="bento-grid">
     <!-- 跨列大卡片 -->
     <view class="bento-card bento-card-large" @click="goToServices">
       <view class="card-bg-effect"></view>
       <view class="card-content">
         <ClipboardCheck class="card-icon" />
         <view class="card-text">
           <text class="card-title">任务指引</text>
           <text class="card-desc">查看本周待完成的学术与行政任务</text>
         </view>
       </view>
       <ArrowRight class="card-arrow" />
     </view>
     
     <!-- 下方两个小卡片 -->
     <view class="bento-card" @click="goToClassroomApply">
       <view class="icon-box bg-secondary">
         <Armchair class="icon" />
       </view>
       <text class="card-title">空教室预约</text>
       <text class="card-desc">实时查看并预约学习空间</text>
     </view>
     
     <view class="bento-card" @click="goToApplyStatus">
       <view class="icon-box bg-tertiary">
         <Activity class="icon" />
       </view>
       <text class="card-title">申请进度</text>
       <text class="card-desc">追踪您的所有审批状态</text>
     </view>
   </view>
   ```

4. **新增：官方校园链接区**（占位功能）
   ```vue
   <view class="links-section">
     <text class="section-title">官方校园链接</text>
     <view class="link-list">
       <view class="link-card" v-for="link in officialLinks" :key="link.name">
         <view class="link-icon-wrap">
           <component :is="link.icon" class="link-icon" />
         </view>
         <view class="link-text">
           <text class="link-name">{{ link.name }}</text>
           <text class="link-en">{{ link.nameEn }}</text>
         </view>
         <ArrowRight class="link-arrow" />
       </view>
     </view>
   </view>
   ```

5. **新增：底部通知 Banner**
   ```vue
   <view class="notice-banner">
     <Info class="notice-icon" />
     <view class="notice-content">
       <text class="notice-title">新学期注册提醒</text>
       <text class="notice-desc">2023秋季学期注册将于下周五截止...</text>
     </view>
   </view>
   ```

---

### 2.2 AI 咨询页 (pages/chat/index.vue)

#### 视觉结构对比

| 现有布局 | 参考布局 | 改造动作 |
|---------|---------|---------|
| 顶部导航栏（自定义） | 顶部导航栏（更简洁） | 简化样式，使用 MD3 颜色 |
| 消息气泡（圆角较小） | 消息气泡（圆角更大，差异化圆角） | 用户：右下小圆角，AI：左下小圆角 |
| 底部输入区（方形） | 底部输入区（药丸形，悬浮） | 改为悬浮药丸输入条 |
| 无快速推荐区 | "猜你想问" 卡片 | 新增该区域 |
| 无快捷标签 | 底部快捷标签 | 添加底部快捷操作标签 |

#### 具体改造点

1. **新增：猜你想问区**（顶部）
   ```vue
   <view class="quick-questions" v-if="messageList.length === 0">
     <view class="section-header">
       <Lightbulb class="header-icon" />
       <text class="header-title">猜你想问</text>
     </view>
     <view class="question-list">
       <view class="question-item" v-for="q in suggestedQuestions" :key="q" @click="askQuestion(q)">
         <text class="question-text">{{ q }}</text>
         <ChevronRight class="question-arrow" />
       </view>
     </view>
   </view>
   ```

2. **消息气泡改造**
   - 用户消息：bg-primary, rounded-2xl rounded-tr-sm
   - AI 消息：bg-surface-container-lowest, border, rounded-2xl rounded-tl-sm

3. **底部输入区改造**
   ```vue
   <view class="floating-input-bar">
     <view class="input-container">
       <button class="mic-btn">
         <Mic class="icon" />
       </button>
       <input class="message-input" placeholder="咨询你的校园疑问..." />
       <button class="send-btn">
         <Send class="icon" />
       </button>
     </view>
   </view>
   ```

4. **新增：底部快捷标签**
   ```vue
   <view class="quick-tags">
     <text class="tag" v-for="tag in quickTags" :key="tag">{{ tag }}</text>
   </view>
   ```

---

### 2.3 教室申请页 (pages/apply/classroom.vue)

参考样例代码中的 `BookingFormScreen.tsx` 风格，但保持现有表单项。

#### 改造点

1. **顶部引导区**
   ```vue
   <view class="form-hero">
     <view class="hero-content">
       <text class="hero-title">预约申请单</text>
       <text class="hero-desc">请填写下方表单，我们将根据教学资源占用情况在24小时内完成审核。</text>
     </view>
     <CalendarDays class="hero-bg-icon" />
   </view>
   ```

2. **表单分区标题**
   - 添加左侧竖线装饰：`<view class="section-divider"></view>`
   - 每个区块添加图标前缀

3. **卡片式表单容器**
   - 每个 section 改为 `bg-surface-container-lowest rounded-xl p-5`

4. **提交按钮改造**
   - 改为渐变背景：`bg-gradient-to-br from-primary to-primary-container`
   - 药丸形状：`rounded-full`
   - 添加阴影：`shadow-lg`

5. **新增：底部信息区**
   ```vue
   <view class="form-footer">
     <view class="footer-card">
       <Gavel class="footer-icon" />
       <text class="footer-title">申请规则</text>
       <text class="footer-text">1. 至少提前2个工作日申请...</text>
     </view>
     <view class="footer-card">
       <ListChecks class="footer-icon" />
       <text class="footer-title">审核流程</text>
       <text class="footer-text">1. 提交申请单...</text>
     </view>
   </view>
   ```

---

### 2.4 申请进度页 (pages/apply/status.vue)

当前是列表页，参考样例中的 `ProgressTrackingScreen.tsx` 风格进行美化，同时保留列表功能。

#### 改造点

1. **页面标题区改造**
   ```vue
   <view class="page-hero">
     <text class="hero-label">Progress Tracking</text>
     <text class="hero-title">我的申请</text>
     <text class="hero-subtitle">查看空教室申请进度与历史记录</text>
   </view>
   ```

2. **新建申请按钮改造**
   - 改为圆角大按钮，带图标

3. **申请卡片改造**
   - 添加状态步骤指示器（简化版 Stepper）
   - 审批意见改为时间线样式展示
   - 状态徽章颜色对齐 MD3

4. **新增：申请详情页**（可选，作为第二阶段）
   - 完整复刻 `ProgressTrackingScreen` 的时间线样式
   - 作为点击卡片后的详情页

---

### 2.5 个人中心页 (pages/profile/index.vue)

#### 视觉结构对比

| 现有布局 | 参考布局 | 改造动作 |
|---------|---------|---------|
| 大头像 + 用户信息 | 类似，但布局更紧凑 | 保持现有布局，微调样式 |
| 双宫格快捷入口 | Bento Grid（更多内容） | 保持双宫格，但参考样式 |
| 设置列表 | 设置列表 + 学期进度卡片 + AI历史 | 新增学期进度卡片和AI历史卡片 |

#### 改造点

1. **新增：学期进度卡片**（占位功能）
   ```vue
   <view class="semester-card">
     <text class="card-title">学期进度</text>
     <view class="progress-info">
       <text class="progress-text">第 12 周 / 共 18 周</text>
       <text class="progress-percent">67%</text>
     </view>
     <view class="progress-bar">
       <view class="progress-fill" style="width: 67%"></view>
     </view>
     <view class="todo-section">
       <text class="todo-label">待办提醒</text>
       <text class="todo-text">您有 2 项课程作业即将截止...</text>
     </view>
   </view>
   ```

2. **新增：AI 助手历史卡片**（占位功能）
   ```vue
   <view class="ai-history-card">
     <view class="card-header">
       <Bot class="header-icon" />
       <text class="header-title">AI 助手历史</text>
       <ChevronRight class="header-arrow" />
     </view>
     <view class="history-list">
       <view class="history-item" v-for="item in aiHistory" :key="item.id">
         <text class="item-question">{{ item.question }}</text>
         <text class="item-answer" line-clamp-1>{{ item.answer }}</text>
         <view class="item-meta">
           <text class="item-time">{{ item.time }}</text>
           <text class="item-tag">{{ item.tag }}</text>
         </view>
       </view>
     </view>
   </view>
   ```

3. **新增：常用服务列表**（占位功能）
   ```vue
   <view class="favorite-services">
     <text class="section-title">常用服务</text>
     <view class="service-list">
       <view class="service-item" v-for="svc in favoriteServices" :key="svc.name">
         <view class="service-icon" :class="svc.colorClass">
           <component :is="svc.icon" />
         </view>
         <view class="service-info">
           <text class="service-name">{{ svc.name }}</text>
           <text class="service-desc">{{ svc.desc }}</text>
         </view>
         <ChevronRight class="service-arrow" />
       </view>
     </view>
   </view>
   ```

---

### 2.6 底部导航栏 (pages.json 中的 tabBar)

当前使用 uni-app 原生 tabBar，样式调整空间有限。建议改为自定义组件实现。

#### 方案选择

**方案 A：保持原生 tabBar，仅调整颜色**
- 修改 `pages.json` 中的颜色配置
- 快速但效果有限

**方案 B：使用自定义 tabBar 组件**（推荐）
- 完全复刻参考项目的底部导航样式
- 需要修改 `pages.json` 配置和创建组件

#### 参考样式实现

```vue
<!-- components/CustomTabBar.vue -->
<template>
  <view class="custom-tab-bar">
    <view 
      class="tab-item" 
      :class="{ active: current === 'home' }"
      @click="switchTab('home')"
    >
      <Home class="tab-icon" />
      <text class="tab-text">Home</text>
    </view>
    <view 
      class="tab-item" 
      :class="{ active: current === 'assistant' }"
      @click="switchTab('assistant')"
    >
      <Bot class="tab-icon" />
      <text class="tab-text">Assistant</text>
    </view>
    <view 
      class="tab-item" 
      :class="{ active: current === 'services' }"
      @click="switchTab('services')"
    >
      <LayoutGrid class="tab-icon" />
      <text class="tab-text">Services</text>
    </view>
    <view 
      class="tab-item" 
      :class="{ active: current === 'profile' }"
      @click="switchTab('profile')"
    >
      <User class="tab-icon" />
      <text class="tab-text">Profile</text>
    </view>
  </view>
</template>

<style>
.custom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-around;
  padding: 12rpx 32rpx calc(24rpx + env(safe-area-inset-bottom));
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 48rpx 48rpx 0 0;
  box-shadow: 0px -4px 20px rgba(0, 106, 106, 0.08);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12rpx 40rpx;
  color: #94a3b8;
  transition: all 0.2s;
}

.tab-item.active {
  color: #006565;
  background: rgba(0, 101, 101, 0.08);
  border-radius: 24rpx;
  transform: scale(0.9);
}
</style>
```

---

## 三、组件清单

### 3.1 需要创建的公共组件

| 组件名 | 用途 | 复杂度 |
|-------|------|-------|
| `SvgIcon.vue` | 统一封装 Lucide 风格 SVG 图标 | 中 |
| `BentoCard.vue` | Bento Grid 卡片 | 低 |
| `StatusBadge.vue` | 状态徽章（带颜色） | 低 |
| `LinkCard.vue` | 链接列表项 | 低 |
| `TimelineItem.vue` | 时间线项 | 中 |
| `ProgressBar.vue` | 进度条 | 低 |

### 3.2 SVG 图标清单

从 lucide-react 中提取以下图标转为 Vue 组件：

- Home, Bot, LayoutGrid, User (导航)
- ArrowRight, ChevronRight (箭头)
- Ticket, DoorOpen, GraduationCap, ClipboardCheck, Armchair, Activity (首页图标)
- Globe, Library, Mail, Info (链接图标)
- Lightbulb, Send, Mic (聊天图标)
- CalendarDays, Calendar, Clock, Users, FileText (表单图标)
- Check, CheckCircle2, Search, History, Clock (状态图标)
- Edit2, CreditCard, Wrench, Star, Wallet, Shield, Bell, MessageSquare, HelpCircle, LogOut (个人中心图标)

---

## 四、实施顺序建议

### Phase 1: 基础设施 (1天)
1. 创建主题变量文件 `src/styles/theme.scss`
2. 创建工具类文件 `src/styles/utilities.scss`
3. 在 `App.vue` 中全局引入
4. 创建基础图标组件

### Phase 2: 首页改造 (1天)
1. 重写首页样式
2. 新增 Bento Grid 布局
3. 新增官方链接区（占位）
4. 新增底部通知 Banner

### Phase 3: 聊天页改造 (0.5天)
1. 新增猜你想问区
2. 改造消息气泡样式
3. 改造底部输入区
4. 新增快捷标签

### Phase 4: 申请相关页面 (0.5天)
1. 教室申请页样式改造
2. 申请进度页样式改造

### Phase 5: 个人中心 (0.5天)
1. 新增学期进度卡片（占位）
2. 新增 AI 历史卡片（占位）
3. 新增常用服务列表（占位）

### Phase 6: 底部导航 (0.5天)
1. 评估是否使用自定义 tabBar
2. 实施选定的方案

---

## 五、占位功能说明

以下功能在参考设计中有，但当前需求/接口尚未支持，作为占位符实现：

| 功能 | 位置 | 实现方式 |
|-----|------|---------|
| 官方校园链接 | 首页底部 | 静态数据 + 点击提示"功能开发中" |
| 学期进度 | 个人中心 | 静态展示，连接 mock 数据 |
| AI 助手历史 | 个人中心 | 静态展示，点击跳转聊天页 |
| 常用服务 | 个人中心 | 静态列表，点击提示"功能开发中" |
| 任务指引 | 首页 Bento | 点击提示"功能开发中" |

---

## 六、注意事项

1. **rpx 转换**：Tailwind 的 px 值需要转换为 rpx（1px ≈ 0.5rpx）
2. **safe-area**：底部输入区和导航栏需要适配 iPhone 安全区
3. **dark mode**：参考项目未提供暗色模式，暂不支持
4. **动画性能**：入场动画使用 transform 和 opacity，避免触发重排
5. **图标大小**：uni-app 中使用 SVG 需要调整 viewBox 和尺寸

---

## 七、验收标准

- [ ] 所有页面颜色与参考项目一致
- [ ] 圆角、阴影、间距符合设计系统
- [ ] 首页 Bento Grid 布局正确
- [ ] 底部导航样式与参考一致（或接近）
- [ ] 所有现有功能正常工作
- [ ] 占位功能有点击反馈
