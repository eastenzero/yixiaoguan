---
id: "p1d-intent-fallback"
parent: "phase-1-data-foundation"
type: "bugfix"
status: "done"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

scope:
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"
out_of_scope:
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiChatServiceImpl.java"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/controller/"
  - "apps/student-app/"
  - "apps/teacher-web/"
  - "services/ai-service/"
  - "knowledge-base/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - ".tasks/_spec.yaml"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"

done_criteria:
  L0: "AiCoordinatorServiceImpl.java 中 handleServiceIntent 方法存在且已修改"
  L1: "mvn compile 无错误（仅编译 ruoyi-admin 模块）"
  L2: "发送'我想预约教室'→ 收到包含 https://www.sdfmu.edu.cn/ 的兜底回复；3 个办事意图（book_classroom / submit_repair_request / query_application_status）均测试通过"
  L3: "返回的兜底消息语义友好，包含意图识别说明和可点击的官网链接"

root_cause: "学校业务接口未对接，当前 handleServiceIntent 直接返回错误或空响应，用户体验差"
affected_modules:
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/service/impl/AiCoordinatorServiceImpl.java"
regression_test: "发送办事类意图消息，验证回复中包含 https://www.sdfmu.edu.cn/"

depends_on: []
created_at: "2026-04-04 01:43:00"
---

# p1d：办事意图官网兜底

> 3 个办事意图（预约教室 / 报修 / 查询申请状态）均返回含学校官网链接的友好提示，不再报错或无响应。

## 背景

`IntentExtractor` 能正确识别 3 类办事意图，但因学校业务接口尚未对接，
`handleServiceIntent` 没有合适的处理路径。

用户确认的兜底策略：统一返回提示 + 学校官网链接 `https://www.sdfmu.edu.cn/`

示例回复格式：
> 我理解您想要[办理某事]。目前该功能正在与学校系统对接中，您可以先通过学校官网办理：https://www.sdfmu.edu.cn/

后期学校接口打通后，只需更新 URL 映射或替换为实际接口调用。

## 执行步骤

1. 打开 `AiCoordinatorServiceImpl.java`，找到 `handleServiceIntent` 方法
2. 为 3 个意图类型各添加一个友好回复消息，消息中包含官网链接
3. 编译验证：`mvn compile -pl ruoyi-admin`
4. 启动服务后测试 3 个意图均正确返回

## 已知陷阱

- 只改 `handleServiceIntent` 方法，不碰其他方法
- 注意回复格式需与其他 AI 回复格式一致（SSE 流式输出 or 普通 JSON 响应，确认当前调用链）
- 改完必须编译验证，不能只改不验
