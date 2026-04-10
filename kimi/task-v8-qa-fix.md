# T3 任务: Phase 6 QA修复 — 批量修复 first-batch-drafts/ 格式缺失字段

## 目标
对 113 个格式不合规的 KB 文件，自动补全缺失的 `tags`、`source`、`status` 字段。

## Step 1: 用 Python 脚本批量修复

创建并运行 `scripts/fix_kb_format.py`：

```python
import pathlib, re

drafts = pathlib.Path("knowledge-base/entries/first-batch-drafts")
fixed = skipped = 0

for f in sorted(drafts.glob("KB-*.md")):
    content = f.read_text(encoding="utf-8")
    
    # 找到 frontmatter 边界
    if not content.startswith("---"):
        continue
    end = content.find("---", 3)
    if end == -1:
        continue
    
    fm = content[3:end]
    body = content[end:]
    changed = False
    
    # 从 source 推断 tags
    source_match = re.search(r'source:\s*"?([^"\n]+)"?', fm)
    source_val = source_match.group(1).strip() if source_match else ""
    
    # 补 status
    if "status:" not in fm:
        fm = fm.rstrip() + '\nstatus: "active"\n'
        changed = True
    
    # 补 source（如果缺失，从文件名或 category 推断）
    if "source:" not in fm:
        # 尝试从 tags 中提取
        tag_match = re.search(r'tags:.*?"wechat/([^"]+)"', fm)
        if tag_match:
            src = f'wechat/{tag_match.group(1)}'
        else:
            src = "wechat/山东第一医科大学"
        fm = fm.rstrip() + f'\nsource: "{src}"\n'
        source_val = src
        changed = True
    
    # 补 tags（如果缺失）
    if "tags:" not in fm:
        # 从 category 推断基础标签
        cat_match = re.search(r'category:\s*"?([^"\n]+)"?', fm)
        cat = cat_match.group(1).strip() if cat_match else "其他"
        src_short = source_val.replace("wechat/", "") if source_val else "山东第一医科大学"
        fm = fm.rstrip() + f'\ntags: ["{cat}", "公众号", "{src_short}"]\n'
        changed = True
    
    # 补 source_url（如果缺失）
    if "source_url:" not in fm:
        fm = fm.rstrip() + '\nsource_url: ""\n'
        changed = True
    
    # 补 campus（如果缺失）
    if "campus:" not in fm:
        fm = fm.rstrip() + '\ncampus: "通用"\n'
        changed = True
    
    if changed:
        new_content = "---" + fm + body
        f.write_text(new_content, encoding="utf-8")
        fixed += 1
    else:
        skipped += 1

print(f"修复: {fixed} 个文件  跳过(已合规): {skipped} 个文件")
```

## Step 2: 运行脚本

```powershell
python scripts\fix_kb_format.py
```

## Step 3: 修复后再次验证

```powershell
$errors = 0
foreach ($f in Get-ChildItem "knowledge-base\entries\first-batch-drafts" -Filter "KB-*.md") {
    $content = Get-Content $f.FullName -Raw
    foreach ($field in @("title:","category:","tags:","source:","status:")) {
        if ($content -notmatch $field) { $errors++; break }
    }
}
Write-Host "修复后格式错误数: $errors"
```

## 验收标准
- 格式错误数 = 0
- 修复文件数 ≥ 100

请开始执行。
