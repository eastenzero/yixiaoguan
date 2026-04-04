---
id: "v3-student-ui"
parent: ""
type: "feature"
status: "pending"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

scope:
  - "apps/student-app/src/"

out_of_scope:
  - "services/"
  - "apps/teacher-web/"
  - "knowledge-base/"
  - "scripts/"
  - ".tasks/_archived-v2/"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/_spec-v3-student-ui.yaml"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"

done_criteria:
  L0: "所有子任务 _report.md 存在"
  L1: "TypeScript 编译零错误 (npm run build:h5 in apps/student-app)"
  L2: "int-v3-final 集成测试全部通过"
  L3: "TabBar 四项正确（首页/智能问答/事务导办/我的）、AI 对话显示医小管品牌、事务导办服务矩阵可访问、已有功能无回归（SSE/来源引用/空教室申请/登录）"

depends_on: []
created_at: "2026-04-04"

batches:
  - name: "batch-1"
    tasks: ["s1-theme-unification", "s2-tabbar-routing"]
    parallel: true
  - name: "int-phase1"
    tasks: ["int-phase1"]
    depends_on: "batch-1"
  - name: "batch-2"
    tasks: ["s4-services-page"]
    depends_on: "int-phase1"
  - name: "batch-3"
    tasks: ["s3-chat-redesign"]
    depends_on: "batch-2"
  - name: "batch-4"
    tasks: ["s5-home-polish", "s6-profile-polish"]
    parallel: true
    depends_on: "batch-3"
  - name: "int-v3-final"
    tasks: ["int-v3-final"]
    depends_on: "batch-4"
---

# spec-v3 学生端 UI 重做（总任务）

> 学生端从"功能可用"升级为"界面可展示"：品牌名统一"医小管"，主题 teal 化，AI 对话界面按设计稿重做，新建事务导办服务大厅页面，首页和个人中心收尾抛光。已有 SSE/来源引用/空教室申请功能完全保留，不新增任何后端接口。

## 背景

spec-v2 解决了 AI 回答质量问题（Recall@5=92.86%，拒答率=100%）。现进入"展示可用性"阶段，项目处于计划书落地期，需向学校展示完整可用的学生端。当前学生端 AI 对话界面过于简陋，第 3 个 Tab 仅有空教室申请占位，与参考设计差距大。

## 执行顺序说明

| Batch | 任务 | 并行 | 门控条件 |
|---|---|---|---|
| batch-1 | s1-theme-unification + s2-tabbar-routing | ✅ | 无前置 |
| int-phase1 | int-phase1（验收门控） | — | batch-1 全部 done |
| batch-2 | s4-services-page | — | int-phase1 通过 |
| batch-3 | s3-chat-redesign | — | batch-2 done |
| batch-4 | s5-home-polish + s6-profile-polish | ✅ | batch-3 done |
| int-v3-final | int-v3-final（全量回归） | — | batch-4 全部 done |

## 技术债清单（本轮顺带清理）

| ID | 描述 | 归属任务 |
|---|---|---|
| DEBT-V3-01 | theme.scss primary 蓝色阶与页面 $primary 内联重复 | s1 |
| DEBT-V3-02 | CustomTabBar.vue 英文标签 | s2 |
| DEBT-V3-03 | chat/index.vue 残留 history:[] 冗余字段 | s3 |

## 已知陷阱

- RISK-V3-01: custom tabBar 渲染机制需先探查（见 s2 任务）
- RISK-V3-02: chat/index.vue ~600行 style 大改，须分段验证（见 s3 任务）
- RISK-V3-03: switchTab apply/status 全局迁移，须全局 grep 后逐一修改（见 s2 任务）
