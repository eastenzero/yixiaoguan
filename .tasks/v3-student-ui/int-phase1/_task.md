---
id: "int-phase1"
parent: "v3-student-ui"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

scope: []
out_of_scope:
  - "apps/student-app/src/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/v3-student-ui/s1-theme-unification/_report.md"
  - ".tasks/v3-student-ui/s2-tabbar-routing/_report.md"

done_criteria:
  L0: "s1-theme-unification/_report.md 存在；s2-tabbar-routing/_report.md 存在"
  L1: "apps/student-app 编译零错误（npm run build:h5 退出码=0）"
  L2: "无自动化测试（前端 H5 预览为主）"
  L3: |
    以下全部通过：
    1. theme.scss 中 $primary-40 = #006a64（grep 验证）
    2. theme.scss 中 $md-sys-color-surface-container-lowest 变量存在（grep 验证）
    3. pages.json Tab3 pagePath = pages/services/index（grep 验证）
    4. pages.json Tab2 text = 智能问答，Tab3 text = 事务导办（grep 验证）
    5. CustomTabBar.vue labels 为中文：首页/智能问答/事务导办/我的（grep 验证）
    6. 全局无残留 switchTab.*apply/status（grep 验证，预期零结果）
    7. pages/services/index.vue 文件存在（L0 存在性）

depends_on: ["s1-theme-unification", "s2-tabbar-routing"]
created_at: "2026-04-04"
---

# int-phase1：Phase 1 地基验收门控

> batch-1（s1+s2）全部完成后的集成验收。通过后才放行 batch-2（s4-services-page）。验收方式为自动化 grep 检查 + 编译验证，无需手动启动 H5 服务。

## 背景

s1 和 s2 是所有后续模块的地基。必须在 int-phase1 通过后才能开始 s4，防止带着错误的路由结构继续叠加。

## 验收检查清单

T2 执行以下 grep 命令，逐条记录结果到 `_report.md`：

```powershell
# 1. primary 色阶已改为 teal
Select-String -Path "apps/student-app/src/styles/theme.scss" -Pattern "primary-40.*006a64"

# 2. surface container token 已新增
Select-String -Path "apps/student-app/src/styles/theme.scss" -Pattern "surface-container-lowest"

# 3. Tab3 路由已改
Select-String -Path "apps/student-app/src/pages.json" -Pattern "services/index"

# 4. Tab 文字
Select-String -Path "apps/student-app/src/pages.json" -Pattern "智能问答"
Select-String -Path "apps/student-app/src/pages.json" -Pattern "事务导办"

# 5. CustomTabBar 中文标签
Select-String -Path "apps/student-app/src/components/CustomTabBar.vue" -Pattern "智能问答"

# 6. 无残留 switchTab apply/status（预期无输出）
Select-String -Path "apps/student-app/src/" -Pattern "switchTab.*apply" -Recurse

# 7. services/index.vue 占位文件存在
Test-Path "apps/student-app/src/pages/services/index.vue"
```

```powershell
# 8. 编译验证（在 apps/student-app 目录执行）
npm run build:h5
```

## 放行条件

以上 8 项全部通过 → 在本文件 frontmatter 改 `status: "done"`，放行 batch-2。

任意一项失败 → 回退对应任务（s1 或 s2），记录失败原因，**不得跳过进入 batch-2**。
