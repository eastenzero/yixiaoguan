# 任务报告：v6a-01-teacher-purple

## STEP-PLAN

1. 修改 `apps/teacher-web/src/assets/main.css` 的 :root CSS 变量，将绿色主题色改为紫色系
2. 逐一修改 .vue 文件中的硬编码绿色值：
   - AnalyticsView.vue (9处+2处补充)
   - DashboardView.vue (8处+1处补充)
   - MainLayout.vue (4处)
   - ProfileView.vue (4处)
   - KnowledgeView.vue (3处+1处补充)
   - QuestionsView.vue (3处+2处补充)
   - ApprovalView.vue (2处+2处补充)
   - LoginView.vue (1处+3处补充)
   - NotFoundView.vue (1处)

## STEP-EXECUTED

### main.css 修改 (9处)
- `--primary-color`: #00685f → #7C3AED
- `--primary-container`: #008378 → #6D28D9
- `--primary-light`: #0D9488 → #8B5CF6
- `--primary-dark`: #004d47 → #5B21B6
- `--primary-bg`: #f0fdfa → #F5F3FF
- `--primary-bg-soft`: #ccfbf1 → #EDE9FE
- `--secondary`: #006a63 → #6D28D9
- `--card-shadow-hover`: rgba(0, 104, 95, 0.08) → rgba(124, 58, 237, 0.08)
- `textarea focus`: rgba(0, 104, 95, 0.1) → rgba(124, 58, 237, 0.1)

### .vue 文件修改
| 文件 | 修改内容 |
|------|---------|
| AnalyticsView.vue | 图表线色、面积渐变、图标背景色等 13处 |
| DashboardView.vue | 图标颜色、快捷入口、渐变背景、阴影等 9处 |
| MainLayout.vue | 侧边栏头部渐变、菜单图标背景、按钮阴影 4处 |
| ProfileView.vue | 头部卡片渐变、switch active-color 4处 |
| KnowledgeView.vue | 图标颜色、快捷入口、AI卡片渐变 4处 |
| QuestionsView.vue | 统计值颜色、AI卡片渐变、背景渐变、置信度颜色 5处 |
| ApprovalView.vue | 头像背景色、按钮渐变、阴影、hover背景 4处 |
| LoginView.vue | 页面背景、品牌区渐变、按钮阴影 4处 |
| NotFoundView.vue | 图标颜色 1处 |

### 补充修复
在验证过程中发现并修复了额外的绿色硬编码：
- AnalyticsView.vue: 饼图颜色 #00685f, #008378 → 紫色
- ApprovalView.vue: 审批按钮渐变和阴影
- QuestionsView.vue: 置信度颜色函数返回值

## STEP-CHECK

### 验证结果
1. ✅ **main.css**: `--primary-color` 值为 `#7C3AED` (violet-600)
2. ✅ **绿色代码清理**: 搜索 `#00685f`, `#008378`, `#0D9488`, `#004d47`, `#006a63`, `rgba(0, 104, 95` 无结果
3. ✅ **构建成功**: `npm run build` 完成，dist/assets/ 下 CSS 文件包含紫色颜色值
4. ✅ **CSS 输出验证**: 
   - #7c3aed (violet-600) ✓
   - #6d28d9 (violet-700) ✓
   - #8b5cf6 (violet-500) ✓
   - #5b21b6 (violet-800) ✓

### 注意事项
- `--success` (#10b981) 未修改，保持为功能色绿色
- 浅绿色 `#14b8a6`, `#5eead4` 为图表辅助色，不在任务指定替换范围内

## BLOCKERS

无阻塞问题。

---
完成时间: 2026-04-11
