#!/usr/bin/env python3
"""
filter_and_download.py
Phase 2+3: 读取 wechat-meta/*.jsonl，过滤后批量下载为 Markdown。

用法:
    python scripts/wechat/filter_and_download.py --auth-key YOUR_KEY [--meta-dir wechat-meta] [--out wechat-articles]
"""
import argparse
import json
import os
import re
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "http://localhost:3000"
START_TS = 1711900800   # 2024-04-01
END_TS   = 1775779200   # 2026-04-10
SLEEP_DOWNLOAD = 1.5    # 每篇文章下载间隔（秒）

INCLUDE_KEYWORDS = [
    "通知", "公告", "安排", "须知", "指南", "攻略", "流程", "办理",
    "报名", "缴费", "政策", "规定", "奖学金", "助学金", "选课", "考试",
    "成绩", "宿舍", "校园卡", "图书馆", "网络", "VPN", "毕业", "就业",
    "考研", "保研", "实习", "社团", "竞赛", "志愿", "心理", "讲座",
    "申请", "开放", "服务", "公示", "结果", "名单", "调剂", "录取",
    "奖励", "处分", "学籍", "缓考", "补考", "重修", "保险", "医保",
    "签证", "护照", "出国", "访学", "交流", "合作", "实验室", "科创",
    "招聘", "实习", "简历", "面试", "offer",
]

EXCLUDE_KEYWORDS = [
    "人才引进", "论文发表", "SCI", "学术会议",
    "领导调研", "视察", "座谈", "工作会议",
    "先进事迹", "劳模", "党建",
]


def should_include(title: str, ts: int) -> bool:
    if not (START_TS <= ts <= END_TS):
        return False
    if any(kw in title for kw in EXCLUDE_KEYWORDS):
        return False
    return any(kw in title for kw in INCLUDE_KEYWORDS)


def safe_name(s: str, max_len: int = 60) -> str:
    return re.sub(r'[\\/:*?"<>|]', "", s)[:max_len]


def download_article(session: requests.Session, auth_key: str, url: str, out_path: Path) -> bool:
    if out_path.exists() and out_path.stat().st_size > 200:
        return True  # 已下载
    try:
        enc = urllib.parse.quote(url, safe="")
        resp = session.get(
            f"{BASE_URL}/api/public/v1/download?url={enc}&format=markdown",
            headers={"X-Auth-Key": auth_key},
            timeout=60,
        )
        if resp.status_code == 200 and len(resp.text) > 200:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(resp.text, encoding="utf-8")
            return True
        print(f"  SKIP [{resp.status_code}] {out_path.name[:50]}")
        return False
    except Exception as e:
        print(f"  ERROR: {e} — {out_path.name[:50]}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth-key", required=True)
    parser.add_argument("--meta-dir", default="wechat-meta")
    parser.add_argument("--out", default="wechat-articles")
    args = parser.parse_args()

    meta_dir = Path(args.meta_dir)
    out_dir  = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Phase 2: 读取并过滤
    all_articles = []
    for jsonl in sorted(meta_dir.glob("*.jsonl")):
        for line in jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                art = json.loads(line)
            except json.JSONDecodeError:
                continue
            title = art.get("title", "")
            ts    = art.get("create_time", 0)
            if should_include(title, ts):
                all_articles.append(art)

    print(f"\nPhase 2 筛选结果: {len(all_articles)} 篇（共读取自 {meta_dir}/）")
    if not all_articles:
        print("⚠ 没有符合条件的文章，检查时间范围和关键词配置")
        return

    # 保存筛选列表
    filtered_path = meta_dir / "filtered.jsonl"
    with filtered_path.open("w", encoding="utf-8") as f:
        for a in all_articles:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    print(f"筛选列表已保存: {filtered_path}")

    # 按账号分组统计
    by_account: dict[str, int] = {}
    for a in all_articles:
        acc = a.get("account", "unknown")
        by_account[acc] = by_account.get(acc, 0) + 1
    for acc, cnt in sorted(by_account.items(), key=lambda x: -x[1]):
        print(f"  {acc}: {cnt} 篇")

    # Phase 3: 下载
    print(f"\nPhase 3 开始下载 {len(all_articles)} 篇文章…")
    session   = requests.Session()
    auth_key  = args.auth_key
    ok = fail = skip = 0

    for art in all_articles:
        title   = art.get("title", "untitled")
        url     = art.get("link", "")
        ts      = art.get("create_time", 0)
        account = art.get("account", "unknown")
        date_s  = datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else "0000-00-00"
        fname   = safe_name(f"{date_s}-{title}") + ".md"
        out_path = out_dir / safe_name(account) / fname

        if out_path.exists() and out_path.stat().st_size > 200:
            skip += 1
            continue

        success = download_article(session, auth_key, url, out_path)
        if success:
            ok += 1
            print(f"  ✓ [{ok+fail}/{len(all_articles)}] {date_s} {title[:40]}")
        else:
            fail += 1
        time.sleep(SLEEP_DOWNLOAD)

    print(f"\n下载完成: ✅ {ok} 篇  ⏭ 已存在 {skip} 篇  ❌ 失败 {fail} 篇")

    # 生成报告
    report_lines = [
        "# Phase 2+3 下载报告\n\n",
        f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
        f"## 筛选结果\n\n总文章数: {len(all_articles)}\n\n",
        "| 账号 | 篇数 |\n|------|------|\n",
    ]
    for acc, cnt in sorted(by_account.items(), key=lambda x: -x[1]):
        report_lines.append(f"| {acc} | {cnt} |\n")
    report_lines += [
        f"\n## 下载结果\n\n",
        f"- 成功下载: {ok} 篇\n",
        f"- 已存在跳过: {skip} 篇\n",
        f"- 失败: {fail} 篇\n",
        f"- 输出目录: `{out_dir}/`\n",
    ]
    report_path = out_dir / "download-report.md"
    report_path.write_text("".join(report_lines), encoding="utf-8")
    print(f"报告: {report_path}")


if __name__ == "__main__":
    main()
