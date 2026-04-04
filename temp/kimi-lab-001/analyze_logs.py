import csv, json, datetime, os, collections

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
