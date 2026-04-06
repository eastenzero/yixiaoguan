#!/usr/bin/env python3
"""
build_page_mapping_v2.py
Page mapping for KB entries from student-handbook-mineru/content_list_v2.json.

Matching strategies (in priority order):
  1. § section reference (KB-20260324 entries with full.md § ... source)
  2. 第X.X节 section number (医小管知识库二次修改版.md 第X.X节 source)
  3. Body-text needle search (fallback)

Outputs:
  scripts/page_mapping_report_v2.csv
  Updates frontmatter page_start/page_end in all 34 target entries.
"""
import json, re, csv
from pathlib import Path

REPO = Path(__file__).parent.parent
MINERU_JSON = REPO / "knowledge-base/raw/student-handbook-mineru/content_list_v2.json"
DRAFTS = REPO / "knowledge-base/entries/first-batch-drafts"
REPORT = REPO / "scripts/page_mapping_report_v2.csv"

TARGET_PATTERNS = [
    "KB-015[0-9]-*.md",
    "KB-016[0-9]-*.md",
    "KB-0170-*.md",
    "KB-0171-*.md",
    "KB-20260324-013[89].md",
    "KB-20260324-014[0-9].md",
]


# ---------------------------------------------------------------------------
# MinerU helpers
# ---------------------------------------------------------------------------

def _iter_title_texts(page_blocks):
    for blk in page_blocks:
        if blk.get("type") == "title":
            for item in blk["content"].get("title_content", []):
                if item.get("type") == "text" and item["content"].strip():
                    yield item["content"].strip()


def extract_page_text(page_blocks):
    parts = []
    for blk in page_blocks:
        t, c = blk.get("type", ""), blk.get("content", {})
        if t == "title":
            for item in c.get("title_content", []):
                if item.get("type") == "text":
                    parts.append(item["content"])
        elif t == "paragraph":
            for item in c.get("paragraph_content", []):
                if item.get("type") == "text":
                    parts.append(item["content"])
        elif t == "list":
            for li in c.get("list_items", []):
                for item in li.get("item_content", []):
                    if item.get("type") == "text":
                        parts.append(item["content"])
    return " ".join(p for p in parts if p)


def build_section_map(mineru):
    """
    Returns dict: section_number -> (content_page_start, content_page_end)
    Uses last occurrence of each section number (skips TOC pages).
    """
    # Pass 1: collect all occurrences
    occurrences = {}  # sec -> [page_idx, ...]
    for i, page in enumerate(mineru):
        for title in _iter_title_texts(page):
            m = re.match(r'^(\d+\.\d+(?:\.\d+)?)', title)
            if m:
                sec = m.group(1)
                occurrences.setdefault(sec, []).append(i)

    # Pass 2: content page = last occurrence
    content_page = {sec: pages[-1] for sec, pages in occurrences.items()}

    # Pass 3: end page = next sibling section start - 1
    def end_page(sec, start_idx):
        parts = sec.split(".")
        next_num = int(parts[-1]) + 1
        next_sec = ".".join(parts[:-1] + [str(next_num)])
        if next_sec in content_page and content_page[next_sec] > start_idx:
            return content_page[next_sec] - 1
        # fallback: parent's next sibling
        if len(parts) > 1:
            parent_parts = parts[:-1]
            parent_next = ".".join(parent_parts[:-1] + [str(int(parent_parts[-1]) + 1)])
            if parent_next in content_page and content_page[parent_next] > start_idx:
                return content_page[parent_next] - 1
        return min(start_idx + 12, len(mineru) - 1)

    return {
        sec: (idx + 1, end_page(sec, idx) + 1)
        for sec, idx in content_page.items()
    }


# ---------------------------------------------------------------------------
# Frontmatter helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end].strip(), text[end + 4:].strip()
    return None, text


def get_fm_field(fm_str, field):
    m = re.search(rf'^{field}:\s*["\']?(.+?)["\']?\s*$', fm_str, re.MULTILINE)
    return m.group(1).strip() if m else ""


