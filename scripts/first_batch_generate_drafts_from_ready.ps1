param(
    [string]$ReadyCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-ready.csv",
    [string]$QueueCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-queue.csv",
    [string]$FillCsv = "knowledge-base/raw/first-batch-processing/manifests/first-batch-entry-draft-fill-progress.csv",
    [string]$DraftRoot = "knowledge-base/entries/first-batch-drafts"
)

$ErrorActionPreference = "Stop"

$ready = Import-Csv $ReadyCsv
$queue = Import-Csv $QueueCsv
$fill = Import-Csv $FillCsv

$queuedTaskMap = @{}
$maxEntryNo = 0

foreach ($q in $queue) {
    $queuedTaskMap[$q.task_id] = $true
    if ($q.entry_id -match 'KB-\d{8}-(\d{4})') {
        $n = [int]$Matches[1]
        if ($n -gt $maxEntryNo) {
            $maxEntryNo = $n
        }
    }
}

$newRows = @()
$newFillRows = @()

foreach ($r in $ready) {
    if ($queuedTaskMap.ContainsKey($r.task_id)) {
        continue
    }

    $maxEntryNo += 1
    $entryId = ('KB-20260324-{0:D4}' -f $maxEntryNo)
    $entryPath = "$DraftRoot/$entryId.md"
    $entryAbs = Join-Path (Get-Location).Path $entryPath

    New-Item -ItemType Directory -Path (Split-Path -Parent $entryAbs) -Force | Out-Null

    $content = @"
---
title: "$($r.rule_title)"
category: "$($r.knowledge_category)"
audience: "$($r.audience)"
source_files:
  - "$($r.source_path)"
material_id: "$($r.material_id)"
rule_task_id: "$($r.task_id)"
status: "draft"
---

## 问题概述
$($r.candidate_question)

## 标准答复
$($r.rule_title)在满足触发条件后，应按既定办理流程执行，并重点核对办理条件、材料完整性与时间节点要求。

## 办理条件
$($r.eligibility)

## 所需材料
$($r.required_materials)

## 办理流程
$($r.process_steps)

## 时间节点
$($r.time_limits)

## 注意事项
$($r.exceptions)

## 依据与证据
$($r.evidence_quote)
"@

    Set-Content -Path $entryAbs -Value $content -Encoding UTF8

    $newRows += [PSCustomObject]@{
        entry_id = $entryId
        task_id = $r.task_id
        draft_id = $r.draft_id
        material_id = $r.material_id
        knowledge_category = $r.knowledge_category
        audience = $r.audience
        candidate_question = $r.candidate_question
        source_path = $r.source_path
        rule_title = $r.rule_title
        extraction_status = $r.status
        review_result = $r.review_result
        entry_path = $entryPath
        draft_status = "drafted"
    }

    $newFillRows += [PSCustomObject]@{
        entry_id = $entryId
        task_id = $r.task_id
        file_path = $entryPath
        fill_status = "filled"
        notes = "第二批扩量已完成自动填充并待抽样复核"
    }
}

$queueOut = @($queue + $newRows)
$queueOut | Export-Csv -Path $QueueCsv -NoTypeInformation -Encoding UTF8

$fillOut = @($fill + $newFillRows)
$fillOut | Export-Csv -Path $FillCsv -NoTypeInformation -Encoding UTF8

Write-Output "new_drafts=$($newRows.Count)"
Write-Output "queue_total=$($queueOut.Count)"
Write-Output "fill_total=$($fillOut.Count)"
