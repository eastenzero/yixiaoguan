#requires -Version 5.1
<#
.SYNOPSIS
    Sync remaining WeChat accounts (excluding already synced ones)
#>

$ErrorActionPreference = "Stop"
$BaseUrl = "http://localhost:3000"
$AuthKey = "b982b119ba0744358c1dbcd6711c06fe"
$OutputDir = "kimi"

# Already synced: 教务部, 研究生处
# Remaining accounts to sync
$Accounts = @(
    @{ Name = "山一大学工"; FakeId = "Mzg5MDc2MDMwNA=="; Type = "A" },
    @{ Name = "山一大后勤"; FakeId = "Mzg5NTQyMzg4NQ=="; Type = "A" },
    @{ Name = "山一大 心理健康教育中心"; FakeId = "MzkxNzU2NTQxMg=="; Type = "A" },
    @{ Name = "山东第一医科大学图书馆"; FakeId = "MzU1OTI5MzIwNA=="; Type = "A" },
    @{ Name = "山东第一医科大学就业"; FakeId = "MzkwMDQxNDA2Nw=="; Type = "A" },
    @{ Name = "山东第一医科大学科研部"; FakeId = "MzkzOTE5OTI5Mg=="; Type = "A" },
    @{ Name = "山东第一医科大学 山东省医学科学院"; FakeId = "MjM5NjA2NjcyMg=="; Type = "B" },
    @{ Name = "山一大招生办"; FakeId = "MzAxNzYyMzM1OA=="; Type = "B" },
    @{ Name = "青春山一大"; FakeId = "MzIyMTA3MDc4OA=="; Type = "B" },
    @{ Name = "山东第一医科大学医药管理学院"; FakeId = "Mzg2NTY5ODAwNA=="; Type = "B" },
    @{ Name = "山东第一医科大学科创中心"; FakeId = "Mzg3NDcwOTc0Mw=="; Type = "B" },
    @{ Name = "山一大饮食"; FakeId = "MzkxOTU2MTMyNg=="; Type = "B" },
    @{ Name = "山东第一医科大学对外合作交流部"; FakeId = "Mzg2MzYwNDM0MQ=="; Type = "B" },
    @{ Name = "山东第一医科大学计划财务处"; FakeId = "Mzg4NDUxNDU1OA=="; Type = "B" }
)

function Get-ArticlesForAccount {
    param(
        [string]$FakeId,
        [string]$AccountName
    )
    
    $allArticles = @()
    $begin = 0
    $pageSize = 20
    $pageCount = 0
    $retryCount = 0
    $maxRetries = 3
    
    Write-Host "  Fetching: $AccountName" -ForegroundColor Cyan
    
    do {
        $url = "$BaseUrl/api/public/v1/article?fakeid=$FakeId&begin=$begin&count=$pageSize"
        try {
            $response = curl.exe -s -H "X-Auth-Key: $AuthKey" $url | ConvertFrom-Json
            
            if ($response.base_resp.ret -ne 0) {
                if ($response.base_resp.err_msg -like "*freq*" -and $retryCount -lt $maxRetries) {
                    Write-Warning "    Rate limited, waiting 20s... (retry $($retryCount+1)/$maxRetries)"
                    Start-Sleep -Seconds 20
                    $retryCount++
                    continue
                }
                Write-Warning "    API error: $($response.base_resp.err_msg)"
                break
            }
            
            $retryCount = 0  # Reset retry count on success
            $articles = $response.articles
            if ($articles -eq $null -or $articles.Count -eq 0) {
                break
            }
            
            $allArticles += $articles
            $pageCount++
            
            $begin += $articles.Count
            Start-Sleep -Milliseconds 600  # Moderate delay
            
        } catch {
            Write-Warning "    Error: $_"
            break
        }
    } while ($true)
    
    Write-Host "  Done: $AccountName - $($allArticles.Count) articles" -ForegroundColor Green
    return $allArticles
}

function Format-UnixTime {
    param([long]$timestamp)
    if ($timestamp -eq 0 -or $timestamp -eq $null) { return "N/A" }
    try {
        $dateTime = [System.DateTimeOffset]::FromUnixTimeSeconds($timestamp).LocalDateTime
        return $dateTime.ToString("yyyy-MM-dd")
    } catch {
        return "N/A"
    }
}

# Load existing results if any
$existingJson = "$OutputDir/wechat-sync-data.json"
$allResults = @()
if (Test-Path $existingJson) {
    $existing = Get-Content $existingJson | ConvertFrom-Json
    $allResults = $existing.accounts | ForEach-Object { $_ }
    Write-Host "Loaded $($allResults.Count) existing accounts" -ForegroundColor Gray
}

# Sync remaining accounts
Write-Host "=== Syncing $($Accounts.Count) remaining accounts ===" -ForegroundColor Yellow

foreach ($account in $Accounts) {
    try {
        $articles = Get-ArticlesForAccount -FakeId $account.FakeId -AccountName $account.Name
        
        $latestDate = "N/A"
        $earliestDate = "N/A"
        
        if ($articles.Count -gt 0) {
            $sorted = $articles | Sort-Object -Property { $_.create_time -as [long] } -Descending
            $latestDate = Format-UnixTime -timestamp ($sorted[0].create_time -as [long])
            $earliestDate = Format-UnixTime -timestamp ($sorted[-1].create_time -as [long])
        }
        
        $result = [PSCustomObject]@{
            name = $account.Name
            fakeid = $account.FakeId
            type = $account.Type
            total_count = $articles.Count
            latest_date = $latestDate
            earliest_date = $earliestDate
            status = "✅"
            articles = $articles | ForEach-Object {
                @{
                    title = $_.title
                    link = $_.link
                    create_time = $_.create_time
                    update_time = $_.update_time
                    aid = $_.aid
                }
            }
        }
        
        $allResults += $result
        
        # Save progress after each account
        $jsonData = @{
            sync_time = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
            auth_key = $AuthKey
            accounts = $allResults
        } | ConvertTo-Json -Depth 10
        $jsonData | Out-File -FilePath $existingJson -Encoding UTF8
        
        Start-Sleep -Seconds 3  # Delay between accounts
        
    } catch {
        Write-Warning "Failed to sync $($account.Name): $_"
    }
}

# Generate final report
$aClass = $allResults | Where-Object { $_.type -eq "A" }
$bClass = $allResults | Where-Object { $_.type -eq "B" }
$totalArticles = ($allResults | Measure-Object -Property total_count -Sum).Sum

$report = @"
# 公众号文章同步统计

同步时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
auth-key: $AuthKey

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
Generated by sync_remaining.ps1
"@

$reportPath = "$OutputDir/wechat-sync-stats.md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "=== Complete ===" -ForegroundColor Green
Write-Host "Total accounts: $($allResults.Count)" -ForegroundColor Green
Write-Host "Total articles: $totalArticles" -ForegroundColor Green
Write-Host "Report: $reportPath" -ForegroundColor Green
