# T3 任务: v8 CONTENT-TRIAGE 批次A — 就业+图书馆（共139篇）

## 分类标准
- **Tier-1**: 含具体流程/规定/时间/联系方式 → 直接转 KB
- **Tier-2**: 含可用事实片段但不完整 → 提取部分
- **Tier-3**: 纯活动回顾/领导讲话/无实用信息 → 跳过

## 目录范围

### 山东第一医科大学就业（~78篇）
`wechat-articles/山东第一医科大学就业/`

### 山东第一医科大学图书馆（~61篇）
`wechat-articles/山东第一医科大学图书馆/`

## 执行步骤

### Step 1: 列出两个目录的所有文件
```powershell
Get-ChildItem "wechat-articles\山东第一医科大学就业" -Filter "*.md" | Select-Object Name | Sort-Object Name
Get-ChildItem "wechat-articles\山东第一医科大学图书馆" -Filter "*.md" | Select-Object Name | Sort-Object Name
```

### Step 2: 逐篇读取前 300 字，判断 Tier

对每篇文章读取标题和前 300 字，按标准分类。

### Step 3: 生成分类报告，写入 `kimi/triage-a-report.md`

```markdown
# TRIAGE 批次A 报告

文章总数: XX
- Tier-1: XX 篇
- Tier-2: XX 篇
- Tier-3: XX 篇

## Tier-1 清单（直接转KB）

| 文件名 | 账号 | 关键信息点 | 预估KB条数 |
|--------|------|----------|-----------|

## Tier-2 清单

| 文件名 | 账号 | 可提取内容 | 预估KB条数 |
|--------|------|----------|-----------|
```

请开始执行。