def update_frontmatter(path, page_start, page_end):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    fm_str, body = parse_frontmatter(text)
    if fm_str is None:
        return
    fm_lines = [l for l in fm_str.splitlines() if not re.match(r'^page_(start|end):', l)]
    fm_lines += [f"page_start: {page_start}", f"page_end: {page_end}"]
    path.write_text(f"---\n{chr(10).join(fm_lines)}\n---\n\n{body}\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Matching strategies
# ---------------------------------------------------------------------------

def _norm(s):
    return re.sub(r'[\s\u3000\uff0e\u00b7\uff08\uff09()（）]+', '', s)


def match_section_ref(source, pages_titles):
    """Match § section reference against MinerU title blocks."""
    m = re.search(r'§\s*(.+)', source)
    if not m:
        return None, None, 0, ""
    ref = m.group(1).strip()
    segments = [s.strip() for s in re.split(r'[-–]', ref) if s.strip()]
    for candidate in reversed(segments):
        cand_norm = _norm(candidate)
        if len(cand_norm) < 3:
            continue
        for i, titles in enumerate(pages_titles):
            for title in titles:
                if cand_norm in _norm(title) or _norm(title) in cand_norm:
                    ps = i + 1
                    pe = ps
                    for j in range(i + 1, min(i + 15, len(pages_titles))):
                        for t in pages_titles[j]:
                            if _norm(t) in cand_norm or cand_norm in _norm(t):
                                pe = j + 1
                    return ps, pe, 2, candidate
    return None, None, 0, ""


def match_section_number(source, section_map):
    """
    Match 第X.X节 or 第X.X-X.X节 references against section_map.
    Returns (page_start, page_end, score, snippet).
    """
    # Extract all section numbers from source like "第8.2-8.6节" or "第10.1节"
    nums = re.findall(r'(\d+\.\d+(?:\.\d+)?)', source)
    if not nums:
        return None, None, 0, ""

    pages = []
    for num in nums:
        if num in section_map:
            ps, pe = section_map[num]
            pages.append((ps, pe))

    if not pages:
        return None, None, 0, ""

    # Merge ranges
    all_starts = [p[0] for p in pages]
    all_ends = [p[1] for p in pages]
    return min(all_starts), max(all_ends), 1, ",".join(nums)


def match_body_needle(body, pages_text):
    """Fallback: search body text in MinerU pages."""
    body_clean = re.sub(r'^#+\s+', '', body, flags=re.MULTILINE)
    body_clean = re.sub(r'\s+', ' ', body_clean).strip()
    needle = _norm(body_clean[:120])
    if len(needle) < 10:
        return None, None, 0, ""
    for length in [len(needle), len(needle) * 2 // 3, len(needle) // 2, 20]:
        sub = needle[:max(length, 10)]
        for i, pt in enumerate(pages_text):
            if sub in _norm(pt):
                return i + 1, i + 1, 0.5, body_clean[:40]
    return None, None, 0, ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def collect_targets():
    files = []
    for pat in TARGET_PATTERNS:
        files.extend(sorted(DRAFTS.glob(pat)))
    return files


def main():
    with open(MINERU_JSON, encoding="utf-8") as f:
        mineru = json.load(f)

    pages_text = [extract_page_text(page) for page in mineru]
    pages_titles = [list(_iter_title_texts(page)) for page in mineru]
    section_map = build_section_map(mineru)
    print(f"Loaded {len(pages_text)} logical pages, {len(section_map)} sections")

    targets = collect_targets()
    print(f"Found {len(targets)} target KB entries")

    rows = []
    for path in targets:
        m = re.match(r'^(KB-\d{4}(?:-\d+)?)', path.stem)
        entry_id = m.group(1) if m else path.stem

        text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        fm_str, body = parse_frontmatter(text)
        title = get_fm_field(fm_str, "title") if fm_str else ""
        source = get_fm_field(fm_str, "source") if fm_str else ""

        ps = pe = None
        score = 0
        snippet = ""

        # Strategy 1: § section reference (KB-20260324 entries)
        if "§" in source:
            ps, pe, score, snippet = match_section_ref(source, pages_titles)

        # Strategy 2: 第X.X节 section number (医小管知识库 entries)
        if ps is None and "第" in source and "节" in source:
            ps, pe, score, snippet = match_section_number(source, section_map)

        # Strategy 3: body needle fallback
        if ps is None:
            ps, pe, score, snippet = match_body_needle(body, pages_text)

        match_failed = ps is None
        ps = ps or 0
        pe = pe or 0

        rows.append({
            "entry_id": entry_id,
            "file": path.name,
            "title": title,
            "page_start": ps,
            "page_end": pe,
            "match_score": score,
            "match_snippet": snippet,
            "match_failed": match_failed,
        })

        update_frontmatter(path, ps, pe)
        status = "OK  " if not match_failed else "FAIL"
        print(f"  {status} {path.name}: pages {ps}-{pe} (score={score})")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "entry_id", "file", "title", "page_start", "page_end",
            "match_score", "match_snippet", "match_failed"
        ])
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nReport written: {REPORT}")
    failed = [r for r in rows if r["match_failed"]]
    print(f"Total: {len(rows)}, matched: {len(rows)-len(failed)}, failed: {len(failed)}")
    if failed:
        print("match_failed entries:")
        for r in failed:
            print(f"  {r['file']}")


if __name__ == "__main__":
    main()
