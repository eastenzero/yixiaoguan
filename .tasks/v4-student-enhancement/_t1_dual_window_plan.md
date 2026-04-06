# T1 双窗口协作方案

> 确保 T1 在监控和验收两个阶段都能高效工作

**创建时间**: 2026-04-06  
**状态**: ✅ 方案确定，待执行

---

## 🎯 核心策略

T1 使用 **2 个窗口** 分别负责：
1. **窗口 1（T1-Coordinator）**：任务监控与协调
2. **窗口 2（T1-Integrator）**：集成验收与发布

---

## 📋 窗口职责划分

### 窗口 1：T1-Coordinator（当前窗口）

**生命周期**: Day 1 上午 → Day 2 下午

**职责**:
- ✅ 任务分解与编排（已完成）
- ⏳ 下发任务包给 3 个 T2
- ⏳ 监控 3 个 T2 进度
- ⏳ 执行检查点 1-3（L0-L1 快速验证）
- ⏳ 协调 T2 之间的同步
- ⏳ 处理阻塞问题
- ⏳ 更新进度跟踪文档

**关键产出**:
- 任务树（已完成）
- 进度跟踪记录
- 检查点验证记录
- 问题处理记录

**结束标志**: Checkpoint 4 通过，所有 9 个任务完成

---

### 窗口 2：T1-Integrator（新开窗口）

**生命周期**: Day 2 下午 → Day 3

**职责**:
- ⏳ 准备集成测试环境
- ⏳ 执行 INT-V4-FINAL 任务
- ⏳ 验证 10 个 AC
- ⏳ 端到端测试
- ⏳ 编写验收报告
- ⏳ 签字发布

**关键产出**:
- 集成测试报告
- AC 验收记录
- 问题清单
- 最终发布决策

**开启条件**: 窗口 1 完成 Checkpoint 4

---

## ⏱️ 时间线与窗口切换

```
Day 1 上午（0-4h）
└─ 窗口 1（T1-Coordinator）
   ├─ ✅ 任务分解完成
   ├─ ⏳ 下发任务包 FC-1, FU-1, DK-1
   └─ ⏳ 启动监控

Day 1 下午（4-8h）
└─ 窗口 1（T1-Coordinator）
   ├─ ⏳ 监控 T2 进度
   ├─ ⏳ Checkpoint 1: FC-1 完成
   ├─ ⏳ Checkpoint 3: FU-1 完成
   └─ ⏳ 下发任务包 FC-2

Day 2 上午（8-12h）
└─ 窗口 1（T1-Coordinator）
   ├─ ⏳ 监控 T2 进度
   ├─ ⏳ Checkpoint 2: DK-1 完成
   └─ ⏳ 下发任务包 DK-2

Day 2 下午（12-16h）
├─ 窗口 1（T1-Coordinator）
│  ├─ ⏳ 监控 T2 进度
│  ├─ ⏳ Checkpoint 4: 所有任务完成
│  └─ 🚨 触发窗口 2 开启
│
└─ 窗口 2（T1-Integrator）🆕
   ├─ ⏳ 接收任务树和进度信息
   ├─ ⏳ 启动集成测试环境
   └─ ⏳ 开始 INT-V4-FINAL

Day 2 晚上 - Day 3（16-20h）
├─ 窗口 1（T1-Coordinator）
│  └─ ⏳ 待命（处理验收中发现的问题）
│
└─ 窗口 2（T1-Integrator）
   ├─ ⏳ 执行 10 个 AC 验证
   ├─ ⏳ 编写验收报告
   └─ ⏳ 签字发布
```

---

## 🚨 窗口 2 开启触发器

### 触发条件（必须全部满足）

- [ ] Checkpoint 4 通过
- [ ] 所有 9 个任务完成（F-V4-01 到 F-V4-GR）
- [ ] 所有任务 L0-L1 验证通过
- [ ] 无阻塞性问题
- [ ] 3 个 T2 已提交最终产出

### 触发时机

**预计时间**: Day 2 下午（约 12-16h）

### 触发动作

**窗口 1（T1-Coordinator）执行**:

1. ✅ 确认 Checkpoint 4 通过
2. ✅ 更新 `_progress.md`，标记所有任务完成
3. ✅ 生成窗口 2 启动包（见下文）
4. 🚨 **提醒指挥官开启窗口 2**
5. ✅ 将启动包路径发送给窗口 2

---

## 📦 窗口 2 启动包

### 启动包内容

**文件路径**: `.tasks/v4-student-enhancement/_window2_handover.md`

**包含信息**:
1. 任务树总览
2. 所有任务完成状态
3. 检查点验证记录
4. 已知问题清单
5. INT-V4-FINAL 任务文档路径
6. 测试环境启动命令
7. 10 个 AC 清单

### 启动包生成时机

**在 Checkpoint 4 通过后，窗口 1 立即生成**

---

## 📝 窗口 2 启动流程

### Step 1: 接收启动包

**窗口 2 首先阅读**:
```
.tasks/v4-student-enhancement/_window2_handover.md
```

