import csv
p = r'C:\Users\Administrator\Documents\code\yixiaoguan\knowledge-base\raw\first-batch-processing\manifests\batch-a1-award-aid-queue.csv'
with open(p, 'r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    for r in reader:
        if r['queue_seq'] in ('1','2','3','4','5','6','7','8','9','10','11','12'):
            print(f"seq={r['queue_seq']}, mid={r['material_id']}, kb={r['kb_draft_id']}, status={r['status']}")
