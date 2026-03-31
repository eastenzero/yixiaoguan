param(
    [string]$InputCsv = "knowledge-base/raw/first-batch-material-index.csv",
    [string]$OutputRoot = "knowledge-base/raw/first-batch-processing"
)

$ErrorActionPreference = "Stop"

$markdownDir = Join-Path $OutputRoot "converted/markdown"
$tablesDir = Join-Path $OutputRoot "converted/tables"
$pdfDir = Join-Path $OutputRoot "converted/pdf"
$logDir = Join-Path $OutputRoot "logs"

$null = New-Item -ItemType Directory -Path $markdownDir -Force
$null = New-Item -ItemType Directory -Path $tablesDir -Force
$null = New-Item -ItemType Directory -Path $pdfDir -Force
$null = New-Item -ItemType Directory -Path $logDir -Force

function Get-SafeName {
    param([string]$Name)
    $safe = $Name
    [System.IO.Path]::GetInvalidFileNameChars() | ForEach-Object {
        $safe = $safe.Replace($_, "_")
    }
    return $safe
}

function Convert-DocToDocx {
    param(
        [string]$InputPath,
        [string]$OutputPath,
        $WordApp
    )
    $doc = $WordApp.Documents.Open($InputPath)
    try {
        $wdFormatXMLDocument = 16
        $doc.SaveAs([ref]$OutputPath, [ref]$wdFormatXMLDocument)
    }
    finally {
        $doc.Close()
    }
}

function Export-WorkbookSheetsToCsv {
    param(
        [string]$InputPath,
        [string]$OutputDir,
        $ExcelApp
    )

    $null = New-Item -ItemType Directory -Path $OutputDir -Force
    $workbook = $ExcelApp.Workbooks.Open($InputPath)
    $generated = @()
    try {
        foreach ($sheet in $workbook.Worksheets) {
            $sheetName = Get-SafeName $sheet.Name
            $csvPath = Join-Path $OutputDir ("$sheetName.csv")
            $sheet.Copy() | Out-Null
            $tempWb = $ExcelApp.ActiveWorkbook
            try {
                $xlCSVUTF8 = 62
                $tempWb.SaveAs($csvPath, $xlCSVUTF8)
                $generated += $csvPath
            }
            finally {
                $tempWb.Close($false)
            }
        }
    }
    finally {
        $workbook.Close($false)
    }
    return $generated
}

$rows = Import-Csv $InputCsv
$results = @()

$wordApp = $null
$excelApp = $null

if (($rows | Where-Object { $_.extension -ieq ".doc" }).Count -gt 0) {
    $wordApp = New-Object -ComObject Word.Application
    $wordApp.Visible = $false
}

if (($rows | Where-Object { $_.extension -ieq ".xls" -or $_.extension -ieq ".xlsx" }).Count -gt 0) {
    $excelApp = New-Object -ComObject Excel.Application
    $excelApp.Visible = $false
    $excelApp.DisplayAlerts = $false
}

try {
    foreach ($row in $rows) {
        $materialId = $row.material_id
        $sourcePath = $row.source_path
        $extension = $row.extension.ToLowerInvariant()
        $sourceAbsPath = (Resolve-Path $sourcePath).Path
        $safeBase = Get-SafeName ($row.file_name -replace "\.[^.]+$", "")

        $record = [ordered]@{
            material_id = $materialId
            source_path = $sourcePath
            extension = $extension
            status = "success"
            output_main = ""
            output_detail = ""
            error_type = ""
            error_message = ""
            converted_at = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
        }

        try {
            switch ($extension) {
                ".md" {
                    $outPath = Join-Path $markdownDir ("$materialId`__$safeBase.md")
                    $content = Get-Content -LiteralPath $sourceAbsPath -Raw
                    [System.IO.File]::WriteAllText((Resolve-Path (Split-Path $outPath -Parent)).Path + "\\" + (Split-Path $outPath -Leaf), $content, [System.Text.UTF8Encoding]::new($false))
                    $record.output_main = $outPath
                }
                ".docx" {
                    $outPath = Join-Path $markdownDir ("$materialId`__$safeBase.md")
                    pandoc -f docx -t gfm --wrap=none -o $outPath $sourceAbsPath
                    if ($LASTEXITCODE -ne 0) {
                        throw "pandoc_docx_failed"
                    }
                    $record.output_main = $outPath
                }
                ".doc" {
                    if ($null -eq $wordApp) {
                        throw "word_com_unavailable"
                    }
                    $tempDocx = Join-Path $markdownDir ("$materialId`__$safeBase.__converted.docx")
                    Convert-DocToDocx -InputPath $sourceAbsPath -OutputPath $tempDocx -WordApp $wordApp
                    $outPath = Join-Path $markdownDir ("$materialId`__$safeBase.md")
                    pandoc -f docx -t gfm --wrap=none -o $outPath $tempDocx
                    if ($LASTEXITCODE -ne 0) {
                        throw "pandoc_doc_failed"
                    }
                    $record.output_main = $outPath
                    $record.output_detail = $tempDocx
                }
                ".xlsx" {
                    if ($null -eq $excelApp) {
                        throw "excel_com_unavailable"
                    }
                    $sheetDir = Join-Path $tablesDir $materialId
                    $generated = Export-WorkbookSheetsToCsv -InputPath $sourceAbsPath -OutputDir $sheetDir -ExcelApp $excelApp
                    $record.output_main = $sheetDir
                    $record.output_detail = ($generated -join ";")
                }
                ".xls" {
                    if ($null -eq $excelApp) {
                        throw "excel_com_unavailable"
                    }
                    $sheetDir = Join-Path $tablesDir $materialId
                    $generated = Export-WorkbookSheetsToCsv -InputPath $sourceAbsPath -OutputDir $sheetDir -ExcelApp $excelApp
                    $record.output_main = $sheetDir
                    $record.output_detail = ($generated -join ";")
                }
                ".pdf" {
                    $materialPdfDir = Join-Path $pdfDir $materialId
                    $null = New-Item -ItemType Directory -Path $materialPdfDir -Force
                    python scripts/mineru_api_extract.py --input "$sourceAbsPath" --output-dir "$materialPdfDir"
                    if ($LASTEXITCODE -ne 0) {
                        throw "mineru_api_failed"
                    }
                    $record.output_main = $materialPdfDir
                }
                default {
                    $record.status = "skipped"
                    $record.output_detail = "unsupported_extension"
                }
            }
        }
        catch {
            $record.status = "failed"
            $record.error_type = $_.Exception.GetType().Name
            $record.error_message = $_.Exception.Message
        }

        $results += [PSCustomObject]$record
    }
}
finally {
    if ($null -ne $wordApp) {
        $wordApp.Quit()
    }
    if ($null -ne $excelApp) {
        $excelApp.Quit()
    }
}

$logPath = Join-Path $logDir "conversion-log.csv"
$results | Export-Csv -Path $logPath -NoTypeInformation -Encoding UTF8
Write-Output "conversion_log=$logPath"
