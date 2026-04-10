#!/usr/bin/env python3
"""
WeChat Articles Triage Script
Processes articles from two directories and classifies them into Tier-1, Tier-2, or Tier-3
"""

import os
import re
import glob

# Directories to process
EMPLOYMENT_DIR = "wechat-articles/山东第一医科大学就业"
LIBRARY_DIR = "wechat-articles/山东第一医科大学图书馆"

# Output file
OUTPUT_FILE = "kimi/triage-a-report.md"

# Tier classification patterns
TIER1_KEYWORDS = [
    "招聘", "公告", "简章", "报名", "报名时间", "考试时间", "联系电话", "邮箱",
    "岗位", "职位", "要求", "条件", "流程", "薪资待遇", "福利", "简历投递",
    "报名方式", "资格条件", "考试", "面试", "笔试", "录用", "聘用"
]

TIER3_KEYWORDS = [
    "活动回顾", "获奖名单", "圆满落幕", "成功举办", "主题党日", "观影活动",
    "参观交流", "洽谈交流", "学习交流", "庆三八", "庆七一", "党课",
    "颁奖", "表彰", "获奖", "揭晓", "会议", "座谈会"
]

def get_first_n_words(filepath, n_words=300):
    """Read first n words from a file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            # Remove CSS and markdown formatting
            content = re.sub(r'#js_row_immersive.*?\}', '', content)
            content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
            content = re.sub(r'\[.*?\]\(.*?\)', '', content)
            content = re.sub(r'[#*|`]', '', content)
            words = content.split()
            return ' '.join(words[:n_words])
    except Exception as e:
        return ""

def extract_account(filename):
    """Extract account name from filename or content patterns"""
    # Default account based on directory
    if "就业" in filename or "employment" in filename.lower():
        return "山东第一医科大学就业"
    elif "图书馆" in filename or "library" in filename.lower():
        return "山东第一医科大学图书馆"
    return "未知"

def classify_article(content, filename):
    """Classify article into Tier-1, Tier-2, or Tier-3"""
    content_lower = content.lower()
    
    # Check for Tier-3 indicators (event reviews, speeches, etc.)
    tier3_score = 0
    for keyword in TIER3_KEYWORDS:
        if keyword in content:
            tier3_score += 1
    
    # If strong Tier-3 indicators, skip
    if tier3_score >= 2:
        return "Tier-3", "纯活动回顾/新闻，无实用信息"
    
    # Check for Tier-1 indicators (specific actionable info)
    tier1_score = 0
    tier1_indicators = []
    
    if "报名" in content and "时间" in content:
        tier1_score += 2
        tier1_indicators.append("报名时间")
    if "招聘" in content and ("岗位" in content or "职位" in content):
        tier1_score += 2
        tier1_indicators.append("招聘岗位")
    if "联系" in content and ("电话" in content or "邮箱" in content):
        tier1_score += 1
        tier1_indicators.append("联系方式")
    if "薪资" in content or "待遇" in content or "福利" in content:
        tier1_score += 1
        tier1_indicators.append("薪资福利")
    if "条件" in content and ("要求" in content or "资格" in content):
        tier1_score += 1
        tier1_indicators.append("招聘条件")
    
    # Strong Tier-1: Official recruitment with specific details
    if tier1_score >= 4:
        return "Tier-1", "、".join(tier1_indicators) if tier1_indicators else "包含具体流程、条件、联系方式"
    
    # Tier-2: Has some useful info but incomplete or outdated
    if "招聘" in content or "公告" in content or "简章" in content:
        return "Tier-2", "部分招聘信息，但可能已过期或信息不完整"
    
    if "通知" in content and ("开馆" in content or "安排" in content or "时间" in content):
        return "Tier-1" if "具体时间" in content or re.search(r'\d+月\d+日', content) else "Tier-2", "开馆/服务时间通知"
    
    # Default to Tier-3 if unclear
    return "Tier-3", "内容不明确或无实用信息"

def estimate_kb_entries(content, tier):
    """Estimate number of KB entries that could be extracted"""
    if tier == "Tier-1":
        # Count distinct sections that could be KB entries
        entries = 0
        if "报名" in content:
            entries += 1
        if "岗位" in content or "职位" in content:
            entries += 1
        if "条件" in content or "要求" in content:
            entries += 1
        if "流程" in content:
            entries += 1
        if "联系" in content:
            entries += 1
        return max(entries, 1)
    elif tier == "Tier-2":
        return 1
    else:
        return 0

def process_directory(directory, account_name):
    """Process all markdown files in a directory"""
    results = []
    pattern = os.path.join(directory, "*.md")
    
    for filepath in glob.glob(pattern):
        filename = os.path.basename(filepath)
        content = get_first_n_words(filepath, 300)
        
        if not content.strip():
            continue
            
        tier, reason = classify_article(content, filename)
        kb_estimate = estimate_kb_entries(content, tier)
        
        results.append({
            "filename": filename,
            "account": account_name,
            "tier": tier,
            "reason": reason,
            "kb_estimate": kb_estimate,
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        })
    
    return results

def generate_report(employment_results, library_results):
    """Generate the markdown report"""
    all_results = employment_results + library_results
    
    tier1 = [r for r in all_results if r["tier"] == "Tier-1"]
    tier2 = [r for r in all_results if r["tier"] == "Tier-2"]
    tier3 = [r for r in all_results if r["tier"] == "Tier-3"]
    
    report = """# TRIAGE 批次A 报告

