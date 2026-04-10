# v6-kb-expansion 父任务

## 概述
spec: `.tasks/_spec-v6-kb-expansion.yaml`
目标: 利用 7 份 Kimi 探查报告，新增 ~84 条 KB 条目，使知识库从 ~126 条扩充至 210+ 条。

## 执行批次
- **Wave 1**: batch-p0（单独先跑，最高优先级）
- **Wave 2**: batch-p1 + batch-p2 + batch-p3（P0 完成后并行）
- **Wave 3**: qa-review（全部 batch 完成后）
- **Wave 4**: ingest（qa-review 通过后）
- **Wave 5**: rag-eval（ingest 完成后）

## 子任务
| 任务 ID       | 描述                          | 状态      | 依赖       |
|--------------|-------------------------------|-----------|-----------|
| batch-p0     | P0 高频刚需条目（35条）         | pending   | -          |
| batch-p1     | P1 教务核心条目（20条）         | pending   | batch-p0  |
| batch-p2     | P2 学生权益条目（13条）         | pending   | batch-p0  |
| batch-p3     | P3 发展类条目（16条）           | pending   | batch-p0  |
| qa-review    | 质量审查与去重                  | pending   | p1+p2+p3  |
| ingest       | ChromaDB 全量重入库             | pending   | qa-review |
| rag-eval     | RAG 评测回归                    | pending   | ingest    |

## 编号规范
新条目统一使用 `KB-20260409-NNNN` 格式（四位补零，从 0001 起）。
文件位置：`knowledge-base/entries/first-batch-drafts/`

## T1 执行记录
- 2026-04-09: 任务树创建，Wave 1 开始下发
