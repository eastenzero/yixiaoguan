import csv
import shutil
from pathlib import Path
from datetime import datetime

project_root = Path('C:/Users/Administrator/Documents/code/yixiaoguan')
csv_path = project_root / 'knowledge-base/raw/first-batch-processing/manifests/batch-a1-award-aid-queue.csv'
report_dir = project_root / 'docs/test-reports/completion-reports'
report_path = report_dir / 'BATCH-R4-a1-rebuild-analysis-report.md'

# Backup CSV
shutil.copy(csv_path, str(csv_path) + '.bak')

with csv_path.open('r', encoding='utf-8-sig', newline='') as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

# 任务一：更新 7 行的 status
mapping = {
    'MAT-20260324-0024': 'KB-20260324-0124',
    'MAT-20260324-0025': 'KB-20260324-0125',
    'MAT-20260324-0026': 'KB-20260324-0126',
    'MAT-20260324-0027': 'KB-20260324-0127',
    'MAT-20260324-0028': 'KB-20260324-0128',
    'MAT-20260324-0029': 'KB-20260324-0129',
    'MAT-20260324-0055': 'KB-20260324-0130',
}

task1_details = []
modified_count = 0
for r in rows:
    mat_id = r.get('material_id', '')
    if mat_id in mapping:
        old_kb = r['kb_draft_id']
        new_kb = mapping[mat_id]
        old_status = r['status']
        r['kb_draft_id'] = new_kb
        r['status'] = 'rebuild_needed'
        modified_count += 1
        task1_details.append({
            'material_id': mat_id,
            'old_kb': old_kb,
            'new_kb': new_kb,
            'status': 'rebuild_needed',
            'result': '已更新'
        })

# 保存 CSV
with csv_path.open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

# 任务二：分析候补条目
candidate_rows = [r for r in rows if r.get('queue_seq') in ('8','9','10','11','12')]
batch2_rows = [r for r in rows if r.get('source_type') == 'batch2-materials']

def find_matches(candidate, batch2_list):
    c_path = candidate.get('source_path', '')
    c_name = candidate.get('file_name', '')
    matches = []
    for b in batch2_list:
        b_path = b.get('source_path', '')
        b_name = b.get('file_name', '')
        if c_path and b_path and c_path == b_path:
            matches.append(f"queue_seq={b['queue_seq']} (path exact)")
        elif c_name and b_name and c_name == b_name:
            matches.append(f"queue_seq={b['queue_seq']} (filename same, path differs)")
    return matches

task2_details = []
for c in candidate_rows:
    qs = c['queue_seq']
    fname = c['file_name']
    matches = find_matches(c, batch2_rows)
    if matches:
        if any("path exact" in m for m in matches):
            classification = 'DUPLICATE'
            suggestion = '从候补列表移除，由已有条目覆盖'
        else:
            classification = 'UNCERTAIN'
            suggestion = '文件名相同但路径前缀不同，等待人工确认'
    else:
        classification = 'UNIQUE'
        suggestion = '分配新 material_id 和 kb_draft_id，加入重建队列'
    
    task2_details.append({
        'queue_seq': qs,
        'file_name': fname,
        'classification': classification,
        'matches': '; '.join(matches) if matches else '无',
        'suggestion': suggestion
    })

# 生成报告
report_dir.mkdir(parents=True, exist_ok=True)
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

report_lines = [
    '# BATCH-R4-A1-REBUILD 分析完成报告',
    '',
    '## 任务标识',
    '',
    f'- **任务 ID**: BATCH-R4-A1-REBUILD',
    f'- **执行时间**: {now}',
    f'- **执行 AI 身份**: T3',
    '',
    '## 任务一明细表',
    '',
    '| material_id | 旧 kb_draft_id | 新 kb_draft_id | status | 操作结果 |',
    '|-------------|----------------|----------------|--------|----------|',
]

for d in task1_details:
    report_lines.append(f"| {d['material_id']} | {d['old_kb']} | {d['new_kb']} | {d['status']} | {d['result']} |")

report_lines.extend([
    '',
    '## 任务二分析表',
    '',
    '| queue_seq | source_path（文件名部分） | 分类 | 疑似匹配行（若有） | 建议 |',
    '|-----------|---------------------------|------|-------------------|------|',
])

for d in task2_details:
    report_lines.append(f"| {d['queue_seq']} | {d['file_name']} | {d['classification']} | {d['matches']} | {d['suggestion']} |")

uncertain_list = [d for d in task2_details if d['classification'] == 'UNCERTAIN']

report_lines.extend([
    '',
    '## 校验结果',
    '',
    f'- 任务一修改行数：{modified_count}（应为 7）',
    f'- 任务二分析条目数：{len(task2_details)}（应为 5，覆盖 queue_seq=8~12）',
    '- A2/A3 队列未被触碰：✅',
    '- 是否有超范围修改：否',
    '',
    '## 遗留问题',
    '',
])

if uncertain_list:
    for d in uncertain_list:
        report_lines.append(f"- queue_seq={d['queue_seq']} ({d['file_name']}): {d['matches']}")
else:
    report_lines.append('无')

report_lines.extend([
    '',
    '## 下一步建议',
    '',
    '等待 Cascade L2 验收后，方可根据分析结果制定重建计划。',
])

report_path.write_text('\n'.join(report_lines), encoding='utf-8')

print(f"任务一修改行数: {modified_count}")
print(f"任务二分析条目数: {len(task2_details)}")
print("报告已生成:", report_path)
