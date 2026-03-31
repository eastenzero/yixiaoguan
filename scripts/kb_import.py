"""
知识库入库脚本：将 first-batch-drafts/ 下所有草稿解析为标准 JSONL
输出路径：knowledge-base/raw/first-batch-processing/converted/first-batch-entries.jsonl
"""

import glob
import json
import os
import re
import sys

# 路径配置
DRAFTS_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge-base", "entries", "first-batch-drafts")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "knowledge-base", "raw", "first-batch-processing", "converted")
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "first-batch-entries.jsonl")

def parse_yaml_frontmatter(text):
    """从 Markdown YAML frontmatter 中提取字段"""
    metadata = {}
    m = re.match(r"---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return metadata, text
    yaml_block = m.group(1)
    body = text[m.end():]

    # 解析简单键值
    for line in yaml_block.splitlines():
        kv = re.match(r'^(\w+):\s+"?([^"]+)"?\s*$', line)
        if kv:
            metadata[kv.group(1)] = kv.group(2).strip()
        # 列表项（source_files）
        item = re.match(r'^\s+-\s+"?([^"]+)"?\s*$', line)
        if item:
            metadata.setdefault("source_files", []).append(item.group(1).strip())

    return metadata, body

def parse_sections(body):
    """将正文按 ## 标题分割为各章节"""
    sections = {}
    current_key = None
    current_lines = []

    SECTION_MAP = {
        "问题概述": "question",
        "标准答复": "answer",
        "办理条件": "conditions",
        "所需材料": "materials",
        "办理流程": "process",
        "时间节点": "timeline",
        "注意事项": "notes",
        "依据与证据": "evidence",
    }

    for line in body.splitlines():
        heading = re.match(r'^## (.+)$', line)
        if heading:
            if current_key:
                sections[current_key] = "\n".join(current_lines).strip()
            title = heading.group(1).strip()
            current_key = SECTION_MAP.get(title, title)
            current_lines = []
        else:
            if current_key is not None:
                current_lines.append(line)

    if current_key:
        sections[current_key] = "\n".join(current_lines).strip()

    return sections

def build_full_text(metadata, sections):
    """拼接完整检索文本"""
    parts = []
    parts.append(f"标题：{metadata.get('title', '')}")
    parts.append(f"分类：{metadata.get('category', '')}  受众：{metadata.get('audience', '')}")
    for field in ["question", "answer", "conditions", "materials", "process", "timeline", "notes", "evidence"]:
        val = sections.get(field, "")
        if val:
            parts.append(val)
    return "\n".join(parts)

def process_file(filepath):
    """处理单个 Markdown 文件，返回结构化 dict"""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()

    metadata, body = parse_yaml_frontmatter(text)
    sections = parse_sections(body)

    # entry_id 从文件名提取
    entry_id = os.path.splitext(os.path.basename(filepath))[0]

    record = {
        "entry_id": entry_id,
        "title": metadata.get("title", ""),
        "category": metadata.get("category", ""),
        "audience": metadata.get("audience", ""),
        "material_id": metadata.get("material_id", ""),
        "rule_task_id": metadata.get("rule_task_id", ""),
        "status": metadata.get("status", "draft"),
        "source_files": metadata.get("source_files", []),
        **sections,
        "full_text": build_full_text(metadata, sections),
    }
    return record

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = sorted(glob.glob(os.path.join(DRAFTS_DIR, "KB-*.md")))

    if not files:
        print(f"[错误] 未找到草稿文件，路径：{DRAFTS_DIR}")
        sys.exit(1)

    records = []
    errors = []

    for filepath in files:
        try:
            record = process_file(filepath)
            records.append(record)
        except Exception as e:
            errors.append((os.path.basename(filepath), str(e)))

    # 写出 JSONL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"✅ 入库完成：共处理 {len(records)} 条，写出至：{OUTPUT_FILE}")

    if errors:
        print(f"\n⚠️  以下文件处理失败（{len(errors)} 条）：")
        for fname, err in errors:
            print(f"  {fname}: {err}")
    else:
        print("✅ 无错误")

    # 输出前3条摘要预览
    print("\n--- 前3条摘要预览 ---")
    for r in records[:3]:
        print(f"  [{r['entry_id']}] {r['title']} | {r['category']} | {r['audience']}")
        print(f"    Q: {r.get('question', '')[:50]}")
        print(f"    A: {r.get('answer', '')[:80]}")
        print()

if __name__ == "__main__":
    main()
