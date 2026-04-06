# V4 学生端功能增强与质量提升

## 项目信息
- **Spec 版本**: spec-v4-student-enhancement
- **创建日期**: 2026-04-06
- **T0 架构师**: Cascade
- **T1 协调员**: Kiro
- **状态**: 任务分解完成，待执行

## 总体目标

在 spec-v3 和 spec-v4-chat-bugfix 的基础上，完成学生端的功能补全和质量提升：
1. 清理遗留技术债
2. 对接已有后端 API
3. 新增聊天历史功能
4. 扩充知识库覆盖面
5. 验证 AI 防幻觉机制

## 任务树结构

```
v4-student-enhancement/
├── batch_1 (并行) ─────────────────────────────┐
│   ├── f01-knowledge-detail-api/               │
│   ├── f02-theme-token-unify/                  │
│   ├── f03-chat-history/                       │
│   └── f04-services-stats/                     │
│                                                ├─→ batch_2 (串行)
├── batch_2 (串行，依赖 batch_1) ───────────────┤
│   ├── f05-quick-questions-dynamic/            │
│   ├── f05a2-source-preview-markdown/          │
│   └── f06-chat-integration/                   │
│                                                │
├── batch_kb (与前端完全并行) ──────────────────┤
│   └── fkb-knowledge-expansion/                │
│                                                │
├── batch_verify (依赖 batch_kb) ───────────────┤
│   └── fgr-ai-grounding-verify/                │
│                                                │
└── batch_int (依赖 batch_2 + batch_verify) ────┘
    └── int-v4-final/
```

## 执行编排

### Batch 1: 并行主批次（零文件冲突）
**任务**: F-V4-01, F-V4-02, F-V4-03, F-V4-04  
**并行**: ✅ 可同时执行  
**预计时间**: 6-8 小时（并行）

| 任务 ID | 名称 | 优先级 | 工作量 | 文件 |
|---------|------|--------|--------|------|
| F-V4-01 | 知识详情页 API 对接 | P0 | 1-2h | knowledge/detail.vue, api/knowledge.ts |
| F-V4-02 | 主题色 Token 统一 | P1 | 1h | 11 个文件 CSS 替换 |
| F-V4-03 | 聊天历史记录 | P0 | 3-4h | NEW pages/chat/history.vue, pages.json |
| F-V4-04 | 事务导办统计卡片 | P2 | 1-2h | services/index.vue |

**文件冲突检查**: ✅ 无冲突

---

### Batch 2: Chat 集成批次（串行）
**任务**: F-V4-05 → F-V4-05-A2 → F-V4-06  
**并行**: ❌ 必须串行  
**依赖**: batch_1 完成  
**预计时间**: 5-7 小时（串行）

| 任务 ID | 名称 | 优先级 | 工作量 | 依赖 |
|---------|------|--------|--------|------|
| F-V4-05 | 快捷问题动态化 | P1 | 1-2h | batch_1 |
| F-V4-05-A2 | 来源弹层 Markdown 渲染 | P1 | 0.5-1h | F-V4-05 |
| F-V4-06 | Chat 页面集成增强 | P0 | 3-4h | F-V4-01, F-V4-03, F-V4-05, F-V4-05-A2 |

**串行原因**: 三个任务都修改 chat/index.vue，必须按顺序执行

---

### Batch KB: 知识库通道（与前端完全并行）
**任务**: F-V4-KB  
**并行**: ✅ 可与 batch_1/batch_2 同时执行  
**预计时间**: 6-8 小时

| 任务 ID | 名称 | 优先级 | 工作量 | 说明 |
|---------|------|--------|--------|------|
| F-V4-KB | 知识库扩量 — 生活服务类 | P0 | 6-8h | 纯数据层操作，零代码交叉 |

**目标**: 从 55 个条目扩充到 75+ 个，补齐生活服务类高频问题

---

### Batch Verify: 验证收尾
**任务**: F-V4-GR  
**依赖**: batch_kb 完成  
**预计时间**: 2-3 小时

| 任务 ID | 名称 | 优先级 | 工作量 | 依赖 |
|---------|------|--------|--------|------|
| F-V4-GR | AI 防幻觉端到端验证 | P1 | 2-3h | F-V4-KB |

**目标**: 验证 KB 扩量后防幻觉机制有效性

---

### Batch Int: 集成验收
**任务**: INT-V4-FINAL  
**依赖**: batch_2 + batch_verify 完成  
**预计时间**: 2-3 小时

| 任务 ID | 名称 | 优先级 | 工作量 | 依赖 |
|---------|------|--------|--------|------|
| INT-V4-FINAL | V4 集成验收 | P0 | 2-3h | 所有任务完成 |

