# 窗口 2 启动包（移交文档）

> 此文件将在 Checkpoint 4 通过后由窗口 1 生成  
> 当前为模板，实际内容将在移交时填充

**生成时间**: [待填充]  
**生成者**: 窗口 1（T1-Coordinator）  
**接收者**: 窗口 2（T1-Integrator）

---

## 🎯 移交摘要

**状态**: ⏳ 等待 Checkpoint 4 通过

**完成情况**:
- Batch 1: [待填充]
- Batch 2: [待填充]
- Batch KB: [待填充]
- Batch Verify: [待填充]

**总体进度**: [待填充] / 9 任务完成

---

## 📋 任务完成清单

### Batch 1（并行）

| 任务 ID | 名称 | 负责人 | 状态 | 完成时间 | L0-L1 验证 |
|---------|------|--------|------|---------|-----------|
| F-V4-01 | 知识详情页 API 对接 | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-02 | 主题色 Token 统一 | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-03 | 聊天历史记录 | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-04 | 事务导办统计卡片 | [待填充] | [待填充] | [待填充] | [待填充] |

### Batch 2（串行）

| 任务 ID | 名称 | 负责人 | 状态 | 完成时间 | L0-L1 验证 |
|---------|------|--------|------|---------|-----------|
| F-V4-05 | 快捷问题动态化 | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-05-A2 | 来源弹层 Markdown | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-06 | Chat 集成 | [待填充] | [待填充] | [待填充] | [待填充] |

### Batch KB + Verify

| 任务 ID | 名称 | 负责人 | 状态 | 完成时间 | L0-L1 验证 |
|---------|------|--------|------|---------|-----------|
| F-V4-KB | 知识库扩量 | [待填充] | [待填充] | [待填充] | [待填充] |
| F-V4-GR | AI 防幻觉验证 | [待填充] | [待填充] | [待填充] | [待填充] |

---

## ✅ 检查点验证记录

### Checkpoint 1: FC-1 完成
- **时间**: [待填充]
- **状态**: [待填充]
- **验证结果**: [待填充]

### Checkpoint 2: DK-1 完成
- **时间**: [待填充]
- **状态**: [待填充]
- **验证结果**: [待填充]

### Checkpoint 3: FU-1 完成
- **时间**: [待填充]
- **状态**: [待填充]
- **验证结果**: [待填充]

### Checkpoint 4: 所有任务完成
- **时间**: [待填充]
- **状态**: [待填充]
- **验证结果**: [待填充]

---

## ⚠️ 已知问题清单

| 问题 ID | 描述 | 严重性 | 相关任务 | 状态 | 备注 |
|---------|------|--------|---------|------|------|
| [待填充] | [待填充] | [待填充] | [待填充] | [待填充] | [待填充] |

**如无问题，此表为空**

---

## 📁 关键文件路径

### 任务文档
- 主任务: `.tasks/v4-student-enhancement/_task.md`
- 集成验收: `.tasks/v4-student-enhancement/int-v4-final/_task.md`
- 执行摘要: `.tasks/v4-student-enhancement/_execution_summary.md`
- 进度跟踪: `.tasks/v4-student-enhancement/_progress.md`

### 各任务报告
- F-V4-01: `.tasks/v4-student-enhancement/f01-knowledge-detail-api/_report.md`
- F-V4-02: `.tasks/v4-student-enhancement/f02-theme-token-unify/_report.md`
- F-V4-03: `.tasks/v4-student-enhancement/f03-chat-history/_report.md`
- F-V4-04: `.tasks/v4-student-enhancement/f04-services-stats/_report.md`
- F-V4-05: `.tasks/v4-student-enhancement/f05-quick-questions-dynamic/_report.md`
- F-V4-05-A2: `.tasks/v4-student-enhancement/f05a2-source-preview-markdown/_report.md`
- F-V4-06: `.tasks/v4-student-enhancement/f06-chat-integration/_report.md`
- F-V4-KB: `.tasks/v4-student-enhancement/fkb-knowledge-expansion/_report.md`
- F-V4-GR: `.tasks/v4-student-enhancement/fgr-ai-grounding-verify/_report.md`

### 代码文件
- 前端代码: `apps/student-app/src/`
- 知识库: `knowledge-base/raw/first-batch-processing/converted/markdown/`
- 测试报告: `docs/test-reports/`

---

