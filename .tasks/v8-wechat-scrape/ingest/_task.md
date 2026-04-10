# INGEST-V8 — ChromaDB 全量重入库

**所属**: v8-wechat-scrape / PHASE 4
**优先级**: P0
**执行者**: Kimi
**预估工时**: 0.5h
**依赖**: QA-REVIEW-V8 (PASS)

## 任务目标

QA 通过后，将所有 KB 条目（v6/v7/v8 共 339-419 条）全量重入 ChromaDB。

## 执行步骤

### Step 1: 同步文件（Mutagen）
确认本地 `knowledge-base/entries/` 下所有新 KB 文件已同步到服务器。

```bash
ssh easten@10.80.3.165 "ls /home/easten/dev/yixiaoguan/knowledge-base/entries/first-batch-drafts/KB-20260410-01*.md | wc -l"
```
期望文件数 ≥ 新增KB条数。

### Step 2: 停止 ai-service
```bash
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml stop ai-service"
```
或按实际部署方式停止。

### Step 3: 清空 ChromaDB 并全量入库
```bash
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/clear_kb_collection.py && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/batch_ingest_kb.py --yes"
```

### Step 4: 重启 ai-service
```bash
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && docker-compose -f deploy/docker-compose.yml start ai-service"
```

### Step 5: 验证入库结果
```bash
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats"
```
期望 `entry_count ≥ 330`。

## 预期结果

| 项目 | 预期值 |
|------|--------|
| 入库总条数 | 330-420 条 |
| entry_count | ≥ 330 |
| chunks | 500-600+ |

## 验收标准

- AC-ING8-01: `batch_ingest_kb.py` 无异常退出
- AC-ING8-02: `/kb/stats` entry_count ≥ 330
- AC-ING8-03: 抽查 5 条公众号来源 KB（source 字段含 "wechat/"）
