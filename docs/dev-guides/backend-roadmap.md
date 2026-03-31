# 后端开发阶段路线图（业务 API）

> 状态：**规划中（按此拆分对话任务）**  
> 目标：将主业务后端（`business-api`）的开发工作拆解为 5 个结构化的对话窗口，确保每一次只关注一个垂直切片，防止上下文污染和开发跑偏。

---

## ✅ 模块 1：用户与认证改造（已完成）
- **核心表**：`yx_user`, `yx_role`, `yx_user_role`, `yx_menu`, `yx_role_menu`
- **任务目标**：
  - 将若依默认的登录认证底层（从 `sys_user` 切换为 `yx_user`）。
  - 实现基于 `yx_user` 的 JWT 签发、校验与 RBAC 权限拦截逻辑。
  - 保留并兼容若依核心的工具类。
- **验证标准**：启动服务后，可以用新表中的用户完整打通`/login`、`/getInfo`等接口。

## ✅ 模块 2：问答会话与 WebSocket 服务（已完成）
- **核心表**：`yx_conversation`, `yx_message`, `yx_escalation`
- **任务目标**：
  - 会话与消息记录的 CRUD。
  - 搭建 WebSocket 服务端点，管理当前用户在线状态。
  - 实现“教师实时介入”机制下的消息定向推送及状态锁切换。
- **验证标准**：通过 API 测试工具（或 WebSocket 客户端）完成双向收发、状态切换不乱序。

## 🟢 模块 3：知识库管理与审核
- **核心表**：`yx_knowledge_category`, `yx_knowledge_entry`, `yx_knowledge_tag`, `yx_knowledge_review`
- **任务目标**：
  - 知识分类与标签的构建与维护。
  - 知识条目的分页查询、草稿保存、关联文件溯源。
  - 完成知识记录的一级审核状态机流转（提审->通过/拒绝）。
- **验证标准**：提供完整的增删改查 REST API，确保状态字段 `status` 的安全流转。

## 🟢 模块 4：申请审批与导办资源库
- **核心表**：`yx_classroom`, `yx_classroom_application`, `yx_application_review`, `yx_quick_link`
- **任务目标**：
  - 空教室资源基础信息查询接口。
  - 空教室申请的提交与审核流。
  - 带有附件 URL `attachments` 字段 JSON 解析落地的完整接口。
  - 快捷链接表（`yx_quick_link`）基础 CRUD。
- **验证标准**：通过接口模拟一条从“发起申请”到“修改状态为通过”的完整生命周期。

## 🟢 模块 5：系统通知推送与底层日志接入
- **核心表**：`yx_notification`, `yx_push_task`, `yx_audit_log`, `yx_ai_persona`
- **任务目标**：
  - 站内信创建与查询功能实现、手工发群发推送的接口落地。
  - 补齐通过 AOP 或配置等手段，使任何关键操作都能静默写入 `yx_audit_log`。
  - AI 人设读取功能的简单实现。
- **验证标准**：测试前面四个模块的接口时，可以在 `yx_audit_log` 里清晰抓到操作留痕。
