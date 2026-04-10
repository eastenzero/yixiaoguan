# T3 任务: Phase 6 QA — 统计 + 格式检查 + 抽样审查

## Step 1: 统计 first-batch-drafts/ 总量

```powershell
$files = Get-ChildItem "knowledge-base\entries\first-batch-drafts" -Filter "KB-*.md"
Write-Host "总文件数: $($files.Count)"
$files | Select-Object Name | Sort-Object Name | Format-Table -AutoSize
```

## Step 2: 格式批量校验

检查每个 KB 文件是否包含必需字段（title/category/tags/source/status）：

```powershell
$errors = @()
foreach ($f in Get-ChildItem "knowledge-base\entries\first-batch-drafts" -Filter "KB-*.md") {
    $content = Get-Content $f.FullName -Raw
    $missing = @()
    foreach ($field in @("title:","category:","tags:","source:","status:")) {
        if ($content -notmatch $field) { $missing += $field }
    }
    if ($missing.Count -gt 0) {
        $errors += "$($f.Name): 缺少 $($missing -join ', ')"
    }
}
if ($errors.Count -eq 0) { Write-Host "✅ 所有文件格式正确" }
else { $errors | ForEach-Object { Write-Host "❌ $_" } }
```

## Step 3: 抽样内容审查（每个 category 抽 2 条）

从以下 category 各随机抽 2 个文件，读取全文，检查：
- 标准答复是否有实质内容（不为空）
- 是否有明显的幻觉/错误信息
- 是否包含"来源"注释

category 列表：毕业与就业、校园生活与服务、图书馆服务、国际交流、财务与缴费、心理健康、研究生事务

```powershell
python -c "
import os, random, pathlib

drafts = pathlib.Path('knowledge-base/entries/first-batch-drafts')
by_cat = {}
for f in drafts.glob('KB-*.md'):
    content = f.read_text(encoding='utf-8')
    for line in content.splitlines():
        if line.startswith('category:'):
            cat = line.split(':',1)[1].strip().strip('\"')
            by_cat.setdefault(cat, []).append(f)
            break

random.seed(42)
for cat, files in sorted(by_cat.items()):
    sample = random.sample(files, min(2, len(files)))
    print(f'\n=== {cat} ({len(files)}条) ===')
    for f in sample:
        print(f'  [{f.name}]')
        print(f.read_text(encoding=\"utf-8\")[:500])
        print('  ---')
"
```

## Step 4: 生成 QA 报告写入 `kimi/qa-report.md`

格式：
```markdown
# KB-GEN QA 报告

- 总条目数: XX
- 格式错误: XX 个（列出）
- 内容质量: 抽样 XX 条，问题 XX 个（列出）
- 建议修正: ...
- 整体评级: A/B/C
```

请开始执行。
