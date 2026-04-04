import json, os

base = 'temp/kimi-lab-001'

def main():
    with open(os.path.join(base, 'summary.json')) as f:
        s = json.load(f)
    
    lines = [
        '# Lab Report: Synthetic Log Analysis',
        '',
        '## Task Description',
        'Generated synthetic log data (10,000+ rows) with fields ts, level, module, message. Analyzed ERROR frequency per minute.',
        '',
        '## Statistics',
        '',
        f'- **Total Rows**: {s["total_rows"]}',
        f'- **ERROR Total**: {s["error_total"]}',
        f'- **ERROR Percentage**: {s["error_percentage"]}%',
        '',
        '## Top 10 High-Error Minutes',
        '',
        '| Rank | Minute | ERROR Count |',
        '|------|--------|-------------|',
    ]
    
    for i, (minute, count) in enumerate(s['top10_error_minutes'], 1):
        lines.append(f'| {i} | {minute} | {count} |')
    
    with open(os.path.join(base, 'report.md'), 'w') as f:
        f.write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()
