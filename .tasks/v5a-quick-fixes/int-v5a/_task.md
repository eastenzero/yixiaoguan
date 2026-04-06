---
id: "int-v5a"
parent: "v5a-quick-fixes"
type: "integration-test"
status: "done"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

depends_on: ["f-v5a-01", "f-v5a-02", "f-v5a-03", "f-v5a-04", "f-v5a-05", "f-v5a-06", "f-v5a-07"]

scope:
  - ".tasks/v5a-quick-fixes/"
out_of_scope:
  - "apps/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5a-quick-fixes.yaml"
  - ".tasks/v5a-quick-fixes/_task.md"

done_criteria:
  L0: "所有 7 个子任务目录下均有 _report.md"
  L1: "所有 _report.md 的 result 字段为 success 或 partial（无 failed）"
  L2: "逐条执行 spec 中 acceptance_criteria_global 的验证命令，AC-1~AC-7 全部通过"
  L3: "在 165 服务器上用学生账号完整走一遍：登录（含验证码）→ 问答（查看参考资料）→ 历史记录（无报错）→ 首页演示数据合理"

acceptance_checklist:
  AC-1: "登录页底部显示"初始密码与学号相同，登录后请及时修改""
  AC-2: "template/JS 中无裸写 #006a64（pages.json 除外）"
  AC-3: "参考资料卡片视觉层次清晰（浅绿背景+边框）"
  AC-4: "历史记录页无 status=undefined 控制台报错"
  AC-5: "登录页显示算术验证码；正确验证码可登录；错误有提示"
  AC-6: "点击参考资料条目后能展示有意义的内容"
  AC-7: "首页演示数据合理完整，无明显占位符"

created_at: "2026-04-06"
---

# int-v5a: 集成验收

> 7 项修复全部完成，spec-v5a 的 AC-1~AC-7 全部通过，可向 T0 提交最终汇报。

## 验收方式

T2 Foreman 按 `acceptance_checklist` 逐项确认，重点验证：
1. 165 服务器端到端流程（登录→问答→历史记录）
2. 代码层面的 grep 验证（AC-2 无硬编码、AC-4 无 undefined 参数）
3. 目视检查（AC-3 卡片样式、AC-7 数据美化）

## 已知陷阱

- AC-5（验证码）需在 165 服务器访问，本地 localhost 不验证
- F-V5A-06 如果采用方案 C（保持现状），AC-6 标记为 PARTIAL 并记录 DEBT-V5A-01，不阻塞整体通过
