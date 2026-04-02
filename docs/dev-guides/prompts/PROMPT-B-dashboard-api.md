# 【提示词 B】后端 DashboardController 实现

> **状态**：待执行 | **预估工时**：3~4小时 | **可并行**：是，与 Prompt-A/C 无依赖冲突

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 Java 后端工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（项目全局规则）
2. `docs/database/schema-phase1.md`（P1 全量数据库 Schema，重点关注以下表：`yx_escalation`、`yx_classroom_application`、`yx_conversation`、`yx_message`、`yx_knowledge_entry`）
3. `docs/dev-guides/backend-roadmap.md`（后端模块完成状态，了解已有哪些 Controller）
4. `apps/teacher-web/src/api/dashboard.ts`（前端调用的接口路径与期望的返回字段——这是你的开发规格说明书）
5. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/conversation/controller/EscalationController.java`（参考现有 Controller 的包结构、注解风格、鉴权方式）
6. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/classroom/controller/ClassroomApplicationController.java`（同上，作为审批模块参考）

**【任务说明】**

当前教师工作台（仪表盘）首页完全空白，因为后端缺失聚合统计接口。你需要新建 `DashboardController` 来实现以下 **6 个接口**（路径以前端 dashboard.ts 中的调用为准）：

| 接口 | 方法 | 路径 | 数据来源 |
|------|------|------|---------|
| 工作台统计概览 | GET | `/api/v1/dashboard/stats` | 聚合多表 COUNT 查询 |
| 今日提问列表 | GET | `/api/v1/dashboard/today-questions` | `yx_escalation` 按日期筛选 + 分页 |
| 高频问题统计 | GET | `/api/v1/dashboard/hot-questions` | `yx_escalation` 按标题聚合 GROUP BY |
| 待审批事项列表 | GET | `/api/v1/dashboard/pending-approvals` | `yx_classroom_application` 状态=待审批 |
| AI 舆情预警 | GET | `/api/v1/dashboard/ai-warnings` | 简单实现：查询近 7 日提问量异常增长的关键词，无 AI 时可返回空数组 |
| 工作台聚合总览 | GET | `/api/v1/dashboard/overview` | 一次调用返回上述全部数据的聚合体 |

**统计概览字段规格**（来自 `dashboard.ts` 中 `DashboardStats` 接口定义）：

```typescript
{
  todayQuestions: number,        // 今日 yx_escalation 新增数
  todayQuestionsGrowth: number,  // 与昨日对比增长率（百分比整数，如 +12 或 -5）
  pendingApprovals: number,      // yx_classroom_application 中 status=0 的数量
  urgentApprovals: number,       // 申请时间距今超过 48h 且仍未审批的数量
  aiResolutionRate: number,      // AI 自动回复数 / 总提问数 * 100（取整）
  avgResponseTime: number,       // 已解决工单平均响应时间（分钟，取整）
  responseTimeImprovement: number // 与上周平均响应时间的差值（正数=提升，如 15 表示缩短了15分钟）
}   
```

**【你的交付物】**

在包 `com.yixiaoguan.dashboard` 下，新建以下文件：

1. `controller/DashboardController.java`（6 个 GET 接口，带鉴权注解）
2. `service/DashboardService.java`（接口定义）
3. `service/impl/DashboardServiceImpl.java`（SQL 查询实现，使用 JDBC 或已有 Mapper 框架）
4. `dto/` 下各接口的返回 DTO 类（DashboardStatsDTO、TodayQuestionDTO、HotQuestionDTO、PendingApprovalDTO、AIWarningDTO、DashboardOverviewDTO）

**【禁止清单（严格遵守）】**

- ❌ 禁止修改或删除任何已有的 Controller、Service、Mapper 文件
- ❌ 禁止修改数据库表结构（不允许 ALTER TABLE、不允许新增表）
- ❌ 禁止修改 `pom.xml` 引入新的 Maven 依赖（用项目已有的工具类）
- ❌ 禁止在 `ai-warnings` 接口中引入任何 AI 调用逻辑——返回空数组或从 `yx_escalation` 做简单关键词统计即可
- ❌ 如果 SQL 查询结果和前端期望的字段名不一致，停下来告知我，不要擅自改前端
- ❌ 每次不要超过 2 个文件，写完一个汇报一次

**【工作方式】**

第一步：阅读背景材料，列出你将新建的全部文件路径，并附上 `DashboardStats` 字段与数据库表字段的对应关系说明，等待我的"同意"。  
第二步：收到"同意"后，按 DTO → Service接口 → ServiceImpl → Controller 顺序进行，逐文件完成后汇报。

**【完成标准】**

✅ `mvn compile` 无编译报错  
✅ 调用 `GET /api/v1/dashboard/stats` 返回 HTTP 200，且 JSON 结构包含 `todayQuestions`、`pendingApprovals` 等字段  
✅ 调用 `GET /api/v1/dashboard/today-questions` 返回分页结构（含 `rows`、`total`）  
✅ 调用 `GET /api/v1/dashboard/pending-approvals` 返回数组结构，无 500 报错  

满足以上标准后，在回复"完成"之前，必须先完成以下步骤：

**【完成汇报文件（必须交付，不可跳过）】**

将本次任务的完整交付报告写入：
`docs/test-reports/TASK-B-dashboard-api-completion-report.md`

报告必须包含以下五个章节（章节缺失视为任务未完成）：

1. **任务标识**：任务 ID（TASK-B）、执行时间
2. **实际修改的文件**：逐条列出新建/修改的文件完整路径，每条附一句变更说明（不需要贴代码）
3. **验证结果**：逐条列出上述四条完成标准，并标注 ✅ 通过 或 ❌ 失败及原因
4. **遗留问题**：执行过程中发现但本次未处理的问题（如字段不对齐、权限配置待确认等），按优先级排列
5. **下一步建议**：对指挥官或下一个任务 AI 的交接说明（如：需要前端配合修改哪个字段、建议下一步做什么）

汇报文件写完后，请明确回复 **"阶段任务 B 完成并停止"**，不要继续优化其他功能。

**现在，请开始第一步：阅读背景文档，提交文件清单与字段对照表。**
