# T3 任务: 前端重构产出合并 + 补丁修复

## 任务背景
AI Studio 生成的前端重构代码已通过校验（CONDITIONAL PASS），需要：
1. Git 安全操作（提交 + 新建分支）
2. 将 AI Studio 产出覆盖到 student-app
3. 补丁修复缺失的 API 函数和组件
4. 编译验证

## Step 1: Git 安全操作

```powershell
# 1.1 提交当前所有改动到 main（含 v8 知识库 + 审计报告等）
cd C:\Users\Administrator\Documents\code\yixiaoguan
git add -A
git commit -m "checkpoint: before v9 frontend redesign - KB v8 complete (731 entries)"

# 1.2 创建新分支
git checkout -b feat/v9-purple-theme
```

**验证**: `git branch` 确认当前在 `feat/v9-purple-theme` 分支。

## Step 2: 覆盖前端文件

将 AI Studio 产出覆盖到 student-app/src/：

```powershell
$src = "C:\Users\Administrator\Documents\code\yixiaoguan\ai-studio-output"
$dst = "C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app\src"

# 2.1 覆盖页面文件（12个）
# 遍历 ai-studio-output 中的 pages/ 目录，复制到 $dst/pages/
Copy-Item "$src\pages\*" "$dst\pages\" -Recurse -Force

# 2.2 覆盖 API 文件
Copy-Item "$src\api\*" "$dst\api\" -Recurse -Force

# 2.3 覆盖工具文件
Copy-Item "$src\utils\request.ts" "$dst\utils\request.ts" -Force

# 2.4 覆盖 Store 文件
Copy-Item "$src\stores\user.ts" "$dst\stores\user.ts" -Force

# 2.5 覆盖/新建样式文件
Copy-Item "$src\styles\theme.scss" "$dst\styles\theme.scss" -Force
```

**注意**: 
- 只覆盖 AI Studio 输出的文件，不删除原有文件（保留图标组件等）
- 如果 ai-studio-output 的目录结构与上述不同，请先 `Get-ChildItem -Recurse` 查看实际结构后再调整路径

## Step 3: 补丁修复 — 补充缺失的 API 函数

从原始源码（可通过 `git show main:apps/student-app/src/api/chat.ts` 查看）补充缺失函数。

### 3.1 chat.ts — 补充 4 个缺失函数

打开新的 `$dst/api/chat.ts`，在文件末尾（export 之前）添加以下函数：

```typescript
// === 以下从原始源码补充 ===

// 获取会话详情
export function getConversationDetail(id: number | string) {
  return request({
    url: `/api/v1/conversations/${id}`,
    method: 'GET'
  })
}

// 更新会话标题
export function updateConversationTitle(id: number | string, title: string) {
  return request({
    url: `/api/v1/conversations/${id}/title`,
    method: 'PUT',
    data: { title }
  })
}

// 关闭会话
export function closeConversation(id: number | string) {
  return request({
    url: `/api/v1/conversations/${id}`,
    method: 'DELETE'
  })
}

// 分页获取消息
export function getMessagePage(conversationId: number | string, params?: any) {
  return request({
    url: `/api/v1/conversations/${conversationId}/messages/page`,
    method: 'GET',
    data: params
  })
}
```

**⚠️ 重要**: 以上是示意代码。请先用 `git show main:apps/student-app/src/api/chat.ts` 查看原始实现，确保参数签名和内部逻辑完全一致后再添加。

### 3.2 apply.ts — 补充 deleteApplication

```typescript
// 删除申请
export function deleteApplication(id: number | string) {
  return request({
    url: `/api/v1/classroom-applications/${id}`,
    method: 'DELETE'
  })
}
```

同样请先对照原始源码确认。

### 3.3 notification.ts — 补充 markAsRead

```typescript
// 标记通知为已读
export function markAsRead(id: number | string) {
  return request({
    url: `/api/v1/notifications/${id}/read`,
    method: 'GET'
  })
}
```

同样请先对照原始源码确认。

## Step 4: 确认组件文件

AI Studio 产出中图标组件不全（仅 2 个），但原始的 `components/icons/` 目录**未被覆盖删除**（Step 2 是增量覆盖），所以原有的 45+ 个图标组件应该还在。

验证：
```powershell
(Get-ChildItem "$dst\components\icons\*.vue").Count
# 预期: ≥ 45
```

同理检查业务组件：
```powershell
Test-Path "$dst\components\BentoCard.vue"
Test-Path "$dst\components\LinkCard.vue"
Test-Path "$dst\components\StatusBadge.vue"
# 预期: 全部 True（原始文件未被删除）
```

如果有缺失，从 main 分支恢复：
```powershell
git checkout main -- apps/student-app/src/components/
```

## Step 5: 编译验证

```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app
npm run build 2>&1 | Tee-Object -FilePath "C:\Users\Administrator\Documents\code\yixiaoguan\kimi\v9-build-log.txt"
```

如果编译报错：
1. 记录错误信息
2. 分析是类型错误还是缺失导入
3. 逐个修复

## Step 6: 提交 + 输出报告

```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan
git add -A
git commit -m "feat(student-app): v9 purple theme redesign - AI Studio output + patches"
```

输出报告到 `kimi/report-v9-apply.md`：

```markdown
# V9 前端重构合并报告

## Git 操作
- main 分支最后提交: {commit hash}
- 当前分支: feat/v9-purple-theme

## 文件覆盖
| 操作 | 文件数 |
|------|--------|
| 覆盖页面 | ? |
| 覆盖 API | ? |
| 覆盖工具 | ? |
| 补丁 API 函数 | 6 |

## 编译结果
- 编译状态: PASS/FAIL
- 错误数: ?
- 警告数: ?

## 组件完整性
- 图标组件数量: ?
- 业务组件: BentoCard ✅/❌, LinkCard ✅/❌, StatusBadge ✅/❌
```
