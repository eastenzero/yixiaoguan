# F-V5E-01 CSS/UI 快速修复报告

**执行时间**: 2026-04-06  
**执行者**: T3 执行器  
**任务状态**: ✅ 已完成

---

## 修改清单

### FIX-1: chat/index.vue .message-sources 加 overflow: hidden
- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: L1172 (box-shadow 后)
- **变更**: 添加 `overflow: hidden;`
- **状态**: ✅ 完成

### FIX-2: chat/index.vue .source-item 加 box-sizing: border-box
- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: L1187 (width: 100% 后)
- **变更**: 添加 `box-sizing: border-box;`
- **状态**: ✅ 完成

### FIX-3: chat/index.vue .source-item 背景/边框配色
- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: L1190-1191
- **变更**:
  - `background: #ffffff;` → `background: rgba(0, 106, 100, 0.04);`
  - `border: 1px solid rgba(0, 106, 100, 0.2);` → `border: 1px solid rgba(0, 106, 100, 0.15);`
- **状态**: ✅ 完成

### FIX-4: chat/index.vue .source-preview-actions padding-bottom
- **文件**: `apps/student-app/src/pages/chat/index.vue`
- **位置**: L1476
- **变更**: `padding-bottom: max(12px, env(safe-area-inset-bottom, 12px));` → `padding-bottom: calc(env(safe-area-inset-bottom, 0px) + 16px);`
- **状态**: ✅ 完成

### FIX-5: viewer/pdf.vue .back-icon color
- **文件**: `apps/student-app/src/pages/viewer/pdf.vue`
- **位置**: L28
- **变更**: `color: #006a64;` → `color: $primary;`
- **状态**: ✅ 完成

### FIX-6: knowledge/detail.vue .fallback-notice text color
- **文件**: `apps/student-app/src/pages/knowledge/detail.vue`
- **位置**: L214
- **变更**: `color: #006a64;` → `color: $primary;`
- **状态**: ✅ 完成

### FIX-7: App.vue CSS 变量
- **文件**: `apps/student-app/src/App.vue`
- **位置**: L18-21
- **变更**:
  - 添加 `@import '@/styles/theme.scss';`
  - `--color-primary: #006a64;` → `--color-primary: #{$primary};`
- **状态**: ✅ 完成

### FIX-8: apply/detail.vue 本地变量替换
- **文件**: `apps/student-app/src/pages/apply/detail.vue`
- **位置**: L370-376
- **变更**:
  - 添加 `@import '@/styles/theme.scss';`
  - 删除 `$primary: #006a64;` (保留其他本地变量)
- **状态**: ✅ 完成

### FIX-9: apply/classroom.vue + questions/index.vue 同 FIX-8
- **文件1**: `apps/student-app/src/pages/apply/classroom.vue`
  - 添加 `@import '@/styles/theme.scss';`
  - 删除 `$primary: #006a64;`
- **文件2**: `apps/student-app/src/pages/questions/index.vue`
  - 添加 `@import '@/styles/theme.scss';`
  - 删除 `$primary: #006a64;`
- **状态**: ✅ 完成

---

## 修改文件汇总

| 序号 | 文件路径 | 修改项数 |
|------|----------|----------|
| 1 | apps/student-app/src/pages/chat/index.vue | 4 |
| 2 | apps/student-app/src/pages/viewer/pdf.vue | 1 |
| 3 | apps/student-app/src/pages/knowledge/detail.vue | 1 |
| 4 | apps/student-app/src/App.vue | 2 |
| 5 | apps/student-app/src/pages/apply/detail.vue | 2 |
| 6 | apps/student-app/src/pages/apply/classroom.vue | 2 |
| 7 | apps/student-app/src/pages/questions/index.vue | 2 |

**总计**: 7 个文件，14 处修改

---

## 硬编码清理验证

执行以下命令验证 #006a64 硬编码:

```bash
grep -r '#006a64' apps/student-app/src --include='*.vue' --include='*.scss' --include='*.ts'
```

**结果**: 剩余 5 处（均为预期保留项）

| 文件 | 行号 | 内容 | 保留原因 |
|------|------|------|----------|
| theme.scss | 11 | `$primary-40: #006a64;` | 主题变量定义文件 |
| CustomTabBar.vue | 11 | `color="var(--color-primary, #006a64)"` | CSS var fallback（模板属性） |
| apply/status.vue | 291 | `confirmColor: 'var(--color-primary, #006a64)'` | CSS var fallback（JS字符串） |
| apply/detail.vue | 321 | `confirmColor: 'var(--color-primary, #006a64)'` | CSS var fallback（JS字符串） |
| chat/index.vue | 38 | `color="var(--color-primary, #006a64)"` | CSS var fallback（模板属性） |

---

## BLOCKERS

无阻塞项。所有 9 项修复均成功完成。

---

## 新发现的错误模式

无新发现。
