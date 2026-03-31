param(
    [Parameter(Mandatory = $true)]
    [string]$MaterialId,

    [Parameter(Mandatory = $true)]
    [string]$SourcePath,

    [Parameter(Mandatory = $true)]
    [string]$OutputMarkdownPath,

    [string]$TempDir = "knowledge-base\raw\first-batch-processing\logs\doc-temp",
    [string]$WordconvPath = "C:\Program Files\Microsoft Office\root\Office16\Wordconv.exe"
)

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$root = (Resolve-Path ".").Path
$fullSourcePath = Join-Path $root $SourcePath
$fullTempDir = Join-Path $root $TempDir
$fullOutputMarkdownPath = Join-Path $root $OutputMarkdownPath

New-Item -ItemType Directory -Force -Path $fullTempDir | Out-Null
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $fullOutputMarkdownPath) | Out-Null

$asciiDocPath = Join-Path $fullTempDir "$MaterialId.doc"
$asciiDocxPath = Join-Path $fullTempDir "$MaterialId.docx"

if (!(Test-Path -LiteralPath $fullSourcePath)) {
    throw "Source file not found: $fullSourcePath"
}

if (!(Test-Path -LiteralPath $WordconvPath)) {
    throw "Wordconv.exe not found: $WordconvPath"
}

if (Test-Path -LiteralPath $asciiDocPath) {
    Remove-Item -LiteralPath $asciiDocPath -Force
}
if (Test-Path -LiteralPath $asciiDocxPath) {
    Remove-Item -LiteralPath $asciiDocxPath -Force
}
if (Test-Path -LiteralPath $fullOutputMarkdownPath) {
    Remove-Item -LiteralPath $fullOutputMarkdownPath -Force
}

Write-Host "[1/6] Copy source to ASCII temp path"
Copy-Item -LiteralPath $fullSourcePath -Destination $asciiDocPath -Force

Write-Host "[2/6] Convert DOC to DOCX with Wordconv.exe"
& $WordconvPath -oice -nme $asciiDocPath $asciiDocxPath | Out-Null

if (!(Test-Path -LiteralPath $asciiDocxPath)) {
    throw "Wordconv.exe did not create DOCX: $asciiDocxPath"
}

Write-Host "[3/6] Verify DOCX output"
Get-Item -LiteralPath $asciiDocxPath | Select-Object Name,Length,LastWriteTime | Format-Table -AutoSize

Write-Host "[4/6] Run pandoc"
& pandoc -f docx -t gfm --wrap=none -o $fullOutputMarkdownPath $asciiDocxPath
if ($LASTEXITCODE -ne 0) {
    throw "pandoc failed with exit code $LASTEXITCODE"
}

Write-Host "[5/6] Verify Markdown output"
Get-Item -LiteralPath $fullOutputMarkdownPath | Select-Object Name,Length,LastWriteTime | Format-Table -AutoSize

Write-Host "[6/6] Done"
[PSCustomObject]@{
    material_id = $MaterialId
    source_path = $SourcePath
    temp_doc = $asciiDocPath
    temp_docx = $asciiDocxPath
    output_markdown = $fullOutputMarkdownPath
    converter = "Wordconv.exe + pandoc"
} | ConvertTo-Json -Compress
