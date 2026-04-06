---
id: "f-v5a-03"
parent: "v5a-quick-fixes"
type: "feature"
status: "pending"
tier: "T3"
priority: "medium"
risk: "low"
foundation: false

depends_on: ["f-v5a-02"]

scope:
  - "apps/student-app/src/pages/chat/index.vue"
out_of_scope:
  - "apps/student-app/src/styles/**"
  - "apps/student-app/src/api/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/chat/index.vue"
  - "apps/student-app/src/styles/theme.scss"

done_criteria:
  L0: "apps/student-app/src/pages/chat/index.vue 存在"
  L1: "grep 'rgba(0, 106, 100' apps/student-app/src/pages/chat/index.vue 有结果（方案B背景色已写入）"
  L2: "grep -c 'surface-container-low' apps/student-app/src/pages/chat/index.vue 在 .source-item 范围内返回 0"
  L3: "参考资料卡片在白色背景上层次清晰，点击态有视觉反馈，不像 disabled 状态"

created_at: "2026-04-06"
---

# F-V5A-03: 参考资料卡片样式优化

> AI 回答下方参考资料卡片视觉层次清晰，与白色背景形成明显区分，不再像 disabled 状态。

## 背景

当前 `.source-item` 使用 `background: $md-sys-color-surface-container-low`（浅灰），在白色气泡背景上视觉层次不清晰，容易被误认为不可点击。

## 变更详情

- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: `.source-item` style block（约 line 1169-1202）
- **采用方案 B**（与主题色呼应）：

```scss
.source-item {
  background: rgba(0, 106, 100, 0.06);
  border: 1px solid rgba(0, 106, 100, 0.15);
  border-radius: 8rpx;
  // 移除原 background: $md-sys-color-surface-container-low
}
```

## 已知陷阱

- **必须在 f-v5a-02 完成后执行**，因为两者都修改 `chat/index.vue`，顺序执行避免冲突
- 保留点击态（`:active` 或 `@tap` 视觉反馈）逻辑不变，只改背景和边框
- uni-app H5 中 `rgba()` 完全兼容，无需担心兼容性
