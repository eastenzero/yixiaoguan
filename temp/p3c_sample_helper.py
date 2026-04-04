from pathlib import Path
import re
import random

random.seed(20260404)
root = Path("knowledge-base/entries/first-batch-drafts")
files = sorted(root.glob("KB-*.md"))

def parse_frontmatter_category(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0].lstrip("\ufeff").strip() != "---":
        return "未分类"
    for i in range(1, len(lines)):
        line = lines[i].strip()
        if line == "---":
            break
        if line.startswith("category:"):
            value = line.split(":", 1)[1].strip().strip('"\'')
            return value or "未分类"
    return "未分类"

cats = {}
for f in files:
    text = f.read_text(encoding="utf-8")
    category = parse_frontmatter_category(text)
    cats.setdefault(category, []).append(f)

selected = []
for category in sorted(cats.keys()):
    choices = cats[category][:]
    random.shuffle(choices)
    take = min(2, len(choices))
    selected.extend([(category, p.name) for p in choices[:take]])

print(f"total_files\t{len(files)}")
print(f"category_count\t{len(cats)}")
for category in sorted(cats.keys()):
    print(f"category\t{category}\t{len(cats[category])}")
print(f"sample_count\t{len(selected)}")
for category, name in selected:
    print(f"sample\t{category}\t{name}")
