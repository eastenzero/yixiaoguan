# V4 任务分发计划（多 T2 并行版）

> T1 Coordinator 给多个 T2 Foreman 的任务分配方案

---

## 分发策略

### 核心原则
1. **T2 并行优先**：充分利用多 T2 能力，最大化并行度
2. **任务包独立**：每个 T2 负责独立的任务包，减少协调成本
3. **技能匹配**：前端/数据/验证任务分配给对应 T2
4. **依赖管理**：T2 内部串行，T2 之间并行

---

## 推荐方案：3 个 T2 并行

### 方案优势
- ✅ 充分并行：3 个 T2 同时工作
- ✅ 任务包独立：每个 T2 负责完整的垂直切片
- ✅ 最短工期：约 1.5-2 天（vs 2-3 天）
- ✅ 协调成本低：T2 之间零依赖

---

## T2 分配方案

### T2-Frontend-Core（前端核心功能）

**职责**：知识详情 + 聊天历史 + Chat 集成

**任务包 1（立即执行）**:
- ✅ F-V4-01: 知识详情页 API 对接 [1-2h]
- ✅ F-V4-03: 聊天历史记录 [3-4h]

**任务包 2（等待任务包 1 完成）**:
- → F-V4-05: 快捷问题动态化 [1-2h]
- → F-V4-05-A2: 来源弹层 Markdown [0.5-1h]
- → F-V4-06: Chat 集成增强 [3-4h]

**总工作量**: 9-13 小时  
**关键路径**: 是（F-V4-06 是最终集成）  
**技能要求**: Vue 3 + TypeScript + uni-app

---

### T2-Frontend-UI（前端 UI 优化）

**职责**：主题统一 + 统计卡片

**任务包（立即执行）**:
- ✅ F-V4-02: 主题色 Token 统一 [1h]
- ✅ F-V4-04: 事务导办统计卡片 [1-2h]

**总工作量**: 2-3 小时  
**关键路径**: 否（不阻塞其他任务）  
**技能要求**: CSS/SCSS + Vue 3

---

### T2-Data-KB（数据与验证）

**职责**：知识库扩量 + AI 验证

**任务包 1（立即执行）**:
- ✅ F-V4-KB: 知识库扩量 [6-8h]

**任务包 2（等待任务包 1 完成）**:
- → F-V4-GR: AI 防幻觉验证 [2-3h]

**总工作量**: 8-11 小时  
**关键路径**: 否（与前端并行）  
**技能要求**: 数据处理 + Markdown + Python

---

## 并行执行时间线

```
Day 1 上午（0-4h）
├─ T2-Frontend-Core: F-V4-01 + F-V4-03 开始
├─ T2-Frontend-UI:   F-V4-02 + F-V4-04 开始
└─ T2-Data-KB:       F-V4-KB 开始

Day 1 下午（4-8h）
├─ T2-Frontend-Core: F-V4-01 + F-V4-03 完成 ✅
│                    → Checkpoint 1
│                    → F-V4-05 开始
├─ T2-Frontend-UI:   F-V4-02 + F-V4-04 完成 ✅
│                    → 空闲（可支援其他 T2）
└─ T2-Data-KB:       F-V4-KB 进行中...

Day 2 上午（8-12h）
├─ T2-Frontend-Core: F-V4-05 完成 ✅
│                    → F-V4-05-A2 + F-V4-06 开始
├─ T2-Frontend-UI:   空闲或支援
└─ T2-Data-KB:       F-V4-KB 完成 ✅
                     → Checkpoint 2
                     → F-V4-GR 开始

Day 2 下午（12-16h）
├─ T2-Frontend-Core: F-V4-06 完成 ✅
│                    → Checkpoint 3
├─ T2-Frontend-UI:   空闲
└─ T2-Data-KB:       F-V4-GR 完成 ✅

Day 2 晚上 - Day 3（16-20h）
└─ T1: INT-V4-FINAL 集成验收 [2-3h]
```

**总工期**: 约 1.5-2 天（vs 单 T2 的 2-3 天）

---

## 任务包详细定义

### 任务包 FC-1：Frontend Core Batch 1
```yaml
id: FC-1
name: "前端核心功能 - 基础"
assignee: T2-Frontend-Core
priority: P0
parallel: true
estimated: 4-6 hours
tasks:
  - F-V4-01: 知识详情页 API 对接
  - F-V4-03: 聊天历史记录
dependencies: []
deliverables:
  - pages/knowledge/detail.vue (修改)
  - pages/chat/history.vue (新建)
  - pages.json (新增路由)
verification:
  - L0: 编译无错误
  - L1: 路由注册成功
  - L2: H5 预览页面可访问
```

