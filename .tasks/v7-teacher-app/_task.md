---
id: "v7-teacher-app"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "high"
foundation: false
spec: ".tasks/_spec-v7-teacher-mobile-app.yaml"

batches:
  - name: "batch-1"
    tasks: ["f-v7-01-project-init"]
    parallel: false
  - name: "batch-2"
    tasks: ["f-v7-02-components-icons"]
    depends_on: "batch-1"
  - name: "batch-3"
    tasks: ["f-v7-03-login-dashboard", "f-v7-04-questions", "f-v7-05-knowledge", "f-v7-06-profile"]
    parallel: true
    depends_on: "batch-2"
  - name: "batch-4"
    tasks: ["f-v7-07-routing-smoke"]
    depends_on: "batch-3"
  - name: "batch-5"
    tasks: ["f-v7-08-login-api"]
    depends_on: "batch-4"
  - name: "batch-6"
    tasks: ["f-v7-09-escalation-api", "f-v7-10-knowledge-api"]
    parallel: true
    depends_on: "batch-5"
---

# V7 教师移动端 (UniApp) — T1 任务树

> 基于 React 原型 + Stitch 设计稿转换为 UniApp，复用学生端脚手架。

## 子任务

| Batch | 任务 ID | 描述 | 状态 | 依赖 |
|-------|---------|------|------|------|
| 1 | f-v7-01-project-init | 项目初始化 + SCSS 色彩系统 | pending | - |
| 2 | f-v7-02-components-icons | 公共组件 (TopAppBar + BottomNavBar) + 27 图标 | pending | batch-1 |
| 3 | f-v7-03-login-dashboard | 登录页 + 工作台 | pending | batch-2 |
| 3 | f-v7-04-questions | 提问列表 + 提问详情 | pending | batch-2 |
| 3 | f-v7-05-knowledge | 知识库列表 + 知识详情 | pending | batch-2 |
| 3 | f-v7-06-profile | 个人中心 | pending | batch-2 |
| 4 | f-v7-07-routing-smoke | 路由配置 + 冒烟测试 | pending | batch-3 |
| 5 | f-v7-08-login-api | API 对接 — 登录 | pending | batch-4 |
| 6 | f-v7-09-escalation-api | API 对接 — 工单/提问 | pending | batch-5 |
| 6 | f-v7-10-knowledge-api | API 对接 — 知识库 | pending | batch-5 |

## Git 分支
- 工作分支: `feat/v7-teacher-app` (from main)
- 合并条件: Phase 1 全部 L0-L2 PASS + T1 L3 验收

## T1 执行记录

| 时间 | 动作 | 结果 |
|------|------|------|
| 2026-04-11 17:15 | 任务树创建，Git 分支 feat/v7-teacher-app 创建 | ✅ |
