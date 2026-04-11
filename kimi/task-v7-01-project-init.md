# 任务: F-V7-01 教师移动端 UniApp 项目初始化

## 目标状态
`apps/teacher-app/` 目录存在，是一个可启动的 UniApp 空壳项目（`npx uni -p h5` 无报错），包含完整的 SCSS 色彩系统和复用的基础设施代码。

## 执行步骤

### 步骤 1: 创建目录结构
在 `apps/teacher-app/` 下创建以下目录结构：
```
apps/teacher-app/
├── src/
│   ├── api/
│   ├── components/
│   │   └── icons/
│   ├── pages/
│   │   └── index/
│   │       └── index.vue    ← 临时首页（空白占位）
│   ├── stores/
│   ├── styles/
│   ├── types/
│   └── utils/
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts
```

### 步骤 2: 创建 package.json
内容如下（直接复制，不要修改版本号）：
```json
{
  "name": "teacher-app",
  "version": "1.0.0",
  "scripts": {
    "dev:h5": "uni",
    "build:h5": "uni build",
    "dev:mp-weixin": "uni -p mp-weixin",
    "build:mp-weixin": "uni build -p mp-weixin",
    "type-check": "vue-tsc --noEmit"
  },
  "dependencies": {
    "@dcloudio/uni-app": "3.0.0-4080420251103001",
    "@dcloudio/uni-app-harmony": "3.0.0-4080420251103001",
    "@dcloudio/uni-app-plus": "3.0.0-4080420251103001",
    "@dcloudio/uni-components": "3.0.0-4080420251103001",
    "@dcloudio/uni-h5": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-alipay": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-baidu": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-harmony": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-jd": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-kuaishou": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-lark": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-qq": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-toutiao": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-weixin": "3.0.0-4080420251103001",
    "@dcloudio/uni-mp-xhs": "3.0.0-4080420251103001",
    "@dcloudio/uni-quickapp-webview": "3.0.0-4080420251103001",
    "pinia": "^2.1.7",
    "vue": "^3.4.21",
    "vue-i18n": "^9.1.9"
  },
  "devDependencies": {
    "@dcloudio/types": "^3.4.8",
    "@dcloudio/uni-automator": "3.0.0-4080420251103001",
    "@dcloudio/uni-cli-shared": "3.0.0-4080420251103001",
    "@dcloudio/uni-stacktracey": "3.0.0-4080420251103001",
    "@dcloudio/vite-plugin-uni": "3.0.0-4080420251103001",
    "@vue/runtime-core": "^3.4.21",
    "@vue/tsconfig": "^0.1.3",
    "sass": "^1.72.0",
    "typescript": "^4.9.4",
    "vite": "5.2.8",
    "vue-tsc": "^1.0.24"
  }
}
```

### 步骤 3: 创建 vite.config.ts
```typescript
import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";

export default defineConfig({
  plugins: [uni()],
  server: {
    port: 5175,
    host: true,
    proxy: {
      '/api/login': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/logout': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/captchaImage': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/getInfo': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      },
      '/api/chat': {
        target: 'http://192.168.100.165:8000',
        changeOrigin: true
      },
      '/api': {
        target: 'http://192.168.100.165:8080',
        changeOrigin: true
      }
    }
  }
});
```

### 步骤 4: 创建 index.html
```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8" />
    <script>
      var coverSupport = 'CSS' in window && typeof CSS.supports === 'function' && (CSS.supports('top: env(a)') ||
        CSS.supports('top: constant(a)'))
      document.write(
        '<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0' +
        (coverSupport ? ', viewport-fit=cover' : '') + '" />')
    </script>
    <title></title>
    <!--preload-links-->
    <!--app-context-->
  </head>
  <body>
    <div id="app"><!--app-html--></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
```

### 步骤 5: 创建 tsconfig.json
```json
{
  "extends": "@vue/tsconfig/tsconfig.json",
  "compilerOptions": {
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "lib": ["esnext", "dom"],
    "types": ["@dcloudio/types"]
  },
  "include": ["src/**/*.ts", "src/**/*.d.ts", "src/**/*.tsx", "src/**/*.vue"]
}
```

