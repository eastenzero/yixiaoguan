# v8-wechat-scrape 任务树

**SPEC**: `_spec-v8-wechat-scrape.yaml`
**日期**: 2026-04-10
**状态**: in_progress
**前置知识库**: v7 完成，259条 / 290 chunks / Recall@5=86.0%
**预计新增 KB**: 80-160 条 (编号 KB-20260410-0101+)

## 账号来源

学生自行整理了 25 个公众号（见 `kimi/wechat-accounts-list.md`）。
已预分类为 A/B/C/D 四档，DISCOVER 阶段优先通过 API 搜索确认 fakeid 后直接进入 SYNC。

## PHASE 1: 环境部署

- [ ] **DEPLOY** — Docker 部署 wechat-article-exporter（Kimi 执行）
- [ ] **LOGIN** — 👤 用户手动扫码登录，提供 auth-key

## PHASE 2: 公众号发现与文章抓取

- [ ] **DISCOVER** — API 搜索确认 fakeid，整合 25 个已知账号，产出完整 `wechat-accounts-list.md`
- [ ] **SYNC-ARTICLES** — 同步 A 类(8个) + B 类(8个) 公众号文章列表
- [ ] **FILTER-DOWNLOAD** — 按筛选条件下载有价值文章（时间: 2024-04-01~2026-04-10）

## PHASE 3: 内容筛选与 KB 生成

- [ ] **CONTENT-TRIAGE** — 文章分 Tier-1/2/3，产出分类报告
- [ ] **KB-GEN-WECHAT** — Tier-1/2 文章 → KB 条目，按公众号分批次生成

## PHASE 4: QA + 入库 + 评测

- [ ] **QA-REVIEW-V8** — frontmatter / 时效性 / 去重 / source_url 审查
- [ ] **INGEST-V8** — ChromaDB 全量重入库 (目标 entry_count ≥ 330)
- [ ] **RAG-EVAL-V8** — 扩充评测集 5-10 题 + 回归 (基线: Recall@5 ≥ 85%, 拒答 ≥ 90%)

---

## T1 执行记录

| 时间 | 动作 | 结果 |
|------|------|------|
| 2026-04-10 | 任务拆解：创建子任务文件 + 预填账号清单 | ✅ |
| | 下一步：下发 DEPLOY 任务 → 等待用户扫码 auth-key | pending |
