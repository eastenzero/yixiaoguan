# T3 任务: v8 Phase 2+3 全量筛选+下载

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3

## 背景
`wechat-meta/` 目录现有 1671 篇文章元数据（.jsonl 格式）。
需要筛选出 2024-04-01 ~ 2026-04-10、符合关键词的文章，并下载为 Markdown。

## Step 1: 先统计去重后的实际唯一文章数

```powershell
python -c "
import json, pathlib
seen = set()
total = dup = 0
for f in pathlib.Path('wechat-meta').glob('*.jsonl'):
    if f.name == 'filtered.jsonl': continue
    for line in f.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line: continue
        try:
            a = json.loads(line)
            link = a.get('link','')
            total += 1
            if link in seen: dup += 1
            else: seen.add(link)
        except: pass
print(f'总行数: {total}  去重后: {total-dup}  重复: {dup}')
"
```

## Step 2: 运行 Phase 2+3 筛选+下载（使用已有脚本）

```powershell
python scripts\wechat\filter_and_download.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --meta-dir wechat-meta --out wechat-articles
```

脚本会自动：
- 读取所有 .jsonl（跳过 filtered.jsonl）
- 按时间范围（2024-04-01 ~ 2026-04-10）+ 关键词过滤
- 已下载文件自动跳过（幂等）
- 输出 `wechat-articles/download-report.md`

## Step 3: 完成后输出统计

```powershell
# 统计已下载文章数（按账号）
Get-ChildItem -Recurse wechat-articles -Filter "*.md" -Exclude "download-report.md" |
  Group-Object DirectoryName |
  Sort-Object Count -Descending |
  Select-Object @{N='账号';E={Split-Path $_.Name -Leaf}}, Count |
  Format-Table -AutoSize

# 合计
$total = (Get-ChildItem -Recurse wechat-articles -Filter "*.md" -Exclude "download-report.md").Count
Write-Host "合计下载: $total 篇"
```

## 验收标准
- filtered.jsonl 行数 ≥ 200（从1671中筛选）
- wechat-articles/ 下载成功数 ≥ 150
- 失败数 < 20

请开始执行，遇到限速错误自动重试。
