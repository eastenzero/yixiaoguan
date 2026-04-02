# 学术智治系统 - 教师端 Web 应用

## 项目简介

基于 Vue 3 + TypeScript + Element Plus 构建的高密度侧边栏管理后台，专为教师设计，提供空教室审批、学生提问管理、知识库管理等功能。

## 技术栈

- **框架**: Vue 3.4 + TypeScript 5.4
- **构建工具**: Vite 6.0
- **UI 组件库**: Element Plus 2.9
- **状态管理**: Pinia 3.0
- **路由**: Vue Router 4.5
- **HTTP 客户端**: Axios 1.8
- **样式**: SCSS + CSS 变量

## 项目结构

```
src/
├── api/              # API 接口封装
│   └── auth.ts       # 认证相关接口
├── assets/           # 静态资源
│   └── main.css      # 全局样式
├── layouts/          # 布局组件
│   └── MainLayout.vue # 主布局（高密度侧边栏）
├── router/           # 路由配置
│   └── index.ts
├── stores/           # 状态管理
│   └── user.ts       # 用户状态
├── utils/            # 工具函数
│   └── request.ts    # Axios 封装
├── views/            # 页面视图
│   ├── LoginView.vue     # 登录页
│   ├── DashboardView.vue # 工作台
│   ├── QuestionsView.vue # 学生提问
│   ├── ApprovalView.vue  # 空教室审批
│   ├── KnowledgeView.vue # 知识库管理
│   ├── AnalyticsView.vue # 数据看板
│   ├── ProfileView.vue   # 个人中心
│   └── NotFoundView.vue  # 404页面
├── App.vue
└── main.ts
```

## 核心特性

### 1. 高密度侧边栏 Layout
- 翠绿色 Logo 区域，展示系统名称
- 菜单项包含图标和标题，选中状态有左侧绿条标记
- 底部个人中心和退出登录入口
- 与参考图高度还原的视觉风格

### 2. 登录/鉴权系统
- 现代化登录页面，响应式设计
- 支持用户名密码登录
- 验证码支持（与若依后端对接）
- Token 存储（Cookie）
- 路由守卫拦截未登录用户

### 3. Axios 封装
- 请求/响应拦截器
- 自动携带 Token
- 统一的错误处理
- 重复请求取消

### 4. 路由体系
- 基于角色的路由控制
- 路由守卫实现登录校验
- 404 页面处理

## 环境配置

### 开发环境 `.env.development`
```
VITE_API_BASE_URL=http://localhost:8080
VITE_APP_TITLE=学术智治系统
```

### 生产环境 `.env.production`
```
VITE_API_BASE_URL=/api
VITE_APP_TITLE=学术智治系统
```

## 启动命令

```bash
# 安装依赖
npm install

# 开发模式启动
npm run dev

# 构建生产环境
npm run build

# 代码格式化
npm run format
```

## 若依后端对接说明

### 登录接口
- 路径: `POST /api/login`
- 参数: `{ username, password, code?, uuid? }`
- 响应: `{ code: 200, msg: "...", data: { token, expires_in } }`

### 获取用户信息
- 路径: `GET /api/getInfo`
- 响应: `{ code: 200, msg: "...", data: { user, roles, permissions } }`

### 退出登录
- 路径: `POST /api/logout`

## 主题配色

```css
--primary-color: #10B981;      /* 主题绿 */
--primary-light: #34D399;      /* 浅绿 */
--primary-dark: #059669;       /* 深绿 */
--sidebar-width: 220px;        /* 侧边栏宽度 */
--header-height: 64px;         /* 顶部栏高度 */
```

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 作者

医小管智能服务平台 - 前端开发团队
