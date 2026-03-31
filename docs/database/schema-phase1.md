# 医小管一期数据库设计（schema-phase1）

> 数据库：PostgreSQL  
> 最后更新：2026-03-31  
> 状态：**待确认**  
> 表命名：snake_case，统一 `yx_` 前缀  
> 公共字段：每表必含 `id`、`created_at`、`updated_at`、`is_deleted`

---

## 公共字段说明

以下四个字段在**每张表中都存在**，后续各表字段列表中不再重复列出。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `id` | BIGINT | PK, AUTO INCREMENT | 主键 |
| `created_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | 创建时间 |
| `updated_at` | TIMESTAMP WITH TIME ZONE | NOT NULL, DEFAULT NOW() | 更新时间（每次修改自动刷新） |
| `is_deleted` | BOOLEAN | NOT NULL, DEFAULT FALSE | 软删除标记 |

---

## 一、用户与权限模块

### 1. yx_user — 用户表

存储所有用户（学生/教师/管理员），学号即用户名，支持首次登录强制改密码。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `username` | VARCHAR(64) | NOT NULL, UNIQUE | 登录用户名（学号或工号） |
| `password` | VARCHAR(255) | NOT NULL | 加密后的密码（BCrypt） |
| `real_name` | VARCHAR(50) | NOT NULL | 真实姓名 |
| `nickname` | VARCHAR(50) | | 昵称 |
| `gender` | SMALLINT | DEFAULT 0 | 性别：0-未知 1-男 2-女 |
| `phone` | VARCHAR(20) | | 手机号 |
| `email` | VARCHAR(128) | | 邮箱 |
| `avatar_url` | VARCHAR(512) | | 头像 URL（COS） |
| `bio` | TEXT | | 个人描述（一期学生特征文本框） |
| `student_id` | VARCHAR(32) | | 学号（学生专用） |
| `employee_id` | VARCHAR(32) | | 工号（教师/管理员专用） |
| `department` | VARCHAR(100) | | 院系 |
| `major` | VARCHAR(100) | | 专业 |
| `class_name` | VARCHAR(50) | | 班级 |
| `grade` | VARCHAR(20) | | 年级 / 入学年份 |
| `wechat_openid` | VARCHAR(128) | UNIQUE | 微信 OpenID（二期小程序登录预留） |
| `status` | SMALLINT | NOT NULL, DEFAULT 2 | 0-停用 1-正常 2-未激活 |
| `password_changed` | BOOLEAN | NOT NULL, DEFAULT FALSE | 是否已修改默认密码 |
| `last_login_at` | TIMESTAMP WITH TIME ZONE | | 最后登录时间 |
| `last_login_ip` | VARCHAR(128) | | 最后登录 IP |
| `remark` | VARCHAR(500) | | 备注 |

> **索引**：`username` UNIQUE；`student_id`；`department, class_name`；`wechat_openid` UNIQUE WHERE NOT NULL

---

### 2. yx_role — 角色表

定义系统角色（学生 / 教师 / 管理员），支持 RBAC。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `role_key` | VARCHAR(64) | NOT NULL, UNIQUE | 角色标识：student / teacher / admin |
| `role_name` | VARCHAR(50) | NOT NULL | 角色显示名称 |
| `sort_order` | INT | DEFAULT 0 | 排序 |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-停用 1-正常 |
| `remark` | VARCHAR(500) | | 备注 |

---

### 3. yx_user_role — 用户-角色关联表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `user_id` | BIGINT | NOT NULL, FK → yx_user.id | 用户 ID |
| `role_id` | BIGINT | NOT NULL, FK → yx_role.id | 角色 ID |

> **约束**：UNIQUE(`user_id`, `role_id`)

---

### 4. yx_menu — 菜单权限表

前端路由 + 按钮级权限资源，树形结构。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `parent_id` | BIGINT | NOT NULL, DEFAULT 0 | 父菜单 ID（0 = 顶级） |
| `menu_name` | VARCHAR(100) | NOT NULL | 菜单名称 |
| `menu_type` | CHAR(1) | NOT NULL | M-目录 C-菜单 F-按钮 |
| `path` | VARCHAR(255) | | 路由路径 |
| `component` | VARCHAR(255) | | 前端组件路径 |
| `permission` | VARCHAR(200) | | 权限标识（如 `knowledge:entry:edit`） |
| `icon` | VARCHAR(100) | | 图标 |
| `sort_order` | INT | DEFAULT 0 | 排序 |
| `visible` | BOOLEAN | NOT NULL, DEFAULT TRUE | 是否可见 |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-停用 1-正常 |
| `remark` | VARCHAR(500) | | 备注 |

---

### 5. yx_role_menu — 角色-菜单关联表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `role_id` | BIGINT | NOT NULL, FK → yx_role.id | 角色 ID |
| `menu_id` | BIGINT | NOT NULL, FK → yx_menu.id | 菜单 ID |

> **约束**：UNIQUE(`role_id`, `menu_id`)

---

## 二、问答与会话模块

### 6. yx_conversation — 会话表

学生与 AI/教师的对话会话，一个学生可有多个会话。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `user_id` | BIGINT | NOT NULL, FK → yx_user.id | 所属学生 |
| `title` | VARCHAR(200) | | 会话标题（可由 AI 自动生成） |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-已关闭 1-进行中 2-教师已介入 |
| `teacher_id` | BIGINT | FK → yx_user.id | 当前介入的教师 ID |
| `teacher_joined_at` | TIMESTAMP WITH TIME ZONE | | 教师介入时间 |
| `last_message_at` | TIMESTAMP WITH TIME ZONE | | 最后消息时间 |
| `message_count` | INT | NOT NULL, DEFAULT 0 | 消息总数 |

> **索引**：`user_id, status`；`teacher_id`；`last_message_at DESC`

---

### 7. yx_message — 消息表

会话中的每条消息，区分学生/AI/教师三种发送者身份。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `conversation_id` | BIGINT | NOT NULL, FK → yx_conversation.id | 所属会话 |
| `sender_type` | SMALLINT | NOT NULL | 1-学生 2-AI 3-教师 4-系统 |
| `sender_id` | BIGINT | | 发送者用户 ID（AI / 系统时为 NULL） |
| `content` | TEXT | NOT NULL | 消息内容 |
| `message_type` | SMALLINT | NOT NULL, DEFAULT 1 | 1-纯文本 2-富文本/Markdown 3-卡片 4-系统提示 |
| `parent_message_id` | BIGINT | | 关联的上游消息 ID（如学生提问 → AI 回答） |
| `ai_confidence` | DECIMAL(5,4) | | AI 回答的置信度（0.0000~1.0000） |
| `ai_source_entry_ids` | VARCHAR(500) | | AI 命中的知识条目 ID 列表（JSON 数组） |
| `ai_source_link_ids` | VARCHAR(500) | | AI 推荐的快捷链接 ID 列表（JSON 数组） |

> **索引**：`conversation_id, created_at`

---

### 8. yx_escalation — 问题上报表

AI 无法回答的问题上报给教师处理的工单。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `conversation_id` | BIGINT | NOT NULL, FK → yx_conversation.id | 来源会话 |
| `message_id` | BIGINT | NOT NULL, FK → yx_message.id | 触发上报的消息 |
| `student_id` | BIGINT | NOT NULL, FK → yx_user.id | 提问学生 |
| `teacher_id` | BIGINT | FK → yx_user.id | 分配给的教师 |
| `question_summary` | VARCHAR(500) | | 问题摘要 |
| `status` | SMALLINT | NOT NULL, DEFAULT 0 | 0-待处理 1-处理中 2-已解决 3-已关闭 4-已转知识库 |
| `priority` | SMALLINT | NOT NULL, DEFAULT 1 | 0-低 1-中 2-高 |
| `trigger_type` | SMALLINT | NOT NULL, DEFAULT 1 | 1-学生主动呼叫 2-AI 判断上报 |
| `teacher_reply` | TEXT | | 教师回复内容 |
| `resolved_at` | TIMESTAMP WITH TIME ZONE | | 解决时间 |
| `knowledge_entry_id` | BIGINT | FK → yx_knowledge_entry.id | 转为知识条目后的关联 ID |
| `remark` | VARCHAR(500) | | 备注 |

> **索引**：`teacher_id, status`；`student_id`；`status, priority`

---

## 三、知识库模块

### 9. yx_knowledge_category — 知识分类表

8 大域 + 子分类的树形结构。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `parent_id` | BIGINT | NOT NULL, DEFAULT 0 | 父分类 ID（0 = 顶级） |
| `name` | VARCHAR(100) | NOT NULL | 分类名称 |
| `code` | VARCHAR(50) | NOT NULL, UNIQUE | 分类编码（如 `admission`、`scholarship`） |
| `sort_order` | INT | DEFAULT 0 | 排序 |
| `description` | VARCHAR(500) | | 分类说明 |
| `icon` | VARCHAR(100) | | 图标 |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-停用 1-启用 |

---

### 10. yx_knowledge_entry — 知识条目表

标准化知识内容，拥有完整的生命周期状态。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `category_id` | BIGINT | NOT NULL, FK → yx_knowledge_category.id | 所属分类 |
| `title` | VARCHAR(200) | NOT NULL | 知识标题 |
| `content` | TEXT | NOT NULL | 知识内容（Markdown 格式） |
| `summary` | VARCHAR(500) | | 摘要（用于搜索结果展示） |
| `status` | SMALLINT | NOT NULL, DEFAULT 0 | 0-草稿 1-待审核 2-已发布 3-已下线 4-审核拒绝 |
| `version` | INT | NOT NULL, DEFAULT 1 | 版本号（每次编辑 +1） |
| `source_id` | BIGINT | FK → yx_knowledge_source.id | 关联的来源记录 |
| `author_id` | BIGINT | NOT NULL, FK → yx_user.id | 创建者 |
| `published_at` | TIMESTAMP WITH TIME ZONE | | 发布时间 |
| `expired_at` | TIMESTAMP WITH TIME ZONE | | 过期时间（可选） |
| `view_count` | INT | NOT NULL, DEFAULT 0 | 被查看次数 |
| `hit_count` | INT | NOT NULL, DEFAULT 0 | AI 问答命中次数 |
| `remark` | VARCHAR(500) | | 备注 |

> **索引**：`category_id, status`；`status, published_at DESC`；`author_id`

---

### 11. yx_knowledge_review — 知识审核记录表

每次审核操作生成一条记录（一期为一级审核）。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `entry_id` | BIGINT | NOT NULL, FK → yx_knowledge_entry.id | 审核的条目 |
| `reviewer_id` | BIGINT | NOT NULL, FK → yx_user.id | 审核人 |
| `action` | SMALLINT | NOT NULL | 1-通过 2-拒绝 3-退回修改 |
| `opinion` | TEXT | | 审核意见 |
| `entry_version` | INT | NOT NULL | 审核时的条目版本号 |

---

### 12. yx_knowledge_tag — 标签表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `name` | VARCHAR(50) | NOT NULL, UNIQUE | 标签名称 |
| `sort_order` | INT | DEFAULT 0 | 排序 |

---

### 13. yx_knowledge_entry_tag — 知识条目-标签关联表

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `entry_id` | BIGINT | NOT NULL, FK → yx_knowledge_entry.id | 知识条目 ID |
| `tag_id` | BIGINT | NOT NULL, FK → yx_knowledge_tag.id | 标签 ID |

> **约束**：UNIQUE(`entry_id`, `tag_id`)

---

### 14. yx_knowledge_source — 知识来源记录表

关联到 raw 层的原始材料文件，实现来源追溯。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `file_name` | VARCHAR(255) | NOT NULL | 原始文件名 |
| `file_path` | VARCHAR(512) | | 原始文件路径（raw/ 目录下的相对路径） |
| `file_url` | VARCHAR(512) | | COS 存储 URL（如已上传） |
| `file_type` | VARCHAR(20) | | 文件类型（pdf / docx / md / …） |
| `file_size` | BIGINT | | 文件大小（bytes） |
| `description` | VARCHAR(500) | | 来源描述 |
| `uploader_id` | BIGINT | FK → yx_user.id | 上传人 |

---

## 四、申请审批模块

### 15. yx_classroom — 空教室资源表

可供申请的教室基础信息。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `building` | VARCHAR(100) | NOT NULL | 教学楼名称 |
| `room_number` | VARCHAR(50) | NOT NULL | 教室编号 |
| `capacity` | INT | | 教室容量（人数） |
| `equipment` | VARCHAR(500) | | 设备信息（投影仪、空调等） |
| `location` | VARCHAR(200) | | 位置描述 |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-不可用 1-可用 |
| `remark` | VARCHAR(500) | | 备注 |

> **约束**：UNIQUE(`building`, `room_number`)

---

### 16. yx_classroom_application — 空教室申请表

学生提交的空教室使用申请。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `applicant_id` | BIGINT | NOT NULL, FK → yx_user.id | 申请人 |
| `classroom_id` | BIGINT | NOT NULL, FK → yx_classroom.id | 申请的教室 |
| `apply_date` | DATE | NOT NULL | 使用日期 |
| `start_time` | TIME | NOT NULL | 开始时间 |
| `end_time` | TIME | NOT NULL | 结束时间 |
| `purpose` | VARCHAR(500) | NOT NULL | 用途说明 |
| `attendee_count` | INT | | 预计使用人数 |
| `contact_phone` | VARCHAR(20) | | 联系电话 |
| `attachments` | VARCHAR(1000) | | 附件 URL 列表（JSON 数组，存 COS 地址） |
| `status` | SMALLINT | NOT NULL, DEFAULT 0 | 0-待审批 1-已通过 2-已拒绝 3-已取消 4-已过期 |
| `remark` | VARCHAR(500) | | 备注 |

> **索引**：`applicant_id, status`；`classroom_id, apply_date`；`status`

---

### 17. yx_application_review — 申请审批记录表

教师对空教室申请的审批操作。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `application_id` | BIGINT | NOT NULL, FK → yx_classroom_application.id | 申请单 ID |
| `reviewer_id` | BIGINT | NOT NULL, FK → yx_user.id | 审批人 |
| `action` | SMALLINT | NOT NULL | 1-通过 2-拒绝 |
| `opinion` | VARCHAR(500) | | 审批意见 |

---

## 五、导办与快捷链接模块

### 18. yx_quick_link — 快捷链接表

管理员维护的校内常用链接库，支持 AI 意图匹配推荐。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `name` | VARCHAR(100) | NOT NULL | 链接名称（如"校外奖学金报名入口"） |
| `url` | VARCHAR(512) | NOT NULL | 目标链接 |
| `description` | VARCHAR(500) | | 简短描述（用于向量化匹配） |
| `category` | VARCHAR(50) | | 分类（比赛报名 / 设施报修 / 学籍办理 / …） |
| `tags` | VARCHAR(500) | | 补充关键词（JSON 数组） |
| `icon` | VARCHAR(100) | | 图标 |
| `sort_order` | INT | DEFAULT 0 | 排序 |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | 是否启用 |
| `click_count` | INT | NOT NULL, DEFAULT 0 | 点击统计 |

> 向量化后的 Embedding 存储在 ChromaDB 的 `quick_links` 集合中，不在本表存储。

---

## 六、通知与消息模块

### 19. yx_notification — 站内通知表

面向用户的站内消息推送（审批结果、主动推送等）。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `user_id` | BIGINT | NOT NULL, FK → yx_user.id | 接收人 |
| `title` | VARCHAR(200) | NOT NULL | 通知标题 |
| `content` | TEXT | | 通知正文 |
| `type` | SMALLINT | NOT NULL | 1-系统通知 2-审批通知 3-推送消息 4-申请结果 |
| `biz_type` | VARCHAR(50) | | 关联业务类型（application / escalation / knowledge） |
| `biz_id` | BIGINT | | 关联业务记录 ID |
| `is_read` | BOOLEAN | NOT NULL, DEFAULT FALSE | 是否已读 |
| `read_at` | TIMESTAMP WITH TIME ZONE | | 阅读时间 |
| `sender_id` | BIGINT | | 发送者 ID（系统发送时为 NULL） |
| `push_task_id` | BIGINT | FK → yx_push_task.id | 关联的推送任务 ID |

> **索引**：`user_id, is_read, created_at DESC`

---

### 20. yx_push_task — 主动推送任务表

教师手动创建的群发推送任务（一期仅支持手动发送）。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `title` | VARCHAR(200) | NOT NULL | 推送标题 |
| `content` | TEXT | NOT NULL | 推送内容 |
| `target_type` | SMALLINT | NOT NULL | 1-全体学生 2-指定班级 3-指定用户 |
| `target_filter` | TEXT | | 目标筛选条件（JSON，如班级列表、用户 ID 列表） |
| `status` | SMALLINT | NOT NULL, DEFAULT 0 | 0-草稿 1-已发送 2-已取消 |
| `sender_id` | BIGINT | NOT NULL, FK → yx_user.id | 发起教师 |
| `sent_at` | TIMESTAMP WITH TIME ZONE | | 实际发送时间 |
| `recipient_count` | INT | NOT NULL, DEFAULT 0 | 接收人数 |
| `read_count` | INT | NOT NULL, DEFAULT 0 | 已读人数 |

---

## 七、AI 配置模块

### 21. yx_ai_persona — AI 人设配置表

存储导员自定义的 AI 名称、头像、语气风格与 Prompt。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `teacher_id` | BIGINT | FK → yx_user.id | 所属教师（NULL = 系统默认人设） |
| `name` | VARCHAR(50) | NOT NULL, DEFAULT '小管' | AI 显示名称 |
| `avatar_url` | VARCHAR(512) | | AI 头像 URL |
| `greeting` | TEXT | | 开场白 / 欢迎语 |
| `system_prompt` | TEXT | | 系统提示词（Prompt） |
| `tone_style` | VARCHAR(50) | | 语气风格（亲切 / 正式 / 活泼） |
| `is_default` | BOOLEAN | NOT NULL, DEFAULT FALSE | 是否为系统默认人设 |
| `status` | SMALLINT | NOT NULL, DEFAULT 1 | 0-停用 1-启用 |

---

## 八、系统日志模块

### 22. yx_audit_log — 审计日志表

记录所有关键操作，不可修改、不做软删除。

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `user_id` | BIGINT | | 操作人 ID |
| `username` | VARCHAR(64) | | 操作人用户名（冗余，便于查询） |
| `module` | VARCHAR(50) | NOT NULL | 功能模块（user / knowledge / application / …） |
| `action` | VARCHAR(50) | NOT NULL | 操作类型（create / update / delete / login / export / …） |
| `target_type` | VARCHAR(50) | | 操作对象类型 |
| `target_id` | BIGINT | | 操作对象 ID |
| `description` | VARCHAR(500) | | 操作描述 |
| `request_method` | VARCHAR(10) | | HTTP 请求方式 |
| `request_url` | VARCHAR(500) | | 请求 URL |
| `request_ip` | VARCHAR(128) | | 请求来源 IP |
| `request_params` | TEXT | | 请求参数（脱敏后） |
| `response_code` | INT | | 响应状态码 |
| `cost_time` | BIGINT | | 耗时（ms） |
| `status` | SMALLINT | NOT NULL | 0-失败 1-成功 |
| `error_msg` | TEXT | | 错误信息 |

> **特殊说明**：本表的 `is_deleted` 始终为 FALSE，审计日志不允许删除。  
> **索引**：`user_id, created_at DESC`；`module, action`；`created_at DESC`

---

## 附录 A：表总览

| 序号 | 表名 | 模块 | 用途概要 |
|---|---|---|---|
| 1 | `yx_user` | 用户与权限 | 用户主表 |
| 2 | `yx_role` | 用户与权限 | 角色定义 |
| 3 | `yx_user_role` | 用户与权限 | 用户-角色关联 |
| 4 | `yx_menu` | 用户与权限 | 菜单权限资源 |
| 5 | `yx_role_menu` | 用户与权限 | 角色-菜单关联 |
| 6 | `yx_conversation` | 问答会话 | 对话会话 |
| 7 | `yx_message` | 问答会话 | 会话消息 |
| 8 | `yx_escalation` | 问答会话 | 问题上报工单 |
| 9 | `yx_knowledge_category` | 知识库 | 知识分类 |
| 10 | `yx_knowledge_entry` | 知识库 | 知识条目 |
| 11 | `yx_knowledge_review` | 知识库 | 审核记录 |
| 12 | `yx_knowledge_tag` | 知识库 | 标签定义 |
| 13 | `yx_knowledge_entry_tag` | 知识库 | 条目-标签关联 |
| 14 | `yx_knowledge_source` | 知识库 | 来源追溯 |
| 15 | `yx_classroom` | 申请审批 | 教室资源 |
| 16 | `yx_classroom_application` | 申请审批 | 空教室申请 |
| 17 | `yx_application_review` | 申请审批 | 申请审批记录 |
| 18 | `yx_quick_link` | 导办链接 | 快捷链接库 |
| 19 | `yx_notification` | 通知消息 | 站内通知 |
| 20 | `yx_push_task` | 通知消息 | 主动推送任务 |
| 21 | `yx_ai_persona` | AI 配置 | AI 人设配置 |
| 22 | `yx_audit_log` | 系统日志 | 审计日志 |

---

## 附录 B：枚举值速查

### 用户状态 (`yx_user.status`)
| 值 | 含义 |
|---|---|
| 0 | 停用 |
| 1 | 正常 |
| 2 | 未激活（默认） |

### 会话状态 (`yx_conversation.status`)
| 值 | 含义 |
|---|---|
| 0 | 已关闭 |
| 1 | 进行中 |
| 2 | 教师已介入 |

### 消息发送者类型 (`yx_message.sender_type`)
| 值 | 含义 |
|---|---|
| 1 | 学生 |
| 2 | AI |
| 3 | 教师 |
| 4 | 系统 |

### 消息内容类型 (`yx_message.message_type`)
| 值 | 含义 |
|---|---|
| 1 | 纯文本 |
| 2 | 富文本 / Markdown |
| 3 | 卡片 |
| 4 | 系统提示 |

### 上报状态 (`yx_escalation.status`)
| 值 | 含义 |
|---|---|
| 0 | 待处理 |
| 1 | 处理中 |
| 2 | 已解决 |
| 3 | 已关闭 |
| 4 | 已转知识库 |

### 上报触发方式 (`yx_escalation.trigger_type`)
| 值 | 含义 |
|---|---|
| 1 | 学生主动呼叫老师 |
| 2 | AI 判断自动上报 |

### 知识条目状态 (`yx_knowledge_entry.status`)
| 值 | 含义 |
|---|---|
| 0 | 草稿 |
| 1 | 待审核 |
| 2 | 已发布 |
| 3 | 已下线 |
| 4 | 审核拒绝 |

### 审核动作 (`yx_knowledge_review.action` / `yx_application_review.action`)
| 值 | 含义 |
|---|---|
| 1 | 通过 |
| 2 | 拒绝 |
| 3 | 退回修改（仅知识审核） |

### 申请状态 (`yx_classroom_application.status`)
| 值 | 含义 |
|---|---|
| 0 | 待审批 |
| 1 | 已通过 |
| 2 | 已拒绝 |
| 3 | 已取消 |
| 4 | 已过期 |

### 通知类型 (`yx_notification.type`)
| 值 | 含义 |
|---|---|
| 1 | 系统通知 |
| 2 | 审批通知 |
| 3 | 推送消息 |
| 4 | 申请结果 |

### 推送目标类型 (`yx_push_task.target_type`)
| 值 | 含义 |
|---|---|
| 1 | 全体学生 |
| 2 | 指定班级 |
| 3 | 指定用户 |

### 推送状态 (`yx_push_task.status`)
| 值 | 含义 |
|---|---|
| 0 | 草稿 |
| 1 | 已发送 |
| 2 | 已取消 |

---

## 附录 C：设计决策说明

1. **若依兼容性**：表 1-5（用户/角色/菜单）的结构参考了若依（RuoYi）的约定，字段名和类型与若依保持高度兼容，便于对接若依框架的认证与权限模块，同时扩展了 `yx_user` 中的学校业务字段（学号、院系、专业、班级等）。

2. **向量数据不入 PG**：知识条目和快捷链接的 Embedding 向量存储在 ChromaDB 中（集合名 `kb_entries` 和 `quick_links`），PostgreSQL 中只存储业务元数据。两者通过 `id` 关联。

3. **一期审核简化**：R03 确认一期采用一级审核（管理员审核 → 发布），`yx_knowledge_review` 表结构已支持多级审核扩展（通过多条记录实现），无需二期改表。

4. **教师插入对话**：通过 `yx_conversation.status` 和 `yx_message.sender_type` 区分 AI 与教师消息。WebSocket 实时通信的连接状态不落库，仅在应用层维护。

5. **主动推送**：`yx_push_task` 记录推送任务元数据，实际发送时批量写入 `yx_notification` 表。一期仅支持手动发送，定时触发为二期预留。

6. **学生特征**：R03 确认一期仅做"个人描述"文本框，已合并到 `yx_user.bio` 字段，不单独建表。二期 AI 自动生成画像时再扩展。

7. **软删除**：所有表均使用 `is_deleted` 软删除（`yx_audit_log` 除外，该表标记永远为 FALSE）。查询时需添加 `WHERE is_deleted = FALSE` 条件（MyBatis-Plus 可通过全局配置自动注入）。
