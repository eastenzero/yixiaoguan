# T0 → 新 T1 交接简报

**日期**: 2026-04-06 13:00
**写作者**: T0 Architect (Cascade)
**背景**: spec-v4-student-enhancement 由上一个 T1 执行，T0 复核发现多项问题，已做外科手术修复代码层面 bug。现在需要新 T1 完成剩余运维类任务。

---

## 当前 Git 状态

```
分支: main
HEAD: b286000 fix(status): add theme.scss import
上一个: c88959d merge: t0-hotfix-v4 into main (V4 外科手术修复)
```

**所有 V4 代码已提交到 main**，工作区干净（仅有 temp/ 残留和部署配置 diff）。

---

## 已完成的任务（不需要再做）

| 任务 | 状态 | 备注 |
|------|------|------|
| F-V4-01 知识详情 API 对接 | ✅ | knowledge/detail.vue + api/knowledge.ts |
| F-V4-02 主题色 Token 统一 | ✅ | 11 文件，残留 5 处不可用 SCSS 的位置 |
| F-V4-03 聊天历史页 | ✅ | history.vue + pages.json 路由 |
| F-V4-04 统计卡片 | ✅ | services/index.vue |
| F-V4-05 快捷问题 | ✅ | 本地 DEFAULT_QUESTIONS，远程获取已注释待后端实现 |
| F-V4-05-A2 来源弹层 markdown | ✅ | v-html + renderMarkdown() |
| F-V4-06 Chat 集成增强 | ✅ | 会话持久化 + 历史导航 + 来源闭环 |
| F-V4-GR eval-set | ✅ | 42 用例已提交 |
| T0 hotfix: sendMessage 契约 | ✅ | {content, messageType:1} |
| T0 hotfix: getSuggestions 404 | ✅ | 已移除远程调用 |
| T0 hotfix: status.vue 编译 500 | ✅ | 补 @import theme.scss |
| T0 hotfix: login.vue 回归 | ✅ | 恢复 $primary |

## ❗ 需要新 T1 完成的任务

### TASK-1: KB 入库 (P0, 阻塞)

**问题**: 22 个新 KB 文件 (KB-0150 ~ KB-0171) 已 commit 到 git，但**从未执行入库到 ChromaDB**。这是"AI 回答变少"的根因。

**操作**:
1. SSH 到 165 服务器
2. 停止 ai-service
3. 执行全量重入库：`python scripts/batch_ingest_kb.py --yes`
4. 重启 ai-service
5. 验证 `/kb/stats` entry_count 增长

**KB 文件位置**: `knowledge-base/raw/first-batch-processing/converted/markdown/`
**当前文件数**: 77 个 .md（55 旧 + 22 新）
**入库脚本**: `services/ai-service/scripts/batch_ingestion.py`

**注意**: 两份参考文档（`学生手册-生活服务.md` 和 `医小管知识库二次修改版.md`）放在 `converted/` 而非 `converted/markdown/`，正常不会被入库脚本扫到。请确认它们没有被移动。

### TASK-2: 端到端验证 (P0)

入库完成后，在 localhost 测试以下问题：
- "怎么交电费" → 应返回完美校园APP操作步骤
- "东西坏了怎么报修" → 应返回后勤管理部流程
- "校园卡怎么办理" → 应返回实体卡+虚拟码+三种充值方式
- "怎么申请奖学金" → 应保持之前的正确回答
- "请假流程是什么" → 应有详细回答

### TASK-3: temp/ 清理 (P2, 非阻塞)

上一个 T1/T2 留下大量测试脚本和日志在 `temp/` 目录。建议：
```bash
git clean -fd temp/
```

---

## 关键上下文

### 165 服务器
- SSH: `easten@192.168.100.165`
- 项目路径: `~/dev/yixiaoguan/`
- ai-service 运行在 Tmux `ai-service` 窗口
- Mutagen 从 Windows 单向同步到 165

### 开发约定
- **本轮只做本地开发**，不涉及远程部署
- 所有 KB 入库操作在 165 上执行（ChromaDB 在那里）
- 前端开发/测试在 Windows localhost:5175

### 技术债记录 (DEBT-V4-01)
5 处 #006a64 硬编码在 template/JS/JSON 中无法用 SCSS 变量替换：
1. `pages.json:84` — tabBar selectedColor (JSON)
2. `chat/index.vue:38` — template :color attr
3. `apply/status.vue:291` — JS confirmColor
4. `apply/detail.vue:321` — JS confirmColor
5. `CustomTabBar.vue:11` — template JS expression

这些是已知残留，非 bug。
