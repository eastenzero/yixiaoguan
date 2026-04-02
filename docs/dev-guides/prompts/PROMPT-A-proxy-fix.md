# 【提示词 A】教师端前端联调修复（Vite 代理与 API 路径对齐）

> **状态**：待执行 | **预估工时**：30分钟 | **可并行**：是，与 Prompt-B/C 无依赖冲突

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 Vue3 前端工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（项目全局规则）
2. `apps/teacher-web/vite.config.ts`（当前 Vite 代理配置）
3. `apps/teacher-web/src/utils/request.ts`（axios 实例与 baseURL 配置）
4. `apps/teacher-web/src/api/dashboard.ts`（前端 API 调用路径样本）
5. `apps/teacher-web/src/api/questions.ts`（前端 API 调用路径样本）
6. `apps/teacher-web/.env.development`（当前环境变量）

**【现象与根因描述（必读）】**

当前存在 API 路径对齐问题，需要你读完代码后自行验证以下推断是否正确：

- Vite 代理规则：匹配 `/api`，转发至 `http://localhost:8080`，并用 rewrite 将 `/api` 前缀剥除
- 前端 API 文件（如 `dashboard.ts`）调用的路径均以 `/api/v1/` 开头
- 经过 rewrite 后，后端实际收到的是 `/v1/...`
- 但后端 Spring Boot Controller 的 `@RequestMapping` 注解路由为 `/api/v1/...`
- **结果**：所有业务接口 404

你需要选择以下两种方案之一，并在第一步规划时说明你的选择理由：

**方案 Option-1（推荐）**：去掉 Vite 代理中的 `rewrite` 规则，让 `/api/v1/...` 原样转发到后端，后端不动。
**方案 Option-2**：保留 rewrite，改前端所有 API 文件中的 URL，将 `/api/v1/` 改为 `/v1/`。

> ⚠️ **注意**：选 Option-1 时，需同步确认 `/captchaImage` 等特殊代理规则是否受影响。

**【你的交付物】**

1. 修改后的 `apps/teacher-web/vite.config.ts`（或各 api/*.ts 文件，取决于你选择的方案）
2. 若修改了 .env 文件，同步给出修改内容
3. 一份验证清单：列出至少 3 个修复后应能返回 200 的接口路径

**【禁止清单（严格遵守）】**

- ❌ 禁止修改任何后端代码（Java 文件）
- ❌ 禁止修改 `src/router/index.ts`
- ❌ 禁止修改 `src/stores/` 下的任何文件  
- ❌ 禁止引入任何新的 npm 依赖包
- ❌ 禁止改动 `src/views/` 下的页面组件
- ❌ 如需修改多个 API 文件，每个文件修改完后单独汇报，不要一次性全塞

**【工作方式】**

第一步：阅读背景材料，分析根因，说明你选择哪个方案及理由，列出你将修改的文件清单，等待我的"同意"。  
第二步：收到"同意"后，逐文件完成修改，每改一个文件汇报一次。

**【完成标准】**

✅ `vite.config.ts` 或 API 文件修改完毕，无语法错误  
✅ 前端开发服务器重启后，访问 `/api/v1/escalations/pending` 能在网络面板中看到非 404 响应  
✅ 访问 `/api/v1/knowledge/entries` 能在网络面板中看到非 404 响应  
✅ 登录流程（`/captchaImage`、`/api/v1/auth/login`）仍能正常工作，未被破坏

满足以上标准后，请明确回复 **"阶段任务 A 完成并停止"**，不要继续优化其他内容。

**现在，请开始第一步：阅读背景文档，分析根因，提交你的方案选择和文件修改清单。**
