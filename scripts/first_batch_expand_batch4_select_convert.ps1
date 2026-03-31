param(
    [string]$CandidatePoolCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-candidate-pool.csv",
    [string]$MaterialIndexCsv = "knowledge-base/raw/first-batch-material-index.csv",
    [string]$ConversionLogCsv = "knowledge-base/raw/first-batch-processing/logs/conversion-log.csv",
    [string]$CleanedCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-material-index.cleaned.csv",
    [string]$BlockersCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-conversion-blockers.csv",
    [string]$BatchMaterialCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-expansion-batch4-materials.csv",
    [int]$BatchSize = 24
)

$ErrorActionPreference = "Stop"

function Get-NextMaterialId {
    param([int]$Seq)
    return ('MAT-20260324-{0:D4}' -f $Seq)
}

$indexRows = Import-Csv $MaterialIndexCsv
$poolRows = Import-Csv $CandidatePoolCsv

$existingPathMap = @{}
$maxSeq = 0
foreach ($r in $indexRows) {
    $existingPathMap[$r.source_path] = $true
    if ($r.material_id -match '^MAT-20260324-(\d{4})$') {
        $n = [int]$Matches[1]
        if ($n -gt $maxSeq) {
            $maxSeq = $n
        }
    }
}

$categoryOrder = @{
    "入学与学籍" = 1
    "奖助贷补" = 2
    "就业与毕业" = 3
    "心理与测评" = 4
    "证件与校园服务" = 5
    "竞赛与第二课堂" = 6
    "事务申请与审批" = 7
}

$badTitlePattern = '发言|寄语|名单|统计|汇总|封皮|目录|典型|倡议书|会务手册|分组|联系|巡考'

$candidates = $poolRows |
    Where-Object {
        -not $existingPathMap.ContainsKey($_.source_path) -and
        $_.value_level -in @('A', 'B') -and
        $_.extension -eq '.docx' -and
        $_.knowledge_category -in @('入学与学籍','奖助贷补','就业与毕业','心理与测评','证件与校园服务','竞赛与第二课堂','事务申请与审批') -and
        $_.title_guess -notmatch $badTitlePattern
    } |
    Sort-Object `
        @{ Expression = { if ($_.processing_action -eq '可转知识') { 0 } else { 1 } } }, `
        @{ Expression = { if ($categoryOrder.ContainsKey($_.knowledge_category)) { $categoryOrder[$_.knowledge_category] } else { 99 } } }, `
        @{ Expression = { $_.source_path } }

$selected = $candidates | Select-Object -First $BatchSize

if ($selected.Count -eq 0) {
    Write-Output "selected_rows=0"
    exit 0
}

$newMaterialRows = @()
foreach ($s in $selected) {
    $maxSeq += 1
    $mid = Get-NextMaterialId -Seq $maxSeq

    $audience = '全体学生'
    if ($s.source_path -match '新生') { $audience = '新生' }
    elseif ($s.source_path -match '毕业') { $audience = '毕业生' }
    elseif ($s.source_path -match '学生') { $audience = '学生' }

    $sourceDir = '模板'
    if ($s.source_path -match '/2025年工作/') { $sourceDir = '2025年工作' }

    $subDir = ''
    if ($s.source_path -match '2025下-25级新生工作') { $subDir = '2025下-25级新生工作' }
    elseif ($s.source_path -match '2025上-21级毕业工作') { $subDir = '2025上-21级毕业工作' }

    $materialType = '通知'
    if ($s.title_guess -match '操作说明|手册|指南|步骤') { $materialType = '操作手册' }
    elseif ($s.title_guess -match '细则|办法|要点') { $materialType = '制度' }
    elseif ($s.title_guess -match '申请表|承诺书|登记表|知情同意书') { $materialType = '模板' }

    $isTemplate = '否'
    if ($s.processing_action -eq '提炼规则后入库') { $isTemplate = '是' }

    $newMaterialRows += [PSCustomObject]@{
        material_id = $mid
        source_path = $s.source_path
        file_name = $s.file_name
        extension = $s.extension
        source_dir = $sourceDir
        sub_dir = $subDir
        title_guess = $s.title_guess
        year_label = '2025'
        audience = $audience
        knowledge_category = $s.knowledge_category
        material_type = $materialType
        value_level = 'B'
        timeliness = $s.timeliness
        is_template = $isTemplate
        is_duplicate = '否'
        primary_reference = $mid
        processing_action = $s.processing_action
        notes = '第4批扩量自动筛选'
    }
}

$newMaterialRows | Export-Csv -Path $BatchMaterialCsv -NoTypeInformation -Encoding UTF8

$mergedIndex = @($indexRows + $newMaterialRows)
$mergedIndex | Export-Csv -Path $MaterialIndexCsv -NoTypeInformation -Encoding UTF8

$logRows = Import-Csv $ConversionLogCsv
$logMap = @{}
foreach ($l in $logRows) {
    $logMap[$l.material_id] = $l
}

$ok = 0
$fail = 0

foreach ($r in $newMaterialRows) {
    $sourceAbs = Join-Path (Get-Location).Path ($r.source_path -replace '/', '\')
    $safeBase = ($r.file_name -replace '\.[^.]+$', '')
    [System.IO.Path]::GetInvalidFileNameChars() | ForEach-Object {
        $safeBase = $safeBase.Replace($_, '_')
    }

    $outRel = "knowledge-base/raw/first-batch-processing/converted/markdown/$($r.material_id)`__$safeBase.md"
    $outAbs = Join-Path (Get-Location).Path $outRel
    New-Item -ItemType Directory -Path (Split-Path -Parent $outAbs) -Force | Out-Null

    $record = [ordered]@{
        material_id = $r.material_id
        source_path = $r.source_path
        extension = $r.extension
        status = 'success'
        output_main = ($outRel -replace '/', '\')
        output_detail = ''
        error_type = ''
        error_message = ''
        converted_at = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss')
    }

    try {
        & pandoc -f docx -t gfm --wrap=none -o $outAbs $sourceAbs
        if ($LASTEXITCODE -ne 0) {
            throw "pandoc_exit_$LASTEXITCODE"
        }
        $ok += 1
    }
    catch {
        $record.status = 'failed'
        $record.error_type = $_.Exception.GetType().Name
        $record.error_message = $_.Exception.Message
        $fail += 1
    }

    $logMap[$r.material_id] = [PSCustomObject]$record
}

