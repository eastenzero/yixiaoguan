# T3 任务: v8 CONTENT-TRIAGE Round2 — 新文章分类

## 背景
`wechat-exports-full/` 目录有约 40 篇新下载文章（A类29篇 + B类11篇）。
第一轮已处理 `wechat-exports/` 中的 33 篇（已生成 KB-0101~0119）。
本轮对新目录中的文章做分类，**跳过已在第一轮处理过的内容重复文章**。

## 分类标准

**Tier-1（直接转 KB）**: 含具体流程/规定/时间/联系方式
**Tier-2（提取部分）**: 含可用事实片段
**Tier-3（跳过）**: 纯活动回顾/领导讲话/无实用信息
**Tier-DUP（重复跳过）**: 与已处理的 KB-0101~0119 内容高度重叠

## 执行步骤

### Step 1: 列出所有新文章
```powershell
Get-ChildItem -Recurse -Filter "*.md" wechat-exports-full | Select-Object FullName, Length | Sort-Object FullName
```

### Step 2: 读取每篇文章标题和前 400 字，判断 Tier

对每篇文章：
- 如果与已有 KB（0101~0119）主题高度重叠 → Tier-DUP，记录重叠的 KB 编号
- 否则按 Tier-1/2/3 标准分类

### Step 3: 生成分类报告

写入 `kimi/wechat-triage-r2.md`：

```markdown
# 公众号文章分类报告 Round2

文章总数: XX
- Tier-1: XX 篇 → 预估 KB: XX 条
- Tier-2: XX 篇 → 预估 KB: XX 条
- Tier-3: XX 篇 → 跳过
- Tier-DUP: XX 篇 → 跳过（已有对应 KB）

## Tier-1 文章清单

| 序号 | 账号 | 文件名 | 关键信息点 | 预估KB条数 |
|------|------|--------|----------|-----------|

## Tier-2 文章清单

| 序号 | 账号 | 文件名 | 可提取内容 | 预估KB条数 |
|------|------|--------|----------|-----------|

## Tier-DUP 文章清单

| 序号 | 账号 | 文件名 | 重叠 KB |
|------|------|--------|---------|
```

## 验收标准
- 所有 40 篇均有 Tier 标注
- Tier-1 预估 KB 条数 ≥ 10

请开始执行。
