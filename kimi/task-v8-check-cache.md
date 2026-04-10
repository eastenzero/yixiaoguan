# T3 任务: 检查 wechat-article-exporter 本地缓存

## 目标
看 Docker 容器挂载的 `.data/` 目录里有没有历史文章数据，如果有就直接导出。

## Step 1: 列出 .data 目录内容

```powershell
Get-ChildItem -Recurse "C:\wechat-exporter\.data" | Select-Object FullName, Length, LastWriteTime | Sort-Object LastWriteTime -Descending | Select-Object -First 30
```

## Step 2: 查找数据库文件

```powershell
Get-ChildItem -Recurse "C:\wechat-exporter\.data" -Include "*.db","*.sqlite","*.sqlite3","*.json","*.jsonl" | Select-Object FullName, Length
```

## Step 3: 如果找到 SQLite 数据库

对找到的 .db 文件，查看表结构：
```powershell
python -c "
import sqlite3, sys
db_path = sys.argv[1]
conn = sqlite3.connect(db_path)
tables = conn.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()
print('表:', [t[0] for t in tables])
for t in tables:
    cols = conn.execute(f\"PRAGMA table_info({t[0]})\").fetchall()
    print(f'{t[0]}: {[c[1] for c in cols]}')
    count = conn.execute(f\"SELECT COUNT(*) FROM {t[0]}\").fetchone()[0]
    print(f'  行数: {count}')
conn.close()
" "C:\wechat-exporter\.data\{实际db文件名}"
```

## Step 4: 如果找到文章数据，导出为 JSONL

如果数据库里有文章表（含 title/link/fakeid/create_time），运行：
```powershell
python -c "
import sqlite3, json
conn = sqlite3.connect('C:\wechat-exporter\.data\{db文件}')
# 查询所有文章
rows = conn.execute('SELECT * FROM {文章表名}').fetchall()
cols = [d[0] for d in conn.execute('SELECT * FROM {文章表名}').description]
with open('wechat-meta/from-cache.jsonl', 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(json.dumps(dict(zip(cols, r)), ensure_ascii=False) + '\n')
print(f'导出 {len(rows)} 条')
"
```

## 输出

报告：
1. `.data/` 目录结构（文件名 + 大小）
2. 是否找到 SQLite 数据库
3. 如找到文章数据：表结构 + 行数 + 已导出的文件路径
4. 如找到：文章总数是多少？最早和最新的发布时间是？

---

## 执行结果

**状态**: ✅ 已完成  
**报告文件**: `kimi/task-v8-check-cache-report.md`

### 主要发现

| 检查项 | 结果 |
|--------|------|
| SQLite 数据库 | ❌ 未找到 |
| 文章数据缓存 | ❌ 不存在 |
| Cookie/认证 | ✅ 已设置，有效至 2026-04-14 |

**结论**: wechat-article-exporter 本地 `.data/` 目录仅包含认证 cookie，无文章缓存数据。文章需通过 Web UI 实时获取或从已有导出目录使用。
