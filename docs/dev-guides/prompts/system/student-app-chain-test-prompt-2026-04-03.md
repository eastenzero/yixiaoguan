# 任务：全链路 UI 验证（student-app → business-api → ai-service）

**任务编号**：TASK-4b  
**创建日期**：2026-04-03  
**优先级**：高  
**预计时长**：20–30 分钟

---

## 通用前置（执行模式，不得跳过）

1. **先计划后执行**：读完本文档后，先输出你的执行计划（步骤编号 + 预期结果），再开始任何操作。
2. **文件是真相**：所有判断基于实际文件内容和命令输出，不依赖假设。
3. **超范围即停止**：如遇本任务范围外的问题（如数据库报错、业务逻辑 bug），记录到报告中，不自行修复，等待指挥官指示。
4. **每步骤输出确认**：每个步骤执行后，输出实际结果。如失败，停止并说明原因。

---

## 背景材料（必读）

### 当前已知状态
- **ai-service**：已在宿主机以 `python -m uvicorn main:app --port 8000` 直接运行（非 Docker），ChromaDB 有 90 条知识条目，RAG 检索正常
- **API 验证**：通过 `POST http://localhost:8000/api/chat` 已验证三类场景（KB 命中/KB 无匹配/完全跑题）均符合预期
- **business-api**：Spring Boot，目标端口 8080，启动命令见 AGENT.md 第七节
- **student-app**：uni-app H5，目标端口 5174，启动命令：`npm run dev:h5`（在 `apps/student-app/` 目录）

### 关键文件
- `AGENT.md` → 项目概览、服务启动命令、本机 Java/Maven 路径
- `apps/student-app/src/` → 学生端源码，关注 `pages/chat/` 目录
- `services/business-api/ruoyi-admin/src/` → AI 对话相关 Controller

---

## 任务目标

验证完整链路：**学生在 UI 输入问题 → business-api 接收 → 转发 ai-service → 返回答案 → 界面展示来源引用**。

---

## 交付物（必须全部完成）

### 步骤 1：环境检查
- 检查端口 8080（business-api）和 8000（ai-service）是否监听
- 检查 student-app 端口 5174 是否在运行
- **如果 business-api 未运行**：按 AGENT.md 第七节命令启动，等待健康检查通过
- **如果 student-app 未运行**：在 `apps/student-app/` 目录执行 `npm run dev:h5`

### 步骤 2：接口路径核查
找到 business-api 中 AI 对话接口的实际路由路径（搜索 `@PostMapping` + `chat` 关键词），确认：
- 实际接口路径（如 `/api/v1/ai/chat` 或 `/api/chat`）
- student-app 中调用该接口的代码位置

如路径不一致，记录差异但**不修改代码**，在报告中说明。

### 步骤 3：Playwright 截图验证
在 student-app 上用 Playwright（或手动截图）完成以下验证：

| 测试用例 | 预期结果 |
|---------|---------|
| 提问：「国家助学金怎么申请？」 | 有实质性回答 + 显示来源引用（至少 1 条） |
| 提问：「学校宿舍电费怎么交？」 | 显示"尚未学习到相关说明"类拒答提示 |

每个用例截图，命名格式：`temp/screenshots/chain-test-case1.png`、`chain-test-case2.png`

### 步骤 4：差异记录
- 如果答案正确但来源引用未显示在 UI（说明前端未渲染 sources 字段）→ 记录为问题项，不修复
- 如果 business-api 无法转发到 ai-service → 记录错误日志片段

---

## 禁止事项

- 禁止修改 business-api 的任何 Java 代码
- 禁止修改数据库 schema
- 禁止修改 ai-service 任何代码
- 禁止自行解决 business-api 启动失败（如 Redis/PostgreSQL 未启动）

---

## 完成标准

- [x] 所有服务均在运行（端口检查通过）
- [x] 至少完成 2 个测试用例的截图
- [x] 已确认 business-api 到 ai-service 的接口路径（一致或不一致均需记录）
- [x] 已提交完成报告

---

## 完成汇报（写入以下文件）

**路径**：`docs/test-reports/completion-reports/TASK-4b-chain-ui-test-report.md`

报告必须包含：
1. 各服务启动状态
2. business-api → ai-service 接口路径核查结果
3. 每个测试用例的结果（通过/失败/异常）及截图路径
4. UI 来源引用渲染状态（是否正确显示）
5. 发现的问题项列表（每项含严重程度和建议处理方式）
