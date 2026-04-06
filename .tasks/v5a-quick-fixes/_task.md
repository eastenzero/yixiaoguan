---
id: "v5a-quick-fixes"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "low"
foundation: false

batches:
  - name: "batch-1"
    tasks: ["f-v5a-01", "f-v5a-04", "f-v5a-05"]
    parallel: true
    note: "f-v5a-01 与 f-v5a-04 完全无文件冲突可并行；f-v5a-05 为服务器操作独立执行"
  - name: "batch-2"
    tasks: ["f-v5a-02", "f-v5a-03"]
    parallel: false
    depends_on: "batch-1"
    note: "两任务均触碰 chat/index.vue，T2 在同一次执行中按序完成（先 02 再 03）"
  - name: "batch-3"
    tasks: ["f-v5a-06"]
    depends_on: "batch-2"
  - name: "batch-4"
    tasks: ["f-v5a-07"]
    depends_on: "batch-3"
  - name: "batch-int"
    tasks: ["int-v5a"]
    depends_on: "batch-4"

created_at: "2026-04-06"
---

# v5a Quick Fixes — 父任务

> spec-v4 交付后 demo 演示前的 7 项快速修复，全部限定在 `apps/student-app/src/` 内（F-V5A-05 额外包含 165 服务器 Redis 配置）。

## 背景

spec-v4 已于 2026-04-06 签收。本轮针对 demo 演示前发现的 UI/Bug 问题进行快速修复，不涉及新功能开发。

## 已知陷阱

- F-V5A-02 与 F-V5A-03 均修改 `chat/index.vue`，**必须串行**，否则 git 合并冲突
- F-V5A-05 需要 SSH 到 165 服务器操作 Redis，与代码变更完全独立
- F-V5A-06 有 2h 上限，超出则降级为 DEBT 记录，不阻塞其他任务
