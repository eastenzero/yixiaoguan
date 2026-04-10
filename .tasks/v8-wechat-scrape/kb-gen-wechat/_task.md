# KB-GEN-WECHAT — 从公众号文章生成 KB 条目

**所属**: v8-wechat-scrape / PHASE 3
**优先级**: P1
**执行者**: Kimi（分批次）
**预估工时**: 4h
**依赖**: CONTENT-TRIAGE

## 任务目标

将 Tier-1 和 Tier-2 文章转化为标准 KB 条目（YAML frontmatter + Markdown 正文）。

## KB 编号规则

**起始编号**: `KB-20260410-0101`（承接 v7 的 0051，预留 50 号缓冲）

## KB 格式模板

```markdown
---
title: "标题"
category: "分类"
tags: ["标签1", "标签2", "公众号来源"]
source: "wechat/{公众号名称}"
source_url: "https://mp.weixin.qq.com/s/xxxxx"
campus: "通用|济南校区|泰安校区"
status: "active"
---

## 问题概述

学生常见问题描述...

## 标准答复

从文章提取的事实性信息（流程/规定/联系方式/时间）...

> 注：以上信息来源于公众号"{公众号名称}"，具体以学校最新通知为准。
```

## 生成规则

1. **一篇文章 → 0~3 条 KB**
   - 内容聚焦的短文章 → 1 条
   - 包含多个独立信息点 → 拆分为多条
   - 纯新闻无实用信息 → 0 条

2. **内容处理**:
   - 提取事实性信息（时间/地点/流程/要求/联系方式）
   - 去除时效性过强表述（"本学期""今年" → 具体日期）
   - 去除营销语句/表情符号引用
   - 去除图片链接

3. **去重规则**:
   - 与 v6/v7 已有 259 条 KB 对比主题
   - 同主题取信息量最大或最新的版本
   - 公众号有多篇同主题文章时，取最新一篇

## 执行批次（按账号分批）

| 批次 | 账号 | 预估KB条数 | Kimi 任务文件 |
|------|------|-----------|------------|
| 批次A | A01教务部 / A02研究生处 | 20-35 | task-v8-kb-gen-a.md |
| 批次B | A03学工 / A04后勤 / A05心理健康 | 20-35 | task-v8-kb-gen-b.md |
| 批次C | A06图书馆 / A07就业 / A08科研部 | 15-25 | task-v8-kb-gen-c.md |
| 批次D | B 类公众号（优先处理） | 15-30 | task-v8-kb-gen-d.md |

## 输出目录

`knowledge-base/entries/first-batch-drafts/KB-20260410-0101.md` 起

## 验收标准

- AC-KGW-01: Tier-1 文章全部转化
- AC-KGW-02: 每条 KB 有合法 frontmatter（title/category/tags/source/source_url）
- AC-KGW-03: source_url 指向原始公众号文章
- AC-KGW-04: 与已有 259 条 KB 无实质重复
- AC-KGW-05: 时效性信息标注具体日期，末尾注明"以最新通知为准"
