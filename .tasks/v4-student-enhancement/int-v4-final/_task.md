# INT-V4-FINAL：V4 学生端增强集成验收

## 元信息
- **任务 ID**: INT-V4-FINAL
- **优先级**: P0
- **类型**: integration
- **批次**: batch_int
- **预计工作量**: 2-3 小时
- **前置依赖**: batch_1, batch_2, batch_kb, batch_verify 全部完成

## 目标

对 spec-v4-student-enhancement 的所有功能进行端到端集成验收，确保所有改动协同工作，无回归问题。

## 验收范围

本次集成验收覆盖以下模块：
- F-V4-01: 知识详情页 API 对接
- F-V4-02: 主题色 Token 统一
- F-V4-03: 聊天历史记录
- F-V4-04: 事务导办统计卡片
- F-V4-05: 快捷问题动态化
- F-V4-05-A2: 来源弹层 Markdown 渲染
- F-V4-06: Chat 页面集成增强
- F-V4-KB: 知识库扩量
- F-V4-GR: AI 防幻觉验证

## 验收标准（AC）

### AC-1: 知识详情页从 AI 来源点击可进入，显示完整条目
**覆盖**: F-V4-01, F-V4-06

**测试步骤**:
1. 启动 business-api 和 ai-service
2. H5 预览 → 智能问答
3. 发送问题："如何申请空教室？"
4. 点击 AI 回复中的来源引用
5. 验证跳转到知识详情页
6. 验证显示完整条目（标题、正文、标签）

**预期结果**: ✅ 详情页正确显示，Markdown 格式正确渲染

---

### AC-2: 所有页面 grep #006a64 仅剩 theme.scss 定义行
**覆盖**: F-V4-02

**测试步骤**:
```powershell
cd apps/student-app/src
grep -r '#006a64' . --exclude-dir=node_modules
```

**预期结果**: ✅ 仅输出 `styles/theme.scss:XX:$primary: #006a64;`

---

### AC-3: 会话历史页可列出/新建会话
**覆盖**: F-V4-03

**测试步骤**:
1. H5 预览 → 智能问答
2. 点击导航栏"历史记录"按钮
3. 验证跳转到会话历史页
4. 验证显示历史会话列表（或空状态）
5. 点击"新建对话"按钮
6. 验证创建新会话并跳转到对话页

**预期结果**: ✅ 历史页功能正常，UI 与 chat 页面风格统一

---

### AC-4: 事务导办页统计卡片显示
**覆盖**: F-V4-04

**测试步骤**:
1. H5 预览 → 事务导办
2. 验证顶部显示统计卡片区域
3. 验证显示"进行中的申请"数量
4. 验证显示"待处理通知"数量（可为 0 或 mock）

**预期结果**: ✅ 统计卡片正确显示，数据获取失败时显示 "--"

---

### AC-5: 快捷问题非硬编码
**覆盖**: F-V4-05

**测试步骤**:
```powershell
cd apps/student-app/src
grep -A 10 "quickQuestions" pages/chat/index.vue
```

**预期结果**: ✅ quickQuestions 为 ref 响应式数据，非 const 硬编码

---

### AC-6: 来源弹层 markdown 正确渲染
**覆盖**: F-V4-05-A2

**测试步骤**:
1. H5 预览 → 智能问答
2. 发送问题，获得 AI 回复
3. 点击来源引用（无 entryId 的来源，触发弹层）
4. 验证弹层内容 Markdown 正确渲染（粗体、列表、标题等）

**预期结果**: ✅ 弹层内容格式化显示，无原始 Markdown 标记裸露

---

### AC-7: Chat 页面有历史入口，来源点击跳详情页
**覆盖**: F-V4-06

**测试步骤**:
1. H5 预览 → 智能问答
2. 验证导航栏有"历史记录"按钮
3. 点击历史按钮，验证跳转到历史页
4. 返回对话页，发送问题
5. 点击来源引用（有 entryId），验证跳转到详情页
6. 刷新页面，验证消息从后端恢复（需 business-api）

