# F-V4-02：主题色 Token 统一

## 元信息
- **任务 ID**: F-V4-02
- **优先级**: P1
- **类型**: refactor
- **批次**: batch_1（并行）
- **预计工作量**: 1 小时
- **前置依赖**: 无

## 目标

将 11 个文件中的 23 处 #006a64 内联硬编码替换为 theme.scss 中的 $primary 或对应语义 token 引用。

## 背景

- spec-v3 已在 theme.scss 中定义 $primary: #006a64
- 但各页面仍有 23 处内联硬编码
- 这导致主题色修改时需要改动多个文件，维护成本高

## 范围

### In Scope
替换以下文件中的 #006a64：
- pages/chat/index.vue (8 处，仅 CSS 中 color/background 值)
- pages/knowledge/detail.vue (3 处)
- components/CustomTabBar.vue (2 处)
- pages/apply/detail.vue (2 处)
- pages/apply/status.vue (2 处)
- components/StatusBadge.vue (1 处)
- pages/apply/classroom.vue (1 处)
- pages/login/index.vue (1 处)
- pages/profile/index.vue (1 处)
- pages/questions/index.vue (1 处)
- styles/theme.scss (确认 $primary 已为 #006a64，保留定义)

### Out of Scope
- 新增或修改 theme.scss token 定义（已在 spec-v3 F-S1 完成）
- 修改其他颜色值
- JavaScript 逻辑修改

## 技术要点

1. **替换规则**：
   ```scss
   // 替换前
   color: #006a64;
   background: #006a64;
   background-color: #006a64;
   
   // 替换后
   color: $primary;
   background: $primary;
   background-color: $primary;
   ```

2. **注意事项**：
   - 仅替换 CSS/SCSS 中的颜色值
   - 不替换注释中的颜色值
   - 确保文件已导入 theme.scss（uni-app 通常全局导入）

3. **验证方法**：
   ```powershell
   # 检查是否还有遗漏
   grep -r '#006a64' apps/student-app/src/ --exclude-dir=node_modules
   # 应该只剩 theme.scss 中的定义行
   ```

## 完成标准

### L0: 存在性检查
- 编译无错误
- 所有目标文件已修改

### L1: 静态检查
- `grep -r '#006a64' apps/student-app/src/` 结果仅剩 theme.scss 中的定义行
- TypeScript 编译无错误
- 无 ESLint error

### L2: 运行时检查
- H5 预览：各页面颜色表现无变化
- 智能问答、知识详情、事务导办、个人中心页面主题色正常

### L3: 语义检查
- 所有 teal 主题色统一使用 token
- 未来修改主题色只需改 theme.scss 一处

## 文件清单

### 必须修改（11 个文件）
- `apps/student-app/src/pages/chat/index.vue`
- `apps/student-app/src/pages/knowledge/detail.vue`
- `apps/student-app/src/components/CustomTabBar.vue`
- `apps/student-app/src/pages/apply/detail.vue`
- `apps/student-app/src/pages/apply/status.vue`
- `apps/student-app/src/components/StatusBadge.vue`
- `apps/student-app/src/pages/apply/classroom.vue`
- `apps/student-app/src/pages/login/index.vue`
- `apps/student-app/src/pages/profile/index.vue`
- `apps/student-app/src/pages/questions/index.vue`

### 必须阅读
- `apps/student-app/src/styles/theme.scss` (确认 $primary 定义)

## 执行提示

1. 先确认 theme.scss 中 $primary 已定义为 #006a64
2. 使用 find-replace 批量替换（注意大小写）
3. 逐文件检查，确保只替换 CSS 属性值
4. 编译验证
5. H5 预览验证视觉效果

## 批量替换命令（参考）

```powershell
# 查找所有包含 #006a64 的文件
cd apps/student-app/src
grep -rl '#006a64' . --exclude-dir=node_modules

# 手动替换（推荐使用 IDE 的 find-replace 功能）
# 搜索: #006a64
# 替换: $primary
# 范围: 仅 .vue 文件的 <style> 块
```

## 验证命令

```powershell
# L0: 编译检查
cd apps/student-app
npm run type-check

# L1: 检查是否还有硬编码
cd src
grep -r '#006a64' . --exclude-dir=node_modules
# 应该只输出 styles/theme.scss:XX:$primary: #006a64;

# L2: 启动 dev server 预览
npm run dev:h5
```

## 风险

- 低风险任务，纯文本替换
- 注意不要替换注释或字符串中的颜色值
