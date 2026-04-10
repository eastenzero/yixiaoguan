# T3 任务: v7 KB-GEN-COLLEGES 子批次B — 学院 KB 生成（report-13 + report-14）

## 角色
你是山东第一医科大学（医小管）知识库条目的生成专家。

## 任务目标
基于以下 2 份探查报告，批量生成 KB 知识库条目：
- `kimi/report-13-colleges-batch3.md` — 临床与基础医学院 / 放射学院 / 护理学院
- `kimi/report-14-colleges-batch4.md` — 口腔医学院 / 运动医学与康复学院 / 公共卫生与健康管理学院

## 生成规格

- **输出目录**: `knowledge-base/entries/first-batch-drafts/`
- **命名规则**: `KB-20260410-{NNNN}.md`
- **编号范围**: 0036 ~ 0050（按实际条目数调整，不超过 0050）
- **来源**: 对应的 report 文件

## KB 条目模板

```markdown
---
title: "条目标题"
category: "分类"
tags: ["标签1", "标签2"]
source: "kimi/report-13-colleges-batch3"
source_url: ""
campus: ""
status: "draft"
---

## 问题概述
## 标准答复（不少于50字）
## 详细说明
## 咨询方式（如有）
## 来源说明
```

## 生成规则

### A. 学院概况与专业（每学院 1 条，本批次共 6 条）
- 标题格式: "XX学院简介与专业设置"
- category: 院系与专业

### B. 学院特色内容（按需，约 3-6 条）
- 实验室/研究平台、实习基地、国际交流、特色竞赛
- category: 按内容归入合适分类

## 去重要求
- KB-20260409-0069（学校简介）
- KB-20260409-0071（本科招生专业）
- KB-20260409-0072（优势学科）
请读取这些文件确认互补不重复。

## 质量要求
1. frontmatter 完整 / 2. 标准答复 ≥ 50 字 / 3. 无占位符 / 4. 无幻觉 / 5. tags ≥ 2 / 6. campus 准确 / 7. source 准确

## 执行步骤
1. 读取 report-13 和 report-14
2. 读取去重参考 KB
3. 规划条目清单
4. 逐一生成
5. 输出统计

请开始执行。
