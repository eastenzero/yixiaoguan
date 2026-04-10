# T3 任务: v6-kb-expansion RAG-EVAL

## 角色
你是山东第一医科大学（医小管）AI助手的质量评测专家。

## 任务目标
在现有评测集 `scripts/eval/eval-set-v1.yaml` 基础上，生成扩充版评测集 **v2**，并写入 `scripts/eval/eval-set-v2.yaml`。

扩充要求：
1. **保留所有原有 42 题**（不删除、不修改原题逻辑）
2. **更新部分原题的 expected_behavior**：因为新 KB 已覆盖之前无法答复的问题，部分 reject/boundary 题现在应为 hit
3. **新增 10 题**，覆盖新入库的主题，总题数达到 **52 题**（满足 AC-EVAL-01: 42-47 题+ 的要求）

---

## 需更新的原有题目（expected_behavior 变更）

新 KB（KB-20260409-*）已入库，以下原有题目现在应能命中：

| 原题 ID | 原 behavior | 新 behavior | 命中的新 KB |
|---------|------------|------------|------------|
| eval-025 | boundary | hit | KB-20260409-0026（图书借阅规则与续借） |
| eval-026 | boundary | hit | KB-20260409-0006（校医院与医疗服务） |
| eval-028 | reject | hit | KB-20260409-0031（网上报修操作指南） |
| eval-030 | reject | hit | KB-20260409-0021（校园网常见问题与技术支持） |
| eval-032 | reject | hit | KB-20260409-0023（一卡通充值方式） |

说明：
- eval-029（电费）: 现有 KB-0150 已覆盖，保持 hit (expected_entry_ids 更新为 KB-0150)
- eval-031（热水时间）: 暂无新 KB 覆盖，保持 reject

---

## 新增 10 题

新增题目需覆盖新入库主题，格式参照现有 eval-set-v1.yaml。

### 新增题目清单（edit 以下为确切题目）

1. **new-001** — 上课时间
   - question: "上午第三节课几点开始，几点结束？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0001"]
   - category: grounding-verify-in

2. **new-002** — 信息门户
   - question: "信息门户密码忘了怎么重置？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0014"]

3. **new-003** — 企业微信
   - question: "山一大企业微信怎么加入，有什么功能？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0016"]

4. **new-004** — 图书馆开馆
   - question: "黄河图书馆24小时自习室在哪，怎么进？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0027"]

5. **new-005** — 校园网
   - question: "泰安校区怎么连接有线网，认证页地址是多少？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0019"]

6. **new-006** — 缓考
   - question: "期末考试那天生病了，怎么申请缓考？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0046"]

7. **new-007** — 毕业离校
   - question: "毕业离校需要办哪些手续，线上怎么提交离校单？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0060", "KB-20260409-0061"]

8. **new-008** — 学校简介
   - question: "山东第一医科大学有几个校区，地址在哪？"
   - expected_behavior: hit
   - expected_entry_ids: ["KB-20260409-0069", "KB-20260409-0070"]

9. **new-009** — 校外无关（防幻觉）
   - question: "山东大学图书馆几点开门？"
   - expected_behavior: reject
   - expected_entry_ids: []
   - category: grounding-verify-out

10. **new-010** — 心理咨询热线
    - question: "济南校区心理咨询热线是多少？"
    - expected_behavior: hit
    - expected_entry_ids: ["KB-20260409-0064"]

---

## 输出格式

请按照 eval-set-v1.yaml 的 YAML 格式，生成完整的 `eval-set-v2.yaml` 文件。

文件头部注释格式：
```yaml
# 医小管 RAG 检索质量评测集 v2
# 生成时间: 2026-04-09
# 总题数: 52
# 基于 v1（42题）扩充，更新5题 behavior，新增10题
```

---

## 执行步骤

1. 读取 `scripts/eval/eval-set-v1.yaml` 的完整内容
2. 复制所有 42 题，按照更新表修改 eval-025/026/028/030/032 的 expected_behavior 和 expected_entry_ids
3. 在文件末尾添加 10 道新题，ID 格式为 "new-001" 到 "new-010"
4. 写入 `scripts/eval/eval-set-v2.yaml`
5. 最终输出统计：总题数、各类型分布

请开始执行。
