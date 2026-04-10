# T3 任务: v8 全量文章下载（修复版）

## 背景
`scripts/wechat/full_download.py` 已修复两个 bug：
1. END_TS 从 1744214400 (2025-04-09) 改为 1775779200 (2026-04-10)
2. 外层键名从 `data` 改为 `articles`

## ⚠️ 不要运行 curl，脚本已用 requests 库

## Step 1: 确认脚本版本正确

```powershell
Select-String -Path scripts\wechat\full_download.py -Pattern "END_TS"
```
应该显示 `1775779200`。

## Step 2: 先跑 A 类账号

```powershell
python scripts\wechat\full_download.py --auth-key b982b119ba0744358c1dbcd6711c06fe --tier A
```

预计耗时 30-60 分钟，预计下载 80-200 篇。

## Step 3: 完成后跑 B 类账号

```powershell
python scripts\wechat\full_download.py --auth-key b982b119ba0744358c1dbcd6711c06fe --tier B
```

## 输出

下载完成后读取并输出 `kimi/wechat-full-download-stats.md` 的内容。

请开始执行，先跑 A 类。