### 步骤 6: 创建 src/main.ts
```typescript
import { createSSRApp } from 'vue'
import { pinia } from './stores'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  app.use(pinia)

  import('./stores/user').then(({ useUserStore }) => {
    const userStore = useUserStore()
    userStore.init()
  })

  return {
    app
  }
}
```

### 步骤 7: 创建 src/App.vue
```vue
<script setup lang="ts">
import { onLaunch, onShow, onHide } from "@dcloudio/uni-app";
import './styles/theme.scss';
import './styles/global.scss';

onLaunch(() => {
  console.log("Teacher App Launch");
});
onShow(() => {
  console.log("Teacher App Show");
});
onHide(() => {
  console.log("Teacher App Hide");
});
</script>

<style lang="scss">
@import '@/styles/theme.scss';

:root {
  --color-primary: #{$primary};
}

page {
  font-family: 'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif;
  background: $surface;
  color: $on-surface;
  -webkit-tap-highlight-color: transparent;
}

button {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  font: inherit;
  color: inherit;
}

button::after {
  border: none;
}

.hover-effect {
  opacity: 0.7;
  transition: opacity 0.2s;
}
</style>
```

### 步骤 8: 创建 src/env.d.ts
```typescript
/// <reference types="vite/client" />

declare module '*.vue' {
  import { DefineComponent } from 'vue'
  const component: DefineComponent<{}, {}, any>
  export default component
}
```

### 步骤 9: 创建 src/manifest.json
```json
{
    "name": "医小管教师端",
    "appid": "",
    "description": "医小管教师工作台",
    "versionName": "1.0.0",
    "versionCode": "100",
    "transformPx": false,
    "h5": {
        "title": "医小管教师端",
        "router": {
            "mode": "hash"
        }
    },
    "mp-weixin": {
        "appid": "",
        "setting": {
            "urlCheck": false
        },
        "usingComponents": true
    },
    "uniStatistics": {
        "enable": false
    },
    "vueVersion": "3"
}
```

### 步骤 10: 创建 src/pages.json
```json
{
  "pages": [
    {
      "path": "pages/index/index",
      "style": {
        "navigationBarTitleText": "医小管教师端"
      }
    }
  ],
  "globalStyle": {
    "navigationBarTextStyle": "black",
    "navigationBarTitleText": "医小管教师端",
    "navigationBarBackgroundColor": "#faf5fb",
    "backgroundColor": "#faf5fb"
  }
}
```

### 步骤 11: 创建 src/pages/index/index.vue（临时占位首页）
```vue
<template>
  <view class="container">
    <text class="title">医小管教师端</text>
    <text class="subtitle">项目初始化成功</text>
  </view>
</template>

<script setup lang="ts">
</script>

<style lang="scss" scoped>
@import '@/styles/theme.scss';

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: $surface;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: $primary;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  color: $on-surface-variant;
}
</style>
```

### 步骤 12: 创建 src/styles/theme.scss
这是最关键的文件。必须包含所有 55 个 MD3 色彩令牌作为 SCSS 变量。

