# INGEST-V7 — ChromaDB 全量重入库

**SPEC 模块**: INGEST-V7
**优先级**: P0
**状态**: pending
**依赖**: QA-REVIEW-V7
**预计工时**: 0.5h

## 执行步骤

1. 确保所有新 KB 文件已同步到 165 服务器 (Mutagen)
2. 停止 ai-service（Docker 容器）
3. 清空 ChromaDB 旧数据
4. 全量入库: `python scripts/batch_ingest_kb.py --yes`
5. 验证入库数量
6. 重启 ai-service
7. `GET /kb/stats` 确认

## 预期结果

- 入库总量: 现有 ~210 + v7 新增 ~55-68 = **~265-278 条**
- chunks: **~400+**（按 800 字/chunk）

## 验收标准
- AC-ING7-01: batch_ingest_kb.py 运行无异常
- AC-ING7-02: /kb/stats entry_count ≥ 260
- AC-ING7-03: 抽查 5 条 KB-20260410-* metadata 正确
