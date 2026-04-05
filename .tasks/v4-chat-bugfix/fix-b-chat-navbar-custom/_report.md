# FIX-B 报告：Chat 双层导航栏修复

## 任务信息
- **任务ID**: fix-b-chat-navbar-custom
- **类型**: bugfix
- **状态**: completed
- **完成时间**: 2026-04-06

## 问题背景 (BUG-1)
进入智能问答页面时，顶部出现 "AI 咨询"（原生导航栏）+ "医小管"（自定义 .navbar）双层 header，导致内容区被大幅下推，输入框在部分机型上完全不可见。

## 修复内容

### 1. pages.json 修改
**文件**: `apps/student-app/src/pages.json`

为 chat 页面添加 `navigationStyle: "custom"`，禁用原生导航栏：

```json
{
  "path": "pages/chat/index",
  "style": {
    "navigationBarTitleText": "AI 咨询",
    "navigationStyle": "custom"
  }
}
```

### 2. chat/index.vue 状态
**文件**: `apps/student-app/src/pages/chat/index.vue`

页面已包含自定义导航栏（第4-6行），无需修改：
```vue
<view class="navbar">
  <text class="title">医小管</text>
</view>
```

样式定义（第786-801行）完整保留，确保状态栏高度正确计算：
```scss
.navbar {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  padding-top: var(--status-bar-height, 44px);
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  flex-shrink: 0;
}
```

## 验证结果

### L0: 配置命中验证
```powershell
Select-String -Path "apps/student-app/src/pages.json" -Pattern "navigationStyle.*custom"
```
输出命中第20行（chat页面）：
```
apps\student-app\src\pages.json:20:		"navigationStyle": "custom"
```

### L1: 编译验证
```bash
npm run build:h5
```
结果：**✅ 编译零错误**
- 仅有 Sass 废弃警告（与本次修改无关）
- 无 Vue/template 编译错误

### L3: H5 实机验证（预期）
- [ ] 智能问答空状态首屏仅显示单层 header（自定义 .navbar "医小管"）
- [ ] 原生导航栏 "AI 咨询" 已隐藏
- [ ] 输入框在首屏可见，无需手动下滑

## 未修改内容（符合约束）
- ✅ 未修改 chat 页核心逻辑（消息发送、来源引用、SSE）
- ✅ 未修改 chat/index.vue 除 navbar 外的其他代码
- ✅ 未触碰禁止修改的目录（services/, apps/teacher-web/, knowledge-base/等）

## 依赖关系
- 前置任务: fix-a-chat-markdown-penetration, fix-d-login-userinfo-mapping
- 执行顺序: Batch 2（串行在 FIX-A 之后）

## 风险说明
- **风险**: 低。navigationStyle: custom 是 uni-app 标准配置，已在登录页、申请详情页、服务页使用。
- **回滚**: 如需恢复原生导航栏，移除 navigationStyle 配置即可。
