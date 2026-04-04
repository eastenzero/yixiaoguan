---
id: "p2b-full-reingest"
parent: "phase-2-vectorize"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"
foundation: true

scope:
  - "services/ai-service/data/chroma/"
  - "temp/"
  - "docs/test-reports/completion-reports/"
out_of_scope:
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/chunker.py"
  - "knowledge-base/entries/first-batch-drafts/"
  - "apps/"
  - "services/business-api/"

context_files:
  - "teb-starter-kit/antipatterns.md"
  - "scripts/batch_ingest_kb.py"
  - "services/ai-service/app/core/config.py"
  - "AGENT.md"

done_criteria:
  L0: "docs/test-reports/completion-reports/P2B-full-reingest-report.md 存在"
  L1: "入库脚本执行无 Python 异常输出"
  L2: "ChromaDB kb_entries 集合条目数 > 90（chunk 拆分后应显著多于草稿文件数）；GET http://localhost:8000/kb/stats 返回 total_chunks > 90"
  L3: "抽查 5 条 chunk 的 metadata：entry_id / chunk_index / category / title 字段全部正确"

depends_on: ["p2a-chunker-integration"]
created_at: "2026-04-04 01:43:00"
---

# p2b：全量清空 + 重新入库

> ChromaDB `kb_entries` 集合已全量清空并重新入库，条目数 > 90，chunk 格式和 metadata 正确。

## 背景

p2a 完成 chunker 接入后，需要清空旧的整条目向量并全量重入库。
旧向量（无 `__chunk_` 后缀的 ID）与新 chunk 格式不兼容，必须全量清空后重入。

## 执行步骤

1. 停止 ai-service 容器（避免读写冲突）：`docker compose stop ai-service`
2. 运行入库脚本清空并重入：`python scripts/batch_ingest_kb.py --clear-all`（确认脚本支持 `--clear-all` 参数，否则先手动清空集合）
3. 等待入库完成，记录总 chunk 数
4. 重启 ai-service：`docker compose start ai-service`
5. 调用 `GET http://localhost:8000/kb/stats` 验证统计数据
6. 随机抽查 5 条 chunk 的 metadata
7. 将结果写入报告

## 已知陷阱

- **全量清空是不可逆操作**，执行前确认 p2a 代码改造已验证通过
- ai-service 容器需先停止，否则可能有并发写入冲突
- ChromaDB bind mount 路径：`services/ai-service/data/chroma/`（宿主机路径）
- 如果 batch_ingest_kb.py 没有 `--clear-all` 参数，需要先用 Python 直接连接 ChromaDB 删除集合再重建
