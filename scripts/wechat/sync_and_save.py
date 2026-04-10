#!/usr/bin/env python3
"""
sync_and_save.py
全量抓取所有公众号文章元数据，每页实时写盘，防止会话中断丢数据。

用法:
    python scripts/wechat/sync_and_save.py --auth-key YOUR_KEY [--out wechat-meta/]
"""
import argparse
import json
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests

BASE_URL = "http://localhost:3000"
PAGE_SIZE = 20
SLEEP_PAGE = 2       # 每翻一页等待（秒）
SLEEP_ACCOUNT = 5   # 每账号结束后等待（秒）

ACCOUNTS = [
    {"name": "山东第一医科大学教务部",          "fakeid": "Mzg3ODMyNjg1Nw==",   "tier": "A"},
    {"name": "山东第一医科大学研究生处",        "fakeid": "Mzg5MTY0Njg2NA==",   "tier": "A"},
    {"name": "山一大学工",                     "fakeid": "Mzg5MDc2MDMwNA==",   "tier": "A"},
    {"name": "山一大后勤",                     "fakeid": "Mzg5NTQyMzg4NQ==",   "tier": "A"},
    {"name": "山一大心理健康教育中心",          "fakeid": "MzkxNzU2NTQxMg==",   "tier": "A"},
    {"name": "山东第一医科大学图书馆",          "fakeid": "MzU1OTI5MzIwNA==",   "tier": "A"},
    {"name": "山东第一医科大学就业",            "fakeid": "MzkwMDQxNDA2Nw==",   "tier": "A"},
    {"name": "山东第一医科大学科研部",          "fakeid": "MzkzOTE5OTI5Mg==",   "tier": "A"},
    {"name": "山东第一医科大学 山东省医学科学院","fakeid": "MjM5NjA2NjcyMg==",  "tier": "B"},
    {"name": "山一大招生办",                   "fakeid": "MzAxNzYyMzM1OA==",   "tier": "B"},
    {"name": "青春山一大",                     "fakeid": "MzIyMTA3MDc4OA==",   "tier": "B"},
    {"name": "山东第一医科大学医药管理学院",    "fakeid": "Mzg2NTY5ODAwNA==",   "tier": "B"},
    {"name": "山东第一医科大学科创中心",        "fakeid": "Mzg3NDcwOTc0Mw==",   "tier": "B"},
    {"name": "山一大饮食",                     "fakeid": "MzkxOTU2MTMyNg==",   "tier": "B"},
    {"name": "山东第一医科大学对外合作交流部",  "fakeid": "Mzg2MzYwNDM0MQ==",   "tier": "B"},
    {"name": "山东第一医科大学计划财务处",      "fakeid": "Mzg4NDUxNDU1OA==",   "tier": "B"},
]


def fetch_account(session: requests.Session, auth_key: str, account: dict, out_dir: Path, proxy: str = "") -> int:
    name = account["name"]
    fakeid = account["fakeid"]
    safe_name = name.replace("/", "_").replace(" ", "_")
    out_file = out_dir / f"{safe_name}.jsonl"

    # 如果已有数据文件，统计已写行数，从断点续爬
    existing = 0
    if out_file.exists():
        existing = sum(1 for _ in out_file.open("r", encoding="utf-8"))
        print(f"  [续爬] 已有 {existing} 篇，从 begin={existing} 继续")

    begin = existing
    page = existing // PAGE_SIZE
    new_count = 0

    with out_file.open("a", encoding="utf-8") as fout:
        while True:
            url = (
                f"{BASE_URL}/api/public/v1/article"
                f"?fakeid={urllib.parse.quote(fakeid)}&begin={begin}&count={PAGE_SIZE}"
            )
            if proxy:
                url += f"&proxy={urllib.parse.quote(proxy, safe='')}"
            try:
                resp = session.get(url, headers={"X-Auth-Key": auth_key}, timeout=30)
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"\n  ⚠ 第{page+1}页请求失败: {e}，等待 10 秒后重试…")
                time.sleep(10)
                try:
                    resp = session.get(url, headers={"X-Auth-Key": auth_key}, timeout=30)
                    data = resp.json()
                except Exception as e2:
                    print(f"\n  ✗ 重试仍失败: {e2}，跳过此页")
                    break

            articles = (
                data.get("articles")
                or data.get("data")
                or data.get("list")
                or []
            )
            if not isinstance(articles, list) or not articles:
                break

            for art in articles:
                record = {
                    "title":       art.get("title", ""),
                    "link":        art.get("link", art.get("url", "")),
                    "create_time": art.get("create_time", art.get("update_time", 0)),
                    "account":     name,
                    "fakeid":      fakeid,
                    "tier":        account["tier"],
                }
                fout.write(json.dumps(record, ensure_ascii=False) + "\n")

            new_count += len(articles)
            page += 1
            print(f"  第{page}页: +{len(articles)} 篇（累计新增 {new_count} 篇）", end="\r")

            if len(articles) < PAGE_SIZE:
                break

            begin += PAGE_SIZE
            time.sleep(SLEEP_PAGE)

    total = existing + new_count
    print(f"\n  完成: 共 {total} 篇（本次新增 {new_count} 篇）→ {out_file.name}")
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--auth-key", required=True)
    parser.add_argument("--out", default="wechat-meta", help="元数据输出目录")
    parser.add_argument("--tier", default="A,B", help="处理等级，如 A 或 A,B")
    parser.add_argument("--proxy", default="", help="代理 URL，如 https://vproxy-01.deno.dev")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    tiers = set(args.tier.split(","))
    accounts = [a for a in ACCOUNTS if a["tier"] in tiers]

    print(f"开始全量元数据抓取 — {len(accounts)} 个账号")
    print(f"输出目录: {out_dir}/\n")

    session = requests.Session()
    summary = []

    for acc in accounts:
        print(f"\n[{acc['tier']}] {acc['name']}")
        total = fetch_account(session, args.auth_key, acc, out_dir, args.proxy)
        summary.append({"account": acc["name"], "tier": acc["tier"], "total": total})
        time.sleep(SLEEP_ACCOUNT)

    # 写汇总报告
    grand = sum(s["total"] for s in summary)
    report = ["# wechat-meta 全量抓取报告\n\n",
              f"执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n",
              "| 账号 | 等级 | 文章总数 |\n",
              "|------|------|--------|\n"]
    for s in summary:
        report.append(f"| {s['account']} | {s['tier']} | {s['total']} |\n")
    report.append(f"\n**合计**: {grand} 篇\n")

    report_path = out_dir / "sync-report.md"
    report_path.write_text("".join(report), encoding="utf-8")

    print(f"\n{'='*50}")
    print(f"全部完成！合计 {grand} 篇元数据已保存至 {out_dir}/")
    print(f"汇总报告: {report_path}")


if __name__ == "__main__":
    main()
