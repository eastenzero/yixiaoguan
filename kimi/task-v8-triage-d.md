# T3 任务: v8 CONTENT-TRIAGE 批次D — 医药管理+财务+青春山一大+山科院+饮食（共60篇）

## 分类标准
- **Tier-1**: 含具体流程/规定/时间/联系方式 → 直接转 KB
- **Tier-2**: 含可用事实片段但不完整 → 提取部分
- **Tier-3**: 纯活动回顾/领导讲话/无实用信息 → 跳过

## 目录范围

### 山东第一医科大学医药管理学院（~16篇）
`wechat-articles/山东第一医科大学医药管理学院/`

### 山东第一医科大学计划财务处（~15篇）
`wechat-articles/山东第一医科大学计划财务处/`

### 青春山一大（~12篇）
`wechat-articles/青春山一大/`

### 山东第一医科大学 山东省医学科学院（~10篇）
`wechat-articles/山东第一医科大学_山东省医学科学院/`

### 山一大饮食（~7篇）
`wechat-articles/山一大饮食/`

## 执行步骤

### Step 1: 列出五个目录的所有文件
```powershell
Get-ChildItem "wechat-articles\山东第一医科大学医药管理学院","wechat-articles\山东第一医科大学计划财务处","wechat-articles\青春山一大","wechat-articles\山东第一医科大学_山东省医学科学院","wechat-articles\山一大饮食" -Filter "*.md" -ErrorAction SilentlyContinue | Select-Object DirectoryName, Name | Sort-Object DirectoryName, Name
```

### Step 2: 逐篇读取前 300 字，判断 Tier

### Step 3: 生成分类报告，写入 `kimi/triage-d-report.md`

```markdown
# TRIAGE 批次D 报告

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
