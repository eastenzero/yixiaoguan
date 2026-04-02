# 【提示词 D4】学生端前后端联调 + AI 接入

> **状态**：待执行 | **预估工时**：2~3小时  
> **前置依赖**：TASK-D1、D2、D3 均已完成  
> **目标**：把 D2/D3 已经写好但还跑在 mock 上的代码，全部对接真实后端和真实 AI 服务

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**全栈联调工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（**必读**：包含本机 Java/Maven 非标准路径、数据库密码、服务启动命令）
2. `docs/dev-guides/ai-antipatterns.md`（**错题本，必读**）
3. `docs/test-reports/completion-reports/TASK-D2-chat-page-completion-report.md`（D2 的遗留问题清单）
4. `docs/test-reports/completion-reports/TASK-D3-apply-page-completion-report.md`（D3 的遗留问题清单）
5. `apps/student-app/src/pages/chat/index.vue`（D2 已实现的对话页，注意其中的 mock AI 调用部分）
6. `apps/student-app/src/api/chat.ts`（D2 已实现的 chat API 封装）
7. `apps/student-app/src/api/apply.ts`（D3 已实现的申请 API 封装）
8. `services/ai-service/app/api/chat.py`（AI 服务接口定义，重点：请求参数格式和响应格式）

**【本次任务概述】**

这是一次**纯联调任务**——代码逻辑 D2/D3 已完成，你只需要：
1. 验证各接口是否连通
2. 修复连通时发现的数据格式问题
3. 将 AI 对话从 mock 切换到真实调用

不允许重构已有页面逻辑，只做**最小范围修改**使联调通过。

---

## 联调任务清单（按顺序执行）

### ✅ 验证项 1：验证码接口确认

**问题背景**：D1 报告遗留 —— 前端调用了 `/api/v1/auth/captcha`，但不确定后端是否存在此接口。

**操作步骤**：
1. 读取 `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/auth/controller/AuthController.java`，确认验证码接口的实际路径
2. 同时确认登录接口 `/api/v1/auth/login` 的请求参数（是否包含 `captchaKey` + `captchaCode`）
3. 对比 `apps/student-app/src/api/auth.ts` 中前端实际发送的登录参数
4. 如果路径或参数不匹配，修正 `apps/student-app/src/api/auth.ts` 使其与后端对齐

**完成标准**：登录接口路径和参数格式前后端完全匹配（无需真实运行，代码核查通过即可）

---

### ✅ 验证项 2：AI 对话接入真实 ai-service

**问题背景**：D2 中 `pages/chat/index.vue` 的 `callAIService()` 函数使用 1.5s 定时器 mock，真实调用代码已注释。

**已知信息**：
- AI 服务地址：`http://localhost:8000`
- 接口路径：`POST /api/chat`（非流式）
- 请求格式：
  ```json
  {
    "query": "用户问题",
    "history": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}],
    "use_kb": true
  }
  ```
- 响应格式：
  ```json
  {
    "code": 0,
    "msg": "success",
    "data": {
      "answer": "AI 回答内容",
      "sources": [{"entry_id": "...", "title": "...", "content": "...", "score": 0.92}]
    }
  }
  ```

**操作步骤**：
1. 读取 `apps/student-app/src/api/chat.ts` 中的 `aiChat` 函数，确认调用方式
2. 读取 `apps/student-app/src/pages/chat/index.vue` 中 `callAIService` 函数的 mock 代码和注释掉的真实代码
3. 将 mock 代码替换为真实调用，并：
   - **加 try/catch**：AI 服务失败时显示 `"AI 服务暂时不可用，请稍后重试"` 的气泡，不崩溃
   - **AI 接口从 H5 前端直接调用会有跨域问题**：需要在 `apps/student-app/vite.config.ts` 的代理里加一条：`/api/chat` → `http://localhost:8000`（注意不要和 business-api 的 `/api` 代理冲突，因为二者路径不同）

> ⚠️ **关键注意**：`/api` 代理指向 `localhost:8080`（business-api），而 `/api/chat` 指向 `localhost:8000`（ai-service）。Vite 会按最长路径优先匹配，所以只要把 `/api/chat` 的代理配置放在 `/api` 前面即可正确路由。

