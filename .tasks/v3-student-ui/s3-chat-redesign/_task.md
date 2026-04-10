---
id: "s3-chat-redesign"
parent: "v3-student-ui"
type: "feature"
status: "done"
tier: "T2"
priority: "high"
risk: "high"
foundation: false

scope:
  - "apps/student-app/src/pages/chat/index.vue"

out_of_scope:
  - "apps/student-app/src/pages/chat/index.vue <script> 逻辑层（SSE/API/来源引用逻辑）"
  - "apps/student-app/src/styles/theme.scss"
  - "services/"

context_files:
  - ".teb/antipatterns.md"
  - "apps/student-app/src/styles/theme.scss"
  - "apps/student-app/src/pages/chat/index.vue"
  - "_references/前端参考/stitch_ (1)/学生移动端/_1/screen.png"
  - "_references/前端参考/stitch_ (1)/学生移动端/jade_scholar/DESIGN.md"

done_criteria:
  L0: "chat/index.vue 中不含字符串'学术助手'和'学术亭'（grep 验证零结果）"
  L1: "apps/student-app 编译无错误 (npm run build:h5)"
  L2: "无"
  L3: |
    H5 preview 中：
    1. 空状态页显示"医小管智能助手"欢迎语 + teal 渐变机器人头像
    2. 快捷问题 chips 显示正常（pill 形状 + icon）
    3. 发送消息后 AI 气泡正常渲染（白底 + 左上小圆角）
    4. 用户气泡 teal 渐变 + 右下小圆角
    5. 来源引用区域显示白底实色卡片 + 右箭头 icon + 点击可跳转
    6. 输入框 pill 形状，无 border-top 分割线
    7. navbar 无 border-bottom，有毛玻璃效果，标题"医小管"
    8. 已有 SSE 流式回复功能完全正常

depends_on: ["s1-theme-unification", "s4-services-page"]
created_at: "2026-04-04"
---

# s3: AI 对话 UI 重做（Chat Redesign）

> `chat/index.vue` 的样式层按参考设计 Screen _1 标准全面升级，品牌名从"学术助手/学术亭智能助手"统一替换为"医小管"，同时清理 DEBT-V3-03（history:[] 冗余字段）。**所有 `<script>` 逻辑（SSE/来源引用/Markdown/快捷问题功能）保持完全不变。**

## 背景

chat/index.vue 共 1371 行，其中 `<style>` 约 600 行。当前样式与参考设计差距大：navbar 有 border-bottom，消息列表背景过暗，来源引用区域没有实色白底，输入区有 border-top 分割线。品牌名残留"学术助手"和"学术亭智能助手"。

## ⚠️ 重要约束（RISK-V3-02）

**只改样式，不动逻辑。** 具体说：
- `<script setup>` 内的所有函数、变量、API 调用、SSE 逻辑 → **一律不动**
- 快捷问题数组的值（文字内容）→ **不动**（只改 chip 的样式）
- 来源引用的点击逻辑（`handleSourceClick` 等）→ **不动**
- `history: []` 字段清理（DEBT-V3-03）是唯一的逻辑层修改，仅删除此字段，不改其他

**分段验证策略**（RISK-V3-02 缓解）：每修改一个区块，在 H5 预览中确认该区块正常后再继续下一区块。

## 执行步骤

### 步骤 1：品牌名替换（先做，最安全）

全局替换以下字符串：
- `"学术助手"` → `"医小管"`
- `"学术亭智能助手"` → `"医小管智能助手"`
- `"学术亭"` → `"医小管"`（兜底）
- navbar 标题 `"AI 助手"` → `"医小管"`

### 步骤 2：清理 DEBT-V3-03

在 `<script>` 中找到发送消息的 API 请求参数，删除 `history: []` 字段（后端已从 DB 取历史，此字段冗余）。

### 步骤 3：Navbar 样式

```scss
// 目标状态：
// - 毛玻璃背景：rgba(255,255,255,0.85) + backdrop-filter: blur(20px)
// - 移除 border-bottom（No-Line Rule）
// - 标题"医小管"居中
```

### 步骤 4：消息列表背景

```scss
// 目标：从 #e1e7e6 渐变 → 使用 $md-sys-color-background（#F5F5F9）浅色调
// 或 $md-sys-color-surface-container-low（更轻盈）
```

### 步骤 5：空状态样式

```scss
// 机器人头像：圆角矩形（radius-xl）+ teal 渐变背景（#006a64 → #008a83）
// 欢迎标题："同学你好！我是医小管智能助手。"（品牌名已在步骤1替换）
// 快捷 chips：pill 形状（border-radius: $radius-full）+ teal 边框/填充
//   每个 chip 左侧有小 icon（如闪光/问号等）
```

### 步骤 6：来源引用区域

```scss
// 目标：白色实底卡片（#ffffff）+ 轻阴影（$md-sys-elevation-1）
// 移除半透明背景
// 每条来源右侧添加 "›" 箭头 icon（暗示可点击）
// 保持现有点击逻辑不变
```

### 步骤 7：输入区域

```scss
// 移除 border-top 分割线（No-Line Rule）
// 背景改为 surface 色调（白色或 $md-sys-color-surface）
// 输入框保持 pill 形状（已有，确认保留）
```

### 步骤 8：气泡样式确认

- AI 气泡（白底 + 左上 4px 圆角 + 其余 18px 圆角）→ 已实现，确认保持
- 用户气泡（teal 渐变 + 右下小圆角）→ 已实现，确认保持
- AI 头像（teal 渐变圆形 + Bot icon）→ 已实现，确认保持

## 已知陷阱

- **严禁修改** `<script>` 中的 SSE 逻辑、来源引用逻辑、快捷问题点击逻辑
- **不要添加** 新的 `$primary: #006a64` 内联声明，改用 `@import 'styles/theme.scss'` 后的 `$primary`
- 600行 style 改动量大，每改完一个区块先 build 验证，再进行下一区块
- 改样式时注意检查 `scoped` 属性，不要意外影响全局
