# ingest: ChromaDB 全量重入库

## 任务信息
- **spec 引用**: `_spec-v6-kb-expansion.yaml` § INGEST
- **优先级**: P0（Wave 4，串行）
- **依赖**: qa-review 通过
- **执行位置**: 165 服务器 (`~/dev/yixiaoguan/services/ai-service`)

## 步骤
1. 确认新 KB 文件已通过 Mutagen 同步到 165
2. 停止 ai-service：`tmux send-keys -t ai-service C-c`
3. 清空 ChromaDB 旧数据
4. 全量入库：`python scripts/batch_ingestion.py --yes`
5. 验证入库数量
6. 重启 ai-service
7. `GET /kb/stats` 确认 entry_count

## 预期结果
- 现有 ~126 条 + 新增 ~84 条 = **210+ 条**
- chunks: ~300+

## 验收标准
- AC-ING-01: batch_ingestion.py 无 Python 异常
- AC-ING-02: `/kb/stats` entry_count ≥ 200
- AC-ING-03: 抽查 5 条 KB-20260409-* metadata 包含 entry_id/category/title

## 状态
- [ ] 等待 qa-review 通过
- [ ] 执行入库
- [ ] T1 验收
