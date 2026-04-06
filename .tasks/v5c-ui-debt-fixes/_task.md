---
id: "v5c-ui-debt-fixes"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "medium"
risk: "low"
foundation: false

batches:
  - name: "batch-1"
    tasks: ["fix-01", "fix-04"]
    parallel: true
    note: "fix-01 走 165 服务器 Docker；fix-04 改 knowledge/detail.vue；无文件冲突"
  - name: "batch-2"
    tasks: ["fix-02", "fix-03"]
    parallel: false
    depends_on: "batch-1"
    note: "两任务均修改 chat/index.vue，T2 在同一次执行中按序完成（先 02 再 03）"
  - name: "batch-int"
    tasks: ["int-v5c"]
    depends_on: "batch-2"

created_at: "2026-04-06"
---

# v5c UI Debt Fixes — 父任务

> spec-v5a/v5b 遗留的 4 项 UI/配置问题修复，全部为轻量变更。

## 背景

- FIX-01：DEBT-V5A-02，captchaImage 500 修复
- FIX-02/03：聊天页参考资料卡片样式统一 + 弹层底部按钮防遮挡
- FIX-04：知识详情页移除"暂不可用"误导提示

## 已知陷阱

- FIX-02 与 FIX-03 均修改 `chat/index.vue`，**必须串行**
- FIX-01 涉及 Docker 重建，若容器内缺字体则 `apk add ttf-dejavu` 后需重建镜像
