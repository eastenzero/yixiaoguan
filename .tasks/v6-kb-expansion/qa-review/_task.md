# qa-review: 质量审查与去重

## 任务信息
- **spec 引用**: `_spec-v6-kb-expansion.yaml` § QA-REVIEW
- **优先级**: P1（Wave 3，串行）
- **依赖**: batch-p0 + batch-p1 + batch-p2 + batch-p3 全部完成
- **Kimi 指令文件**: `kimi/task-v6-qa-review.md`

## 检查项
1. **frontmatter 完整性**: title, category, tags, source, status 均存在且合法
2. **内容质量**: 标准答复 ≥ 50 字，无占位符，信息可追溯
3. **去重**: 新条目间无重复，与 KB-0150~0171 无实质重复
4. **编号连续性**: KB-20260409-0001 到末尾连续无跳号

## 输出
- 审查报告: `kimi/qa-review-report.md`
- 包含: 通过 / 需修改 / 删除 三类条目列表

## 验收标准
- AC-QA-01: 审查报告覆盖所有新条目
- AC-QA-02: frontmatter 校验 100% 通过
- AC-QA-03: 无重复条目
- AC-QA-04: 编号连续无跳号

## 状态
- [ ] 等待 Wave 2 全部验收
- [ ] Kimi 下发
- [ ] Kimi 回传
- [ ] T1 验收
