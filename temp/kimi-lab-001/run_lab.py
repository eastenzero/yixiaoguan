import os, time, csv, random, datetime, json, collections, subprocess

base = 'temp/kimi-lab-001'
os.makedirs(base, exist_ok=True)
print('Step 1 done: dir created')
time.sleep(45)

levels = ['INFO']*70 + ['WARN']*20 + ['ERROR']*10
modules = ['auth', 'db', 'api', 'worker', 'cache', 'gateway']
messages = ['Connection established', 'Query executed', 'Request processed', 'Timeout occurred', 'Invalid token', 'Retry failed', 'Cache miss', 'Rate limit hit']
start = datetime.datetime(2024,1,1,0,0,0)
csv_path = os.path.join(base, 'synthetic_logs.csv')
with open(csv_path, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ts','level','module','message'])
    for i in range(12000):
        ts = start + datetime.timedelta(seconds=random.randint(0,3600))
        w.writerow([ts.strftime('%Y-%m-%d %H:%M:%S'), random.choice(levels), random.choice(modules), random.choice(messages)])
print('Step 2 done: CSV generated')
time.sleep(45)

py_path = os.path.join(base, 'analyze_logs.py')
with open(py_path, 'w') as f:
    f.write("""import csv, json, datetime, os, collections

base = 'temp/kimi-lab-001'

def main():
    input_path = os.path.join(base, 'synthetic_logs.csv')
    output_path = os.path.join(base, 'summary.json')
    
    error_per_minute = collections.Counter()
    total = 0
    error_total = 0
    
    with open(input_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            if row['level'] == 'ERROR':
                error_total += 1
                ts = datetime.datetime.strptime(row['ts'], '%Y-%m-%d %H:%M:%S')
                minute = ts.strftime('%Y-%m-%d %H:%M')
                error_per_minute[minute] += 1
    
    error_pct = round(error_total / total * 100, 2) if total else 0
    top10 = error_per_minute.most_common(10)
    
    summary = {
        'total_rows': total,
        'error_total': error_total,
        'error_percentage': error_pct,
        'top10_error_minutes': top10
    }
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f'Total: {total}, ERROR: {error_total}, Pct: {error_pct}%')

if __name__ == '__main__':
    main()
""")
print('Step 3 done: analyze_logs.py written')
time.sleep(45)

gen_report_path = os.path.join(base, 'generate_report.py')
with open(gen_report_path, 'w') as f:
    f.write("""import json, os

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
        f.write('\\n'.join(lines) + '\\n')

if __name__ == '__main__':
    main()
""")
print('Step 4 done: generate_report.py written')
time.sleep(45)

subprocess.run(['python', py_path], check=True)
subprocess.run(['python', gen_report_path], check=True)

print('--- Self Check ---')
for fname in ['synthetic_logs.csv', 'analyze_logs.py', 'summary.json', 'report.md']:
    fpath = os.path.join(base, fname)
    if os.path.exists(fpath):
        with open(fpath) as f:
            line_count = sum(1 for _ in f)
        print(f'{fname} exists, lines: {line_count}')
    else:
        print(f'{fname} MISSING')

with open(os.path.join(base, 'summary.json')) as f:
    summary = json.load(f)

total_rows = summary['total_rows']
error_total = summary['error_total']
highest = summary['top10_error_minutes'][0] if summary['top10_error_minutes'] else ('N/A', 0)
print(f'DONE | 总行数: {total_rows} | ERROR总数: {error_total} | 最高错误分钟: {highest[0]} ({highest[1]})')
