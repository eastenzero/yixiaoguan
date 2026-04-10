# Update report from current data
$OutputDir = "kimi"
$existingJson = "$OutputDir/wechat-sync-data.json"

$data = Get-Content $existingJson | ConvertFrom-Json

# Use ArrayList to collect results
$accountList = [System.Collections.ArrayList]::new()

# Helper function to add or update account
function Add-Account {
    param($fakeId, $totalCount, $name, $type, $latestDate, $earliestDate)
    
    if (-not $fakeId -or $fakeId -eq "True") { return }
    
    # Check if we already have this fakeid
    $existing = $accountList | Where-Object { $_.fakeid -eq $fakeId }
    if ($existing -and $existing.total_count -ge $totalCount) {
        return
    }
    
    # Remove existing entry if present
    for ($i = $accountList.Count - 1; $i -ge 0; $i--) {
        if ($accountList[$i].fakeid -eq $fakeId) {
            $accountList.RemoveAt($i)
        }
    }
    
    # Add new entry
    $newEntry = [PSCustomObject]@{
        name = $name
        fakeid = $fakeId
        type = $type
        total_count = $totalCount
        latest_date = $latestDate
        earliest_date = $earliestDate
        status = "✅"
    }
    [void]$accountList.Add($newEntry)
}

# Helper function to get property value with fallback
function Get-Prop($obj, $lower, $upper) {
    $val = $obj.$lower
    if ($val -eq $null) { $val = $obj.$upper }
    return $val
}

# Process existing accounts
foreach ($a in $data.accounts) {
    $fakeId = Get-Prop $a "fakeid" "FakeId"
    $totalCount = Get-Prop $a "total_count" "TotalCount"
    $name = Get-Prop $a "name" "Name"
    $type = Get-Prop $a "type" "Type"
    $latestDate = Get-Prop $a "latest_date" "LatestDate"
    $earliestDate = Get-Prop $a "earliest_date" "EarliestDate"
    
    Add-Account -fakeId $fakeId -totalCount $totalCount -name $name -type $type -latestDate $latestDate -earliestDate $earliestDate
}

# Also load individual result files
$individualFiles = Get-ChildItem "$OutputDir/sync-result-*.json" -ErrorAction SilentlyContinue
foreach ($file in $individualFiles) {
    $indData = Get-Content $file | ConvertFrom-Json
    $fakeId = Get-Prop $indData "fakeid" "FakeId"
    $totalCount = Get-Prop $indData "total_count" "TotalCount"
    $name = Get-Prop $indData "name" "Name"
    $type = Get-Prop $indData "type" "Type"
    $latestDate = Get-Prop $indData "latest_date" "LatestDate"
    $earliestDate = Get-Prop $indData "earliest_date" "EarliestDate"
    
    Add-Account -fakeId $fakeId -totalCount $totalCount -name $name -type $type -latestDate $latestDate -earliestDate $earliestDate
    
    if ($fakeId -and $fakeId -ne "True") {
        Write-Host "Loaded from $($file.Name): $name - $totalCount articles" -ForegroundColor Gray
    }
}

$allResults = $accountList | Sort-Object type, name

# Save deduplicated data
$jsonData = @{
    sync_time = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    auth_key = $data.auth_key
    accounts = $allResults
} | ConvertTo-Json -Depth 10
$jsonData | Out-File -FilePath $existingJson -Encoding UTF8

# Generate report
$aClass = $allResults | Where-Object { $_.type -eq "A" }
$bClass = $allResults | Where-Object { $_.type -eq "B" }
$totalArticles = ($allResults | Measure-Object -Property total_count -Sum).Sum

$report = @"
# 公众号文章同步统计

同步时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
auth-key: $($data.auth_key)

## 汇总

| 分类 | 账号数 | 文章总数 |
|------|--------|----------|
| A 类 | $($aClass.Count) | $($aClass | Measure-Object -Property total_count -Sum | Select-Object -ExpandProperty Sum) |
| B 类 | $($bClass.Count) | $($bClass | Measure-Object -Property total_count -Sum | Select-Object -ExpandProperty Sum) |
| 合计 | $($allResults.Count) | $totalArticles |

## A 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
"@

foreach ($r in $aClass) {
    $shortName = $r.name -replace "山东第一医科大学", "山一大"
    $report += "| $($shortName) | $($r.fakeid) | $($r.total_count) | $($r.latest_date) | $($r.earliest_date) | $($r.status) |`n"
}

$report += @"

## B 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
"@

foreach ($r in $bClass) {
    $shortName = $r.name -replace "山东第一医科大学", "山一大"
    $report += "| $($shortName) | $($r.fakeid) | $($r.total_count) | $($r.latest_date) | $($r.earliest_date) | $($r.status) |`n"
}

$report += @"

---
Updated by update_report.ps1
"@

$reportPath = "$OutputDir/wechat-sync-stats.md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "Report updated!" -ForegroundColor Green
Write-Host "Total accounts: $($allResults.Count)" -ForegroundColor Green
Write-Host "Total articles: $totalArticles" -ForegroundColor Green
