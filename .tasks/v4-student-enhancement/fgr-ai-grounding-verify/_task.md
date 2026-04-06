# F-V4-GR：AI 防幻觉端到端验证

## 元信息
- **任务 ID**: F-V4-GR
- **优先级**: P1
- **类型**: test
- **批次**: batch_verify
- **预计工作量**: 2-3 小时
- **前置依赖**: F-V4-KB

## 目标

llm_chat.py 已实现检索门控 (grounded 检查) 和证据不足拒答 (FALLBACK_NO_GROUNDING_ANSWER)。需端到端验证防幻觉机制有效性。

## 背景

- ai-service 已实现 grounded 检查机制
- 当检索结果相关性低于阈值时，返回拒答
- F-V4-KB 扩量后，需验证边界问题的转变

## 范围

### In Scope
1. 发送 KB 覆盖范围外的问题，确认返回拒答
2. 发送 KB 覆盖范围内的问题，确认正常回答且 grounded=true
3. KB 扩量后重新验证边界问题（如"电费怎么交"从拒答变为正常回答）
4. 更新 eval-set-v1.yaml 评测集，补充生活服务类用例

### Out of Scope
- 修改 llm_chat.py 防幻觉逻辑
- 调整检索阈值
- 新增评测指标

## 技术要点

### 1. 测试用例设计

#### 范围外问题（应拒答）
- "北京今天天气怎么样？"
- "如何做红烧肉？"
- "Python 如何安装 numpy？"
- "最新的 iPhone 价格是多少？"

#### 范围内问题（应正常回答）
- "如何申请空教室？"
- "奖学金评定标准是什么？"
- "图书馆开放时间？"
- "如何办理请假手续？"

#### 边界问题（KB 扩量后应从拒答变为正常回答）
- "电费怎么交？"
- "宿舍报修流程是什么？"
- "校园卡如何办理？"
- "如何使用淋浴？"

### 2. 验证方法

```powershell
# 方法 1：通过 H5 前端测试
# 启动 business-api 和 ai-service
# 在智能问答页面发送测试问题
# 观察回复内容和 grounded 标记

# 方法 2：直接调用 ai-service API
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "电费怎么交？", "user_id": "test"}'
```

### 3. 评测集更新

在 `scripts/eval/eval-set-v1.yaml` 中补充生活服务类用例：

```yaml
test_cases:
  # ... 现有用例 ...
  
  # 生活服务类（KB 扩量后新增）
  - id: life-001
    query: "电费怎么交？"
    expected_grounded: true
    expected_keywords: ["完美校园", "支付宝", "充值"]
    
  - id: life-002
    query: "宿舍报修流程是什么？"
    expected_grounded: true
    expected_keywords: ["后勤管理部", "报修"]
    
  - id: life-003
    query: "校园卡如何办理？"
    expected_grounded: true
    expected_keywords: ["实体卡", "虚拟码", "充值"]
    
  # 范围外问题（应拒答）
  - id: out-001
    query: "北京今天天气怎么样？"
    expected_grounded: false
    expected_fallback: true
```

## 完成标准

### L0: 存在性检查
- 验证报告文件存在（`docs/test-reports/v4-grounding-verification.md`）
- eval-set-v1.yaml 已更新（新增至少 10 个用例）

### L1: 静态检查
- 拒答用例返回 FALLBACK 文案
- 正常回答用例 grounded=true
- 边界问题在 KB 扩量后转变为正常回答

### L2: 运行时检查
- Recall@5 ≥ 90%（范围内问题检索准确率）
- 拒答准确率 = 100%（范围外问题全部拒答）
- 无误答（范围外问题不应编造答案）

### L3: 语义检查
- 拒答文案友好，不生硬
- 正常回答内容准确，有来源引用
- 边界问题回答质量符合预期

## 文件清单

### 必须创建
- `docs/test-reports/v4-grounding-verification.md` (验证报告)

### 必须修改
- `scripts/eval/eval-set-v1.yaml` (评测集更新)

### 必须阅读
- `services/ai-service/app/services/llm_chat.py` (防幻觉逻辑)
- `services/ai-service/app/config.py` (检索阈值配置)

## 验证报告模板

```markdown
# V4 AI 防幻觉端到端验证报告

## 测试环境
- ai-service 版本: v1.0
- KB entry_count: 75+
- 测试时间: 2026-04-06

## 测试用例

### 1. 范围外问题（应拒答）

| 问题 | grounded | 是否拒答 | 结果 |
|------|----------|---------|------|
| 北京今天天气怎么样？ | false | ✅ | PASS |
| 如何做红烧肉？ | false | ✅ | PASS |
| ... | ... | ... | ... |

### 2. 范围内问题（应正常回答）

| 问题 | grounded | 是否回答 | 关键词命中 | 结果 |
|------|----------|---------|-----------|------|
| 如何申请空教室？ | true | ✅ | 申请、教室 | PASS |
| 奖学金评定标准是什么？ | true | ✅ | 奖学金、评定 | PASS |
| ... | ... | ... | ... | ... |

### 3. 边界问题（KB 扩量后）

| 问题 | KB 扩量前 | KB 扩量后 | 结果 |
|------|----------|----------|------|
| 电费怎么交？ | 拒答 | 正常回答 | PASS |
| 宿舍报修流程是什么？ | 拒答 | 正常回答 | PASS |
| ... | ... | ... | ... |

## 评测指标

- **Recall@5**: 92% (≥ 90% ✅)
- **拒答准确率**: 100% (= 100% ✅)
- **误答率**: 0% (= 0% ✅)

## 结论

防幻觉机制有效，KB 扩量后边界问题转变符合预期。
```

## 执行提示

1. 先确认 F-V4-KB 已完成，KB entry_count ≥ 75
2. 设计测试用例（范围外、范围内、边界问题）
3. 通过 H5 前端或 API 直接测试
4. 记录测试结果
5. 更新 eval-set-v1.yaml
6. 编写验证报告

## 注意事项

- 测试前确保 ai-service 和 business-api 都在运行
- 边界问题需要在 KB 扩量前后分别测试
- 拒答文案应友好，不应生硬或误导

## 风险

- **RISK-V4-03**: KB 扩量内容准确性影响验证结果
  - 缓解：优先验证高质量条目覆盖的问题
  - 发现问题及时反馈给 F-V4-KB 任务

## 验证命令

```powershell
# L0: 检查文件存在
ls docs/test-reports/v4-grounding-verification.md
ls scripts/eval/eval-set-v1.yaml

# L1: 测试拒答用例
curl -X POST http://localhost:8000/api/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"query": "北京今天天气怎么样？", "user_id": "test"}'

# L2: 运行评测集（如有评测脚本）
cd services/ai-service
python scripts/eval/run_eval.py --eval-set eval-set-v1.yaml
```

## 参考资料

- 防幻觉设计文档：`docs/architecture/ai-grounding-design.md`
- 检索门控阈值：`services/ai-service/app/config.py`
- 现有评测集：`scripts/eval/eval-set-v1.yaml`
