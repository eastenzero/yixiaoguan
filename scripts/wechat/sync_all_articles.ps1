#requires -Version 5.1
<#
.SYNOPSIS
    Sync WeChat articles from all A/B class accounts
.DESCRIPTION
    Fetches article lists via API with pagination, generates stats report
#>

$ErrorActionPreference = "Stop"
$BaseUrl = "http://localhost:3000"
$AuthKey = "b982b119ba0744358c1dbcd6711c06fe"
$OutputDir = "kimi"

# Account definitions
$AClassAccounts = @(
    @{ Name = "山东第一医科大学教务部"; FakeId = "Mzg3ODMyNjg1Nw=="; Type = "A" },
    @{ Name = "山东第一医科大学研究生处"; FakeId = "Mzg5MTY0Njg2NA=="; Type = "A" },
    @{ Name = "山一大学工"; FakeId = "Mzg5MDc2MDMwNA=="; Type = "A" },
    @{ Name = "山一大后勤"; FakeId = "Mzg5NTQyMzg4NQ=="; Type = "A" },
    @{ Name = "山一大 心理健康教育中心"; FakeId = "MzkxNzU2NTQxMg=="; Type = "A" },
    @{ Name = "山东第一医科大学图书馆"; FakeId = "MzU1OTI5MzIwNA=="; Type = "A" },
    @{ Name = "山东第一医科大学就业"; FakeId = "MzkwMDQxNDA2Nw=="; Type = "A" },
    @{ Name = "山东第一医科大学科研部"; FakeId = "MzkzOTE5OTI5Mg=="; Type = "A" }
)

$BClassAccounts = @(
    @{ Name = "山东第一医科大学 山东省医学科学院"; FakeId = "MjM5NjA2NjcyMg=="; Type = "B" },
    @{ Name = "山一大招生办"; FakeId = "MzAxNzYyMzM1OA=="; Type = "B" },
    @{ Name = "青春山一大"; FakeId = "MzIyMTA3MDc4OA=="; Type = "B" },
    @{ Name = "山东第一医科大学医药管理学院"; FakeId = "Mzg2NTY5ODAwNA=="; Type = "B" },
    @{ Name = "山东第一医科大学科创中心"; FakeId = "Mzg3NDcwOTc0Mw=="; Type = "B" },
    @{ Name = "山一大饮食"; FakeId = "MzkxOTU2MTMyNg=="; Type = "B" },
    @{ Name = "山东第一医科大学对外合作交流部"; FakeId = "Mzg2MzYwNDM0MQ=="; Type = "B" },
    @{ Name = "山东第一医科大学计划财务处"; FakeId = "Mzg4NDUxNDU1OA=="; Type = "B" }
)

$AllAccounts = $AClassAccounts + $BClassAccounts

