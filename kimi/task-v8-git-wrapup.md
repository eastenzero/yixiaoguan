# T3 任务：v8 本轮 Git 收尾（仅提交本轮相关变更）

## 目标
- 产出一个干净的 commit（必要时拆分为 2 个 commit）
- push 到当前分支（不要改分支名，不要 rebase）

## 约束
- **必须先输出检查结果，再执行任何 add/commit/push**
- **只提交本轮 v8 相关文件**，不相关的变更要么还原要么暂存但不提交（说明原因）
- 如果发现 `knowledge-base/entries/**` 有大量生成文件：
  - 只在本轮确实需要版本化时才提交
  - 否则先确认 `.gitignore` 策略，避免把大体量内容误提交

---

## Step 1: 检查工作区状态（只读）
在仓库根目录执行：

```bash
git status
```

```bash
git diff --stat
```

```bash
git diff
```

输出：
- 修改/新增文件清单（按目录分组）
- 是否存在大文件/大量条目

## Step 2: 生成“提交白名单”
只允许纳入本轮的典型目录：
- `kimi/` 下的 v8 任务文件（如 `task-v8-*.md`）
- `.tasks/v8-wechat-scrape/**`
- `scripts/wechat/**`
- `scripts/eval/**`（仅本轮确有改动时）

如果有超出范围的变更：
- 列出并说明（保留/还原/延后）

## Step 3: add（严格按白名单逐个添加）
示例（以实际文件为准，逐个 add，不要一把梭）：

```bash
git add kimi/task-v8-*.md
```

```bash
git add .tasks/v8-wechat-scrape
```

```bash
git add scripts/wechat
```

（如有其它具体文件，逐个 `git add path/to/file`）

## Step 4: commit
commit message 模板（二选一或拆分两次 commit）：

1)
```bash
git commit -m "v8: finalize wechat scrape pipeline tasks"
```

2)
```bash
git commit -m "v8: fix wechat scripts for full sync & download"
```

## Step 5: push

```bash
git push
```

## Step 6: 输出收尾报告
写入 `kimi/git-wrapup-v8-report.md`：
- `git status`（commit 后）
- commit hash
- push 结果
- 若有未提交变更：列表 + 原因
