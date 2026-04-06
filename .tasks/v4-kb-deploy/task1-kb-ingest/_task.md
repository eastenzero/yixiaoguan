---
id: "task1-kb-ingest"
parent: "v4-kb-deploy"
type: "feature"
status: "pending"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/"
out_of_scope:
  - "knowledge-base/raw/"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/"
  - "apps/"

context_files:
  - ".teb/antipatterns.md"
  - "scripts/batch_ingest_kb.py"
  - "knowledge-base/raw/first-batch-processing/converted/markdown/KB-0150-电费缴纳指南.md"

done_criteria:
  L0: "22个文件 KB-0150-*.md ~ KB-0171-*.md 存在于 knowledge-base/entries/first-batch-drafts/"
  L1: "165服务器上 python scripts/batch_ingest_kb.py --yes 无 Python 异常退出"
  L2: "165服务器上 GET http://localhost:8000/kb/stats 返回 entry_count > 1059"
  L3: "AI 能正确回答'怎么交电费'（返回完美校园APP步骤）"

depends_on: []
created_at: "2026-04-06 13:15:00"
---

# KB 入库：移动22条新KB文件并全量重入库

> 22条新KB文件已存在于 raw 目录，但从未被入库脚本扫到。完成后，ChromaDB 应包含全部124条KB（102旧+22新），AI能回答电费/报修/校园卡等生活服务问题。

## 背景

`batch_ingest_kb.py` 扫描路径硬编码为 `knowledge-base/entries/first-batch-drafts/`。
22条新文件在 `knowledge-base/raw/first-batch-processing/converted/markdown/`，需移动到正确目录。

## 执行步骤

### Step 1：在 Windows 端移动文件

将以下22个文件从：
`knowledge-base/raw/first-batch-processing/converted/markdown/`

复制（不是移动，保留 raw 原件）到：
`knowledge-base/entries/first-batch-drafts/`

文件列表：
- KB-0150-电费缴纳指南.md
- KB-0151-宿舍报修流程.md
- KB-0152-校园卡办理与使用.md
- KB-0153-水电管理与节约.md
- KB-0154-学生公寓管理规定.md
- KB-0155-请假销假制度.md
- KB-0156-奖学金评定指南.md
- KB-0157-学生纪律处分规定.md
- KB-0158-图书馆使用指南.md
- KB-0159-学籍管理规定.md
- KB-0160-校园交通安全管理.md
- KB-0161-勤工助学指南.md
- KB-0162-困难认定与助学金申请.md
- KB-0163-助学贷款指南.md
- KB-0164-学费缴纳指南.md
- KB-0165-考试纪律与违纪处理.md
- KB-0166-校外住宿管理规定.md
- KB-0167-心理健康教育与咨询.md
- KB-0168-出国留学指南.md
- KB-0169-学生证件管理.md
- KB-0170-食堂就餐公约.md
- KB-0171-绿色通道与学费减免.md

### Step 2：等待 Mutagen 同步（约10秒）

验证165上文件已存在：
```bash
ls ~/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-015*.md | wc -l
```
预期输出 ≥ 10

### Step 3：165 服务器 — 停止 ai-service

```bash
tmux send-keys -t ai-service C-c
sleep 3
```

### Step 4：165 服务器 — 执行全量重入库

```bash
cd ~/dev/yixiaoguan
source services/ai-service/venv/bin/activate
python scripts/batch_ingest_kb.py --yes
```

### Step 5：165 服务器 — 重启 ai-service

```bash
tmux send-keys -t ai-service "cd ~/dev/yixiaoguan/services/ai-service && source ../venv/bin/activate 2>/dev/null || source venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 8000" Enter
sleep 5
```

### Step 6：验证

```bash
curl -s http://localhost:8000/kb/stats
```
预期 entry_count > 1059

## 已知陷阱

- `batch_ingest_kb.py` 用 `upsert`，重复入库旧条目无副作用
- 新KB文件 frontmatter 无 `status`/`audience`/`rule_task_id` 字段，ingest script 用 `.get()` 取默认值，无需修改
- 165 ai-service 的 venv 路径：`~/dev/yixiaoguan/services/ai-service/venv/`
