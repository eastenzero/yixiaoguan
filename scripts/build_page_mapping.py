#!/usr/bin/env python3
"""
KB Entry Page Mapping Script
为来自 student-handbook.pdf 的 KB 条目标注 page_start / page_end
"""

import json
import os
import re
import csv
import difflib
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# 配置路径
MINERU_JSON_PATH = "knowledge-base/raw/student-handbook-mineru/content_list_v2.json"
ENTRIES_DIR = "knowledge-base/entries/first-batch-drafts"
REPORT_PATH = "scripts/page_mapping_report.csv"

# 目标条目模式
GROUP_A_PATTERN = r"KB-015[0-9]-.*\.md|KB-016[0-9]-.*\.md|KB-017[0-1]-.*\.md"
GROUP_B_PATTERN = r"KB-20260324-01(3[8-9]|4[0-9])\.md"


def extract_text_from_block(block: dict) -> str:
    """从单个 block 中提取文本"""
    block_type = block.get("type", "")
    content = block.get("content", "")
    
    texts = []
    
    if block_type == "title":
        # title 块: content["title_content"] 里 type=="text" 的 content 字段
        if isinstance(content, dict):
            title_content = content.get("title_content", [])
            for item in title_content:
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("content", ""))
    elif block_type == "paragraph":
        # paragraph 块: content["paragraph_content"] 里提取文本
        if isinstance(content, dict):
            para_content = content.get("paragraph_content", [])
            for item in para_content:
                if isinstance(item, dict) and item.get("type") == "text":
                    texts.append(item.get("content", ""))
    elif block_type == "list":
        # list 块: content["list_items"] 里提取文本
        if isinstance(content, dict):
            list_items = content.get("list_items", [])
            for item in list_items:
                if isinstance(item, list):
                    for sub_item in item:
                        if isinstance(sub_item, dict) and sub_item.get("type") == "text":
                            texts.append(sub_item.get("content", ""))
                elif isinstance(item, dict):
                    if item.get("type") == "text":
                        texts.append(item.get("content", ""))
    elif isinstance(content, str):
        texts.append(content)
    elif isinstance(content, dict):
        # 尝试直接获取 text 字段
        text_val = content.get("text", "")
        if text_val:
            texts.append(text_val)
    
    return "".join(texts)


def extract_page_text(page_blocks: List[dict]) -> str:
    """从一页的所有 blocks 中提取完整文本"""
    texts = []
    for block in page_blocks:
        text = extract_text_from_block(block)
        if text.strip():
            texts.append(text)
    return " ".join(texts)


