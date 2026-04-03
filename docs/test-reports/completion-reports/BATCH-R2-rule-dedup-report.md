# BATCH-R2 规则去重报告

## 执行概要

| 项目 | 数值 |
|------|------|
| 原始规则总数 | 29 条 |
| 去重后保留 | 23 条 |
| 删除重复规则 | 6 条 |
| 重复组数 | 5 组 |

---

## 重复组处理详情

### G1: 一网通办系统操作说明 (2条)

| rule_id | material_id | evidence_status | 处理结果 |
|---------|-------------|-----------------|----------|
| RULE-A1-010 | MAT-20260324-0039 | 部分 | ✅ 保留 (canonical) |
| RULE-A1-011 | MAT-20260324-0040 | 部分 | ❌ 删除 |

**保留理由**: evidence_status相同，material_id均非空，RULE-A1-010编号更小

---

### G2: 家庭经济困难学生认定工作报告模板 (4条)

| rule_id | material_id | evidence_status | 处理结果 |
|---------|-------------|-----------------|----------|
| RULE-A1-015 | - | 部分 | ✅ 保留 (canonical) |
| RULE-A1-016 | - | 部分 | ❌ 删除 |
| RULE-A1-024 | - | 部分 | ❌ 删除 |
| RULE-A1-027 | - | 部分 | ❌ 删除 |

**保留理由**: evidence_status相同，material_id均为空，RULE-A1-015编号最小

---

### G3: 社会救助家庭经济状况核对授权 (2条)

| rule_id | material_id | evidence_status | 处理结果 |
|---------|-------------|-----------------|----------|
| RULE-A1-023 | - | 部分 | ✅ 保留 (canonical) |
| RULE-A1-026 | - | 部分 | ❌ 删除 |

**保留理由**: evidence_status相同，material_id均为空，RULE-A1-023编号更小

---

### G4: 贫困认定弃权声明 (2条)

| rule_id | material_id | evidence_status | 处理结果 |
|---------|-------------|-----------------|----------|
| RULE-A1-028 | - | 部分 | ✅ 保留 (canonical) |
| RULE-A1-029 | - | 部分 | ❌ 删除 |

**保留理由**: evidence_status相同，material_id均为空，RULE-A1-028编号更小

---

## 输出文件清单

| 文件 | 路径 | 说明 |
|------|------|------|
| v2去重文件 | `knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-rule-extraction-v2-dedup.csv` | 23条去重后规则 |
| 映射文件 | `knowledge-base/raw/first-batch-processing/manifests/batch-r2-dedup-mapping.csv` | 6条删除规则映射关系 |
| 本报告 | `docs/test-reports/completion-reports/BATCH-R2-rule-dedup-report.md` | 去重过程文档 |

---

## 删除规则清单

- [x] RULE-A1-011
- [x] RULE-A1-016
- [x] RULE-A1-024
- [x] RULE-A1-026
- [x] RULE-A1-027
- [x] RULE-A1-029

---

## 保留规则清单 (23条)

- [x] RULE-A1-001
- [x] RULE-A1-002
- [x] RULE-A1-003
- [x] RULE-A1-004
- [x] RULE-A1-005
- [x] RULE-A1-006
- [x] RULE-A1-007
- [x] RULE-A1-008
- [x] RULE-A1-009
- [x] RULE-A1-010 (canonical)
- [x] RULE-A1-012
- [x] RULE-A1-013
- [x] RULE-A1-014
- [x] RULE-A1-015 (canonical)
- [x] RULE-A1-017
- [x] RULE-A1-018
- [x] RULE-A1-019
- [x] RULE-A1-020
- [x] RULE-A1-021
- [x] RULE-A1-022
- [x] RULE-A1-023 (canonical)
- [x] RULE-A1-025
- [x] RULE-A1-028 (canonical)

---

## 校验汇总

- [x] 原始文件未修改
- [x] 所有DUP-*标记已处理
- [x] mapping文件字段完整
- [x] v2文件可直接替换使用

---

*报告生成时间: BATCH-R2 去重任务完成*
