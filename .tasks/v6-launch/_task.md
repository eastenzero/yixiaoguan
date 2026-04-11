---
id: "v6-launch"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false
spec: ".tasks/_spec-v6-internal-testing-launch.yaml"

batches:
  - name: "batch-1"
    tasks: ["v6a-01-teacher-purple", "v6a-02-call-teacher-btn", "v6a-03-batch-accounts"]
    parallel: true
  - name: "batch-2"
    tasks: ["v6b-01-teacher-intervention"]
    depends_on: "batch-1"
  - name: "batch-3"
    tasks: ["v6c-01-teacher-mobile"]
    depends_on: "batch-2"
---

# V6 内测上线 — Phase A 基础就绪

> 教师端主题换紫 + 学生端呼叫老师按钮 + 批量测试账号全部就绪，Phase B/C 可启动。

## 子任务

| 任务 ID | 描述 | 状态 | 依赖 |
|---------|------|------|------|
| v6a-01-teacher-purple | 教师端主题色绿→紫 | done | - |
| v6a-02-call-teacher-btn | 学生端"呼叫老师"按钮 | done | - |
| v6a-03-batch-accounts | 批量生成内测账号 (25学生+12教师) | done | - |
| v6b-01-fix-callteacher | 修复 callTeacher messageId=0 + reason→questionSummary | done | v6a-02 |

## Git 分支
- 工作分支: `feat/v6-launch` (from main)
- 合并条件: batch-1 全部 L0-L2 PASS + T1 L3 验收

## 遗留 DEBT

| ID | 描述 | 优先级 |
|----|------|--------|
| DEBT-V6A-01 | 左侧栏“+ 新建任务”按钮仍为紫色渐变，但底部“个人中心”“退出登录”图标颜色可能未统一 | P3 |
| DEBT-V6A-02 | 数据看板柱状图使用棕/橙色，非紫色系（可能是 ECharts 配色未跟随主题） | P3 |
| DEBT-V6A-03 | student-app call-teacher-btn CSS 硬编码 #008a7a（继承 main 分支基线绿色） | P3 |

## T1 执行记录
- 2026-04-11: 任务树创建，batch-1 开始下发
- 2026-04-11: batch-1 全部 3 任务 Kimi 执行完毕，T1 独立验收 L0-L2 全 PASS，scope 审计无越界
- 2026-04-11: T0 目视确认教师端紫色主题效果 OK，标注 3 项 P3 DEBT，放行继续 Phase B
- 2026-04-11: Phase B 侦察完成—后端 Escalation CRUD + WebSocket 全就绪；唯一阻塞=callTeacher messageId=0
- 2026-04-11: v6b-01 Kimi 修复 + T1 验收 PASS；T1 API 链路测试 create→pending→assign→resolve 全通
