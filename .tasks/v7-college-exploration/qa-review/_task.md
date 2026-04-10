# QA-REVIEW-V7 — 质量审查

**SPEC 模块**: QA-REVIEW-V7
**优先级**: P0
**状态**: pending
**依赖**: KB-GEN-P0 + KB-GEN-COLLEGES
**预计工时**: 1h

## 审查范围
所有 `KB-20260410-*.md` 文件

## 检查项

1. **frontmatter 完整性** — title, category, tags, source, status 均存在
2. **category 合法** — 在枚举列表中（含 v7 新增：院系与专业、科研与创新、研究生教育）
3. **tags** — 至少 2 个
4. **标准答复** — 段落存在且不少于 50 字
5. **无幻觉** — 不含虚构信息
6. **内部去重** — 新增条目之间无重复
7. **外部去重** — 与 v6 及更早的 KB 无实质重复
8. **编号连续** — 无跳号

## 输出
`kimi/qa-review-v7-report.md`

## 验收标准
- AC-QAV7-01: 审查报告存在且覆盖所有新条目
- AC-QAV7-02: frontmatter 校验 100% 通过
- AC-QAV7-03: 无重复条目
- AC-QAV7-04: 编号连续无跳号
