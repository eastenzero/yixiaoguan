# T3 任务: Git 安全操作（仅此一步）

## 目标
在 main 分支上提交当前所有文件，然后创建 feat/v9-purple-theme 分支。

## 执行步骤

请依次执行以下 3 条命令：

```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan

# 1. 提交所有未跟踪/修改的文件到 main
git add -A
git commit -m "checkpoint: before v9 frontend redesign"

# 2. 创建并切换到新分支
git checkout -b feat/v9-purple-theme

# 3. 验证当前分支
git branch --show-current
```

## 输出要求

在终端中执行上述命令，确认：
1. commit 成功（输出 commit hash）
2. `git branch --show-current` 输出 `feat/v9-purple-theme`

**不需要写报告文件，只需要执行命令并确认结果。**
**不要做任何其他操作。**
