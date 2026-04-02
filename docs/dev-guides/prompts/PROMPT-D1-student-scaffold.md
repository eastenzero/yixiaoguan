# 【提示词 D1】学生端 uni-app 项目骨架搭建（基础层）

> **状态**：待执行 | **预估工时**：2小时 | **依赖**：无前置，必须先于 D2/D3 完成  
> **执行完成后**：D2（对话页）和 D3（申请页）可以**并行**发布

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 uni-app 前端工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（项目全局规则，包含技术栈约定：学生端为 uni-app + TypeScript，H5 优先）
2. `docs/dev-guides/ai-antipatterns.md`（**错题本，必读**）
3. `_references/前端风格/学生移动端/jade_scholar/DESIGN.md`（**设计规范文档，必读——包含颜色系统、排版规则、组件规范**）
4. `_references/前端风格/学生移动端/_1/screen.png`（参考截图：AI 对话页）
5. `_references/前端风格/学生移动端/_2/screen.png`（参考截图：空教室申请表单）
6. `apps/teacher-web/src/utils/request.ts`（参考教师端的 axios 封装模式，学生端对应改为 uni.request 封装）
7. `apps/teacher-web/src/stores/user.ts`（参考教师端的 Pinia 用户状态管理模式）
8. `docs/database/schema-phase1.md`（了解 `yx_user` 表的字段结构，尤其是 `student_id`、`real_name`、`class_name`、`grade`、`department`）
9. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/auth/controller/AuthController.java`（了解现有的登录接口 `/api/v1/auth/login` 的入参/出参格式）

**【任务说明】**

`apps/student-app/` 目前是**完全空目录**。你需要从零初始化一个 uni-app + Vue 3 + TypeScript 项目，并完成以下基础层建设：

**阶段一：项目初始化**
- 在 `apps/student-app/` 目录下初始化 uni-app 项目（使用 HBuilderX 命令行 / Vue CLI 方式初始化，选择 Vue 3 + TypeScript 模板）
- 配置好 `manifest.json`（H5 模式，appid 不填，title 配置为"医小管"）
- 配置好 `pages.json`（见下方页面列表）
- 配置好 `vite.config.ts` 或 `vue.config.js`，让 H5 开发服务在 **5174 端口**运行（和教师端 5173 区分），并配置 API 代理：`/api` → `http://localhost:8080`

**阶段二：工具层**
- `src/utils/request.ts`：基于 `uni.request` 封装的 HTTP 工具，支持 JWT 自动注入、统一错误处理（401 跳转登录）、统一响应格式解析（`{ code, msg, data }`）
- `src/stores/user.ts`：Pinia 用户状态（token、userInfo、isLoggedIn），含持久化到 `uni.setStorageSync`

**阶段三：路由定义（pages.json）**
需要预先定义所有页面路由（后续 D2/D3 会填充内容），本次只需建空页面文件：

```json
// pages.json 结构
{
  "pages": [
    { "path": "pages/login/index", "style": { "navigationBarTitleText": "登录" } },
    { "path": "pages/home/index", "style": { "navigationBarTitleText": "首页" } },
    { "path": "pages/chat/index", "style": { "navigationBarTitleText": "AI 咨询" } },
    { "path": "pages/questions/index", "style": { "navigationBarTitleText": "我的提问" } },
    { "path": "pages/apply/classroom", "style": { "navigationBarTitleText": "空教室申请" } },
    { "path": "pages/apply/status", "style": { "navigationBarTitleText": "我的申请" } },
    { "path": "pages/profile/index", "style": { "navigationBarTitleText": "个人中心" } }
  ],
  "tabBar": {
    "color": "#999",
    "selectedColor": "#00685f",
    "list": [
      { "pagePath": "pages/home/index", "text": "首页", "iconPath": "...", "selectedIconPath": "..." },
      { "pagePath": "pages/chat/index", "text": "咨询", "iconPath": "...", "selectedIconPath": "..." },
      { "pagePath": "pages/apply/status", "text": "申请", "iconPath": "...", "selectedIconPath": "..." },
      { "pagePath": "pages/profile/index", "text": "我的", "iconPath": "...", "selectedIconPath": "..." }
    ]
  }
}
```