$mergedLog = $logMap.Values | Sort-Object material_id
$mergedLog | Export-Csv -Path $ConversionLogCsv -NoTypeInformation -Encoding UTF8

$conversionMap = @{}
foreach ($c in $mergedLog) {
    $conversionMap[$c.material_id] = $c
}

$cleanedRows = @()
foreach ($r in $mergedIndex) {
    $c = $null
    if ($conversionMap.ContainsKey($r.material_id)) {
        $c = $conversionMap[$r.material_id]
    }

    $cleanedRows += [PSCustomObject]@{
        material_id = $r.material_id
        source_path = $r.source_path
        file_name = $r.file_name
        extension = $r.extension
        source_dir = $r.source_dir
        sub_dir = $r.sub_dir
        title_guess = $r.title_guess
        year_label = $r.year_label
        audience = $r.audience
        knowledge_category = $r.knowledge_category
        material_type = $r.material_type
        value_level = $r.value_level
        timeliness = $r.timeliness
        is_template = $r.is_template
        is_duplicate = $r.is_duplicate
        primary_reference = $r.primary_reference
        processing_action = $r.processing_action
        notes = $r.notes
        conversion_status = $(if ($null -ne $c) { $c.status } else { 'not_run' })
        conversion_path = $(if ($null -ne $c) { $c.output_main } else { '' })
        conversion_error_type = $(if ($null -ne $c) { $c.error_type } else { '' })
        conversion_error_message = $(if ($null -ne $c) { $c.error_message } else { '' })
    }
}

$cleanedRows | Export-Csv -Path $CleanedCsv -NoTypeInformation -Encoding UTF8

$historyResolved = @()
if (Test-Path $BlockersCsv) {
    $historyResolved = Import-Csv $BlockersCsv | Where-Object { $_.blocker_status -eq 'resolved' }
}

$openBlockers = @()
foreach ($r in $cleanedRows | Where-Object { $_.conversion_status -eq 'failed' }) {
    $openBlockers += [PSCustomObject]@{
        material_id = $r.material_id
        source_path = $r.source_path
        stage = 'conversion'
        error_type = $r.conversion_error_type
        error_message = $r.conversion_error_message
        impact_scope = '该材料转换失败，无法进入规则抽取'
        fallback_plan = 'doc按ASCII+Wordconv+pandoc，pdf重跑提取，docx重跑pandoc'
        blocker_status = 'open'
        resolution_notes = ''
        resolved_at = ''
    }
}

$mergedBlockers = @($historyResolved + $openBlockers)
$mergedBlockers | Export-Csv -Path $BlockersCsv -NoTypeInformation -Encoding UTF8

Write-Output "selected_rows=$($newMaterialRows.Count)"
Write-Output "convert_ok=$ok"
Write-Output "convert_fail=$fail"
Write-Output "material_index_rows=$($mergedIndex.Count)"
Write-Output "conversion_log_rows=$($mergedLog.Count)"
Write-Output "cleaned_rows=$($cleanedRows.Count)"
Write-Output "blockers_open=$($openBlockers.Count)"
