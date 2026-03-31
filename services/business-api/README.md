# business-api — 主业务后端（若依 Spring Boot）

## 定位

本服务是医小管的主业务后端，承载所有与 AI 无关的稳定业务能力：
用户认证、权限控制、问答会话记录、知识库管理、申请审批、消息通知、审计日志。

## 技术栈

- Java 21
- Spring Boot 3
- 若依框架（RuoYi-Vue3）作为基础脚手架
- MyBatis-Plus
- Spring Security + JWT
- WebSocket（实时通信）
- PostgreSQL（主数据库）
- Redis（缓存 / 会话 / 限流）

## 模块划分（一期）

| 模块 | 说明 | 若依原生 / 新增 |
|---|---|---|
| 用户与认证 | 登录、JWT、角色、权限 | 若依原生 |
| 用户管理 | 批量导入学号、账号激活 | 若依原生扩展 |
| 审计日志 | 操作记录 | 若依原生 |
| 问答会话 | 创建会话、消息记录、状态管理 | 新增 |
| 知识库管理 | 条目 CRUD、审核状态机、标签分类 | 新增（若依生成器辅助） |
| 快捷链接库 | 链接条目 CRUD | 新增（若依生成器直接生成） |
| 申请审批 | 空教室申请、审批流转、操作留痕 | 新增 |
| 消息通知 | 站内消息、主动推送配置 | 新增 |
| WebSocket 服务 | 教师实时插入对话、主动推送到学生 | 新增 |
| AI 服务代理 | 向 ai-service 发起检索和问答请求 | 新增（HTTP 调用） |

## 与 AI 服务的关系

- business-api 不直接调用大模型 API
- 所有 AI 能力（RAG 检索、链接匹配、知识草稿生成）通过调用 `services/ai-service` 的 HTTP 接口实现
- AI 服务对外只暴露给 business-api，不直接与前端通信

## 开发文档

- `docs/database/schema-phase1.md`（数据库表结构）
- `docs/api/business-api-spec.md`（接口定义）
- `docs/dev-guides/ruoyi-guide.md`（若依使用约定与裁剪说明）
- `docs/dev-guides/local-setup.md`（本地环境启动）
