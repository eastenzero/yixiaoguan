# T3 任务: v8 Phase1 — 全量元数据抓取（新 session，立刻执行）

## ⚠️ 时间紧迫：WeChat session 新鲜，必须立即开始，不要拖延

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3

## Step 1: 确认脚本和依赖
```powershell
pip install requests -q
Get-Item scripts\wechat\sync_and_save.py
```

## Step 2: 立即运行全量抓取

```powershell
python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta
```

**重要说明**：
- 脚本每翻一页等 2 秒，每账号结束等 5 秒
- 每页数据**实时写入** `wechat-meta/{账号名}.jsonl`，中断可续跑
- 目标：≥ 500 篇（如果 session 新鲜，预计 1000-1800 篇）
- 如果某账号翻页到 0 结果就停止，继续下一账号
- **不要中断，耐心等待全部账号完成**

## Step 3: 完成后输出汇总

运行结束后输出 `wechat-meta/sync-report.md` 的完整内容。

同时列出每个 .jsonl 文件的行数：
```powershell
Get-ChildItem wechat-meta\*.jsonl | ForEach-Object { "$($_.Name): $($(Get-Content $_.FullName).Count) 行" }
```

请立即开始执行，不要等待。
