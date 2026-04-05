# Batch-1 T2 验收汇总报告

**验收时间**: 2026-04-06 01:15:00  
**验收人**: T2-Reviewer  
**批次**: v4-chat-bugfix / batch-1  

---

## 批次概览

| 任务 ID | 类型 | 优先级 | 状态 | Scope 审计 | L0 | L1 | L2 | L3 | Commit Hash |
|---------|------|--------|------|------------|----|----|----|----|-------------|
| fix-a-chat-markdown-penetration | bugfix | high | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ⏳ PENDING | d749a22 |
| fix-d-login-userinfo-mapping | bugfix | high | ✅ PASS | ✅ PASS | ✅ PASS | ✅ PASS | ⏳ PENDING | ⏳ PENDING | fba53e2 |

---

## FIX-A: Chat Markdown 样式穿透修复

### 验收结果

**总体状态**: ✅ PASS

**Scope 合规性**: ✅ PASS
- 仅修改 `apps/student-app/src/pages/chat/index.vue` 的 `<style>` 区域
- 未修改 `<script>` 逻辑层、`pages.json`、services/

**验证详情**:

| 层级 | 状态 | 证据 |
|------|------|------|
| L0 | ✅ PASS | `.markdown-body` 子选择器已全部改为 `:deep()` 穿透写法，覆盖 p/h1-h4/ul/ol/li/code/pre/a/blockquote/hr/strong/b |
| L1 | ✅ PASS | `npm run build:h5` 编译成功，零错误 |
| L2 | ✅ PASS | `<script>` 逻辑层未修改，v-html 渲染路径保留 |
| L3 | ⏳ PENDING | 需 H5 环境验证 AI 气泡高度自适应 |

**修改文件**:
- `apps/student-app/src/pages/chat/index.vue` (第 958-1010 行)

**Commit**: `d749a22` - fix(chat): 修复 Markdown 样式穿透问题 - AI 气泡高度自适应 [task:fix-a-chat-markdown-penetration]

---

## FIX-D: 登录用户信息映射兼容修复

### 验收结果

**总体状态**: ✅ PASS

**Scope 合规性**: ✅ PASS
- 仅修改 `apps/student-app/src/pages/login/index.vue` 和 `apps/student-app/src/api/auth.ts`
- 未修改 `apps/student-app/src/pages/apply/**`、`utils/request.ts`、services/

**验证详情**:

| 层级 | 状态 | 证据 |
|------|------|------|
| L0 | ✅ PASS | login/index.vue 使用双字段兜底映射（id/username/realName），auth.ts 类型同步更新 |
| L1 | ✅ PASS | `npm run build:h5` 编译成功，零错误 |
| L2 | ⏳ PENDING | 需 H5 环境登录后验证 `userStore.userInfo.id` 有值 |
| L3 | ⏳ PENDING | 需 H5 环境验证进入"我的申请"不触发 401 回跳 |

**修改文件**:
- `apps/student-app/src/api/auth.ts` (第 54-70 行)
- `apps/student-app/src/pages/login/index.vue` (第 144-158 行)

**Commit**: `fba53e2` - fix(auth): 兼容 yx_user 版本字段映射 - 解决申请页 401 回跳 [task:fix-d-login-userinfo-mapping]

---

## 批次验收表

| 验收项 | 预期值 | 实测 | 状态 |
|--------|--------|------|------|
| FIX-A 代码修改完成 | .markdown-body 子选择器穿透 | ✅ 已完成 | ✅ PASS |
| FIX-A 编译无错误 | npm run build:h5 成功 | ✅ DONE Build complete. | ✅ PASS |
| FIX-A Scope 合规 | 仅修改 chat/index.vue style | ✅ 已验证 | ✅ PASS |
| FIX-D 代码修改完成 | 双字段兜底映射 | ✅ 已完成 | ✅ PASS |
| FIX-D 编译无错误 | npm run build:h5 成功 | ✅ DONE Build complete. | ✅ PASS |
| FIX-D Scope 合规 | 仅修改 login/index.vue + auth.ts | ✅ 已验证 | ✅ PASS |
| 路径冲突检查 | 两任务无文件重叠 | ✅ 无冲突 | ✅ PASS |
| Git Commits | 每任务独立 commit | ✅ 2 commits | ✅ PASS |

---

## 证据路径

### FIX-A
- 任务文件: `.tasks/v4-chat-bugfix/fix-a-chat-markdown-penetration/_task.md`
- T3 报告: `.tasks/v4-chat-bugfix/fix-a-chat-markdown-penetration/_report.md`
- T2 验收: `.tasks/v4-chat-bugfix/fix-a-chat-markdown-penetration/_t2_verification.yaml`
- 修改文件: `apps/student-app/src/pages/chat/index.vue` (行 958-1010)

### FIX-D
- 任务文件: `.tasks/v4-chat-bugfix/fix-d-login-userinfo-mapping/_task.md`
- T3 报告: `.tasks/v4-chat-bugfix/fix-d-login-userinfo-mapping/_report.md`
- T2 验收: `.tasks/v4-chat-bugfix/fix-d-login-userinfo-mapping/_t2_verification.yaml`
- 修改文件: 
  - `apps/student-app/src/api/auth.ts` (行 54-70)
  - `apps/student-app/src/pages/login/index.vue` (行 144-158)

---

## 门禁判定

### Batch-1 状态: ✅ PASS

**判定依据**:
- FIX-A: ✅ PASS (L0/L1/L2 全部通过，L3 待集成测试)
- FIX-D: ✅ PASS (L0/L1 全部通过，L2/L3 待集成测试)
- Scope 审计: ✅ 两任务均无越界修改
- 编译验证: ✅ 零错误
- Git Commits: ✅ 已提交

**放行 Batch-2**: ✅ 可以继续执行

---

## 遗留事项（待集成测试验证）

### FIX-A
- [ ] [H5] 发送多行问题后 AI 气泡高度自适应
- [ ] 段落/列表/加粗/链接完整显示

### FIX-D
- [ ] [H5] 登录后 `userStore.userInfo.id` 有值
- [ ] 进入"事务导办 → 我的申请"不触发 401 回跳

---

## 风险提示

### RISK-1 (FIX-A)
- **描述**: `:deep()` 在 uni-app H5 模式下可能不生效
- **兜底方案**: 改用独立 `<style>` 块（不加 scoped）
- **当前状态**: 已应用 `:deep()` 方案，待 H5 验证

### RISK-2 (FIX-D)
- **描述**: 字段映射修复后仍可能 401，涉及后端接口权限
- **兜底方案**: 上报 T0 诊断后端 `/api/v1/classroom-applications` 接口
- **当前状态**: 字段映射已修复，待 H5 验证

---

## T2 建议

1. **立即放行 Batch-2**: FIX-A 与 FIX-D 均已通过 L0/L1 验证，可继续执行 FIX-B
2. **集成测试优先级**: L3 验证项需在 165 H5 环境完成，建议在 Batch-3 完成后统一验收
3. **风险监控**: 若 H5 验证发现 `:deep()` 不生效或仍 401，按 RISK-1/RISK-2 执行兜底方案

---

**T2 签收**: ✅ Batch-1 验收完成，可放行 Batch-2
