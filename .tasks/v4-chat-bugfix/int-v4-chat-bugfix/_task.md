---
id: "int-v4-chat-bugfix"
parent: "v4-chat-bugfix"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

scope:
  - ".tasks/v4-chat-bugfix/**"

out_of_scope:
  - "apps/student-app/src/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v4-chat-bugfix.yaml"
  - ".tasks/v4-chat-bugfix/fix-a-chat-markdown-penetration/_report.md"
  - ".tasks/v4-chat-bugfix/fix-b-chat-navbar-custom/_report.md"
  - ".tasks/v4-chat-bugfix/fix-c-knowledge-markdown-fallback/_report.md"
  - ".tasks/v4-chat-bugfix/fix-d-login-userinfo-mapping/_report.md"

done_criteria:
  L0: "FIX-A/FIX-B/FIX-C/FIX-D 四份 _report.md 全部存在"
  L1: "集成报告包含 npm run build:h5 零错误证据"
  L2: "集成报告逐条覆盖自动验收项：navigationStyle custom、chat/knowledge 样式穿透、userinfo 兼容映射"
  L3: "集成报告逐条覆盖 AC-1~AC-7 手工验收并给出 PASS/PARTIAL/FAIL 语义结论"

depends_on: ["fix-c-knowledge-markdown-fallback"]
created_at: "2026-04-06 00:55:00"
---

# INT：spec-v4-chat-bugfix 集成验收

> 汇总四个修复任务证据，形成可签收的语义结论，判断 5 个 bug 是否全部闭环。

## 背景

spec-v4 属于前端展示与登录链路质量收口任务。必须通过“自动化证据 + H5 人工验收”双轨确认，才能标记任务树完成。

## 验收输出要求

- 使用结构化验收表（验收项 / 预期值 / 实测 / 状态）
- 给出证据路径（命令输出、报告文件）
- 最终结论仅允许：`PASS` / `PARTIAL` / `FAIL`
- 若非 PASS，明确阻塞点与返工任务 ID

## 自动化检查清单

1. `npm run build:h5` 编译零错误
2. `pages.json` chat 页面命中 `navigationStyle: custom`
3. `chat/index.vue` markdown 样式穿透方案存在
4. `knowledge/detail.vue` markdown 样式穿透方案存在且与 chat 一致
5. `login/index.vue` 命中 `ruoyiUser.id ?? ruoyiUser.userId` 兼容映射

## 已知陷阱

- 不接受“体感正常”结论，必须逐条对照 spec-v4 AC-1~AC-7
- 集成任务不允许再修改业务代码，仅做验收归档与判定
