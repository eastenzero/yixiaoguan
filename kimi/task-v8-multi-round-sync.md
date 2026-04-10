# T3 任务: 多轮定时抓取脚本 — 持续积累文章元数据

## 目标
编写并执行一个循环脚本，每隔一段时间重新调用 sync_and_save.py，将每轮新增的文章追加写入 .jsonl 文件（脚本已支持断点续跑），持续积累，直到不再有新文章为止。

## auth-key: 01bc3c2fd80b486fbbe42d5c606b55e3

## Step 1: 先做一次"偏移抓取"测试

当前每账号只取到 10-41 篇。尝试带 begin 偏移直接取更早的文章：

```powershell
curl.exe -s -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" "http://localhost:3000/api/public/v1/article?fakeid=MzU1OTI5MzIwNA==&begin=40&count=20" | python -m json.tool | Select-String -Pattern "title|create_time" | Select-Object -First 20
```

（图书馆账号，begin=40 取第 41-60 篇，看是否有更早的文章）

```powershell
curl.exe -s -H "X-Auth-Key: 01bc3c2fd80b486fbbe42d5c606b55e3" "http://localhost:3000/api/public/v1/article?fakeid=MzU1OTI5MzIwNA==&begin=100&count=20" | python -m json.tool | Select-String -Pattern "title|create_time" | Select-Object -First 10
```

（begin=100，看第101篇起是否有数据）

## Step 2: 编写多轮循环脚本

创建文件 `scripts/wechat/loop_sync.ps1`：

```powershell
# loop_sync.ps1 — 每 N 分钟重新抓取一轮，追加新文章
param(
    [string]$AuthKey = "01bc3c2fd80b486fbbe42d5c606b55e3",
    [int]$Rounds = 5,
    [int]$IntervalMinutes = 10
)

Write-Host "开始多轮抓取，共 $Rounds 轮，每轮间隔 $IntervalMinutes 分钟"

for ($i = 1; $i -le $Rounds; $i++) {
    Write-Host "`n=== 第 $i 轮 $(Get-Date -Format 'HH:mm:ss') ==="
    python scripts\wechat\sync_and_save.py --auth-key $AuthKey --tier A,B --out wechat-meta
    
    $count = (Get-ChildItem wechat-meta\*.jsonl | Get-Content).Count
    Write-Host "累计元数据: $count 篇"
    
    if ($i -lt $Rounds) {
        Write-Host "等待 $IntervalMinutes 分钟后进行下一轮..."
        Start-Sleep -Seconds ($IntervalMinutes * 60)
    }
}

Write-Host "`n全部完成！"
$finalCount = (Get-ChildItem wechat-meta\*.jsonl | Get-Content).Count
Write-Host "最终累计: $finalCount 篇"
```

## Step 3: 立即执行 3 轮（每轮间隔 5 分钟）

```powershell
powershell -File scripts\wechat\loop_sync.ps1 -Rounds 3 -IntervalMinutes 5
```

## Step 4: 完成后统计每个账号的新增文章数

```powershell
Get-ChildItem wechat-meta\*.jsonl | ForEach-Object {
    $name = $_.BaseName
    $count = (Get-Content $_.FullName).Count
    Write-Host "$name`: $count 篇"
}
```

## 输出

1. Step 1 的偏移抓取结果：begin=40 和 begin=100 各返回几篇？最早的文章日期是什么？
2. loop_sync.ps1 文件已创建路径
3. 3 轮执行结果（每轮新增数）
4. 最终累计篇数

请开始执行。