### 任务包 FC-2：Frontend Core Batch 2
```yaml
id: FC-2
name: "前端核心功能 - 集成"
assignee: T2-Frontend-Core
priority: P0
parallel: false  # 串行
estimated: 5-7 hours
tasks:
  - F-V4-05: 快捷问题动态化
  - F-V4-05-A2: 来源弹层 Markdown
  - F-V4-06: Chat 集成增强
dependencies: [FC-1]
deliverables:
  - pages/chat/index.vue (修改)
verification:
  - L0: 编译无错误
  - L1: 所有功能点代码存在
  - L2: H5 预览功能正常
  - L3: 会话持久化测试通过
```

### 任务包 FU-1：Frontend UI Optimization
```yaml
id: FU-1
name: "前端 UI 优化"
assignee: T2-Frontend-UI
priority: P1
parallel: true
estimated: 2-3 hours
tasks:
  - F-V4-02: 主题色 Token 统一
  - F-V4-04: 事务导办统计卡片
dependencies: []
deliverables:
  - 11 个文件 CSS 修改
  - pages/services/index.vue (修改)
verification:
  - L0: 编译无错误
  - L1: grep #006a64 仅剩 theme.scss
  - L2: H5 预览颜色无变化
```

### 任务包 DK-1：Data & Knowledge Base
```yaml
id: DK-1
name: "知识库扩量"
assignee: T2-Data-KB
priority: P0
parallel: true
estimated: 6-8 hours
tasks:
  - F-V4-KB: 知识库扩量
dependencies: []
deliverables:
  - 至少 20 个新增 .md 文件
  - 入库脚本执行日志
verification:
  - L0: 新增文件存在
  - L1: 入库脚本无错误
  - L2: KB entry_count ≥ 75
```

### 任务包 DK-2：Data Verification
```yaml
id: DK-2
name: "AI 防幻觉验证"
assignee: T2-Data-KB
priority: P1
parallel: false
estimated: 2-3 hours
tasks:
  - F-V4-GR: AI 防幻觉验证
dependencies: [DK-1]
deliverables:
  - docs/test-reports/v4-grounding-verification.md
  - scripts/eval/eval-set-v1.yaml (更新)
verification:
  - L0: 报告文件存在
  - L1: 拒答用例返回 FALLBACK
  - L2: Recall@5 ≥ 90%
```

### 任务包 INT：Integration Test
```yaml
id: INT
name: "集成验收"
assignee: T1
priority: P0
parallel: false
estimated: 2-3 hours
tasks:
  - INT-V4-FINAL: 集成验收
dependencies: [FC-2, DK-2]
deliverables:
  - 10 个 AC 验收记录
  - 集成测试报告
verification:
  - 所有 AC 通过
  - 无阻塞性问题
  - 无严重回归
```

---

## 检查点与同步机制

### Checkpoint 1: Frontend Core Batch 1 完成
**时间**: Day 1 下午  
**触发**: T2-Frontend-Core 完成 FC-1  
**检查**:
- [ ] F-V4-01 完成，知识详情页可用
- [ ] F-V4-03 完成，历史页面可用
- [ ] L0-L1 验证通过

**决策**: 通过后 T2-Frontend-Core 继续 FC-2

---

### Checkpoint 2: Knowledge Base 完成
**时间**: Day 2 上午  
**触发**: T2-Data-KB 完成 DK-1  
**检查**:
- [ ] F-V4-KB 完成，KB entry_count ≥ 75
- [ ] 入库脚本运行成功
- [ ] 新增条目可检索

**决策**: 通过后 T2-Data-KB 继续 DK-2

---

### Checkpoint 3: Frontend UI 完成
**时间**: Day 1 下午  
**触发**: T2-Frontend-UI 完成 FU-1  
**检查**:
- [ ] F-V4-02 完成，主题色统一
- [ ] F-V4-04 完成，统计卡片显示
- [ ] L0-L2 验证通过

**决策**: T2-Frontend-UI 可释放或支援其他 T2

---

### Checkpoint 4: 所有任务完成
**时间**: Day 2 下午  
**触发**: FC-2 + DK-2 全部完成  
**检查**:
- [ ] 所有 9 个任务完成
- [ ] 所有 L0-L2 验证通过
- [ ] 无阻塞性问题

**决策**: T1 开始集成验收

---

## T2 协调机制

### 每日站会
- **时间**: 每天上午 10:00
- **参与**: T1 + 3 个 T2
- **时长**: 15 分钟
- **内容**:
  - 昨日完成情况
  - 今日计划
  - 阻塞问题
  - 风险识别

