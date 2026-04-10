# T3 任务: student-app 前端代码结构审计 + AI Studio Prompt 生成

## 任务背景
学生端前端 (apps/student-app/) 需要进行整体 UI 重构：
1. 主色调从青色/蓝色 → **紫色**（契合学校官网和校徽色调）
2. 整体 UI 质量提升（当前 Kimi 生成的 UI 审美较差）
3. 重构将由 Google AI Studio 完成，本任务目标是生成交给 AI Studio 的精确 prompt

## 任务目标

### Part 1: 代码结构审计

请全面阅读 `apps/student-app/src/` 下所有源文件，输出结构化报告，包含：

#### 1.1 项目技术栈
- 框架版本（Vue 2/3, React 等）
- 构建工具（Vite/Webpack）
- UI 框架/组件库（如有）
- 状态管理
- 路由方案
- CSS 方案（Tailwind / SCSS / CSS Modules / scoped CSS）
- HTTP 客户端

#### 1.2 路由与页面
列出所有路由，格式：
| 路径 | 组件文件 | 页面说明 |
|------|---------|---------|

#### 1.3 组件树
列出所有组件及其层级关系：
```
App.vue
├── Layout.vue (或类似)
│   ├── Navbar.vue
│   ├── RouterView
│   │   ├── Home.vue
│   │   ├── Chat.vue (AI 对话页)
│   │   ├── Knowledge.vue (知识库页)
│   │   ├── Services.vue (事务导办页)
│   │   └── ...
│   └── TabBar.vue (底部导航)
└── Login.vue
```

#### 1.4 后端 API 对接清单（⚠️ 最关键，重构时必须保留）
逐个列出所有 API 调用，格式：
| 文件 | 函数/方法 | API 端点 | 方法 | 说明 | 特殊处理 |
|------|----------|---------|------|------|---------|

特别标注：
- SSE 流式聊天（EventSource / fetch stream）
- 登录鉴权（token 存储/刷新/拦截器）
- 文件上传（如有）
- WebSocket（如有）

#### 1.5 状态管理
列出所有 store/state：
- 用户状态（token, userInfo）
- 聊天状态（messages, streaming）
- 其他全局状态

#### 1.6 当前样式分析
- 主色调色值（HEX/RGB）
- 配色方案（主色/辅助色/背景色/文字色）
- 布局方式（flex/grid/定位）
- 响应式策略
- 图标库

#### 1.7 静态资源
- 图片/图标文件清单
- 字体文件（如有）

### Part 2: AI Studio Prompt 生成

基于 Part 1 的审计结果，生成一份完整的 **AI Studio prompt**，要求：

#### Prompt 结构

```markdown
# 任务：山东第一医科大学学生端 App 前端重构

## 项目概述
[简述项目用途：校园AI助手学生端，包含AI对话、知识库浏览、事务导办等功能]

## 技术栈约束
[必须使用的技术栈，与现有保持一致]

## 设计要求

### 色彩方案
- 主色调：紫色系（建议 #7C3AED 或类似，需与山东第一医科大学校徽紫色协调）
- 提供完整色板：主色/浅色/深色/背景色/文字色/成功/警告/错误

### UI 风格
- 现代简约风格，圆角卡片设计
- 适合移动端（375px 宽度优先）
- 参考优秀校园类 App 设计

### 页面清单
[列出所有需要重构的页面及其功能描述]

## 必须保留的后端对接逻辑
[⚠️ 关键：列出所有 API 调用代码，要求 AI Studio 在重构时原封不动保留这些逻辑]

## 组件结构要求
[期望的组件组织方式]

## 事务导办页面特别说明
- 此页面只需要做入口跳转
- 企业微信入口：[URL placeholder]
- 学校官网入口：https://www.sdfmu.edu.cn
- 设计为卡片式链接列表即可

## 输出要求
- 输出完整的 Vue SFC 文件（.vue）
- 每个文件包含 <template>、<script setup> (或 Options API，与现有一致)、<style>
- 保留所有现有的 API 调用逻辑
- 不要删除任何功能，只改善 UI
```

#### Prompt 要求
1. prompt 必须足够精确，让 AI Studio 不需要看源码就能理解项目结构
2. 后端对接逻辑必须逐行列出，标注"不可修改"
3. 色彩方案给出具体 HEX 值
4. 每个页面给出详细的布局描述和交互说明

## 输出文件

将完整报告写入 `kimi/report-v9-frontend-audit.md`，包含：
1. Part 1 代码结构审计（全部 7 个子项）
2. Part 2 AI Studio Prompt（可直接复制使用的完整 prompt）

## 注意事项
- 阅读每个 .vue / .ts / .js / .css 文件的完整内容
- 不要遗漏任何 API 调用或状态管理逻辑
- 特别关注 SSE/流式聊天的实现细节
- 如发现配置文件（.env, config.ts 等）也要记录
- 当前项目可能有一些 TODO/技术债，也请记录
