# T3 任务: 3路并发抓取 — direct + vproxy-01 + vproxy-02

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3
## 目标: 将 wechat-meta/ 文章总量扩充到 1500+ 篇

---

## Step 1: 修改 sync_and_save.py 支持 --proxy 参数

在 `scripts/wechat/sync_and_save.py` 中：

1. 在 `argparse` 部分添加：
   ```python
   parser.add_argument("--proxy", default="", help="代理 URL，如 https://vproxy-01.deno.dev")
   ```

2. 在 `fetch_account` 函数的 GET 请求 URL 中，如果 proxy 不为空，追加 `&proxy=<proxy_url>` 参数：
   ```python
   if proxy:
       url += f"&proxy={urllib.parse.quote(proxy, safe='')}"
   ```

3. 将 proxy 参数传递给 `fetch_account`

## Step 2: 启动 3 路并行抓取（分 3 个后台进程）

```powershell
# 路1: 直连（无代理），5轮
Start-Process powershell -ArgumentList "-Command python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta 2>&1 | Tee-Object -FilePath wechat-meta\log-direct.txt; for(`$i=1;`$i -le 4;`$i++){Start-Sleep 30; python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta 2>&1 | Tee-Object -Append -FilePath wechat-meta\log-direct.txt}" -WindowStyle Hidden

# 路2: vproxy-01，5轮
Start-Process powershell -ArgumentList "-Command python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta --proxy https://vproxy-01.deno.dev 2>&1 | Tee-Object -FilePath wechat-meta\log-proxy1.txt; for(`$i=1;`$i -le 4;`$i++){Start-Sleep 30; python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta --proxy https://vproxy-01.deno.dev 2>&1 | Tee-Object -Append -FilePath wechat-meta\log-proxy1.txt}" -WindowStyle Hidden

# 路3: vproxy-02，5轮
Start-Process powershell -ArgumentList "-Command python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta --proxy https://vproxy-02.deno.dev 2>&1 | Tee-Object -FilePath wechat-meta\log-proxy2.txt; for(`$i=1;`$i -le 4;`$i++){Start-Sleep 30; python scripts\wechat\sync_and_save.py --auth-key 01bc3c2fd80b486fbbe42d5c606b55e3 --tier A,B --out wechat-meta --proxy https://vproxy-02.deno.dev 2>&1 | Tee-Object -Append -FilePath wechat-meta\log-proxy2.txt}" -WindowStyle Hidden

Write-Host "3路并发已启动，等待 3 分钟后检查进度..."
Start-Sleep -Seconds 180
```

## Step 3: 等待 3 分钟后检查进度

```powershell
Start-Sleep -Seconds 180

# 统计当前总量
$total = (Get-ChildItem wechat-meta\*.jsonl | Get-Content).Count
Write-Host "当前累计: $total 篇"

Get-ChildItem wechat-meta\*.jsonl | ForEach-Object {
    $count = (Get-Content $_.FullName).Count
    Write-Host "$($_.BaseName): $count"
}
```

## Step 4: 再等 5 分钟，做最终统计

```powershell
Start-Sleep -Seconds 300

$total = (Get-ChildItem wechat-meta\*.jsonl | Get-Content).Count
Write-Host "最终累计: $total 篇"

Get-ChildItem wechat-meta\*.jsonl | ForEach-Object {
    $count = (Get-Content $_.FullName).Count
    Write-Host "$($_.BaseName): $count"
}
```

## 输出

1. sync_and_save.py 是否成功修改（--proxy 支持）
2. 3路进程是否已启动
3. 3分钟后中间统计结果
4. 8分钟后最终统计（目标 ≥ 1000 篇）

请开始执行。