**预期结果**: ✅ 所有集成功能正常工作

---

### AC-8: KB entry_count ≥ 75
**覆盖**: F-V4-KB

**测试步骤**:
```powershell
curl http://localhost:8000/kb/stats
```

**预期结果**: ✅ 返回 `{"entry_count": 75+, "chunk_count": ...}`

---

### AC-9: 拒答准确率 100%，Recall@5 ≥ 90%
**覆盖**: F-V4-GR

**测试步骤**:
1. 阅读 `docs/test-reports/v4-grounding-verification.md`
2. 验证评测指标符合要求

**预期结果**: 
- ✅ 拒答准确率 = 100%
- ✅ Recall@5 ≥ 90%
- ✅ 误答率 = 0%

---

### AC-10: TypeScript 编译零错误，所有已有功能无回归
**覆盖**: ALL

**测试步骤**:
```powershell
cd apps/student-app
npm run type-check
npm run lint
npm run build:h5
```

**预期结果**: 
- ✅ 编译零错误
- ✅ Lint 无 error
- ✅ 构建成功

**回归测试**:
- 登录功能正常
- 首页个性化问候正常
- 事务导办功能正常
- 个人中心功能正常
- SSE 流式回复正常
- 复制按钮正常

---

## 验收流程

### 阶段 1: 静态检查（L0-L1）
```powershell
cd apps/student-app

# 编译检查
npm run type-check

# Lint 检查
npm run lint

# 主题色检查
cd src
grep -r '#006a64' . --exclude-dir=node_modules

# 快捷问题检查
grep -A 10 "quickQuestions" pages/chat/index.vue

# 构建检查
cd ..
npm run build:h5
```

### 阶段 2: 功能验收（L2）

启动服务：
```powershell
# 启动基础设施
cd deploy
docker compose up -d

# 启动 business-api
cd ../services/business-api
$env:POSTGRES_PASSWORD = "Yx@Admin2026!"
$env:REDIS_PASSWORD = "Yx@Redis2026!"
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f pom.xml spring-boot:run -pl ruoyi-admin

# 启动 student-app
cd ../../apps/student-app
npm run dev:h5
```

逐个验证 AC-1 到 AC-10。

### 阶段 3: 集成测试（L3）

完整用户流程测试：
1. 登录 → 首页 → 智能问答
2. 发送问题 → 查看回复 → 点击来源 → 查看详情
3. 返回对话 → 点击历史 → 查看历史会话
4. 新建对话 → 发送消息 → 刷新页面 → 验证消息恢复
5. 事务导办 → 查看统计 → 申请空教室
6. 个人中心 → 查看信息 → 退出登录

## 问题记录

如发现问题，记录到此处：

| 问题 ID | 描述 | 严重性 | 相关任务 | 状态 |
|---------|------|--------|---------|------|
| - | - | - | - | - |

## 验收结论

- [ ] 所有 AC 通过
- [ ] 无阻塞性问题
- [ ] 无严重回归
- [ ] 可以发布

**签字**: ___________  
**日期**: ___________

## 回滚方案

如验收失败，回滚步骤：
1. 切换到 spec-v3 完成时的 commit
2. 重新审查失败的任务
3. 修复后重新验收

## 文件清单

### 必须阅读
- 所有任务的 `_task.md` 和 `_report.md`
- `docs/test-reports/v4-grounding-verification.md`

### 必须执行
- 所有 AC 的测试步骤
- 静态检查命令
- 构建命令

## 注意事项

- 验收需要 business-api 和 ai-service 都在运行
- 部分 AC（如 AC-7 的消息恢复）需要后端支持
- 如后端未运行，L0-L2 仍可验证，L3 需要后端
- 发现问题及时记录，不要跳过

## 参考资料

- TEB 验证指南：`.teb/guides/verification-guide.md`
- Spec V4 文档：`.tasks/_spec-v4-student-enhancement.yaml`
- 各任务文档：`.tasks/v4-student-enhancement/*/`