## 🎯 集成验收任务（INT-V4-FINAL）

### 任务文档
**路径**: `.tasks/v4-student-enhancement/int-v4-final/_task.md`

### 10 个验收标准（AC）

#### AC-1: 知识详情页从 AI 来源点击可进入，显示完整条目
**覆盖**: F-V4-01, F-V4-06  
**验证步骤**: [见任务文档]

#### AC-2: 所有页面 grep #006a64 仅剩 theme.scss 定义行
**覆盖**: F-V4-02  
**验证步骤**: [见任务文档]

#### AC-3: 会话历史页可列出/新建会话
**覆盖**: F-V4-03  
**验证步骤**: [见任务文档]

#### AC-4: 事务导办页统计卡片显示
**覆盖**: F-V4-04  
**验证步骤**: [见任务文档]

#### AC-5: 快捷问题非硬编码
**覆盖**: F-V4-05  
**验证步骤**: [见任务文档]

#### AC-6: 来源弹层 markdown 正确渲染
**覆盖**: F-V4-05-A2  
**验证步骤**: [见任务文档]

#### AC-7: Chat 页面有历史入口，来源点击跳详情页
**覆盖**: F-V4-06  
**验证步骤**: [见任务文档]

#### AC-8: KB entry_count ≥ 75
**覆盖**: F-V4-KB  
**验证步骤**: [见任务文档]

#### AC-9: 拒答准确率 100%，Recall@5 ≥ 90%
**覆盖**: F-V4-GR  
**验证步骤**: [见任务文档]

#### AC-10: TypeScript 编译零错误，所有已有功能无回归
**覆盖**: ALL  
**验证步骤**: [见任务文档]

---

## 🛠️ 测试环境启动命令

### 基础设施（PostgreSQL + Redis + AI Service）
```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\deploy
docker compose up -d
```

### business-api
```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\services\business-api
$env:POSTGRES_PASSWORD = "Yx@Admin2026!"
$env:REDIS_PASSWORD = "Yx@Redis2026!"
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f pom.xml spring-boot:run -pl ruoyi-admin
```

### student-app
```powershell
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app
npm run dev:h5
```

### 验证服务状态
```powershell
# PostgreSQL
docker ps | grep postgres

# Redis
docker ps | grep redis

# AI Service
curl http://localhost:8000/health

# business-api
curl http://localhost:8080/actuator/health

# student-app
# 浏览器访问 http://localhost:5174
```

---

## 📝 窗口 2 执行流程

### Step 1: 接收启动包（当前步骤）
- [x] 阅读本文档
- [ ] 确认任务完成情况
- [ ] 了解已知问题

### Step 2: 准备测试环境
- [ ] 启动基础设施
- [ ] 启动 business-api
- [ ] 启动 student-app
- [ ] 验证服务状态

### Step 3: 执行集成验收
- [ ] 阅读 INT-V4-FINAL 任务文档
- [ ] 执行 10 个 AC 验证
- [ ] 记录验证结果

### Step 4: 编写验收报告
- [ ] 创建 `int-v4-final/_report.md`
- [ ] 记录问题清单
- [ ] 提出改进建议

### Step 5: 签字发布
- [ ] 更新主任务状态
- [ ] 通知窗口 1
- [ ] 发布决策

---

## 🔄 窗口间协作

### 如发现问题需要修复

**窗口 2 操作**:
1. 在下方"问题反馈"区域记录问题
2. 通知窗口 1 协调修复
3. 等待修复完成后继续验收

### 问题反馈区域

| 问题 ID | 描述 | 严重性 | 需要修复的任务 | 状态 | 备注 |
|---------|------|--------|---------------|------|------|
| [窗口 2 填充] | [窗口 2 填充] | [窗口 2 填充] | [窗口 2 填充] | [窗口 2 填充] | [窗口 2 填充] |

---

## ✅ 窗口 2 启动检查清单

- [ ] 已阅读本启动包
- [ ] 已确认任务完成情况
- [ ] 已了解已知问题
- [ ] 已阅读 INT-V4-FINAL 任务文档
- [ ] 已准备测试环境
- [ ] 已验证服务状态
- [ ] 准备开始集成验收

---

## 📞 联系方式

- **窗口 1（T1-Coordinator）**: 继续监控，处理问题
- **指挥官**: 最终决策

---

**窗口 2 准备就绪，开始集成验收！** 🚀
