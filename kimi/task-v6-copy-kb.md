# T3 任务: 拷贝 v6 新生成 KB 文件到归档目录

## 任务目标
将本轮 v6-kb-expansion 新生成的 84 个 KB 文件拷贝到用户指定的归档目录。

## 拷贝规格

**源目录**：
`knowledge-base/entries/first-batch-drafts/`（只取 KB-20260409-* 文件，共 84 个）

**目标目录**：
`C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409\`

## 执行步骤

1. 创建目标目录（如不存在）
2. 将 `knowledge-base/entries/first-batch-drafts/KB-20260409-*.md` 共 84 个文件拷贝到目标目录
3. 验证目标目录文件数量 = 84
4. 列出目标目录前 5 个和后 5 个文件名，确认范围正确

## 执行方式

请使用 PowerShell 命令完成操作：

```powershell
# Step 1: 创建目标目录
New-Item -ItemType Directory -Force -Path "C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409"

# Step 2: 拷贝文件
Copy-Item "knowledge-base\entries\first-batch-drafts\KB-20260409-*.md" "C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409\"

# Step 3: 验证数量
(Get-ChildItem "C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409\").Count

# Step 4: 列出前5和后5
Get-ChildItem "C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409\" | Select-Object -First 5 | Select-Object Name
Get-ChildItem "C:\Users\Administrator\Documents\yixiaoguan\医小管知识库\v6-20260409\" | Select-Object -Last 5 | Select-Object Name
```

请执行以上命令并报告结果。
