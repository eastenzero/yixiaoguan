# T3 任务: v8 Phase1 — 全量元数据抓取（sync_and_save.py）

## 目标
对 16 个公众号账号，逐页翻页抓取所有文章的标题/链接/时间，实时写入 `wechat-meta/` 目录。

## 前置确认

### Step 0: 安装依赖
```powershell
pip install requests
```

### Step 1: 确认脚本存在
```powershell
Get-Item scripts\wechat\sync_and_save.py
```

## Step 2: 运行全量抓取（A 类 + B 类）

```powershell
python scripts\wechat\sync_and_save.py --auth-key b982b119ba0744358c1dbcd6711c06fe --tier A,B --out wechat-meta
```

**说明**：
- 每页间隔 2 秒，每账号结束后等待 5 秒，避免限流
- 每页数据实时写入 `wechat-meta/{账号名}.jsonl`，中断后可断点续跑
- 预计总耗时 30-90 分钟
- 如果某账号被限流（返回空或错误），脚本会自动重试一次后跳过

## Step 3: 运行结束后输出汇总

读取并输出 `wechat-meta/sync-report.md` 内容。

## 验收标准
- 16 个账号均有对应的 `.jsonl` 文件
- 合计文章数 ≥ 500（如果 WeChat 限流严重导致数量少，如实报告原因）
- 输出 sync-report.md

请开始执行，耐心等待全部翻页完成。
