# T3 任务: v8 Phase2+3 — 筛选并下载全量文章

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3

## Step 1: 确认元数据文件
```powershell
Get-ChildItem wechat-meta\*.jsonl | ForEach-Object { "$($_.Name): $($(Get-Content $_.FullName).Count) 行" }
```
应有 16 个文件，合计 263 行。

## Step 2: 运行 Phase 2+3（筛选 + 下载）
```powershell
python scripts\wechat\filter_and_download.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --meta-dir wechat-meta --out wechat-articles
```

脚本会：
1. 读取所有 `.jsonl` 文件，按时间范围（2024-04-01 ~ 2026-04-10）和关键词过滤
2. 保存筛选列表到 `wechat-meta/filtered.jsonl`
3. 逐篇下载为 Markdown，存入 `wechat-articles/{账号名}/`，每篇间隔 1.5 秒

## Step 3: 完成后输出报告

读取并输出 `wechat-articles/download-report.md` 完整内容。

## 验收标准
- `wechat-meta/filtered.jsonl` 存在且行数 ≥ 30
- `wechat-articles/` 下有按账号分目录的 .md 文件
- 下载成功数 ≥ 30 篇

请开始执行。
