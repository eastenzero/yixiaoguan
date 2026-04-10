# Gemini CLI 子代理下发模板（T0 协调用）

> 用途：Cascade/T0 通过 Gemini CLI 下发前端重构等代码生成任务。
> 版本：Gemini CLI 0.34.0，已验证可用。

---

## 1) 环境信息

| 项目 | 值 |
|------|-----|
| CLI 版本 | 0.34.0 |
| 安装方式 | `npm install -g @google/gemini-cli` |
| 升级命令 | `npm install -g @google/gemini-cli@latest` |
| 认证方式 | Google 账号 OAuth（首次运行自动引导） |
| MCP 服务器 | chrome-devtools（自动注册） |

---

## 2) 模型选择

### 可用别名（推荐）

| 别名 | 实际路由 | 用途 |
|------|---------|------|
| `pro` | gemini-3.1-pro-preview → 降级到 gemini-2.5-pro | 复杂任务（前端重构、架构设计） |
| `flash` | gemini-2.0-flash-thinking-exp | 简单任务（格式转换、小修改） |
| `auto` | 自动判断复杂度选择 Pro/Flash | 默认推荐 |

### 直接指定模型名

| 模型名 | 状态 |
|--------|------|
| `gemini-3.1-pro-preview` | ✅ 可用（可能遇到容量限制 429，会自动重试） |
| `gemini-2.5-pro` | ✅ 可用（pro 的降级目标） |
| `gemini-2.5-flash` | ✅ 可用 |
| `gemini-2.0-flash-thinking-exp` | ✅ 可用（flash 的默认） |

### 命令行指定

```powershell
# 别名方式（推荐）
gemini -m pro -p "你的提示词"

# 直接指定模型
gemini -m gemini-3.1-pro-preview -p "你的提示词"
```

### 容量不足处理

`gemini-3.1-pro-preview` 可能返回 429 (MODEL_CAPACITY_EXHAUSTED)。
CLI 会自动重试并降级到 `gemini-2.5-pro`，无需手动干预。

---

## 3) 非交互模式（Headless）

用于 Cascade 自动下发任务，不需要人工交互。

### 基本用法

```powershell
# 直接传入提示词
gemini -m pro -p "你的任务描述"

# 从文件读取提示词（通过管道）
Get-Content task-file.md | gemini -m pro -p "执行以下任务"

# YOLO 模式（自动批准所有文件操作）
gemini -m pro -y -p "你的任务描述"
```

### 审批模式

| 参数 | 说明 |
|------|------|
| `--approval-mode default` | 每次操作都需确认（最安全） |
| `--approval-mode auto_edit` | 自动批准编辑，其他需确认 |
| `--approval-mode yolo` | 自动批准所有操作（⚠️ 慎用） |
| `-y` / `--yolo` | 等同 `--approval-mode yolo` |

### 在 Cascade 中调用

```powershell
# 非阻塞执行（推荐，长任务）
# 在 run_command 中设置 Blocking=false, WaitMsBeforeAsync=5000

gemini -m pro --approval-mode yolo -p "任务描述..."

# 阻塞执行（短任务）
gemini -m flash -p "简单任务..."
```

---

## 4) 单任务下发模板

### 纯生成任务（不操作文件系统）

```powershell
gemini -m pro -p "
你是一个 Vue 3 + UniApp + SCSS 前端专家。

任务：根据以下设计稿描述，生成 pages/login/index.vue 的完整代码。

设计要求：
[具体的页面设计描述]

技术约束：
- Vue 3 <script setup lang='ts'>
- UniApp API (uni.navigateTo, uni.request 等)
- SCSS 样式，使用项目主题变量
- 移动端 375px 宽度

输出：只输出完整的 .vue 文件代码，不要解释。
"
```

### 文件操作任务（需要 yolo 模式）

```powershell
gemini -m pro --approval-mode yolo -p "
在目录 C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app\src 下工作。

任务：重写 pages/login/index.vue，实现以下设计。

[设计描述]

规则：
- 只修改指定文件，不要碰其他文件
- 保留所有后端对接逻辑（API 调用、状态管理）
- 只改 UI 部分（template + style）
"
```

---

## 5) 多步骤任务拆分策略

前端重构等大任务应拆分为独立的单页面任务，逐个执行：

```
Step 1: Login 页面 → 验证效果
Step 2: Home 页面 → 验证效果
Step 3: Chat 页面 → 验证效果
...
```

### 每步的标准流程

1. **Git 快照**：`git add -A && git commit -m "wip: before page-X redesign"`
2. **下发任务**：`gemini -m pro -p "重写 pages/X/index.vue ..."`
3. **验证编译**：`npm run build`（在 student-app 目录）
4. **人工预览**：`npm run dev:h5` 查看效果
5. **决策**：满意 → commit；不满意 → `git checkout -- .` 回退

---

## 6) 稳定性注意事项

### 网络问题

- Gemini CLI 走 Google API（cloudcode-pa.googleapis.com），需要稳定的网络
- 如遇超时，CLI 会自动重试（默认最多 10 次）
- 设置 `general.retryFetchErrors: true` 可增强重试

### 容量限制

- 免费层有每日请求限制
- Pro 模型可能遇到 429 容量不足，自动降级到较低模型
- 高峰时段（美国工作时间）容量更紧张

### 输出截断

- 非常长的输出可能被截断
- 对于大文件生成，建议拆分为多个小任务
- 或使用 `--approval-mode yolo` 让 Gemini 直接写文件而非输出到终端

---

## 7) 配置文件

Gemini CLI 使用 `.gemini/settings.json`（项目级）或全局配置。

### 项目级配置示例

在项目根目录创建 `.gemini/settings.json`：

```json
{
  "model": {
    "name": "gemini-3.1-pro-preview"
  },
  "general": {
    "retryFetchErrors": true,
    "maxAttempts": 10
  }
}
```

### 系统提示词

在项目根目录创建 `.gemini/system.md`：

```markdown
你是一个专注于 Vue 3 + UniApp + TypeScript + SCSS 的前端专家。
项目名：医小管（YiXiaoGuan）— 山东第一医科大学智慧校园助手学生端。
主色调：#7C3AED（学院紫），渐变 #5B21B6 → #8B5CF6。
移动端优先，基准宽度 375px。
```

---

## 8) T0 验收速查（执行后）

1. 文件是否被正确生成/修改
2. `npm run build` 编译通过
3. 无超范围修改（只改了指定文件）
4. UI 样式与设计稿匹配（需人工预览）
5. 后端对接逻辑完整保留（API 调用、SSE、状态管理）
6. Git commit 记录清晰

---

## 9) 与 Kimi CLI 对比

| 维度 | Gemini CLI | Kimi CLI |
|------|-----------|----------|
| 模型 | Gemini 3.1 Pro / 2.5 Pro | Moonshot 系列 |
| 前端代码质量 | ✅ 较好（Google 训练数据丰富） | ⚠️ 一般（UI 审美较弱） |
| 文件操作 | ✅ 内置工具 | ✅ 内置工具 |
| 中文理解 | ✅ 良好 | ✅ 优秀 |
| 网络稳定性 | ⚠️ 需科学上网 | ✅ 国内直连 |
| 免费额度 | 有每日限制 | 有每日限制 |
| 非交互模式 | `-p` 参数 | `-p` 或 `--print` 参数 |

### 推荐分工

- **Gemini CLI**：前端 UI 重构、代码生成（审美好）
- **Kimi CLI**：知识库处理、中文内容生成、文件批量操作（中文强、网络稳）
