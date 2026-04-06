---
id: "task3-temp-cleanup"
parent: "v4-kb-deploy"
type: "feature"
status: "pending"
tier: "T3"
priority: "low"
risk: "low"
foundation: false

scope:
  - "temp/"
out_of_scope:
  - "apps/"
  - "services/"
  - "scripts/"
  - "knowledge-base/"
  - ".tasks/"

context_files:
  - ".teb/antipatterns.md"

done_criteria:
  L0: "temp/ 目录下无 .py/.sh/.log/.txt/.png 残留文件（或目录为空）"
  L1: "git status 显示 temp/ 下无 tracked 文件变更"
  L2: "git clean -n temp/ 输出为空（无 untracked 文件）"
  L3: "项目根目录干净，无测试脚本/日志散落"

depends_on: []
created_at: "2026-04-06 13:15:00"
---

# temp/ 目录清理

> temp/ 目录中无任何有效文件，项目根目录干净整洁。

## 背景

上一轮 T2/T3 执行集成测试时，将测试脚本、日志、截图等临时文件散落在 `temp/` 目录，需清理。

## 执行步骤

### Step 1：检查 temp/ 内容

```powershell
Get-ChildItem C:\Users\Administrator\Documents\code\yixiaoguan\temp\
```

### Step 2：确认无需保留的文件

确认 temp/ 下没有业务代码或重要文档，全部为测试临时文件后执行清理。

### Step 3：执行清理

```bash
git -C C:\Users\Administrator\Documents\code\yixiaoguan clean -fd temp/
```

若有 tracked 文件（已 git add），改用：
```bash
git -C C:\Users\Administrator\Documents\code\yixiaoguan rm -r --cached temp/
git -C C:\Users\Administrator\Documents\code\yixiaoguan commit -m "chore: clean up temp/ directory residuals [task:task3-temp-cleanup]"
```

### Step 4：验证

```powershell
Get-ChildItem C:\Users\Administrator\Documents\code\yixiaoguan\temp\
```
预期：无输出或提示目录为空。

## 已知陷阱

- `git clean -fd` 只删除 untracked 文件，tracked 文件需 `git rm`
- 执行前务必确认 temp/ 下无业务代码
