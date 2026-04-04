import csv
from pathlib import Path

p = Path('C:/Users/Administrator/Documents/code/yixiaoguan/knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv')
with p.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# 检查 queue_seq 1-7 的当前状态
for r in rows:
    qs = r['queue_seq']
    if qs in ('1','2','3','4','5','6','7'):
        print(f"queue_seq={qs}, material_id={r['material_id']}, kb_draft_id={r['kb_draft_id']}, status={r['status']}")

print('---')
# 检查 queue_seq 8-12
for r in rows:
    qs = r['queue_seq']
    if qs in ('8','9','10','11','12'):
        print(f"queue_seq={qs}, source_type={r['source_type']}, file_name={r['file_name']}, status={r['status']}")