**验收标准**: 10 个 AC 全部通过

---

## 时间估算

### 最优路径（充分并行）
- Batch 1 + Batch KB 并行: 6-8 小时
- Batch 2 串行: 5-7 小时
- Batch Verify: 2-3 小时
- Batch Int: 2-3 小时
- **总计**: 15-21 小时

### 保守估算（考虑返工）
- 增加 20% buffer: 18-25 小时
- 约 2-3 个工作日

---

## 风险登记

| 风险 ID | 描述 | 概率 | 影响 | 缓解措施 |
|---------|------|------|------|---------|
| RISK-V4-01 | business-api 未运行导致会话 API 不可用 | 中 | 高 | L0-L2 可在无后端情况下通过 |
| RISK-V4-02 | chat/index.vue 串行批次效率 | 低 | 中 | 可合并 F-V4-05 和 F-V4-05-A2 |
| RISK-V4-03 | KB 扩量内容准确性 | 中 | 中 | 优先使用官方文档，标注不确定信息 |

---

## 验收标准（AC）

1. **AC-1**: 知识详情页从 AI 来源点击可进入，显示完整条目
2. **AC-2**: 所有页面 grep #006a64 仅剩 theme.scss 定义行
3. **AC-3**: 会话历史页可列出/新建会话
4. **AC-4**: 事务导办页统计卡片显示
5. **AC-5**: 快捷问题非硬编码
6. **AC-6**: 来源弹层 markdown 正确渲染
7. **AC-7**: Chat 页面有历史入口，来源点击跳详情页
8. **AC-8**: KB entry_count ≥ 75
9. **AC-9**: 拒答准确率 100%，Recall@5 ≥ 90%
10. **AC-10**: TypeScript 编译零错误，所有已有功能无回归

---

## 执行建议

### 给 T2 Foreman
1. **Batch 1 可并行下发**：4 个任务文件冲突已验证为零，可同时执行
2. **Batch 2 必须串行**：严格按 F-V4-05 → F-V4-05-A2 → F-V4-06 顺序
3. **Batch KB 独立通道**：可由独立 T2 或人工执行，与前端完全并行
4. **F-V4-02 改动简单**：纯 find-replace，建议给 T2 明确替换规则
5. **F-V4-06 改动面大**：是 chat/index.vue 的最终集成，需重点 review

### 给 T3 Executor
- 每个任务目录下有详细的 `_task.md`，包含技术要点和完成标准
- 优先完成 L0-L1 验证，确保代码质量
- L2-L3 需要后端支持，无后端时可跳过
- 完成后编写 `_report.md`，记录执行过程和问题

---

## 上下文文件

### 必读（所有任务）
- `apps/student-app/src/api/chat.ts` — 已有全部会话/消息 API
- `apps/student-app/src/api/knowledge.ts` — 已有 getKnowledgeEntryDetail
- `apps/student-app/src/styles/theme.scss` — $primary 定义
- `apps/student-app/src/pages/chat/index.vue` — 主战场

### 后端参考
- `services/business-api/.../knowledge/controller/KnowledgeEntryController.java`
- `services/business-api/.../conversation/controller/ConversationController.java`

### 知识库
- `knowledge-base/raw/first-batch-processing/converted/学生手册-生活服务.md` (401KB, 5076行)
- `knowledge-base/raw/first-batch-processing/converted/医小管知识库二次修改版.md` (178KB, 2103行)
- `services/ai-service/scripts/batch_ingest_kb.py` — 入库脚本

---

## 下一步行动

### 窗口 1（T1-Coordinator）- 当前窗口
1. ✅ 任务分解完成（T1）
2. ⏳ 下发 batch_1 任务给 T2/T3
3. ⏳ 下发 batch_kb 任务给独立执行者
4. ⏳ 等待 batch_1 完成后下发 batch_2
5. ⏳ 等待 batch_kb 完成后下发 batch_verify
6. ⏳ 所有任务完成后 🚨 **触发窗口 2 开启**

### 窗口 2（T1-Integrator）- Checkpoint 4 后开启
7. ⏳ 接收启动包
8. ⏳ 准备测试环境
9. ⏳ 执行集成验收（INT-V4-FINAL）
10. ⏳ 编写验收报告
11. ⏳ 签字发布

**双窗口协作方案**: 详见 `.tasks/v4-student-enhancement/_t1_dual_window_plan.md`

---

## 联系方式

- **T0 架构师**: 需求澄清、架构问题
- **T1 协调员**: 任务分配、进度跟踪、二次验收
- **T2 Foreman**: 任务分发、初次验证
- **T3 Executor**: 代码实现、自检、报告

---

**任务树创建完成！准备开始执行。**
