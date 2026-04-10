# T3 任务: 汇总 TRIAGE 报告 → 生成 KB-GEN 批次分配表

## 目标
读取 4 份 TRIAGE 报告，提取全部 Tier-1 文件清单，按每批 15 篇分组，输出 KB-GEN 批次分配表。

## Step 1: 读取四份报告

```powershell
Get-Content kimi\triage-a-report.md
Get-Content kimi\triage-b-report.md
Get-Content kimi\triage-c-report.md
Get-Content kimi\triage-d-report.md
```

## Step 2: 汇总所有 Tier-1 文件

从四份报告的 Tier-1 清单中提取：文件名、账号、预估KB条数。
去掉与已有 KB-0101~0119 内容高度重叠的条目（已处理过的文章）。

## Step 3: 分批分组（每批约 15 篇）

将 Tier-1 清单按每批 15 篇分组，编号 E1、E2、E3……

## Step 4: 生成 KB-GEN 批次分配表，写入 `kimi/kb-gen-batches.md`

格式：

```markdown
# KB-GEN 批次分配表

已有编号上限: KB-20260410-0119
新编号起始: KB-20260410-0120

## 批次 E1（KB-0120 ~ KB-0134，约15篇文章）

| 文件路径 | 账号 | 预估KB条数 |
|---------|------|-----------|

## 批次 E2（KB-0135 ~ KB-0149）

...以此类推...

## 统计
- 总 Tier-1 文章数: XX
- 批次总数: XX
- 预估 KB 总条数: XX
```

请开始执行，确保文件路径使用 `wechat-articles/{账号}/{文件名}` 格式。