def load_mineru_data(json_path: str) -> List[str]:
    """加载 MinerU JSON 并返回每页的文本列表"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    pages_text = []
    for page_blocks in data:
        page_text = extract_page_text(page_blocks)
        pages_text.append(page_text)
    
    return pages_text


def parse_frontmatter(content: str) -> Tuple[Dict, str]:
    """解析 frontmatter，返回 (frontmatter_dict, body)"""
    pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
    match = re.match(pattern, content, re.DOTALL)
    
    if not match:
        return {}, content
    
    fm_text = match.group(1)
    body = match.group(2)
    
    # 简单解析 YAML-like frontmatter
    fm = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            fm[key] = val
    
    return fm, body


def build_frontmatter(fm: Dict) -> str:
    """将 frontmatter dict 转换为 YAML 格式字符串"""
    lines = ["---"]
    for key, val in fm.items():
        if isinstance(val, str):
            # 如果值包含特殊字符，使用引号
            if any(c in val for c in ['"', "'", ":", "#", "{", "}"]):
                val = f'"{val.replace("\\", "\\\\").replace('"', '\\"')}"'
            lines.append(f"{key}: {val}")
        else:
            lines.append(f"{key}: {val}")
    lines.append("---")
    return "\n".join(lines)


def extract_needle(body: str, title: str = "", max_len: int = 120) -> str:
    """提取搜索 needle：优先使用标题 + 正文前段"""
    # 清理正文：去除 markdown 标记
    body_clean = re.sub(r'[#*`\[\]()|>]', '', body)
    # 去除空白行和多余空格
    body_clean = re.sub(r'\s+', ' ', body_clean.strip())
    
    # 策略1: 如果有标题，优先只用标题搜索（更精确）
    if title:
        title_clean = title.strip()
        # 移除常见后缀
        title_clean = re.sub(r'(指南|说明|流程|规定|办法|公约)$', '', title_clean)
        if len(title_clean) >= 4:
            return title_clean[:max_len]
    
    # 策略2: 使用正文开头的重要句子
    # 提取正文中的中文字符和关键词
    body_sample = body_clean[:max_len*2].strip()
    # 去除常见的通用开头
    body_sample = re.sub(r'^(学生|学校|校院|各学院|同学们|大家好)\s*', '', body_sample)
    
    return body_sample[:max_len] if body_sample else ""


def search_in_pages(needle: str, pages_text: List[str], threshold: float = 0.25) -> List[Tuple[int, float, str]]:
    """
    在所有页面中搜索 needle，返回匹配的 (页码, 相似度, 片段) 列表
    页码从 1 开始
    使用多种匹配策略提高成功率
    """
    matches = []
    if not needle or len(needle) < 5:
        return matches
    
    # 清理 needle：去除 markdown 标记和多余空白
    needle_clean = re.sub(r'[#*\-\[\]()|`>]', '', needle)
    needle_clean = re.sub(r'\s+', '', needle_clean)  # 去所有空白
    
    if len(needle_clean) < 5:
        return matches
    
    # 使用 needle 的前 80 个字符进行匹配（提高匹配稳定性）
    search_window = min(80, len(needle_clean))
    needle_sample = needle_clean[:search_window]
    
    for i, page_text in enumerate(pages_text):
        # 清理页面文本
        page_clean = re.sub(r'\s+', '', page_text)
        
        # 方法1: 子串匹配（前 80 字符）
        if needle_sample in page_clean:
            matches.append((i + 1, 0.95, page_text[:200]))
            continue
        
        # 方法2: 滑动窗口部分匹配（查找连续 30+ 字符匹配）
        min_match_len = min(30, len(needle_sample))
        partial_match = False
        for j in range(len(needle_sample) - min_match_len + 1):
            substring = needle_sample[j:j + min_match_len]
            if len(substring) >= min_match_len and substring in page_clean:
                partial_match = True
                break
        
        if partial_match:
            # 计算整体相似度
            ratio = difflib.SequenceMatcher(None, needle_sample, page_clean[:500]).ratio()
            if ratio > threshold:
                matches.append((i + 1, ratio, page_text[:200]))
            continue
        
        # 方法3: 整体相似度（对于短文本）
        if len(needle_clean) <= 100:
            ratio = difflib.SequenceMatcher(None, needle_clean, page_clean[:800]).ratio()
            if ratio > threshold + 0.1:  # 提高阈值避免误匹配
                matches.append((i + 1, ratio, page_text[:200]))
    
    return matches


def find_entry_files() -> List[Path]:
    """找到所有目标条目文件"""
    entries_dir = Path(ENTRIES_DIR)
    files = []
    
    for f in entries_dir.iterdir():
        if not f.is_file() or not f.suffix == '.md':
            continue
        
        # GROUP A: KB-0150 ~ KB-0171
        if re.match(GROUP_A_PATTERN, f.name):
            files.append(f)
        # GROUP B: KB-20260324-0138 ~ KB-20260324-0149
        elif re.match(GROUP_B_PATTERN, f.name):
            files.append(f)
    
    return sorted(files)


def process_entry(entry_path: Path, pages_text: List[str]) -> Dict:
    """处理单个条目，返回结果字典"""
    result = {
        "entry_id": entry_path.stem,
        "title": "",
        "material_id": "",
        "page_start": 0,
        "page_end": 0,
        "match_score": 0.0,
        "match_snippet": "",
        "match_failed": True
    }
    
    with open(entry_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm, body = parse_frontmatter(content)
    
    result["title"] = fm.get("title", "")
    result["material_id"] = fm.get("material_id", "")
    
    # 检查是否已有 page_start（幂等）
    if "page_start" in fm:
        result["page_start"] = int(fm.get("page_start", 0))
        result["page_end"] = int(fm.get("page_end", 0))
        result["match_failed"] = False
        result["match_score"] = 1.0
        result["match_snippet"] = "[已存在，跳过]"
        return result
    
    # 过滤 material_id - 匹配任务要求
    material_id = fm.get("material_id", "")
    # GROUP_A: 学生手册 (学生手册-生活服务, 学生手册-学工办事流程等)
    # GROUP_B: HANDBOOK-2026-001 / HANDBOOK-2026-002
    # 注意: 医小管知识库二次修改版 也来自 student-handbook PDF，只是 material_id 不同
    is_target = (
        "学生手册" in material_id or 
        "HANDBOOK" in material_id or 
        "医小管知识库" in material_id
    )
    if not is_target:
        result["match_snippet"] = f"[跳过: material_id={material_id}]"
        return result
    
    # 提取 needle
    needle = extract_needle(body, result["title"], max_len=120)
    if len(needle) < 10:
        # 尝试使用标题作为 needle
        needle = result["title"]
    
    # 搜索匹配
    matches = search_in_pages(needle, pages_text, threshold=0.3)
    
    if matches:
        # 取所有匹配的页码
        page_nums = [m[0] for m in matches]
        result["page_start"] = min(page_nums)
        result["page_end"] = max(page_nums)
        result["match_score"] = max(m[1] for m in matches)
        result["match_snippet"] = matches[0][2][:100].replace('\n', ' ')
        result["match_failed"] = False
        
        # 更新 frontmatter
        fm["page_start"] = result["page_start"]
        fm["page_end"] = result["page_end"]
        
        new_content = build_frontmatter(fm) + "\n" + body
        with open(entry_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        # 无匹配
        result["page_start"] = 0
        result["page_end"] = 0
        result["match_score"] = 0.0
        result["match_snippet"] = "[无匹配]"
        result["match_failed"] = True
        
        # 仍然添加字段但值为 0
        fm["page_start"] = 0
        fm["page_end"] = 0
        
        new_content = build_frontmatter(fm) + "\n" + body
        with open(entry_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return result


def main():
    print("=" * 60)
    print("KB Entry Page Mapping Tool")
    print("=" * 60)
    
    # 步骤1: 加载 MinerU 数据
    print(f"\n[1/4] 加载 MinerU JSON: {MINERU_JSON_PATH}")
    pages_text = load_mineru_data(MINERU_JSON_PATH)
    print(f"      共 {len(pages_text)} 页")
    
    # 步骤2: 找到目标条目
    print(f"\n[2/4] 扫描目标条目: {ENTRIES_DIR}")
    entry_files = find_entry_files()
    print(f"      找到 {len(entry_files)} 个目标条目")
    
    # 步骤3: 处理每个条目
    print(f"\n[3/4] 处理条目并匹配页码...")
    results = []
    success_count = 0
    failed_count = 0
    skipped_count = 0
    
    for i, entry_path in enumerate(entry_files, 1):
        print(f"      [{i}/{len(entry_files)}] {entry_path.name} ... ", end="", flush=True)
        result = process_entry(entry_path, pages_text)
        results.append(result)
        
        if result["match_snippet"].startswith("[已存在"):
            print(f"已存在 (page_start={result['page_start']})")
            skipped_count += 1
        elif result["match_failed"]:
            print(f"失败 (无匹配)")
            failed_count += 1
        else:
            print(f"成功 (page_start={result['page_start']}, page_end={result['page_end']})")
            success_count += 1
    
    # 步骤4: 生成 CSV 报告
    print(f"\n[4/4] 生成报告: {REPORT_PATH}")
    with open(REPORT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            "entry_id", "title", "material_id", 
            "page_start(mineru_logical)", "page_end(mineru_logical)", 
            "match_score", "match_snippet", "match_failed"
        ])
        for r in results:
            writer.writerow([
                r["entry_id"], r["title"], r["material_id"],
                r["page_start"], r["page_end"],
                f"{r['match_score']:.2f}", r["match_snippet"], r["match_failed"]
            ])
    
    # 统计
    print(f"\n" + "=" * 60)
    print("处理完成!")
    print(f"  - 总条目: {len(results)}")
    print(f"  - 成功标注: {success_count}")
    print(f"  - 已存在跳过: {skipped_count}")
    print(f"  - 匹配失败: {failed_count}")
    print("=" * 60)


if __name__ == "__main__":
    main()
