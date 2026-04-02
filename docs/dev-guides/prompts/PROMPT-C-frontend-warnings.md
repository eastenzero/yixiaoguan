# 【提示词 C】前端废弃 API 警告清理（代码质量修复）

> **状态**：待执行 | **预估工时**：1小时 | **可并行**：是，与 Prompt-A/B 无依赖冲突（操作不同文件）

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 Vue3 前端工程师**。

**【背景材料——开始前必须全部阅读】**
 
1. `.globalrules`（项目全局规则）
2. `apps/teacher-web/src/router/index.ts`（当前路由守卫写法）
3. `apps/teacher-web/src/views/DashboardView.vue`（样本页面，检查 `el-link` 用法）
4. `apps/teacher-web/src/views/QuestionsView.vue`（样本页面）
5. `apps/teacher-web/src/views/ApprovalView.vue`（样本页面）
6. `apps/teacher-web/src/views/KnowledgeView.vue`（样本页面） 
7. `apps/teacher-web/package.json`（确认 Element Plus 版本）

**【已知的警告清单（你需要全部修复）】**

| 警告类型 | 所在位置 | 修复方向 |
|---------|---------|---------|
| Vue Router 4 导航守卫 `next()` 废弃写法 | `router/inde x.ts` | 将 `next()` 改为 `return` 语句，将 `next('/path')` 改为 `return '/path'` 或 `return { path: '/path' }` |
| `el-link` 的 `underline` 属性传布尔值废弃 | 各 View 文件中 `:underline="false"` | Element Plus 2.x 最新版中 `underline` 接受字符串 `'always'\|'hover'\|'never'`，将 `:underline="false"` 改为 `underline="never"` |
| `el-tag` 的 `type` 属性传空字符串警告 | 具体位置需你从代码中定位 | 添加条件判断或默认值，确保 `type` 属性不传空字符串 |

**【你的交付物】**

逐一修复以上 3 类警告，涉及的文件可能包括（但不限于）：

1. `apps/teacher-web/src/router/index.ts`
2. `apps/teacher-web/src/views/DashboardView.vue`
3. `apps/teacher-web/src/views/QuestionsView.vue`
4. `apps/teacher-web/src/views/ApprovalView.vue`
5. `apps/teacher-web/src/views/KnowledgeView.vue`
6. 其他你在代码中发现存在同类问题的文件

**【禁止清单（严格遵守）】**

- ❌ 本次任务只做**警告修复**，禁止改动任何业务逻辑、API 调用、数据处理代码
- ❌ 禁止修改 CSS / SCSS 样式
- ❌ 禁止修改 `src/api/` 下任何文件（API 路径问题由另一个任务处理）
- ❌ 禁止升级或降级任何 npm 包版本
- ❌ 禁止修改 `src/stores/` 下任何文件
- ❌ 如果发现警告的根因和上述描述不符，停下来告知我，不要擅自推测修复
- ❌ 每次修改只处理一个文件，修改完后汇报，等我确认再处理下一个

**【工作方式】**

第一步：全局搜索以上 3 类问题，列出所有受影响的文件路径与行号，等待我的"同意"。  
第二步：收到"同意"后，按文件逐一修复，每修复完一个文件汇报变更内容。

**【完成标准】**

✅ `router/index.ts` 中不再出现 `next()` 调用风格  
✅ 全局搜索 `:underline="false"` 结果为 0  
✅ 全局搜索 `type=""` 或 `type=''` 在 `el-tag` 上的用法结果为 0  
✅ 前端开发服务器运行后，浏览器控制台中上述三类警告消失  

满足以上标准后，请明确回复 **"阶段任务 C 完成并停止"**，不要继续优化其他内容。

**现在，请开始第一步：全局搜索代码库，列出所有受影响的文件和行号。**
