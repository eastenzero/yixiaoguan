---
id: "int-login-auth-regression"
parent: "bugfix-login-userdata"
type: "integration-test"
status: "pending"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

scope:
  - ".tasks/bugfix-login-userdata/**"

out_of_scope:
  - "services/**"
  - "apps/**"
  - "scripts/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-bugfix-login-userdata.yaml"
  - ".tasks/bugfix-login-userdata/fix-0-captcha-disabled/_report.md"
  - ".tasks/bugfix-login-userdata/fix-1-generate-userdata-script/_report.md"
  - ".tasks/bugfix-login-userdata/fix-2-fix-and-insert-bcrypt/_report.md"
  - ".tasks/bugfix-login-userdata/fix-3-deploy-and-e2e-login/_report.md"

done_criteria:
  L0: "fix-0~fix-3 四份 _report.md 全部存在，且均有命令证据"
  L1: "脚本修复与部署验收的证据链闭环：列名对齐 + BCrypt + status=1 + captcha 关闭"
  L2: "最终验收表覆盖 T0 acceptance_criteria 全部条目，并逐条标注 PASS/FAIL"
  L3: "给出 T1 语义判定：是否解除登录阻塞并允许放行后续 spec-v4"

depends_on: ["fix-3-deploy-and-e2e-login"]
created_at: "2026-04-05 23:40:00"
---

# INT：登录认证回归总验收

> 汇总 FIX-0~FIX-3 的执行证据，输出可签收的 L3 语义结论，作为是否放行下一阶段的唯一依据。

## 背景

该 bugfix 属于地基阻塞项，若验收标准不闭环，后续功能开发会建立在不稳定登录链路上，风险不可接受。

## 验收输出要求

- 使用结构化验收表（验收项 / 预期值 / 实测 / 状态）
- 明确证据路径（命令输出、报告文件）
- 最终结论仅允许：`PASS` / `PARTIAL` / `FAIL`
- 若非 PASS，必须写清阻塞点与返工任务 ID

## 已知陷阱

- 不接受“主观感觉可用”结论，必须逐条对照 T0 规格
- 不跨范围追加新需求，只做本次 bugfix 的收口判定
