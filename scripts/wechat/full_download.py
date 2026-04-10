#!/usr/bin/env python3
"""
wechat full_download.py
对所有 A/B 类公众号，逐页遍历 wechat-article-exporter 的缓存文章列表，
按时间范围+关键词筛选后批量下载为 Markdown。

用法: python scripts/wechat/full_download.py --auth-key YOUR_KEY
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

# ===== 配置 =====
BASE_URL = "http://localhost:3000"
START_TS = 1711900800   # 2024-04-01
END_TS   = 1775779200   # 2026-04-10 (fixed)
PAGE_SIZE = 20
SLEEP_BETWEEN_PAGES = 1.5   # 秒
SLEEP_BETWEEN_ACCOUNTS = 3  # 秒
OUTPUT_DIR = Path("wechat-exports-full")

INCLUDE_KEYWORDS = [
    "通知", "公告", "安排", "须知", "指南", "攻略", "流程", "办理",
    "报名", "缴费", "政策", "规定", "奖学金", "助学金", "选课", "考试",
    "成绩", "宿舍", "校园卡", "图书馆", "网络", "VPN", "毕业", "就业",
    "考研", "保研", "实习", "社团", "竞赛", "志愿", "心理", "讲座",
    "申请", "开放", "服务", "公示", "结果", "名单", "调剂", "录取",
]

EXCLUDE_KEYWORDS = [
    "招聘", "聘用", "人才引进", "论文发表", "SCI", "学术会议",
    "领导调研", "视察", "座谈", "转发", "转载",
]

# A/B 类账号列表
ACCOUNTS = [
    # A 类
    {"name": "山东第一医科大学教务部",    "fakeid": "Mzg3ODMyNjg1Nw==",   "tier": "A"},
    {"name": "山东第一医科大学研究生处",  "fakeid": "Mzg5MTY0Njg2NA==",   "tier": "A"},
    {"name": "山一大学工",               "fakeid": "Mzg5MDc2MDMwNA==",   "tier": "A"},
    {"name": "山一大后勤",               "fakeid": "Mzg5NTQyMzg4NQ==",   "tier": "A"},
    {"name": "山一大心理健康教育中心",    "fakeid": "MzkxNzU2NTQxMg==",   "tier": "A"},
    {"name": "山东第一医科大学图书馆",    "fakeid": "MzU1OTI5MzIwNA==",   "tier": "A"},
    {"name": "山东第一医科大学就业",      "fakeid": "MzkwMDQxNDA2Nw==",   "tier": "A"},
    {"name": "山东第一医科大学科研部",    "fakeid": "MzkzOTE5OTI5Mg==",   "tier": "A"},
    # B 类
    {"name": "山东第一医科大学 山东省医学科学院", "fakeid": "MjM5NjA2NjcyMg==", "tier": "B"},
    {"name": "山一大招生办",             "fakeid": "MzAxNzYyMzM1OA==",   "tier": "B"},
    {"name": "青春山一大",               "fakeid": "MzIyMTA3MDc4OA==",   "tier": "B"},
    {"name": "山东第一医科大学医药管理学院", "fakeid": "Mzg2NTY5ODAwNA==", "tier": "B"},
    {"name": "山东第一医科大学科创中心",  "fakeid": "Mzg3NDcwOTc0Mw==",   "tier": "B"},
    {"name": "山一大饮食",               "fakeid": "MzkxOTU2MTMyNg==",   "tier": "B"},
    {"name": "山东第一医科大学对外合作交流部", "fakeid": "Mzg2MzYwNDM0MQ==", "tier": "B"},
    {"name": "山东第一医科大学计划财务处", "fakeid": "Mzg4NDUxNDU1OA==",  "tier": "B"},
]


def get_all_articles(session, auth_key: str, fakeid: str, account_name: str):
    """逐页获取账号全部文章列表，返回列表"""
    all_articles = []
    begin = 0
    page = 0

    while True:
        url = f"{BASE_URL}/api/public/v1/article?fakeid={urllib.parse.quote(fakeid)}&begin={begin}&count={PAGE_SIZE}"
        try:
            resp = session.get(url, headers={"X-Auth-Key": auth_key}, timeout=30)
            data = resp.json()
        except Exception as e:
            print(f"  ⚠ 获取第{page+1}页失败: {e}")
            break

        articles = data.get("articles", data.get("data", data.get("list", [])))
        if not isinstance(articles, list):
            print(f"  ⚠ 意外响应格式: {list(data.keys())}")
            break

        if not articles:
            break

        all_articles.extend(articles)
        page += 1
        print(f"  第{page}页: {len(articles)}篇 (累计{len(all_articles)}篇)", end="\r")

        if len(articles) < PAGE_SIZE:
            break  # 末页

        begin += PAGE_SIZE
        time.sleep(SLEEP_BETWEEN_PAGES)

    return all_articles


def should_include(title: str, create_time: int) -> bool:
    """按时间和关键词判断是否下载"""
    if not (START_TS <= create_time <= END_TS):
        return False
    if any(kw in title for kw in EXCLUDE_KEYWORDS):
        return False
    return any(kw in title for kw in INCLUDE_KEYWORDS)


def download_article(session, auth_key: str, url: str, out_path: Path) -> bool:
    """下载单篇文章为 Markdown"""
    if out_path.exists():
        return True  # 已存在，跳过
    try:
        encoded_url = urllib.parse.quote(url, safe="")
        resp = session.get(
            f"{BASE_URL}/api/public/v1/download?url={encoded_url}&format=markdown",
            headers={"X-Auth-Key": auth_key},
            timeout=60,
        )
        if resp.status_code == 200 and len(resp.text) > 100:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(resp.text, encoding="utf-8")
            return True
        else:
            print(f"\n    FAIL [{resp.status_code}] {out_path.name[:40]}")
            return False
    except Exception as e:
        print(f"\n    ERROR: {e} — {out_path.name[:40]}")
        return False


def safe_filename(s: str, max_len: int = 60) -> str:
    s = re.sub(r'[\\/:*?"<>|]', "", s)
    return s[:max_len]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth-key", required=True, help="wechat-article-exporter auth-key")
    parser.add_argument("--tier", default="A,B", help="处理的账号等级，逗号分隔，如 A 或 A,B")
    args = parser.parse_args()

    tiers = set(args.tier.split(","))
    auth_key = args.auth_key
    accounts = [a for a in ACCOUNTS if a["tier"] in tiers]

    print(f"处理账号: {len(accounts)} 个 (等级: {tiers})")
    print(f"时间范围: {datetime.fromtimestamp(START_TS).date()} ~ {datetime.fromtimestamp(END_TS).date()}")
    print(f"输出目录: {OUTPUT_DIR}/\n")

    session = requests.Session()
    stats = []
    total_downloaded = 0
    total_failed = 0

    for acc in accounts:
        name = acc["name"]
        fakeid = acc["fakeid"]
        tier = acc["tier"]
        print(f"\n[{tier}] {name}")

        articles = get_all_articles(session, auth_key, fakeid, name)
        print(f"\n  总文章数: {len(articles)}")

        filtered = [
            a for a in articles
            if should_include(
                a.get("title", ""),
                a.get("create_time", a.get("update_time", 0))
            )
        ]
        print(f"  筛选命中: {len(filtered)} 篇")

        dl_ok = dl_fail = 0
        for a in filtered:
            title = a.get("title", "untitled")
            url = a.get("link", a.get("url", ""))
            ts = a.get("create_time", a.get("update_time", 0))
            date_str = datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts else "0000-00-00"
            fname = safe_filename(f"{date_str}-{title}") + ".md"
            out_path = OUTPUT_DIR / safe_filename(name) / fname

            ok = download_article(session, auth_key, url, out_path)
            if ok:
                dl_ok += 1
            else:
                dl_fail += 1
            time.sleep(1)

        print(f"  下载完成: {dl_ok}篇 ✅  失败: {dl_fail}篇")
        stats.append({"account": name, "tier": tier, "total": len(articles),
                      "filtered": len(filtered), "downloaded": dl_ok, "failed": dl_fail})
        total_downloaded += dl_ok
        total_failed += dl_fail
        time.sleep(SLEEP_BETWEEN_ACCOUNTS)

    # 生成统计报告
    print(f"\n\n{'='*60}")
    print(f"全量下载完成: {total_downloaded} 篇 ✅ / 失败: {total_failed} 篇")
    print(f"{'='*60}")

    report_lines = ["# wechat 全量下载统计\n",
                    f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n",
                    f"时间范围: 2024-04-01 ~ 2026-04-10\n\n",
                    "| 账号 | 等级 | 总篇数 | 筛选命中 | 已下载 | 失败 |\n",
                    "|------|------|--------|---------|--------|------|\n"]
    for s in stats:
        report_lines.append(
            f"| {s['account']} | {s['tier']} | {s['total']} | {s['filtered']} | {s['downloaded']} | {s['failed']} |\n"
        )
    report_lines.append(f"\n**合计下载**: {total_downloaded} 篇\n")

    Path("kimi/wechat-full-download-stats.md").write_text("".join(report_lines), encoding="utf-8")
    print("统计报告: kimi/wechat-full-download-stats.md")


if __name__ == "__main__":
    main()
