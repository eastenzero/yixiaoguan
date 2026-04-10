# T3 任务: v8 QA-REVIEW — 审查 19 条公众号来源 KB

## 角色
你是医小管知识库质量审查员。

## 审查范围
`knowledge-base/entries/first-batch-drafts/KB-20260410-0101.md` 到 `KB-20260410-0119.md`
共 19 条公众号来源 KB 条目。

## 检查项

### 通用检查
1. frontmatter 字段完整（title / category / tags / source / source_url / campus / status）
2. category 在枚举列表中：学籍与教务|考试与成绩|奖励与资助|毕业与就业|研究生事务|科研与创新|校园生活与服务|信息与技术服务|国际交流|证件与校园服务|图书馆服务|心理健康|社团与活动|财务与缴费|其他
3. tags 至少 2 个，包含"公众号来源"
4. "标准答复"段落不少于 50 字
5. 条目之间无重复主题

### 公众号来源特有检查
6. source 字段格式为 `wechat/{公众号名称}`
7. 是否含已过期信息（如报名截止日期已过）→ 若过期但流程有参考价值，末尾需有"以最新通知为准"注记
8. source_url 格式（可为空字符串，但不能是无效格式）

## 执行步骤

### Step 1: 读取所有 19 个文件

```powershell
Get-ChildItem knowledge-base\entries\first-batch-drafts\KB-20260410-01*.md | Sort-Object Name
```

### Step 2: 逐条检查

对每条 KB 检查上述 8 项，记录问题。

### Step 3: 输出报告

写入 `kimi/qa-review-v8-report.md`：

```markdown
# QA Review v8 Report

审查时间: YYYY-MM-DD
审查范围: KB-20260410-0101 ~ 0119（共 19 条）

## 汇总

| 检查项 | 通过数 | 问题数 |
|--------|--------|--------|
| frontmatter 完整性 | | |
| category 合规 | | |
| tags ≥2 且含公众号来源 | | |
| 标准答复 ≥50字 | | |
| source 格式 | | |
| 时效性标注 | | |

## 问题清单

| KB 编号 | 检查项 | 问题描述 | 建议处理 |
|---------|--------|---------|---------|

## 结论: PASS / FAIL（阻塞项为0则PASS）
```

## 验收标准
- frontmatter 100% 通过（阻塞项）
- 无重复条目（阻塞项）
- 时效性标注完成

请开始执行。
