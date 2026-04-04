---
id: "s1-theme-unification"
parent: "v3-student-ui"
type: "feature"
status: "pending"
tier: "T2"
priority: "high"
risk: "low"
foundation: true

scope:
  - "apps/student-app/src/styles/theme.scss"

out_of_scope:
  - "apps/student-app/src/pages/**"
  - "apps/student-app/src/components/**"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"

done_criteria:
  L0: "theme.scss 中 $primary-40 值为 #006a64，$md-sys-color-surface-container-lowest 变量存在"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无（纯样式变量，无可自动化运行时测试）"
  L3: "所有新增 token 命名符合 MD3 规范；teal 色阶完整（$primary-0 ~ $primary-100 共 12 档）；$primary 便捷变量可供页面直接使用"

depends_on: []
created_at: "2026-04-04"
---

# s1: 主题色系统一（Theme Unification）

> `theme.scss` 的 primary 色阶从蓝色（#00639B）统一替换为 teal（#006a64）基准，并补齐设计系统所需的 surface container 层级 token 和 `$primary` 便捷变量，使所有页面不再需要内联覆盖 `$primary`。

## 背景

当前 `theme.scss` 的 `$primary-40: #00639B`（蓝色），但所有页面实际内联覆盖为 teal `#006a64`。这导致 `$md-sys-color-primary` 指向错误颜色，凡是依赖 token 的地方颜色不一致。同时设计稿要求 "Tonal Stacking"（surface → surface_container_low → surface_container_lowest），但当前 theme.scss 缺少这些 token。

## 执行步骤

### 步骤 1：替换 Primary 色阶为 Teal

将 `theme.scss` 的 `// ========== Primary Colors ==========` 区块全部替换为以下 teal MD3 色阶（以 `#006a64` 为 key color，tone-40）：

```scss
$primary-0:   #000000;
$primary-10:  #002020;
$primary-20:  #003735;
$primary-30:  #004f4c;
$primary-40:  #006a64;
$primary-50:  #008580;
$primary-60:  #00a29c;
$primary-70:  #3cbfb9;
$primary-80:  #5edcd4;
$primary-90:  #a0f0ea;
$primary-95:  #d0f8f4;
$primary-99:  #f2fffe;
$primary-100: #ffffff;
```

> 参考验证工具：https://m3.material.io/theme-builder — 输入 #006a64 作为 Primary 可得标准值，上述为近似值，T3 可据此微调。

### 步骤 2：新增 $primary 便捷变量

在 `// ========== Light Theme Tokens ==========` 区块结尾（`$md-sys-color-inverse-primary` 之后）添加：

```scss
// ========== Convenience Aliases ==========
$primary:                    $primary-40;
$on-primary:                 $md-sys-color-on-primary;
$primary-container:          $md-sys-color-primary-container;
$on-primary-container:       $md-sys-color-on-primary-container;
```

### 步骤 3：新增 Surface Container 层级 Token

在 `// ========== Background & Elevation ==========` 区块添加：

```scss
// Surface container 层级（Tonal Stacking 设计原则）
$md-sys-color-surface-container-lowest:  #ffffff;
$md-sys-color-surface-container-low:     #f1f0f4;
$md-sys-color-surface-container:         #ebeaee;
$md-sys-color-surface-container-high:    #e5e4e8;
$md-sys-color-surface-container-highest: #dfdee2;
```

### 步骤 4：清理（DEBT-V3-01 预告）

**本任务不删除各页面内联的 `$primary: #006a64`**——各页面任务（s3/s4/s5/s6）执行时自行移除内联声明、改用 `@use` 或 `@import` 引入 theme.scss 后直接使用 `$primary`。

## 已知陷阱

- **不要修改** Secondary/Tertiary/Neutral 等其他色阶，它们不需要变更
- **不要修改** Glassmorphism 变量（$glass-bg 等已正确）
- **不要动** `$md-sys-color-background: #F5F5F9`，保持不变
- 只改 theme.scss，不动任何页面文件
