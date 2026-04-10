# T3 任务: v8 全量文章下载（利用完整缓存）

## 背景
之前 FILTER-DOWNLOAD 只下载了 33 篇，原因是筛选脚本只取了每账号第一页（5-7篇）。
现在已编写 `scripts/wechat/full_download.py`，会对每个账号逐页翻页获取全量文章后筛选下载。

## 准备工作

### Step 1: 安装依赖
```powershell
pip install requests
```

### Step 2: 确认脚本存在
```powershell
Get-Item scripts\wechat\full_download.py
```

## Step 3: 先跑 A 类账号（优先级最高）

```powershell
python scripts\wechat\full_download.py --auth-key b982b119ba0744358c1dbcd6711c06fe --tier A
```

**预计耗时**: 20-40 分钟（8个账号 × 多页文章，每页间隔1.5秒）
**预计下载量**: 100-200 篇

## Step 4: 跑完 A 类后继续 B 类

```powershell
python scripts\wechat\full_download.py --auth-key b982b119ba0744358c1dbcd6711c06fe --tier B
```

**预计耗时**: 10-20 分钟
**预计下载量**: 30-60 篇

## 输出

- 文章文件: `wechat-exports-full/{账号名}/{日期}-{标题}.md`
- 统计报告: `kimi/wechat-full-download-stats.md`

## 完成后报告

输出统计表（从 kimi/wechat-full-download-stats.md）：

| 账号 | 等级 | 总篇数 | 筛选命中 | 已下载 |
|------|------|--------|---------|--------|

以及合计下载篇数。

## 注意事项
- 脚本会自动跳过已下载的文件（幂等）
- 遇到网络错误会打印并继续，不中断
- auth-key 有效期 4 天（2026-04-10 生成），足够使用

请开始执行，先跑 A 类。
