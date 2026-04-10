# QA-REVIEW-V8 — 质量审查

**所属**: v8-wechat-scrape / PHASE 4
**优先级**: P0
**执行者**: Kimi
**预估工时**: 1h
**依赖**: KB-GEN-WECHAT

## 任务目标

对所有 KB-20260410-0101+ 新条目进行质量审查，确保公众号来源内容的准确性和时效性。

## 检查项

### 通用检查（与 v7 一致）
1. frontmatter 字段完整性（title/category/tags/source/source_url/campus/status）
2. category 在枚举列表中
3. tags 至少 2 个，包含"公众号来源"
4. "标准答复"段落不少于 50 字
5. 新条目之间无重复
6. 与已有 259 条 KB 无实质重复

### 公众号来源特有检查
7. **时效性**: 文章中报名截止日期等是否已过期
   - 若过期但规则/流程仍有参考价值 → 保留，在答复末尾注明"以最新通知为准"
   - 若内容完全时效性失效 → 删除该条目
8. **准确性**: 仅提取原始事实，不含非官方解读
9. **source_url 有效性**: URL 格式正确（以 https://mp.weixin.qq.com/ 开头）
10. **campus 字段**: 济南/泰安/通用 是否正确标注

## 输出

`kimi/qa-review-v8-report.md`:

```markdown
# QA Review v8 Report

审查时间: YYYY-MM-DD
审查范围: KB-20260410-0101 ~ 0XXX (共 N 条)

## 汇总

| 检查项 | 通过 | 问题数 | 问题列表 |
|--------|------|--------|---------|

## 时效性问题列表
| KB 编号 | 问题描述 | 建议处理 |

## 结论: PASS / FAIL
```

## 验收标准

- AC-QA8-01: 审查覆盖所有新条目
- AC-QA8-02: frontmatter 100% 通过
- AC-QA8-03: 无重复条目
- AC-QA8-04: 时效性标注完成
- AC-QA8-05: source_url 格式全部合法