**完成标准**：代码修改完毕，不崩溃，错误时有兜底提示

---

### ✅ 验证项 3：申请列表接口参数修复

**问题背景**：D3 报告遗留 —— `GET /api/v1/classroom-applications/my` 不存在，D3 改用了 `GET /api/v1/classroom-applications?applicantId={id}` 替代，但 D3 代码里 `getMyApplications()` 函数没有自动传入当前用户的 `id`。

**已知信息**：  
- 后端接口：`GET /api/v1/classroom-applications?applicantId=xxx`（`applicantId` 是必要的过滤参数）
- 当前用户 ID 存在 Pinia 的 `stores/user.ts` 中，通过 `userStore.userInfo.id` 获取

**操作步骤**：
1. 读取 `apps/student-app/src/api/apply.ts` 中的 `getMyApplications()` 函数
2. 修改该函数，接收 `userId: number` 参数，并传给接口
3. 读取 `apps/student-app/src/pages/apply/status.vue`，找到调用 `getMyApplications()` 的地方，补充传入 `userStore.userInfo.id`

**完成标准**：`getMyApplications` 调用时自动携带当前用户 ID

---

### ✅ 验证项 4：取消申请接口路径修复

**问题背景**：D3 代码使用 `DELETE /api/v1/classroom-applications/{id}`，但后端实际接口是 `PUT /api/v1/classroom-applications/{id}/cancel`。

**操作步骤**：
1. 读取 `apps/student-app/src/api/apply.ts` 中的 `cancelApplication()` 函数
2. 将请求方法从 `DELETE /{id}` 改为 `PUT /{id}/cancel`

**完成标准**：`cancelApplication` 的 HTTP 方法和路径与后端 `ClassroomApplicationController.cancel()` 对齐

---

### ✅ 验证项 5：Vite 代理配置最终核查

**操作步骤**：
1. 读取 `apps/student-app/vite.config.ts`
2. 确认现有的代理配置
3. 补充验证项 2 中需要新增的 `/api/chat` → `http://localhost:8000` 代理
4. 确认最终代理配置**顺序**正确（`/api/chat` 必须在 `/api` 之前）

**完成标准**：代理配置文件确认无误，顺序正确

---

## 【你的工作方式】

**第一步**：读完所有背景材料，列出你将修改的文件清单，对以上 5 个验证项逐一说明你的修改方案，等待我的"同意"。  
**第二步**：收到"同意"后，按验证项 1→2→3→4→5 顺序逐项修改，每项完成后简短汇报。

---

## 【禁止清单（严格遵守）】

- ❌ 禁止修改任何 `.java` 后端文件
- ❌ 禁止修改 `pages.json`、`stores/user.ts`、`request.ts`（已固化的基础层）
- ❌ 禁止重构 D2/D3 已实现的页面逻辑，只做最小范围修改
- ❌ 禁止因为 ai-service 未启动就放弃——代码层面对齐即可，运行时联调是下一步
- ❌ 禁止修改 `services/` 或 `deploy/` 下的任何文件

---

## 【完成标准】

✅ 验证码接口路径与后端对齐  
✅ `callAIService()` 已切换为真实 AI 调用，有 try/catch 兜底  
✅ `getMyApplications()` 自动携带当前用户 ID  
✅ `cancelApplication()` 使用 `PUT /{id}/cancel`  
✅ `vite.config.ts` 代理配置正确，`/api/chat` 优先于 `/api`

---

## 【完成汇报文件（必须交付，不可跳过）】

满足完成标准后，将本次交付报告写入：  
`docs/test-reports/completion-reports/TASK-D4-student-integration-report.md`

报告章节：
① **任务标识**（执行时间精确到秒：YYYY-MM-DD HH:mm:ss）  
② **实际修改的文件清单**  
③ **验证结果**（5 个验证项各一行，✅/❌ + 说明）  
④ **遗留问题**（特别说明：是否还需要真机/浏览器运行验证）  
⑤ **新发现错误模式**（若有，可建议更新错题本）

汇报文件写完后，请明确回复 **"阶段任务 D4 完成并停止"**。

**现在，请开始第一步：阅读背景材料，提交修改方案和文件清单。**
