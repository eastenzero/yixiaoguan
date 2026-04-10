#requires -Version 5.1
<#
.SYNOPSIS
    Sync WeChat articles from a single account
.PARAMETER FakeId
    The fakeid of the account
.PARAMETER AccountName
    The name of the account
.PARAMETER Type
    A or B class
#>
param(
    [Parameter(Mandatory=$true)]
    [string]$FakeId,
    
    [Parameter(Mandatory=$true)]
    [string]$AccountName,
    
    [Parameter(Mandatory=$true)]
    [string]$Type
)

$ErrorActionPreference = "Stop"
$BaseUrl = "http://localhost:3000"
$AuthKey = "b982b119ba0744358c1dbcd6711c06fe"

function Get-ArticlesForAccount {
    param(
        [string]$FakeId,
        [string]$AccountName
    )
    
    $allArticles = @()
    $begin = 0
    $pageSize = 20
    $pageCount = 0
    
    Write-Host "Fetching articles for: $AccountName" -ForegroundColor Cyan
    
    do {
        $url = "$BaseUrl/api/public/v1/article?fakeid=$FakeId&begin=$begin&count=$pageSize"
        try {
            $response = curl.exe -s -H "X-Auth-Key: $AuthKey" $url | ConvertFrom-Json
            
            if ($response.base_resp.ret -ne 0) {
                if ($response.base_resp.err_msg -like "*freq*") {
                    Write-Warning "Rate limited (freq control). Waiting 30 seconds..."
                    Start-Sleep -Seconds 30
                    continue  # Retry same page
                }
                Write-Warning "API error: $($response.base_resp.err_msg)"
                break
            }
            
            $articles = $response.articles
            if ($articles -eq $null -or $articles.Count -eq 0) {
                break
            }
            
            $allArticles += $articles
            $pageCount++
            Write-Host "  Page $pageCount`: Got $($articles.Count) articles (total: $($allArticles.Count))" -ForegroundColor Gray
            
            $begin += $articles.Count
            Start-Sleep -Milliseconds 800  # Moderate rate limiting
            
        } catch {
            Write-Warning "Error fetching page: $_"
            break
        }
    } while ($true)
    
    Write-Host "Completed: $AccountName - Total: $($allArticles.Count) articles" -ForegroundColor Green
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
$articles = Get-ArticlesForAccount -FakeId $FakeId -AccountName $AccountName

$latestDate = "N/A"
$earliestDate = "N/A"

if ($articles.Count -gt 0) {
    $sorted = $articles | Sort-Object -Property { $_.create_time -as [long] } -Descending
    $latestDate = Format-UnixTime -timestamp ($sorted[0].create_time -as [long])
    $earliestDate = Format-UnixTime -timestamp ($sorted[-1].create_time -as [long])
}

$result = [PSCustomObject]@{
    Name = $AccountName
    FakeId = $FakeId
    Type = $Type
    TotalCount = $articles.Count
    LatestDate = $latestDate
    EarliestDate = $earliestDate
    Articles = $articles
}

# Save individual result
$outputFile = "kimi/sync-result-$($AccountName -replace '[^\w]', '-').json"
$result | Select-Object -Property Name, FakeId, Type, TotalCount, LatestDate, EarliestDate | ConvertTo-Json | Out-File -FilePath $outputFile -Encoding UTF8

Write-Host ""
Write-Host "Result saved to: $outputFile" -ForegroundColor Green
Write-Host "Total articles: $($articles.Count)" -ForegroundColor Green

# Return the result
return $result