> tabBar 的图标可以使用 Unicode emoji 或空白 1x1 透明 png 占位，不要因为图标未准备好就卡住。

**阶段四：登录页面（`pages/login/index.vue`）**

实现完整功能：
- 用户名（学号）+ 密码输入
- 调用 `POST /api/v1/auth/login`（参数格式和教师端一致，但需要验证码吗？→ 需确认：如果 AuthController 要求验证码，则也需加验证码区域；如不要求，则省略）
- 登录成功后保存 token 和 userInfo 到 Pinia + Storage，跳转首页
- 登录失败弹出 `uni.showToast` 提示

**阶段五：首页（`pages/home/index.vue`）**

实现完整功能：
- 顶部欢迎语（显示用户 real_name）
- 4 个功能入口模块（宫格/卡片布局）：
  - 🗨️ **AI 咨询** → 跳转 `/pages/chat/index`
  - 🏫 **空教室申请** → 跳转 `/pages/apply/classroom`
  - 📋 **申请进度** → 跳转 `/pages/apply/status`
  - 📚 **知识问答** → 跳转 `/pages/chat/index`（复用）
- 底部公告/通知区域（调用 `GET /api/v1/notifications?pageSize=3`，若接口不可用则显示占位文本）

**【样式要求】**

- 主题色：`#00685f`（与教师端一致）
- 使用 `<style scoped lang="scss">`
- 字体：系统默认，不引入外部字体
- 首页风格：简洁明快，大卡片入口，适合移动端点击

**【你的交付物】**

1. `apps/student-app/` 目录下完整的 uni-app 项目骨架（所有空页面文件 + 配置文件）
2. `src/utils/request.ts`（封装完成）
3. `src/stores/user.ts`（封装完成）
4. `pages/login/index.vue`（功能完整）
5. `pages/home/index.vue`（功能完整）
6. 其他所有页面（`chat`、`questions`、`apply/classroom`、`apply/status`、`profile`）只需建空文件，内容为 `<template><view>页面开发中</view></template>`

**【禁止清单（严格遵守）】**

- ❌ 禁止在 D1 阶段开发 chat 和 apply 页面的具体功能，那是 D2/D3 的任务
- ❌ 禁止引入 Element Plus、Vant 等 PC 端组件库（uni-app 有自己的组件体系，或使用 uView/uni-ui）
- ❌ 禁止使用 Vue Router（uni-app 路由由 `pages.json` + `uni.navigateTo` 管理）
- ❌ 禁止使用 `axios`（使用 `uni.request` 封装）
- ❌ 禁止修改 `apps/teacher-web/` 下的任何文件
- ❌ 禁止修改后端代码
- ❌ 如果初始化方式不确定（HBuilderX CLI 还是 @dcloudio/uni-create-project），先停下来说明你的方案，等我确认

**【工作方式】**

第一步：读完所有背景材料，说明你选择的项目初始化方式（命令），列出完整的文件创建清单，等待我的"同意"。  
第二步：收到"同意"后，按初始化 → 工具层 → 路由配置 → 登录页 → 首页的顺序逐步推进，每完成一个阶段汇报。

**【完成标准】**

✅ `npm run dev:h5`（或对应命令）能在 5174 端口启动 H5 开发服务，无编译报错  
✅ 浏览器访问 `http://localhost:5174` 能看到登录页面  
✅ 输入测试账号（用户名：`4523570155`，密码：`admin123`）能成功登录并跳转首页  
✅ 首页四个功能入口可见，点击能跳转对应页面（即使页面只有占位文字）

**【完成汇报文件（必须交付，不可跳过）】**

满足完成标准后，将本次交付报告写入：  
`docs/test-reports/TASK-D1-student-scaffold-completion-report.md`

报告章节：① 实际创建/修改的文件清单 ② 验证结果（逐条对齐完成标准）③ 遗留问题 ④ 新发现错误模式（供更新错题本）⑤ 下一步建议（包括告知 D2/D3 可以开始了）

汇报文件写完后，请明确回复 **"阶段任务 D1 完成并停止"**。

**现在，请开始第一步：阅读背景材料，说明你的初始化方案，提交文件清单。**
