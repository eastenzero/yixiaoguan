---
source: "spec-v5b T0 人工验收 AC-4 观察（2026-04-06）"
status: "pending"
priority: "medium"
scope: "apps/student-app/src/pages/chat/"
---

# 遗留 UI 问题（spec-v5b 观察，非本轮引入）

> 以下问题为 spec-v4 存量，在 spec-v5b T0 人工验收时再次确认。
> 不阻塞 spec-v5b 签收，列入下一轮迭代（spec-v6 或独立 bugfix）处理。

## UI-01：参考资料条目条形框与背景色不配套

- **现象**：聊天页底部弹出的参考资料列表，条目卡片的边框颜色与背景色不协调
- **截图**：test-screenshots 中图1（聊天页参考摘要弹层）
- **影响**：视觉一致性，不影响功能
- **建议修复**：统一使用主题色 `$primary`（#006a64）系列的边框 + 背景组合，参考 `pages/home/index.vue` 的卡片样式

## UI-02：参考摘要弹层底部按钮被遮挡/重叠

- **现象**："查看详细资料" 和 "知道了" 两个按钮在手机屏幕上显示不完整，与底部导航栏重叠
- **截图**：test-screenshots 中图1（聊天页参考摘要弹层底部）
- **影响**：用户操作受阻，影响体验
- **建议修复**：弹层内容区域增加 `padding-bottom` 为底部 safe area + 导航栏高度，
  或将按钮移入滚动区域外固定在弹层底部

---
source: "spec-v5d T0 人工验收（2026-04-07）"

## DEBT-V5D-01：参考资料条目卡片轻微超出容器

- **现象**：chat 页面参考资料列表中，各条目的条形框右侧轻微超出气泡/父容器边界
- **影响**：视觉精确度，不影响功能
- **建议修复**：检查 `.source-item` 的 `width`/`box-sizing`，改为 `box-sizing: border-box` + `width: 100%`；父容器加 `overflow: hidden`

## DEBT-V5D-02：PDF 查看器直接展示完整原始文件（182页），带宽浪费

- **现象**：点击"查看原始文件"后加载的是完整 PDF（学生手册 182 页），未跳转到相关片段
- **T0 建议**：按 chunk 的 `page_start`/`page_end` 裁剪 PDF，只传输相关页码
- **实现方向**（供下轮参考）：
  1. `chunker.py` 提取 `page_start`/`page_end` 写入 chunk metadata
  2. `batch_ingestion.py` 透传两字段到 ChromaDB
  3. API 层将 `page_start` 拼入 URL fragment：`/materials/xxx.pdf#page=42`
  4. 或后端裁剪服务：按页码范围用 `pypdf` 切片后返回子文件
- **优先级**：medium（带宽优化，非 MVP 阻塞项）

---

## UI-03（补充）："知识详情暂不可用" 提示文案

- **现象**：参考资料详情页显示 "知识详情暂不可用，已为你展示引用摘要"
- **定性**：这是 spec-v4 混合方案的**设计降级行为**，符合规格
- **但如需优化**：后续可在知识库数据完善后，修复知识条目与 `material_id` 的对应关系，使详情页正常加载