```scss
// ============================================================
// 医小管教师端 — MD3 色彩系统 (The Ethereal Educator)
// 源自 React 原型 index.css @theme 定义
// ============================================================

// ── Primary ──
$primary: #702ae1;
$primary-dim: #6411d5;
$primary-container: #b28cff;
$primary-fixed: #b28cff;
$primary-fixed-dim: #a67aff;
$on-primary: #f8f0ff;
$on-primary-container: #2e006c;
$on-primary-fixed: #000000;
$on-primary-fixed-variant: #390083;
$inverse-primary: #a476ff;

// ── Secondary ──
$secondary: #7742a6;
$secondary-dim: #6a3599;
$secondary-container: #e6c5ff;
$secondary-fixed: #e6c5ff;
$secondary-fixed-dim: #ddb3ff;
$on-secondary: #fbefff;
$on-secondary-container: #612c90;
$on-secondary-fixed: #4d137b;
$on-secondary-fixed-variant: #6b369a;

// ── Tertiary ──
$tertiary: #9e3657;
$tertiary-dim: #8e294c;
$tertiary-container: #ff8eac;
$tertiary-fixed: #ff8eac;
$tertiary-fixed-dim: #f77c9e;
$on-tertiary: #ffeff1;
$on-tertiary-container: #64042d;
$on-tertiary-fixed: #380016;
$on-tertiary-fixed-variant: #711036;

// ── Error ──
$error: #b41340;
$error-dim: #a70138;
$error-container: #f74b6d;
$on-error: #ffefef;
$on-error-container: #510017;

// ── Surface ──
$surface: #faf5fb;
$surface-dim: #d7d3db;
$surface-bright: #faf5fb;
$surface-variant: #e0dbe3;
$surface-tint: #702ae1;
$surface-container-lowest: #ffffff;
$surface-container-low: #f4eff5;
$surface-container: #ebe7ed;
$surface-container-high: #e5e1e8;
$surface-container-highest: #e0dbe3;
$on-surface: #2f2e32;
$on-surface-variant: #5d5b5f;
$inverse-surface: #0e0e11;
$inverse-on-surface: #9f9ca1;

// ── Outline ──
$outline: #78767b;
$outline-variant: #afacb1;

// ── Background ──
$background: #faf5fb;
$on-background: #2f2e32;

// ── Typography ──
$font-headline: 'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif;
$font-body: 'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif;
$font-label: 'Manrope', 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### 步骤 13: 创建 src/styles/global.scss
```scss
@import './theme.scss';

// ── 基础 Reset ──
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

// ── 动画 ──
@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-up {
  animation: fadeUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}

// 阶梯延迟
@for $i from 1 through 10 {
  .delay-#{$i} {
    animation-delay: #{$i * 50}ms;
  }
}

// ── 工具类 ──
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.pb-safe {
  padding-bottom: env(safe-area-inset-bottom);
}

.line-clamp-1 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

.line-clamp-3 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 3;
}
```

### 步骤 14: 复制基础设施文件（从 student-app 复制，内容不变）

创建 `src/utils/request.ts`，内容与 `apps/student-app/src/utils/request.ts` 完全一致。读取原文件并原样复制。

创建 `src/stores/index.ts`:
```typescript
import { createPinia } from 'pinia'

export const pinia = createPinia()

export * from './user'
```

创建 `src/stores/user.ts`，内容与 `apps/student-app/src/stores/user.ts` 完全一致。读取原文件并原样复制。

创建 `src/types/api.ts`，内容与 `apps/student-app/src/types/api.ts` 完全一致。读取原文件并原样复制。

创建 `src/api/auth.ts`，内容与 `apps/student-app/src/api/auth.ts` 完全一致。读取原文件并原样复制。

### 步骤 15: 创建 src/uni.scss（UniApp 全局样式变量）
```scss
@import '@/styles/theme.scss';
```

## 允许修改的文件
- `apps/teacher-app/**` （新建目录，所有文件均为新建）

## 禁止修改的文件
- `apps/student-app/**`
- `services/**`
- `scripts/**`
- `knowledge-base/**`
- `deploy/**`
- 根目录任何已有文件

## 硬约束
- 只做当前任务，不得顺手修复其他问题
- 从 student-app 复制的文件必须**原样复制**，不做任何修改
- theme.scss 必须包含**全部 55 个**色彩变量，不得遗漏
- package.json 的 name 必须为 `teacher-app`
- vite.config.ts 的 port 必须为 `5175`（不能与学生端 5174 冲突）

## 完成标准
- L0: `apps/teacher-app/` 目录存在，包含 package.json, vite.config.ts, src/styles/theme.scss
- L1: theme.scss 包含 ≥ 40 个 SCSS 变量
- L2: 项目结构完整（src/main.ts, src/App.vue, src/pages.json, src/manifest.json 均存在）

## 报告
最终报告写入: `.tasks/v7-teacher-app/f-v7-01-project-init/_report.md`

最终仅输出四段：
STEP-PLAN
STEP-EXECUTED
STEP-CHECK
BLOCKERS