### 实时沟通
- **工具**: 项目群聊
- **规则**:
  - 阻塞性问题立即上报 T1
  - 检查点完成后通知 T1
  - 发现跨 T2 依赖立即同步

### 进度更新
- **频率**: 每完成一个任务
- **方式**: 更新 `_progress.md`
- **内容**: 任务状态、完成时间、问题记录

---

## 风险应对（多 T2 版）

### RISK-MT-01: T2-Frontend-UI 提前完成导致资源闲置
**概率**: 高  
**影响**: 低  
**应对**:
- T2-Frontend-UI 完成后可支援 T2-Frontend-Core
- 或提前进入集成测试准备
- 或处理其他优先级较低的任务

### RISK-MT-02: T2 之间沟通成本
**概率**: 中  
**影响**: 中  
**应对**:
- 任务包设计确保 T2 之间零依赖
- 每日站会同步进度
- T1 作为协调中心

### RISK-MT-03: T2-Frontend-Core 关键路径延误
**概率**: 中  
**影响**: 高  
**应对**:
- T2-Frontend-Core 是关键路径，优先保障
- 如延误，T2-Frontend-UI 可支援
- T1 密切监控 FC-2 进度

---

## 对比：单 T2 vs 多 T2

| 维度 | 单 T2 | 2 个 T2 | 3 个 T2 |
|------|-------|---------|---------|
| 总工期 | 21-28h | 15-21h | 12-16h |
| 日历天数 | 3-4 天 | 2-3 天 | 1.5-2 天 |
| 并行度 | 低 | 中 | 高 |
| 协调成本 | 无 | 低 | 中 |
| 资源利用率 | 100% | 85% | 70% |
| 推荐度 | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

**推荐**: 3 个 T2（本方案）

---

## 下一步行动

### 立即执行（Day 1 上午）
1. ✅ 确认 3 个 T2 人员
2. ⏳ 下发任务包 FC-1 给 T2-Frontend-Core
3. ⏳ 下发任务包 FU-1 给 T2-Frontend-UI
4. ⏳ 下发任务包 DK-1 给 T2-Data-KB
5. ⏳ 启动每日站会机制

### 等待检查点（Day 1 下午）
6. ⏳ Checkpoint 1: FC-1 完成
7. ⏳ Checkpoint 3: FU-1 完成
8. ⏳ 下发任务包 FC-2 给 T2-Frontend-Core

### 等待检查点（Day 2）
9. ⏳ Checkpoint 2: DK-1 完成
10. ⏳ 下发任务包 DK-2 给 T2-Data-KB
11. ⏳ Checkpoint 4: 所有任务完成
12. ⏳ T1 执行集成验收

---

**3 个 T2 并行，最短工期 1.5-2 天！** 🚀

#### T3-Frontend（前端专员）
**Batch 1（并行启动）**:
- ✅ F-V4-01: 知识详情页 API 对接 [1-2h]
- ✅ F-V4-03: 聊天历史记录 [3-4h]
- ✅ F-V4-04: 事务导办统计卡片 [1-2h]

**Batch 2（等待 batch_1）**:
- → F-V4-05: 快捷问题动态化 [1-2h]
- → F-V4-05-A2: 来源弹层 Markdown [0.5-1h]
- → F-V4-06: Chat 集成 [3-4h]

**总工作量**: 11-15 小时

#### T3-Data（数据专员）
**Batch 1（并行启动）**:
- ✅ F-V4-02: 主题色 Token 统一 [1h]

**Batch KB（独立通道）**:
- ✅ F-V4-KB: 知识库扩量 [6-8h]

**Batch Verify（等待 batch_kb）**:
- → F-V4-GR: AI 防幻觉验证 [2-3h]

**总工作量**: 9-12 小时

#### T1（集成验收）
**Batch Int（最终）**:
- → INT-V4-FINAL: 集成验收 [2-3h]

---

---

## 备选方案对比

### 方案 B：2 个 T2（前端 + 数据）
- T2-Frontend: 所有前端任务 [11-15h]
- T2-Data: 所有数据任务 [9-12h]
- 工期: 2-3 天
- 优点: 协调成本更低
- 缺点: 前端任务串行，工期较长

### 方案 C：4 个 T2（极致并行）
- T2-1: F-V4-01 + F-V4-06
- T2-2: F-V4-03 + F-V4-05
- T2-3: F-V4-02 + F-V4-04
- T2-4: F-V4-KB + F-V4-GR
- 工期: 1-1.5 天
- 优点: 最短工期
- 缺点: 协调成本高，资源利用率低（50%）

**推荐方案 A（3 个 T2）**: 平衡工期、成本和协调复杂度

---

**准备下发任务！** 🚀
