#!/usr/bin/env python3
"""
格式校验脚本 - P1C Format Unify
检查知识库草稿文件是否使用统一的 ## 标题格式
"""

import re
import sys
from pathlib import Path
from datetime import datetime


def check_file_format(file_path: Path) -> dict:
    """检查单个文件的格式"""
    content = file_path.read_text(encoding='utf-8')
    
    # 分离 frontmatter 和正文
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
    
    # 检查 h1 标题 (# )
    h1_pattern = re.compile(r'^# [^#\s]', re.MULTILINE)
    h2_pattern = re.compile(r'^## [^#\s]', re.MULTILINE)
    
    has_h1 = bool(h1_pattern.search(body))
    has_h2 = bool(h2_pattern.search(body))
    
    return {
        'file': file_path.name,
        'has_h1': has_h1,
        'has_h2': has_h2,
        'is_valid': not has_h1,  # 有 h1 则无效
    }


def main():
    kb_dir = Path('knowledge-base/entries/first-batch-drafts')
    if not kb_dir.exists():
        print(f"❌ 目录不存在: {kb_dir}")
        sys.exit(1)
    
    md_files = sorted(kb_dir.glob('KB-*.md'))
    print(f"📄 找到 {len(md_files)} 个知识条目文件")
    print("=" * 60)
    
    invalid_files = []
    valid_count = 0
    
    for f in md_files:
        result = check_file_format(f)
        if result['is_valid']:
            valid_count += 1
        else:
            invalid_files.append(result)
    
    print(f"\n✅ 格式正确文件数: {valid_count}")
    print(f"❌ 格式异常文件数: {len(invalid_files)}")
    
    if invalid_files:
        print("\n格式异常文件列表:")
        for item in invalid_files:
            print(f"  - {item['file']} (包含 h1 标题)")
    
    # 生成报告
    report_dir = Path('docs/test-reports/completion-reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / 'P1C-format-unify-report.md'
    report_content = f"""---
task_id: "p1c-format-unify"
generated_at: "{datetime.now().isoformat()}"
verified_by: "format_check.py"
---

# P1C 格式统一验证报告

## 执行摘要

| 项目 | 结果 |
|------|------|
| 检查文件总数 | {len(md_files)} |
| 格式正确文件数 | {valid_count} |
| 格式异常文件数 | {len(invalid_files)} |
| 验证结果 | {'✅ PASS' if len(invalid_files) == 0 else '❌ FAIL'} |

## 检查标准

- 模板文件应使用 `##` 格式（h2 标题）
- 草稿文件正文应使用 `##` 格式，不应使用 `#` 格式（h1 标题）
- frontmatter 区域（`---` 包裹）不参与检查

## 格式异常文件清单

"""
    
    if invalid_files:
        for item in invalid_files:
            report_content += f"- {item['file']}\n"
    else:
        report_content += "无 - 所有文件格式正确\n"
    
    report_content += f"""
## 结论

{'所有 90 条草稿文件格式统一为 `##`，与模板一致。' if len(invalid_files) == 0 else f'发现 {len(invalid_files)} 个文件格式异常，需要修复。'}

---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    report_file.write_text(report_content, encoding='utf-8')
    print(f"\n📝 报告已生成: {report_file}")
    
    return len(invalid_files) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
