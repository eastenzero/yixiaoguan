---
id: "int-v5c"
parent: "v5c-ui-debt-fixes"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

depends_on: ["fix-01", "fix-02", "fix-03", "fix-04"]

scope:
  - ".tasks/v5c-ui-debt-fixes/"
out_of_scope:
  - "apps/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5c-ui-debt-fixes.yaml"

done_criteria:
  L0: "4 个子任务目录下均有 _report.md"
  L1: "所有 _report.md 的 result 字段为 success 或 partial（无 failed）"
  L2: "逐条执行 AC-1~AC-4 验证命令，全部通过"
  L3: "在 165 服务器用账号 2524010001/2524010001 完整验证：登录（含验证码）→ 问答（参考资料卡片样式一致）→ 点击参考资料（弹层按钮不被遮挡）→ 知识详情（无暂不可用提示）"

acceptance_checklist:
  AC-1: "GET /captchaImage 返回 200，含 img+uuid；登录页显示验证码"
  AC-2: "所有参考资料条目样式统一（内嵌+弹层均为浅绿背景+边框）"
  AC-3: "弹层底部按钮完全可见，不与导航栏重叠"
  AC-4: "知识详情页无"暂不可用"字样，摘要正常展示"

created_at: "2026-04-06"
---

# int-v5c: 集成验收

> 4 项修复全部完成，AC-1~AC-4 通过，可向 T0 提交最终汇报。

## 验收方式

按 acceptance_checklist 逐项验证，重点：
1. AC-1 需在 165 服务器 curl 验证 + 目视登录页
2. AC-2/AC-3 需在 H5 实机或模拟器上目视确认
3. AC-4 grep 验证 + 目视详情页

## 已知陷阱

- FIX-01 若 Docker 重建失败，AC-1 标记 BLOCKED 不阻塞其他 AC
- FIX-02/03 完成后需在 165 上 `docker compose build student-app && docker compose up -d` 使前端生效
