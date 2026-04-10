import json
import subprocess
import urllib.parse
from datetime import datetime

# 配置
AUTH_KEY = 'b982b119ba0744358c1dbcd6711c06fe'
BASE_URL = 'http://localhost:3000'

# 加载账号数据
with open('kimi/wechat-sync-data.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

accounts = data['accounts']
print(f"加载了 {len(accounts)} 个账号")

# 筛选条件
start_ts = 1711900800  # 2024-04-01
end_ts = 1775750400    # 2026-04-10

include_keywords = [
    '通知','公告','安排','须知','指南','攻略','流程','办理','报名','缴费',
    '政策','规定','奖学金','助学金','选课','考试','成绩','宿舍','校园卡',
    '图书馆','网络','VPN','毕业','就业','考研','保研','实习','社团',
    '竞赛','志愿','心理','讲座'
]

exclude_keywords = [
    '招聘','聘用','人才引进','论文发表','SCI','学术会议',
    '领导调研','视察','座谈','转发','转载'
]

def fetch_articles(fakeid, account_name):
    """从API获取账号的所有文章"""
    all_articles = []
    begin = 0
    page = 0
    
    while True:
        url = f"{BASE_URL}/api/public/v1/article?fakeid={fakeid}&begin={begin}&count=20"
        try:
            result = subprocess.run(
                ['curl.exe', '-s', '-H', f'X-Auth-Key: {AUTH_KEY}', url],
                capture_output=True, text=True, encoding='utf-8', timeout=30
            )
            if result.returncode != 0:
                print(f"  curl error: {result.stderr}")
                break
            
            response = json.loads(result.stdout)
            
            if response.get('base_resp', {}).get('ret', -1) != 0:
                err_msg = response.get('base_resp', {}).get('err_msg', 'Unknown error')
                print(f"  API error: {err_msg}")
                break
            
            articles = response.get('articles', [])
            if not articles:
                break
            
            page += 1
            all_articles.extend(articles)
            begin += len(articles)
            
            if len(articles) < 20:
                break
                
        except Exception as e:
            print(f"  Error fetching page: {e}")
            break
    
    return all_articles

results = []
stats = {
    'total_synced': 0,
    'in_time_range': 0,
    'after_exclude': 0,
    'final': 0,
    'by_account': {}
}

for account in accounts:
    account_name = account['name']
    fakeid = account['fakeid']
    account_type = account.get('type', 'unknown')
    
    print(f"\n处理账号: {account_name} ({account_type}类)")
    
    # 获取文章
    articles = fetch_articles(fakeid, account_name)
    print(f"  获取到 {len(articles)} 篇文章")
    
    stats['by_account'][account_name] = {
        'synced': len(articles),
        'in_time': 0,
        'keyword_hit': 0,
        'type': account_type
    }
    stats['total_synced'] += len(articles)
    
    for article in articles:
        title = article.get('title', '')
        create_time = article.get('create_time', article.get('update_time', 0))
        url = article.get('link', article.get('url', ''))
        
        # 时间过滤
        if not (start_ts <= create_time <= end_ts):
            continue
        
        stats['in_time_range'] += 1
        stats['by_account'][account_name]['in_time'] += 1
        
        # 排除关键词
        if any(kw in title for kw in exclude_keywords):
            continue
        
        stats['after_exclude'] += 1
        
        # 纳入关键词
        if any(kw in title for kw in include_keywords):
            results.append({
                'account': account_name,
                'title': title,
                'url': url,
                'date': datetime.fromtimestamp(create_time).strftime('%Y-%m-%d')
            })
            stats['final'] += 1
            stats['by_account'][account_name]['keyword_hit'] += 1

print(f"\n{'='*60}")
print(f"筛选统计:")
print(f"  总同步文章: {stats['total_synced']}")
print(f"  时间范围内: {stats['in_time_range']}")
print(f"  排除后: {stats['after_exclude']}")
print(f"  最终符合: {stats['final']}")
print(f"\n各账号统计:")
for account, s in stats['by_account'].items():
    print(f"  {account}: 同步{s['synced']}篇, 时间内{s['in_time']}篇, 命中{s['keyword_hit']}篇")

# 保存结果
with open('kimi/filtered-articles.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

with open('kimi/filter-stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f"\n结果已保存到:")
print(f"  - kimi/filtered-articles.json ({len(results)} 篇文章)")
print(f"  - kimi/filter-stats.json")
