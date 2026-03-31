from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path('.')
CANDIDATE_PATH = ROOT / 'knowledge-base/raw/first-batch-processing/manifests/first-batch-candidate-knowledge-list.csv'
CLEANED_PATH = ROOT / 'knowledge-base/raw/first-batch-processing/manifests/first-batch-material-index.cleaned.csv'
OUT_PATH = ROOT / 'knowledge-base/raw/first-batch-processing/manifests/first-batch-rule-extraction-draft.csv'

with CANDIDATE_PATH.open('r', encoding='utf-8-sig', newline='') as f:
    candidate_rows = list(csv.DictReader(f))

with CLEANED_PATH.open('r', encoding='utf-8-sig', newline='') as f:
    cleaned_rows = list(csv.DictReader(f))

cleaned_map = {row['material_id']: row for row in cleaned_rows}

fieldnames = [
    'draft_id',
    'material_id',
    'candidate_question',
    'knowledge_category',
    'audience',
    'priority',
    'source_path',
    'conversion_path',
    'processing_action',
    'extract_scope',
    'extraction_status',
    'needs_manual_review',
    'notes',
]

rows: list[dict[str, str]] = []

for idx, cand in enumerate(candidate_rows, start=1):
    material_id = cand['material_id']
    cleaned = cleaned_map.get(material_id, {})
    conversion_path = cleaned.get('conversion_path', '')
    processing_action = cleaned.get('processing_action', '')
    material_type = cleaned.get('material_type', '')
    timeliness = cleaned.get('timeliness', '')
    is_template = cleaned.get('is_template', '')

    if is_template == '是' or processing_action == '提炼规则后入库':
        extract_scope = '仅抽取稳定规则，模板正文保留附件'
    elif processing_action == '可转知识':
        extract_scope = '抽取条件、流程、材料、时限、注意事项'
    else:
        extract_scope = '待人工判断后决定是否抽取'

    if cand['priority'] == 'P0':
        extraction_status = 'ready_p0'
    elif cand['priority'] == 'P1':
        extraction_status = 'ready_p1'
    else:
        extraction_status = 'ready_p2'

    needs_manual_review = '是' if timeliness in {'待确认', '过期'} else '否'

    note_parts = []
    if timeliness:
        note_parts.append(f'时效={timeliness}')
    if material_type:
        note_parts.append(f'材料类型={material_type}')
    if cleaned.get('is_duplicate') == '是':
        note_parts.append(f"主参考={cleaned.get('primary_reference', '')}")
    if is_template == '是':
        note_parts.append('模板材料仅提炼规则')

    rows.append(
        {
            'draft_id': f'REX-20260323-{idx:04d}',
            'material_id': material_id,
            'candidate_question': cand['candidate_question'],
            'knowledge_category': cand['knowledge_category'],
            'audience': cand['audience'],
            'priority': cand['priority'],
            'source_path': cand['source_path'],
            'conversion_path': conversion_path,
            'processing_action': processing_action,
            'extract_scope': extract_scope,
            'extraction_status': extraction_status,
            'needs_manual_review': needs_manual_review,
            'notes': '；'.join(note_parts),
        }
    )

with OUT_PATH.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(str(OUT_PATH))
print(f'rows={len(rows)}')
