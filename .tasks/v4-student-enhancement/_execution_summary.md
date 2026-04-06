# V4 执行摘要 — 快速启动指南

> 给执行者的快速参考，5 分钟了解全貌

---

## 🎯 本轮目标

功能补全 + 质量提升 + 知识库扩量

---

## 📊 任务总览

| 批次 | 任务数 | 并行 | 预计时间 | 状态 |
|------|--------|------|---------|------|
| batch_1 | 4 | ✅ | 6-8h | ⏳ 待执行 |
| batch_2 | 3 | ❌ 串行 | 5-7h | ⏳ 待 batch_1 |
| batch_kb | 1 | ✅ 独立 | 6-8h | ⏳ 可立即开始 |
| batch_verify | 1 | - | 2-3h | ⏳ 待 batch_kb |
| batch_int | 1 | - | 2-3h | ⏳ 最终验收 |

**总计**: 9 个任务，15-21 小时（最优路径）

---

## 🚀 立即可执行

### Batch 1（并行，零冲突）
```
✅ f01-knowledge-detail-api      [P0] 1-2h  知识详情页 API 对接
✅ f02-theme-token-unify         [P1] 1h    主题色 Token 统一
✅ f03-chat-history              [P0] 3-4h  聊天历史记录
✅ f04-services-stats            [P2] 1-2h  事务导办统计卡片
```

### Batch KB（独立通道，可并行）
```
✅ fkb-knowledge-expansion       [P0] 6-8h  知识库扩量（55→75+）
```

---

## ⏳ 等待依赖

### Batch 2（串行，依赖 batch_1）
```
→ f05-quick-questions-dynamic    [P1] 1-2h  快捷问题动态化
  → f05a2-source-preview-markdown [P1] 0.5-1h 来源弹层 Markdown
    → f06-chat-integration        [P0] 3-4h  Chat 集成（最终）
```

### Batch Verify（依赖 batch_kb）
```
→ fgr-ai-grounding-verify        [P1] 2-3h  AI 防幻觉验证
```

### Batch Int（依赖 batch_2 + batch_verify）
```
→ int-v4-final                   [P0] 2-3h  集成验收（10 个 AC）
```

---

## 📁 任务文件位置

```
.tasks/v4-student-enhancement/
├── f01-knowledge-detail-api/_task.md
├── f02-theme-token-unify/_task.md
├── f03-chat-history/_task.md
├── f04-services-stats/_task.md
├── f05-quick-questions-dynamic/_task.md
├── f05a2-source-preview-markdown/_task.md
├── f06-chat-integration/_task.md
├── fkb-knowledge-expansion/_task.md
├── fgr-ai-grounding-verify/_task.md
└── int-v4-final/_task.md
```

每个 `_task.md` 包含：
- 目标和背景
- 技术要点
- 完成标准（L0-L3）
- 文件清单
- 验证命令

---

## ✅ 验收标准速查

1. **AC-1**: 知识详情页可进入，显示完整条目
2. **AC-2**: grep #006a64 仅剩 theme.scss
3. **AC-3**: 会话历史页可列出/新建会话
4. **AC-4**: 事务导办页统计卡片显示
5. **AC-5**: 快捷问题非硬编码
6. **AC-6**: 来源弹层 markdown 正确渲染
7. **AC-7**: Chat 页面有历史入口，来源点击跳详情页
8. **AC-8**: KB entry_count ≥ 75
9. **AC-9**: 拒答准确率 100%，Recall@5 ≥ 90%
10. **AC-10**: 编译零错误，无回归

---

## ⚠️ 关键注意事项

1. **Batch 1 可并行**：4 个任务文件零冲突，可同时下发
2. **Batch 2 必须串行**：严格按 F-V4-05 → F-V4-05-A2 → F-V4-06 顺序
3. **Batch KB 独立**：与前端完全并行，可由独立人员执行
4. **F-V4-06 改动大**：是 chat/index.vue 的最终集成，需重点 review
5. **后端可选**：L0-L2 可在无后端情况下通过，L3 需要 business-api

---

## 🛠️ 快速启动命令

### 编译检查
```powershell
cd apps/student-app
npm run type-check
npm run lint
```

### 启动服务（L3 验证需要）
```powershell
# 基础设施
cd deploy
docker compose up -d

# business-api
cd ../services/business-api
$env:POSTGRES_PASSWORD = "Yx@Admin2026!"
$env:REDIS_PASSWORD = "Yx@Redis2026!"
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f pom.xml spring-boot:run -pl ruoyi-admin

# student-app
cd ../../apps/student-app
npm run dev:h5
```

---

## 📞 遇到问题？

1. 先查看任务的 `_task.md` 文件
2. 检查 `.teb/antipatterns.md` 错题本
3. 参考 `.teb/guides/verification-guide.md` 验证指南
4. 联系 T1 协调员

---

**准备好了吗？开始执行！** 🚀
