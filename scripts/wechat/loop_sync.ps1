# loop_sync.ps1 — 每 N 分钟重新抓取一轮，追加新文章
param(
    [string]$AuthKey = "01bc3c2fd80b486fbbe42d5c606b55e3",
    [int]$Rounds = 5,
    [int]$IntervalMinutes = 10
)

Write-Host "开始多轮抓取，共 $Rounds 轮，每轮间隔 $IntervalMinutes 分钟"

# Get initial counts per file
$initialCounts = @{}
Get-ChildItem wechat-meta\*.jsonl -ErrorAction SilentlyContinue | ForEach-Object {
    $initialCounts[$_.BaseName] = (Get-Content $_.FullName).Count
}

for ($i = 1; $i -le $Rounds; $i++) {
    Write-Host "`n=== 第 $i 轮 $(Get-Date -Format 'HH:mm:ss') ==="
    python scripts\wechat\sync_and_save.py --auth-key $AuthKey --tier A,B --out wechat-meta
    
    # Count total and per-file
    $totalCount = 0
    Write-Host "--- 本轮后统计 ---"
    Get-ChildItem wechat-meta\*.jsonl -ErrorAction SilentlyContinue | ForEach-Object {
        $name = $_.BaseName
        $count = (Get-Content $_.FullName).Count
        $initial = if ($initialCounts.ContainsKey($name)) { $initialCounts[$name] } else { 0 }
        $added = $count - $initial
        $totalCount += $count
        Write-Host "  $name`: $count 篇 (新增: $added)"
    }
    Write-Host "累计元数据: $totalCount 篇"
    
    if ($i -lt $Rounds) {
        Write-Host "等待 $IntervalMinutes 分钟后进行下一轮..."
        Start-Sleep -Seconds ($IntervalMinutes * 60)
    }
}

Write-Host "`n全部完成！"
$finalCount = 0
Get-ChildItem wechat-meta\*.jsonl -ErrorAction SilentlyContinue | ForEach-Object {
    $count = (Get-Content $_.FullName).Count
    $finalCount += $count
}
Write-Host "最终累计: $finalCount 篇"
