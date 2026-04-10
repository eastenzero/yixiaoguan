# batch-p0: P0 高频刚需条目

## 任务信息
- **spec 引用**: `_spec-v6-kb-expansion.yaml` § BATCH-P0
- **优先级**: P0（最高，Wave 1 独立执行）
- **预估条目**: 30-35 条
- **编号范围**: KB-20260409-0001 ~ KB-20260409-0035
- **Kimi 指令文件**: `kimi/task-v6-batch-p0.md`

## 生成清单
1. **作息时间表** (Report 7 §3.8) — 0001-0002
2. **服务电话汇总** (Report 2 DS-1, Report 4 DS-12) — 0003-0012
3. **信息门户操作** (Report 5 §11, §1) — 0013-0018
4. **校园网/WiFi/VPN** (Report 4 DS-4/DS-5/DS-001) — 0019-0023
5. **校园一卡通** (Report 4 DS-011) — 0024-0026
6. **图书馆** (Report 4 DS-006/DS-007/DS-008) — 0027-0032
7. **网上报修** (Report 5 §2) — 0033
8. **企业微信功能导览** (Report 4 DS-009, Report 5 企微清单) — 0034-0035

## 验收标准
- AC-P0-01: 生成 30-35 个 .md 文件，命名符合 KB-20260409-NNNN 格式
- AC-P0-02: 每个文件都有合法 YAML frontmatter (title, category, tags, source, status)
- AC-P0-03: 作息时间表条目包含完整 21 个时段
- AC-P0-04: 服务电话条目区分泰安/济南校区
- AC-P0-05: 与现有 KB-0150~0171 无实质内容重复

## 状态
- [ ] Kimi 下发
- [ ] Kimi 回传
- [ ] T1 验收
