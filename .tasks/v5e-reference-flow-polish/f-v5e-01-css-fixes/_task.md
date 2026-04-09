---
id: "f-v5e-01"
parent: "v5e-reference-flow-polish"
type: "frontend-css"
status: "pending"
tier: "T3"
dispatch_via: "T2(Kiro) → T3(Kimi)"
priority: "high"
risk: "low"
depends_on: []

scope:
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/App.vue"
  - "apps/student-app/src/components/CustomTabBar.vue"
  - "apps/student-app/src/pages/apply/detail.vue"
  - "apps/student-app/src/pages/apply/classroom.vue"
  - "apps/student-app/src/pages/apply/status.vue"
  - "apps/student-app/src/pages/knowledge/detail.vue"
  - "apps/student-app/src/pages/questions/index.vue"
  - "apps/student-app/src/pages/viewer/pdf.vue"
out_of_scope:
  - "services/**"
  - "deploy/**"
  - "apps/student-app/src/pages.json"
  - "apps/student-app/src/styles/theme.scss"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v5e-reference-flow-polish.yaml"
  - ".tasks/_t0-handoff-v5e.md"

done_criteria:
  L0: "_report.md 存在；9 个目标文件均被修改（git diff --name-only 包含这些文件）"
  L1: "grep -r '#006a64' apps/student-app/src --include='*.vue' --include='*.scss' --include='*.ts' 只剩 theme.scss 和 pages.json（其余为0）"
  L2: "cd apps/student-app && npx uni build -p h5 2>&1 | grep -E 'error|Error' | grep -v 'node_modules' 输出为空（构建无错误）"

fixes:
  - id: "FIX-1"
    name: "DEBT-V5D-01 卡片溢出"
    file: "apps/student-app/src/pages/chat/index.vue"
    target: ".source-item 样式（约 L1181）"
    change: "添加 box-sizing: border-box;"
    also: ".message-sources（约 L1161）添加 overflow: hidden"

  - id: "FIX-2"
    name: "UI-02 弹层按钮遮挡"
    file: "apps/student-app/src/pages/chat/index.vue"
    target: ".source-preview-actions 样式（约 L1469）"
    change: "将 padding-bottom: max(12px, env(safe-area-inset-bottom, 12px)) 改为 padding-bottom: calc(env(safe-area-inset-bottom, 0px) + 16px)"

  - id: "FIX-3"
    name: "UI-01 卡片背景/边框色不协调"
    file: "apps/student-app/src/pages/chat/index.vue"
    target: ".source-item 样式（约 L1188-1189）"
    changes:
      - "background: #ffffff → background: rgba(0, 106, 100, 0.04)"
      - "border: 1px solid rgba(0, 106, 100, 0.2) → border: 1px solid rgba(0, 106, 100, 0.15)"

  - id: "FIX-4"
    name: "#006a64 硬编码清理"
    description: |
      替换规则：凡 SCSS style 块中直接写死 #006a64 的，改为引用 $primary（来自 theme.scss）。
      例外：pages.json / theme.scss 本身 / JS 中使用 CSS var 的 fallback（如 var(--color-primary, #006a64)）→ 不改。

      已确认各文件状态（T1 预扫描）：
      1. apps/student-app/src/pages/viewer/pdf.vue
         - 已有 @import '@/styles/theme.scss';
         - L28: .back-icon { color: #006a64; } → color: $primary

      2. apps/student-app/src/pages/knowledge/detail.vue
         - 已有 @import '@/styles/theme.scss';
         - L214: color: #006a64; → color: $primary

      3. apps/student-app/src/App.vue
         - style 块无 @import（script 有 import 但 SCSS 不共享）
         - 在 <style lang="scss"> 开头加 @import '@/styles/theme.scss';
         - L20: --color-primary: #006a64; → --color-primary: #{$primary};

      4. apps/student-app/src/pages/apply/detail.vue
         - style 块无 @import，有本地 $primary: #006a64; 定义
         - 在 <style lang="scss" scoped> 开头加 @import '@/styles/theme.scss';
         - 删除 $primary: #006a64; 这一行（其他本地变量如 $primary-container 保留）

      5. apps/student-app/src/pages/apply/classroom.vue
         - 同上：加 @import，删 $primary: #006a64;

      6. apps/student-app/src/pages/questions/index.vue
         - 同上：加 @import，删 $primary: #006a64;

      7. apps/student-app/src/components/CustomTabBar.vue（模板属性）
         - 仅有 color="var(--color-primary, #006a64)"（CSS var fallback）→ 保留不改

      8. apps/student-app/src/pages/apply/status.vue（JS 字符串）
         - 仅有 confirmColor: 'var(--color-primary, #006a64)'（uni.showModal JS 参数）→ 保留不改

      9. pages/chat/index.vue（模板属性）
         - 仅有 color="var(--color-primary, #006a64)"（CSS var fallback）→ 保留不改

report_path: ".tasks/v5e-reference-flow-polish/f-v5e-01-css-fixes/_report.md"
created_at: "2026-04-07"
---

# F-V5E-01: CSS/UI 快速修复（4项 DEBT）

> 合并修复 DEBT-V5D-01（卡片溢出）、UI-02（弹层遮挡）、UI-01（卡片配色）、DEBT-V3-01（#006a64 硬编码）。
> 纯 CSS/SCSS 修改，不涉及逻辑变更，风险低。
