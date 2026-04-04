---
id: "p5b-multiround-history"
parent: "phase-5-e2e"
type: "bugfix"
status: "done"
tier: "T3"
priority: "low"
risk: "medium"
foundation: false

scope:
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"
  - "apps/student-app/src/pages/chat/index.vue"
out_of_scope:
  - "services/ai-service/"
  - "apps/teacher-web/"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/controller/"
  - "knowledge-base/"
  - "scripts/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"
  - "apps/student-app/src/pages/chat/index.vue"

done_criteria:
  L0: "AiCoordinatorServiceImpl.java 中构造 ChatStreamRequest 时 history 字段非空；代码中存在含 sdfmu.edu.cn 的兜底逻辑"
  L1: "mvn compile -pl ruoyi-admin 无错误；student-app npm run build 无错误"
  L2: "多轮追问测试通过：第一轮问'奖学金申请条件'，第二轮问'那截止日期是什么时候'，第二轮回复包含上下文相关内容；办事意图（预约教室/报修）响应中含 sdfmu.edu.cn 链接"
  L3: "history 长度上限合理（建议 ≤6 条），避免超出模型 context 窗口；前端正确传递本次对话的历史消息"

root_cause: "(1) AiCoordinatorServiceImpl 构造 ChatStreamRequest 时 history=[]（硬编码空列表）；前端 chat/index.vue 也传 history: []，导致多轮追问无上下文（DEBT-04）。(2) 办事意图兜底的 sdfmu.edu.cn 链接在当前运行环境未生效（p1d 签字通过但 p5a 验证发现 TC07/TC08 无官网链接）"
affected_modules:
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"
  - "apps/student-app/src/pages/chat/index.vue"
regression_test: "多轮追问场景：第二轮问题能引用第一轮上下文，不会重复提问基础信息"

depends_on: ["p5a-full-chain-test"]
created_at: "2026-04-04 01:43:00"
---

# p5b：多轮对话历史传递修复

> `AiCoordinatorServiceImpl` 构造 `ChatStreamRequest` 时从数据库取最近 N 条消息传入 `history`，多轮追问能保持上下文。

## 背景

技术债 DEBT-04：当前 `history` 始终为 `[]`，每次对话都像第一轮，
用户无法进行"那截止日期是什么时候"这类追问。

修复路径：
1. **后端**：`AiCoordinatorServiceImpl` 在构造 `ChatStreamRequest` 前，从数据库 `yx_conversation` 取最近 N 条消息（建议 N=6）作为 history
2. **前端**：`chat/index.vue` 在发起请求时传入当前对话的消息历史（或由后端全权管理，前端不需传）

确认哪个方案：后端从 DB 取 history（推荐，前端无需改）还是前端维护 history 并传递（需修改前端）。

## 已知陷阱

- history 长度需要有上限（如最近 6 条），否则长对话会超出大模型 context 窗口
- history 格式必须与 ai-service 的 `ChatStreamRequest` 接口定义一致（确认 `role` 字段是 `user/assistant` 还是其他）
- 后端改造后必须编译验证，前端改造后必须 build 验证
- 不要为了 history 修改 ai-service 的接口定义，应适配现有接口