文章总数: {total}
- Tier-1: {tier1_count} 篇
- Tier-2: {tier2_count} 篇
- Tier-3: {tier3_count} 篇

""".format(
        total=len(all_results),
        tier1_count=len(tier1),
        tier2_count=len(tier2),
        tier3_count=len(tier3)
    )
    
    # Tier-1 Table
    report += "## Tier-1 清单（直接转KB）\n\n"
    report += "| 文件名 | 账号 | 关键信息点 | 预估KB条数 |\n"
    report += "|--------|------|----------|-----------|\n"
    
    for item in sorted(tier1, key=lambda x: x["filename"]):
        # Clean filename for display
        display_name = item["filename"].replace(".md", "")[:50]
        report += f"| {display_name} | {item['account']} | {item['reason']} | {item['kb_estimate']} |\n"
    
    report += "\n"
    
    # Tier-2 Table
    report += "## Tier-2 清单\n\n"
    report += "| 文件名 | 账号 | 可提取内容 | 预估KB条数 |\n"
    report += "|--------|------|----------|-----------|\n"
    
    for item in sorted(tier2, key=lambda x: x["filename"]):
        display_name = item["filename"].replace(".md", "")[:50]
        report += f"| {display_name} | {item['account']} | {item['reason']} | {item['kb_estimate']} |\n"
    
    report += "\n"
    
    # Tier-3 Table
    report += "## Tier-3 清单（跳过）\n\n"
    report += "| 文件名 | 账号 | 跳过原因 |\n"
    report += "|--------|------|----------|\n"
    
    for item in sorted(tier3, key=lambda x: x["filename"]):
        display_name = item["filename"].replace(".md", "")[:50]
        report += f"| {display_name} | {item['account']} | {item['reason']} |\n"
    
    return report

def main():
    print("Starting triage process...")
    
    # Process employment articles
    print(f"Processing employment articles from {EMPLOYMENT_DIR}...")
    employment_results = process_directory(EMPLOYMENT_DIR, "山东第一医科大学就业")
    print(f"  Found {len(employment_results)} employment articles")
    
    # Process library articles
    print(f"Processing library articles from {LIBRARY_DIR}...")
    library_results = process_directory(LIBRARY_DIR, "山东第一医科大学图书馆")
    print(f"  Found {len(library_results)} library articles")
    
    # Generate report
    print("Generating report...")
    report = generate_report(employment_results, library_results)
    
    # Write report
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Report written to {OUTPUT_FILE}")
    print(f"\nSummary:")
    print(f"  Total articles: {len(employment_results) + len(library_results)}")
    print(f"  Tier-1: {len([r for r in employment_results + library_results if r['tier'] == 'Tier-1'])}")
    print(f"  Tier-2: {len([r for r in employment_results + library_results if r['tier'] == 'Tier-2'])}")
    print(f"  Tier-3: {len([r for r in employment_results + library_results if r['tier'] == 'Tier-3'])}")

if __name__ == "__main__":
    main()
