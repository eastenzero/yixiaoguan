# prompts/kb-expansion — 知识库扩量阶段提示词

**阶段状态**：🔜 修复收口后开始执行。

## 批次规划

| 批次 | 领域 | 状态 |
|------|------|------|
| BATCH-B1 | 竞赛申报、评优评选、综合测评 | 准备中 |
| BATCH-B2 | 生活服务高频（电费/报修/校园卡/网络） | 待规划 |
| BATCH-B3 | 学籍变更（休学/复学/转专业） | 待规划 |

## 命名约定

`batch-<批次编号>-<领域简述>-<阶段>-prompt-<日期>.md`

例：`batch-b1-competition-eval-discovery-prompt-2026-04-03.md`

每个批次通常分三个阶段的提示词：
1. `discovery` — 扫描源文件 + 建队列 CSV
2. `draft-gen` — 从队列生成 KB 草稿
3. `ingest` — 入库 ChromaDB
