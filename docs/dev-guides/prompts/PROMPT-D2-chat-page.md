# 【提示词 D2】学生端 AI 对话页面开发

> **状态**：待执行 | **预估工时**：3小时 | **前置依赖**：TASK-D1 完成并确认骨架可正常启动

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 uni-app 前端工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（项目全局规则）
2. `docs/dev-guides/ai-antipatterns.md`（**错题本，必读**）
3. `_references/前端风格/学生移动端/jade_scholar/DESIGN.md`（**设计规范，必读**）
4. `_references/前端风格/学生移动端/_1/screen.png`（**对话页 UI 参考截图，重点参考**）
5. `docs/database/schema-phase1.md`（重点阅读：第二章"问答与会话模块"——`yx_conversation`、`yx_message`、`yx_escalation` 三张表及其枚举值）
6. `docs/test-reports/TASK-D1-student-scaffold-completion-report.md`（**D1 完成报告，了解已有的工具层和 API 封装方式**）
7. `apps/student-app/src/utils/request.ts`（D1 已建好的请求工具，直接复用）
8. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/conversation/controller/ConversationController.java`（后端对话 API 的全部接口定义）
9. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/conversation/controller/EscalationController.java`（后端工单上报 API）


**【任务说明】**

实现学生端的两个核心页面：AI 对话页 和 我的提问列表页。

### 页面 1：AI 对话页（`pages/chat/index.vue`）

**交互流程**：
1. 进入页面时自动调用 `POST /api/v1/conversations` 创建新会话（或从路由参数获取已有 `conversationId`）
2. 历史消息通过 `GET /api/v1/conversations/{id}/messages` 加载
3. 学生在底部输入框输入文字并发送：
   - 调用 `POST /api/v1/conversations/{id}/messages`（body: `{ content, messageType: 1 }`）
   - 发送成功后，在消息列表末尾追加学生消息气泡
   - **然后展示"AI 思考中..."占位**，调用 `POST http://localhost:8000/chat`（AI 服务直连，见下方说明）
   - AI 回复到达后，替换占位，追加 AI 消息气泡，并将 AI 回复也调用 conversation API 保存
4. 消息列表自动滚动到底部
5. 右上角"呼叫老师"按钮：调用 `POST /api/v1/escalations`，type=1（学生主动）

**AI 服务对接说明（重要）**：
- AI 服务地址：`http://localhost:8000`，具体路由需读 `services/ai-service/main.py` 确认
- 如果 D2 开发时 AI 接口路由尚不明确，先使用 mock：定时器 1.5s 后返回固定回复"您好，我是医小管 AI 助手，我已收到您的问题，正在为您查找答案..."
- **不要因为 AI 接口不确定就卡住**，先 mock 上，等 AI 服务联调时再替换

**UI 设计要求**：
- 顶部：会话标题（可编辑）+ 右上角"呼叫老师"按钮
- 消息区：仿微信气泡，学生消息靠右（主题绿色背景），AI 消息靠左（白色背景 + 小头像）
- 底部：输入框 + 发送按钮，键盘弹起时自动上推

### 页面 2：我的提问列表（`pages/questions/index.vue`）

**功能**：
- 列表展示当前学生的所有工单：`GET /api/v1/escalations/my`（先确认该接口是否存在，若不存在改用 `GET /api/v1/conversations`）
- 每条显示：问题摘要、状态（待处理 / 处理中 / 已解决）、创建时间
- 点击进入对应会话（跳转 `/pages/chat/index?conversationId=xxx`）

**【API 清单（直接复用，基于 D1 的 request.ts 封装）】**

新建 `src/api/chat.ts`，包含：
```typescript
// 会话相关
createConversation(title?: string)       // POST /api/v1/conversations
getHistory(conversationId: number)       // GET /api/v1/conversations/{id}/messages
sendMessage(id: number, content: string) // POST /api/v1/conversations/{id}/messages

// 工单相关  
callTeacher(conversationId: number, messageId: number) // POST /api/v1/escalations
getMyEscalations()                       // GET /api/v1/escalations/my（若无此接口，用 my-assigned 替代并在报告里标注）
```

**【你的交付物】**

1. `apps/student-app/src/api/chat.ts`（API 函数封装）
2. `apps/student-app/pages/chat/index.vue`（功能完整的 AI 对话页）
3. `apps/student-app/pages/questions/index.vue`（功能完整的我的提问列表页）

**【禁止清单（严格遵守）】**

- ❌ 禁止修改 D1 已创建的 `request.ts`、`stores/user.ts`、`pages.json`
- ❌ 禁止因为 AI 接口不确定就停工——先 mock 再联调
- ❌ 禁止使用 WebSocket（P1 阶段用 HTTP 轮询或单次请求即可，不做实时推送）
- ❌ 禁止修改后端任何代码
- ❌ 如发现后端缺少 `GET /api/v1/escalations/my` 接口，在汇报报告里标注，不要自己去加后端代码

**【工作方式】**

第一步：阅读背景材料，确认 `services/ai-service/main.py` 里的 AI 接口路径，列出你将新建/修改的文件清单，等待我的"同意"。  
第二步：按 api/ → chat页 → questions页 的顺序开发，每完成一个文件汇报。

**【完成标准】**

✅ H5 开发服务无编译报错  
✅ 进入 `/pages/chat/index`，能发送一条消息，页面出现消息气泡（AI 可以是 mock 回复）  
✅ "呼叫老师"按钮点击后，能调用后端接口（或出现明确错误提示，不是白屏）  
✅ 进入 `/pages/questions/index`，能加载到列表数据（即使是空列表也算通过）

**【完成汇报文件（必须交付，不可跳过）】**

满足完成标准后，将本次交付报告写入：  
`docs/test-reports/completion-reports/TASK-D2-chat-page-completion-report.md`

报告章节：① 实际创建/修改的文件清单 ② 验证结果 ③ 遗留问题（特别标注：AI 接口对接状态、后端缺失的接口） ④ 新发现错误模式 ⑤ 下一步建议

汇报文件写完后，请明确回复 **"阶段任务 D2 完成并停止"**。

**现在，请开始第一步：阅读背景材料（特别是 main.py），提交文件清单。**
