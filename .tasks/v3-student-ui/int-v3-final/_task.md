---
id: "int-v3-final"
parent: "v3-student-ui"
type: "integration-test"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: false

scope: []
out_of_scope:
  - "apps/student-app/src/**"

context_files:
  - ".teb/antipatterns.md"
  - ".tasks/v3-student-ui/s1-theme-unification/_report.md"
  - ".tasks/v3-student-ui/s2-tabbar-routing/_report.md"
  - ".tasks/v3-student-ui/s4-services-page/_report.md"
  - ".tasks/v3-student-ui/s3-chat-redesign/_report.md"
  - ".tasks/v3-student-ui/s5-home-polish/_report.md"
  - ".tasks/v3-student-ui/s6-profile-polish/_report.md"

done_criteria:
  L0: "全部 6 个子任务的 _report.md 存在"
  L1: "apps/student-app 编译零错误零告警 (npm run build:h5)"
  L2: "无"
  L3: |
    以下全部通过（自动化 grep + 编译为主，标注 [H5] 的需人工预览确认）：
    1. 无旧品牌名残留：grep 全库不含"学术助手"/"学术亭智能助手"
    2. TabBar 四项文字正确：首页/智能问答/事务导办/我的（grep pages.json）
    3. 全局无 switchTab.*apply/status 残留（grep 验证零结果）
    4. theme.scss primary-40 = #006a64（grep 验证）
    5. [H5] TabBar 四个 Tab 可正常切换
    6. [H5] 事务导办：服务矩阵可见，空教室申请可跳转，placeholder 显示提示
    7. [H5] AI 对话：医小管品牌名，空状态欢迎语，气泡样式正常，来源引用可点击
    8. [H5] SSE 流式回复功能正常（发送真实问题，AI 逐字回复）
    9. [H5] 首页：医小管品牌名，AI 入口跳转智能问答
    10. [H5] 个人中心：退出登录正常，无异常 mock 数据

depends_on: ["s5-home-polish", "s6-profile-polish"]
created_at: "2026-04-04"
---

# int-v3-final：全量回归集成测试

> spec-v3 所有功能任务完成后的最终验收。自动化 grep 检查 + 编译验证为主，关键路径功能需 H5 预览人工确认。通过后整个 v3-student-ui 任务树标记为 done。

## 背景

所有 6 个功能任务（s1~s6）完成后，进行整体回归，确保：
1. 所有品牌名统一为"医小管"
2. TabBar 路由正确
3. 已有核心功能（登录、SSE 对话、来源引用、空教室申请）无回归

## 自动化验收命令（T2 逐条执行并记录）

```powershell
# ===== 品牌名检查 =====
# 预期：零结果
Select-String -Path "apps/student-app/src/" -Pattern "学术助手|学术亭智能助手|学术亭" -Recurse --include="*.vue"

# ===== 路由检查 =====
# Tab 文字
Select-String -Path "apps/student-app/src/pages.json" -Pattern "智能问答"
Select-String -Path "apps/student-app/src/pages.json" -Pattern "事务导办"
# 无残留 switchTab apply（预期零结果）
Select-String -Path "apps/student-app/src/" -Pattern "switchTab.*apply" -Recurse

# ===== 主题检查 =====
Select-String -Path "apps/student-app/src/styles/theme.scss" -Pattern "primary-40.*006a64"
Select-String -Path "apps/student-app/src/styles/theme.scss" -Pattern "surface-container-lowest"

# ===== 编译验证 =====
# 在 apps/student-app 目录执行
npm run build:h5
```

## H5 人工验收路径

启动 H5 服务：
```powershell
# 在 apps/student-app 目录
npm run dev:h5  # http://localhost:5174
```

按以下顺序验收：
1. **登录** → 确认登录页正常，能进入首页
2. **首页** → 品牌名"医小管"可见，点击 AI 入口跳转到智能问答
3. **TabBar** → 四个 Tab 均可切换，文字正确
4. **事务导办** → 服务矩阵 8 个入口可见，点击空教室申请跳转，placeholder 弹提示
5. **智能问答** → 空状态医小管欢迎语，快捷问题可点击，发送消息后 AI 流式回复，来源引用可点击
6. **个人中心** → 正常显示，退出登录正常
7. **空教室申请** → 从事务导办进入，表单正常，提交正常

## 放行条件

自动化 10 项 + H5 人工 7 路径 全部通过 → 标记 `status: "done"`，同步更新父任务 `v3-student-ui` 状态为 done，可进行 Git commit。

## 报告格式

`_report.md` 须包含：
- 验收结论（通过/失败）
- 验收表格（验收项 | 预期值 | 实测 | 状态）
- 证据路径（grep 输出截图或命令输出）
- 失败项列表（若有）+ 对应需回退的任务
