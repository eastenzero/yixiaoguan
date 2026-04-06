---
id: "f-v5b-01-frontend-build"
parent: "v5b-deploy"
type: "feature"
status: "done"
tier: "T3"
priority: "high"
risk: "medium"

scope:
  - "apps/student-app/src/pages/"
  - "apps/student-app/vite.config.ts"
  - "apps/teacher-web/"
out_of_scope:
  - "services/"
  - "deploy/"
  - "apps/student-app/src/api/"
  - "apps/student-app/src/store/"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/vite.config.ts"
  - "apps/student-app/package.json"
  - "apps/teacher-web/vite.config.ts"
  - "apps/teacher-web/package.json"
  - ".tasks/v5b-deploy/_task.md"

done_criteria:
  L0: |
    以下两个文件存在：
    apps/student-app/dist/build/h5/index.html
    apps/teacher-web/dist/index.html
  L1: "构建过程无 error（Sass deprecation warning 可接受）"
  L2: |
    在 165 服务器上执行验证：
    curl -s -o /dev/null -w "%{http_code}" http://localhost:5174 → 确认 vite dev 仍可用（不影响）
    ls -lh ~/dev/yixiaoguan/apps/student-app/dist/build/h5/index.html → 文件存在且 >10KB
    ls -lh ~/dev/yixiaoguan/apps/teacher-web/dist/index.html → 文件存在且 >10KB
  L3: "T1 检查：index.html 中引用的 JS/CSS 文件路径格式正确（相对路径 ./assets/...）"

depends_on: []
created_at: "2026-04-06"
---

# F-V5B-01: 前端静态构建

> 完成后：165 服务器上同时存在 student-app 和 teacher-web 的静态构建产物，
> 可由 Nginx 直接托管。

## 背景

当前两个前端均以 `vite dev` 模式运行在 Tmux 中。生产部署需要静态产物供 Nginx 托管。

## 执行步骤（在 165 服务器上）

### student-app

```bash
cd ~/dev/yixiaoguan/apps/student-app
npx uni build -p h5
# 产物目录：dist/build/h5/
```

### teacher-web

```bash
cd ~/dev/yixiaoguan/apps/teacher-web
npm run build-only   # 注意：不是 npm run build（后者跑 vue-tsc，Node 18 可能失败）
# 产物目录：dist/
```

## 已知问题：SCSS $primary 未定义（必须先修复再构建）

student-app 部分页面 `<style lang="scss" scoped>` 块有本地变量但缺少 `$primary` 定义，
会导致构建失败。已确认需要修复的文件（执行时如遇同类错误，按相同方式修复）：

| 文件 | 修复方式 |
|------|---------|
| `apps/student-app/src/pages/questions/index.vue` | 在 style 块本地变量区加 `$primary: #006a64;` |
| `apps/student-app/src/pages/apply/classroom.vue` | 同上 |

**检查命令**（找出所有缺少 `$primary` 定义的同类文件）：
```bash
grep -rL '^\$primary:' $(grep -rl '\$primary-container' ~/dev/yixiaoguan/apps/student-app/src/pages/ --include='*.vue')
```

修复定位（在 style 块最顶部的 `// 设计规范颜色` 注释下方加入）：
```scss
$primary: #006a64;   // 与 theme.scss $primary-40 一致
```

## 已知陷阱

- `npm run build` 内含 `vue-tsc --build`，在 Node 18 上可能超时或报错，改用 `npm run build-only`
- Sass deprecation warning（`@import` deprecated、legacy-js-api）属于正常输出，不是错误，不影响产物
