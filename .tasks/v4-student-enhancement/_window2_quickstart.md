# 窗口 2 快速启动指南

> 给窗口 2（T1-Integrator）的 5 分钟快速上手指南

**角色**: T1-Integrator  
**职责**: 集成验收与发布  
**前置**: 窗口 1 已完成所有任务监控

---

## 🚀 快速启动（3 步）

### Step 1: 阅读启动包（2 分钟）
```
📄 .tasks/v4-student-enhancement/_window2_handover.md
```

**关键信息**:
- ✅ 9 个任务完成情况
- ⚠️ 已知问题清单
- 📋 10 个 AC 清单

---

### Step 2: 启动测试环境（5 分钟）

**快速启动脚本**:
```powershell
# 1. 基础设施
cd C:\Users\Administrator\Documents\code\yixiaoguan\deploy
docker compose up -d

# 2. business-api（新开 PowerShell 窗口）
cd C:\Users\Administrator\Documents\code\yixiaoguan\services\business-api
$env:POSTGRES_PASSWORD = "Yx@Admin2026!"
$env:REDIS_PASSWORD = "Yx@Redis2026!"
$env:JAVA_HOME = "C:\Users\Administrator\.vscode\extensions\redhat.java-1.53.0-win32-x64\jre\21.0.10-win32-x86_64"
& "C:\Program Files\JetBrains\IntelliJ IDEA 2025.3.2\plugins\maven\lib\maven3\bin\mvn.cmd" `
  -f pom.xml spring-boot:run -pl ruoyi-admin

# 3. student-app（新开 PowerShell 窗口）
cd C:\Users\Administrator\Documents\code\yixiaoguan\apps\student-app
npm run dev:h5
```

**验证服务**:
```powershell
# 检查所有服务是否启动
docker ps | grep -E "postgres|redis|ai-service"
curl http://localhost:8000/health
curl http://localhost:8080/actuator/health
# 浏览器访问 http://localhost:5174
```

---

### Step 3: 执行集成验收（2-3 小时）

**阅读任务文档**:
```
📄 .tasks/v4-student-enhancement/int-v4-final/_task.md
```

**执行 10 个 AC**:
1. AC-1: 知识详情页 ✅
2. AC-2: 主题色统一 ✅
3. AC-3: 会话历史 ✅
4. AC-4: 统计卡片 ✅
5. AC-5: 快捷问题 ✅
6. AC-6: 来源弹层 ✅
7. AC-7: Chat 集成 ✅
8. AC-8: KB 扩量 ✅
9. AC-9: AI 防幻觉 ✅
10. AC-10: 编译和回归 ✅

---

## 📋 验收流程

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

**完整用户流程测试**:
1. 登录 → 首页 → 智能问答
2. 发送问题 → 查看回复 → 点击来源 → 查看详情
3. 返回对话 → 点击历史 → 查看历史会话
4. 新建对话 → 发送消息 → 刷新页面 → 验证消息恢复
5. 事务导办 → 查看统计 → 申请空教室
6. 个人中心 → 查看信息 → 退出登录

### 阶段 3: 集成测试（L3）

**端到端测试**:
- 知识详情页完整流程
- 会话持久化完整流程
- AI 防幻觉验证
- 回归测试（所有已有功能）

---

## 📝 验收报告模板

**创建文件**:
```
.tasks/v4-student-enhancement/int-v4-final/_report.md
```

**报告结构**:
```markdown
# INT-V4-FINAL 集成验收报告

## 执行信息
- 执行人: T1-Integrator
- 执行时间: [填充]
- 测试环境: [填充]

## AC 验收结果

### AC-1: 知识详情页
- 状态: ✅ / ❌
- 验证步骤: [填充]
- 问题: [如有]

[... 其他 AC ...]

## 问题清单

| 问题 ID | 描述 | 严重性 | 状态 |
|---------|------|--------|------|
| [填充] | [填充] | [填充] | [填充] |

## 验收结论

- [ ] 所有 AC 通过
- [ ] 无阻塞性问题
- [ ] 无严重回归
- [ ] 可以发布

**签字**: ___________  
**日期**: ___________
```

---

## ⚠️ 常见问题

### Q1: 服务启动失败怎么办？
**A**: 检查端口占用，确保 PostgreSQL/Redis/8080/8000/5174 端口未被占用

### Q2: 发现问题需要修复怎么办？
**A**: 在启动包的"问题反馈"区域记录，通知窗口 1 协调修复

### Q3: AC 验证失败怎么办？
**A**: 记录问题详情，判断严重性，决定是否阻塞发布

### Q4: 需要窗口 1 协助怎么办？
**A**: 在启动包中记录问题，窗口 1 会监控并响应

---

## 🎯 成功标准

- ✅ 10 个 AC 全部通过
- ✅ 无阻塞性问题
- ✅ 无严重回归
- ✅ 验收报告完整
- ✅ 签字发布

---

## 📞 需要帮助？

- **窗口 1**: 协调 T2 修复问题
- **任务文档**: `.tasks/v4-student-enhancement/int-v4-final/_task.md`
- **启动包**: `.tasks/v4-student-enhancement/_window2_handover.md`

---

**准备好了吗？开始集成验收！** 🚀
