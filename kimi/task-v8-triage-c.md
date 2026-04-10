# T3 任务: v8 CONTENT-TRIAGE 批次C — 心理+招生办+学工+科创（共95篇）

## 分类标准
- **Tier-1**: 含具体流程/规定/时间/联系方式 → 直接转 KB
- **Tier-2**: 含可用事实片段但不完整 → 提取部分
- **Tier-3**: 纯活动回顾/领导讲话/无实用信息 → 跳过

## 目录范围

### 山一大心理健康教育中心（~31篇）
`wechat-articles/山一大心理健康教育中心/`

### 山一大招生办（~29篇）
`wechat-articles/山一大招生办/`

### 山一大学工（~18篇）
`wechat-articles/山一大学工/`

### 山东第一医科大学科创中心（~17篇）
`wechat-articles/山东第一医科大学科创中心/`

## 执行步骤

### Step 1: 列出四个目录的所有文件
```powershell
Get-ChildItem "wechat-articles\山一大心理健康教育中心","wechat-articles\山一大招生办","wechat-articles\山一大学工","wechat-articles\山东第一医科大学科创中心" -Filter "*.md" | Select-Object DirectoryName, Name | Sort-Object DirectoryName, Name
```

### Step 2: 逐篇读取前 300 字，判断 Tier

### Step 3: 生成分类报告，写入 `kimi/triage-c-report.md`

```markdown
# TRIAGE 批次C 报告

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
