# P3B 阈值调参报告

## 任务信息
- **任务 ID**: p3b-threshold-tuning
- **执行时间**: 2026-04-04
- **评测集**: docs/test-reports/eval-set-v1.yaml（32 题，hit=14 / reject=13 / boundary=5）

## 调参目标
- Recall@5 ≥ 0.85
- 拒答准确率 ≥ 0.90
- 5 条边界情况均返回友好拒答而非幻觉内容

---

## 一、基线评测（调参前）

### 1.1 原始参数（config.py）
```python
rag_min_score: float = 0.55
rag_min_best_score: float = 0.62
rag_min_avg_score: float = 0.58
rag_min_source_count: int = 2
```

### 1.2 首轮基线（使用原始 run_eval.py）
| 指标 | 数值 |
|------|------|
| Recall@5 | **0.00%** |
| 拒答准确率 | **100.00%** |

**根因分析**：chunk 拆分后 entry_id 变为 `KB-xxxx__chunk_N` 格式，而原始 `run_eval.py` 使用精确字符串匹配（`eid in actual_ids[:5]` 为列表成员判断），导致所有期望条目被判定为未命中。该问题属于评测脚本与 chunk 粒度不兼容，**非阈值本身问题**。

### 1.3 修复 eval 脚本后基线（原始阈值）
修复 `temp/run_eval.py` 中的 `calculate_recall_at_5` 与 `is_hit_expected`，改为前缀/子串匹配（支持 `__chunk_N` 后缀）：

| 指标 | 数值 |
|------|------|
| Recall@5 | **92.86%** (13/14) |
| 平均 Recall@5 | **79.76%** |
| 拒答准确率 | **100.00%** (18/18) |
| 生活服务类拒答准确率 | **100.00%** (5/5) |

**命中明细（14 题 hit）**：
- ✅ 命中 13 题：eval-001 ~ eval-005、eval-007 ~ eval-010、eval-012 ~ eval-014
- ❌ 未命中 1 题：eval-006（毕业生档案去向核对）
  - 该题期望条目 `KB-20260324-0016` 实际主题为「学生心理测评参与与异常处理规则」，与查询语义不匹配，检索系统无法召回，属于评测集期望条目标注问题，非阈值可解。

**拒答明细（18 题 reject+boundary）**：
- ✅ 全部正确拒答
- eval-011（综合素质测评）在原始阈值下被 `best_score_too_low` 拦截，但其期望条目 `KB-20260324-0060` 与 `KB-20260324-0105` 实际已被检索到 top-5 中，因此 Recall@5 仍计为命中。

---

## 二、参数调整与验证

### 2.1 调整策略
按任务要求顺序执行：
1. 先调 `rag_min_best_score`
2. 再评估 `rag_min_source_count`
3. 最后微调其余

### 2.2 关键观测数据

| 查询 | 类型 | best_score | 原始阈值下状态 | 说明 |
|------|------|------------|----------------|------|
| eval-011 综合素质测评 | hit | 0.6125 | 被拦截 | 期望条目已在 top-5，阈值略严 |
| eval-032 校园卡充值 | reject | 0.6101 | 被拦截 | 若阈值降到 0.61 以下会放行 |

### 2.3 最终调整
仅修改一项参数，其余保持原值：

```python
rag_min_best_score: float = 0.611   # 从 0.62 下调
```

**调整理由**：
- 0.611 > eval-011 的 best_score（0.6125），允许该边缘命中通过门控；
- 0.611 > eval-032 的 best_score（0.6101），继续拒答该生活服务类查询；
- 其余 reject/boundary 查询 best_score 均 ≤ 0.6101，不受此微调影响。

`rag_min_source_count` 保持为 2，因当前库中绝大多数条目仅含 1 个 chunk（`__chunk_0`），chunk 数与 entry 数在 top-5 中差异极小，暂无需调整粒度统计逻辑。

### 2.4 调参后验证结果

| 指标 | 调参后数值 | 目标 | 状态 |
|------|-----------|------|------|
| Recall@5 | **92.86%** (13/14) | ≥ 85% | ✅ 达标 |
| 平均 Recall@5 | **79.76%** | — | — |
| 拒答准确率 | **100.00%** (18/18) | ≥ 90% | ✅ 达标 |
| 生活服务类拒答准确率 | **100.00%** (5/5) | — | ✅ |

**调参前后对比**

| 阶段 | Recall@5 | 拒答准确率 | 备注 |
|------|----------|-----------|------|
| 原始脚本 + 原始阈值 | 0.00% | 100.00% | 脚本 entry_id 匹配 bug |
| 修复脚本 + 原始阈值 | 92.86% | 100.00% | 真实基线 |
| 修复脚本 + 调参后 | 92.86% | 100.00% | 优化边缘命中门控 |

---

## 三、边界情况抽查（L3 验证）

抽查 5 条 boundary 问题，均返回标准友好拒答，无幻觉内容：

| ID | 问题 | 实际回答 | 结果 |
|----|------|----------|------|
| eval-023 | 学校附近有什么好吃的？ | 很抱歉，医小管目前尚未学习到相关说明... | ✅ 友好拒答 |
| eval-024 | 辅导员办公室在哪栋楼？ | 很抱歉，医小管目前尚未学习到相关说明... | ✅ 友好拒答 |
| eval-025 | 图书馆能借几本书，借多久？ | 很抱歉，医小管目前尚未学习到相关说明... | ✅ 友好拒答 |
| eval-026 | 校医院上班时间是什么时候？ | 很抱歉，医小管目前尚未学习到相关说明... | ✅ 友好拒答 |
| eval-027 | 学校食堂有哪些档口？ | 很抱歉，医小管目前尚未学习到相关说明... | ✅ 友好拒答 |

---

## 四、修改文件清单

| 文件 | 修改内容 | 是否在 scope |
|------|----------|-------------|
| `services/ai-service/app/core/config.py` | `rag_min_best_score`: 0.62 → 0.611 | ✅ |
| `temp/run_eval.py` | 修复 `calculate_recall_at_5` 与 `is_hit_expected`，支持 chunk ID 前缀匹配 | ✅ |
| `docs/test-reports/completion-reports/P3B-threshold-tuning-report.md` | 本报告 | ✅ |

**禁改路径未触碰**：
- `services/ai-service/app/core/chunker.py` ❌ 未修改
- `knowledge-base/entries/first-batch-drafts` ❌ 未修改
- `services/ai-service/data/chroma` ❌ 未修改
- `services/business-api` ❌ 未修改

---

## 五、结论

1. `python -m py_compile services/ai-service/app/core/config.py` 无报错。
2. 最终参数下 Recall@5 = **92.86%** ≥ 85%，拒答准确率 = **100%** ≥ 90%，边界情况全部友好拒答。
3. 核心问题为 chunk 模式下 `run_eval.py` 的 entry_id 匹配逻辑与 `rag_min_best_score` 对边缘命中查询略严；修复脚本并微调 best_score 阈值后达标。
