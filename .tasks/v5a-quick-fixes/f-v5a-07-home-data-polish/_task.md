---
id: "f-v5a-07"
parent: "v5a-quick-fixes"
type: "feature"
status: "pending"
tier: "T3"
priority: "low"
risk: "low"
foundation: false

depends_on: ["f-v5a-06"]

scope:
  - "apps/student-app/src/pages/home/"
  - "apps/student-app/src/pages/services/"
  - "apps/student-app/src/pages/profile/"
out_of_scope:
  - "apps/student-app/src/pages/chat/**"
  - "apps/student-app/src/pages/login/**"
  - "apps/student-app/src/api/**"
  - "services/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/pages/home/index.vue"
  - "apps/student-app/src/pages/services/index.vue"
  - "apps/student-app/src/pages/profile/index.vue"

done_criteria:
  L0: "home/index.vue, services/index.vue, profile/index.vue 均存在"
  L1: "grep -r '占位\\|placeholder\\|TODO\\|FIXME' apps/student-app/src/pages/home/ apps/student-app/src/pages/services/ apps/student-app/src/pages/profile/ 返回 0"
  L2: "页面数字字段无明显 0 值或空字符串占位"
  L3: "首页无空白区域或占位数据；各功能卡片图标与文案匹配；个人中心显示合理的学生信息"

created_at: "2026-04-06"
---

# F-V5A-07: 首页与功能页静态数据美化

> 首页、事务导办页、个人中心页使用贴近真实场景的演示数据，无明显占位符或空白区域。

## 背景

当前各页面仍使用开发阶段的占位数据（0 值、空字符串、"测试XXX"等），demo 演示时影响专业感。本任务用静态 mock 数据替换，不需要真实后端接口。

## 各页面美化要点

### 首页 (`pages/home/index.vue`)
- 轮播图/公告：使用医学院相关内容，如"关于 2026 年春季学期期末考试安排的通知"
- 快捷入口：图标与文案对应，如 🏥 就医绿色通道、📋 事务申请、💬 智能问答
- 统计数据：显示合理数字（如"已服务学生 1,234 人次"、"知识库 120 条"）

### 事务导办 (`pages/services/index.vue`)
- 8 格服务大厅：确保每格有图标+文案，如：请假申请、奖学金申请、住宿申请、成绩查询、图书馆、校园卡、报修、校医院预约

### 个人中心 (`pages/profile/index.vue`)
- 显示学生 demo 信息：张小洋 / 学号 2524010001 / 护理学院 2024 级
- 头像使用默认头像（无需真实图片）

## 已知陷阱

- 数据改为静态 mock 时，**不要破坏**已有的动态数据绑定逻辑（如果有的话）
- 仅替换"开发占位"数据，不替换来自 API 的真实响应数据
- 个人中心如果有 `uni.getStorageSync('userInfo')` 读取登录信息，优先使用真实登录数据，静态 fallback 仅在无数据时显示