### Step 2: 确认上下文

**检查清单**:
- [ ] 理解任务树结构
- [ ] 了解所有任务完成情况
- [ ] 知晓已知问题
- [ ] 熟悉 10 个 AC

### Step 3: 准备测试环境

**启动服务**:
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

### Step 4: 执行集成验收

**阅读任务文档**:
```
.tasks/v4-student-enhancement/int-v4-final/_task.md
```

**执行 10 个 AC 验证**

### Step 5: 编写验收报告

**创建报告**:
```
.tasks/v4-student-enhancement/int-v4-final/_report.md
```

### Step 6: 签字发布

**更新主任务状态**:
```
.tasks/v4-student-enhancement/_task.md
```

---

## 🔄 窗口间协作机制

### 窗口 1 → 窗口 2

**移交内容**:
- 任务树和进度信息
- 检查点验证记录
- 已知问题清单
- 启动包文档

**移交方式**:
- 生成 `_window2_handover.md`
- 提醒指挥官开启窗口 2
- 提供启动包路径

### 窗口 2 → 窗口 1

**反馈内容**:
- 验收中发现的问题
- 需要 T2 修复的问题
- 阻塞性问题

**反馈方式**:
- 在 `_window2_handover.md` 中记录问题
- 窗口 1 监控并协调 T2 修复

---

## 📋 检查清单

### 窗口 1（T1-Coordinator）检查清单

**Day 1 上午**:
- [ ] 下发任务包 FC-1, FU-1, DK-1
- [ ] 启动每日站会机制
- [ ] 创建进度跟踪记录

**Day 1 下午**:
- [ ] Checkpoint 1: FC-1 完成
- [ ] Checkpoint 3: FU-1 完成
- [ ] 下发任务包 FC-2

**Day 2 上午**:
- [ ] Checkpoint 2: DK-1 完成
- [ ] 下发任务包 DK-2

**Day 2 下午**:
- [ ] Checkpoint 4: 所有任务完成
- [ ] 生成窗口 2 启动包
- [ ] 🚨 提醒指挥官开启窗口 2

---

### 窗口 2（T1-Integrator）检查清单

**启动阶段**:
- [ ] 阅读启动包
- [ ] 确认上下文
- [ ] 启动测试环境

**验收阶段**:
- [ ] 执行 AC-1: 知识详情页
- [ ] 执行 AC-2: 主题色统一
- [ ] 执行 AC-3: 会话历史
- [ ] 执行 AC-4: 统计卡片
- [ ] 执行 AC-5: 快捷问题
- [ ] 执行 AC-6: 来源弹层
- [ ] 执行 AC-7: Chat 集成
- [ ] 执行 AC-8: KB 扩量
- [ ] 执行 AC-9: AI 防幻觉
- [ ] 执行 AC-10: 编译和回归

**报告阶段**:
- [ ] 编写验收报告
- [ ] 记录问题清单
- [ ] 签字发布

---

## 🚨 关键提醒点

### 提醒 1: Checkpoint 4 通过时

**窗口 1 输出**:
```
🚨 重要提醒：Checkpoint 4 已通过！

所有 9 个任务已完成，现在需要开启窗口 2 进行集成验收。

请执行以下操作：
1. 开启新的对话窗口（窗口 2）
2. 让窗口 2 阅读启动包：.tasks/v4-student-enhancement/_window2_handover.md
3. 窗口 2 开始执行 INT-V4-FINAL 任务

窗口 1 将继续待命，处理验收中发现的问题。
```

### 提醒 2: 验收中发现问题时

**窗口 2 输出**:
```
⚠️ 验收中发现问题，需要窗口 1 协调修复。

问题详情已记录在：.tasks/v4-student-enhancement/_window2_handover.md

请窗口 1 协调相关 T2 进行修复。
```

---

## 📊 双窗口优势

| 维度 | 单窗口 | 双窗口 |
|------|--------|--------|
| 上下文切换 | 频繁 | 少 |
| 集成验收质量 | 可能受干扰 | 专注，质量高 |
| 响应速度 | 监控时快，验收时慢 | 两阶段都快 |
| 问题处理 | 串行 | 并行 |
| 风险 | 验收时间不足 | 低 |

---

## 📝 文档更新计划

### 窗口 1 负责更新
- `_progress.md` - 实时进度
- `_dispatch_plan.md` - 分发记录
- `_window2_handover.md` - 启动包（生成）

### 窗口 2 负责更新
- `int-v4-final/_report.md` - 验收报告
- `_task.md` - 最终状态
- `_window2_handover.md` - 问题反馈（追加）

---

## ✅ 方案确认

- [x] 双窗口职责明确
- [x] 触发条件清晰
- [x] 启动流程完整
- [x] 协作机制明确
- [x] 提醒点设置
- [x] 文档更新计划

**状态**: ✅ 方案确定，待执行

---

**窗口 1 现在继续监控任务，窗口 2 在 Checkpoint 4 通过后开启！** 🚀

