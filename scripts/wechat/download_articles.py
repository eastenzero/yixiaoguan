import json
import os
import time
import re
import urllib.parse
import subprocess

# 加载筛选结果
with open('kimi/filtered-articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

auth_key = 'b982b119ba0744358c1dbcd6711c06fe'
headers = {'X-Auth-Key': auth_key}

downloaded = 0
failed = 0
skipped = 0

print(f"开始下载 {len(articles)} 篇文章...")
print("="*60)

for i, article in enumerate(articles, 1):
    account = article['account']
    title = article['title']
    date = article['date']
    url = article['url']
    
    # 创建输出目录
    out_dir = f"wechat-exports/{account}"
    os.makedirs(out_dir, exist_ok=True)
    
    # 安全文件名（去除特殊字符）
    safe_title = re.sub(r'[\\/:*?"<>|]', '', title)[:50]
    out_file = f"{out_dir}/{date}-{safe_title}.md"
    
    # 跳过已下载
    if os.path.exists(out_file):
        print(f"[{i}/{len(articles)}] SKIP: {title[:40]}...")
        skipped += 1
        continue
    
    # URL编码
    encoded_url = urllib.parse.quote(url, safe='')
    api_url = f"http://localhost:3000/api/public/v1/download?url={encoded_url}&format=markdown"
    
    # 下载
    try:
        result = subprocess.run(
            ['curl.exe', '-s', '-o', out_file, '-H', f'X-Auth-Key: {auth_key}', api_url],
            capture_output=True, text=True, encoding='utf-8', timeout=60
        )
        
        if result.returncode == 0 and os.path.exists(out_file) and os.path.getsize(out_file) > 0:
            print(f"[{i}/{len(articles)}] OK: {title[:40]}...")
            downloaded += 1
        else:
            print(f"[{i}/{len(articles)}] FAIL: {title[:40]}...")
            failed += 1
            # 删除空文件
            if os.path.exists(out_file) and os.path.getsize(out_file) == 0:
                os.remove(out_file)
    except Exception as e:
        print(f"[{i}/{len(articles)}] ERROR: {title[:40]}... - {e}")
        failed += 1
    
    time.sleep(1)  # 频率限制

print("="*60)
print(f"完成: 下载 {downloaded} 篇, 跳过 {skipped} 篇, 失败 {failed} 篇")