function Get-ArticlesForAccount {
    param(
        [string]$FakeId,
        [string]$AccountName
    )
    
    $allArticles = @()
    $begin = 0
    $pageSize = 20
    $pageCount = 0
    
    Write-Host "  Fetching articles for: $AccountName" -ForegroundColor Cyan
    
    do {
        $url = "$BaseUrl/api/public/v1/article?fakeid=$FakeId&begin=$begin&count=$pageSize"
        try {
            $response = curl.exe -s -H "X-Auth-Key: $AuthKey" $url | ConvertFrom-Json
            
            if ($response.base_resp.ret -ne 0) {
                Write-Warning "    API error: $($response.base_resp.err_msg)"
                break
            }
            
            $articles = $response.articles
            if ($articles -eq $null -or $articles.Count -eq 0) {
                break
            }
            
            $allArticles += $articles
            $pageCount++
            Write-Host "    Page $pageCount`: Got $($articles.Count) articles (total: $($allArticles.Count))" -ForegroundColor Gray
            
            # Continue to next page - API doesn't always fill pageSize even if more exist
            $begin += $articles.Count
            Start-Sleep -Seconds 3  # Rate limiting - be gentle to avoid freq control
            
        } catch {
            Write-Warning "    Error fetching page: $_"
            break
        }
    } while ($true)
    
    Write-Host "  Completed: $AccountName - Total: $($allArticles.Count) articles" -ForegroundColor Green
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

# Main execution
Write-Host "=== WeChat Article Sync ===" -ForegroundColor Yellow
Write-Host "Accounts to sync: $($AllAccounts.Count)" -ForegroundColor Yellow
Write-Host ""

$results = @()
$successCount = 0
$failCount = 0

foreach ($account in $AllAccounts) {
    try {
        $articles = Get-ArticlesForAccount -FakeId $account.FakeId -AccountName $account.Name
        
        $latestDate = "N/A"
        $earliestDate = "N/A"
        
        if ($articles.Count -gt 0) {
            # Sort by create_time to find latest and earliest
            $sorted = $articles | Sort-Object -Property { $_.create_time -as [long] } -Descending
            $latestDate = Format-UnixTime -timestamp ($sorted[0].create_time -as [long])
            $earliestDate = Format-UnixTime -timestamp ($sorted[-1].create_time -as [long])
        }
        
        $result = [PSCustomObject]@{
            Name = $account.Name
            FakeId = $account.FakeId
            Type = $account.Type
            TotalCount = $articles.Count
            LatestDate = $latestDate
            EarliestDate = $earliestDate
            Status = "✅"
            Articles = $articles  # Store for potential later use
        }
        
        $results += $result
        $successCount++
        Start-Sleep -Seconds 5  # Delay between accounts to avoid rate limiting
    } catch {
        Write-Warning "Failed to sync $($account.Name): $_"
        $results += [PSCustomObject]@{
            Name = $account.Name
            FakeId = $account.FakeId
            Type = $account.Type
            TotalCount = 0
            LatestDate = "N/A"
            EarliestDate = "N/A"
            Status = "❌ Failed"
            Articles = @()
        }
        $failCount++
    }
    
    Write-Host ""
}

# Generate Markdown report
$report = @"
# 公众号文章同步统计

同步时间: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
auth-key: $AuthKey

## 汇总

| 分类 | 账号数 | 文章总数 |
|------|--------|----------|
| A 类 | $($results | Where-Object { $_.Type -eq "A" } | Measure-Object | Select-Object -ExpandProperty Count) | $($results | Where-Object { $_.Type -eq "A" } | Measure-Object -Property TotalCount -Sum | Select-Object -ExpandProperty Sum) |
| B 类 | $($results | Where-Object { $_.Type -eq "B" } | Measure-Object | Select-Object -ExpandProperty Count) | $($results | Where-Object { $_.Type -eq "B" } | Measure-Object -Property TotalCount -Sum | Select-Object -ExpandProperty Sum) |
| 合计 | $($results.Count) | $($results | Measure-Object -Property TotalCount -Sum | Select-Object -ExpandProperty Sum) |

## A 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
"@

foreach ($r in ($results | Where-Object { $_.Type -eq "A" })) {
    $shortName = $r.Name -replace "山东第一医科大学", "山一大"
    $report += "| $($shortName) | $($r.FakeId) | $($r.TotalCount) | $($r.LatestDate) | $($r.EarliestDate) | $($r.Status) |`n"
}

$report += @"

## B 类账号

| 公众号 | fakeid | 文章总数 | 最新文章日期 | 最早文章日期 | 状态 |
|--------|--------|---------|------------|------------|------|
"@

foreach ($r in ($results | Where-Object { $_.Type -eq "B" })) {
    $shortName = $r.Name -replace "山东第一医科大学", "山一大"
    $report += "| $($shortName) | $($r.FakeId) | $($r.TotalCount) | $($r.LatestDate) | $($r.EarliestDate) | $($r.Status) |`n"
}

$report += @"

## 同步详情

成功: $successCount / $($AllAccounts.Count)
失败: $failCount / $($AllAccounts.Count)

---
Generated by sync_all_articles.ps1
"@

# Save report
$reportPath = "$OutputDir/wechat-sync-stats.md"
$report | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host ""
Write-Host "=== Sync Complete ===" -ForegroundColor Green
Write-Host "Report saved to: $reportPath" -ForegroundColor Green
Write-Host "Success: $successCount, Failed: $failCount" -ForegroundColor $(if ($failCount -eq 0) { "Green" } else { "Yellow" })

# Also save raw data as JSON for later processing
$jsonPath = "$OutputDir/wechat-sync-data.json"
$jsonData = @{
    sync_time = (Get-Date -Format "yyyy-MM-ddTHH:mm:ss")
    auth_key = $AuthKey
    accounts = $results | ForEach-Object {
        @{
            name = $_.Name
            fakeid = $_.FakeId
            type = $_.Type
            total_count = $_.TotalCount
            latest_date = $_.LatestDate
            earliest_date = $_.EarliestDate
            status = $_.Status
            articles = $_.Articles | ForEach-Object {
                @{
                    title = $_.title
                    link = $_.link
                    create_time = $_.create_time
                    update_time = $_.update_time
                    aid = $_.aid
                }
            }
        }
    }
} | ConvertTo-Json -Depth 10

$jsonData | Out-File -FilePath $jsonPath -Encoding UTF8
Write-Host "Raw data saved to: $jsonPath" -ForegroundColor Gray
