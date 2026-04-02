# 【提示词 D3】学生端申请页面开发

> **状态**：待执行 | **预估工时**：2~3小时 | **前置依赖**：TASK-D1 完成  
> **并行说明**：与 D2 完全独立，可同时执行，操作不同的文件

---

## 提示词正文（直接粘贴给 AI）

---

你是 **医小管（yixiaoguan）** 项目的**资深 uni-app 前端工程师**。

**【背景材料——开始前必须全部阅读】**

1. `.globalrules`（项目全局规则）
2. `docs/dev-guides/ai-antipatterns.md`（**错题本，必读**）
3. `_references/前端风格/学生移动端/jade_scholar/DESIGN.md`（**设计规范，必读**）
4. `_references/前端风格/学生移动端/_2/screen.png`（**空教室申请表单 UI 参考截图，重点参考**）
5. `docs/database/schema-phase1.md`（重点阅读：第四章"申请审批模块"——`yx_classroom`、`yx_classroom_application`、`yx_application_review` 三张表及枚举值）
6. `docs/test-reports/TASK-D1-student-scaffold-completion-report.md`（**D1 完成报告，了解已有的工具层**）
7. `apps/student-app/src/utils/request.ts`（D1 已建好的请求工具）
8. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/classroom/controller/ClassroomApplicationController.java`（后端申请 API 的全部接口，包括学生提交和查询接口）
9. `services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/classroom/controller/ClassroomController.java`（教室列表查询接口，供申请表单时选择教室）


**【任务说明】**

实现学生端的两个申请相关页面：空教室申请表单 和 我的申请进度列表。

### 页面 1：空教室申请（`pages/apply/classroom.vue`）

**功能**：
1. 顶部提示文案：说明申请规则（使用时段提前 24h 申请，联系辅导员等）
2. 申请表单，字段对应 `yx_classroom_application` 表：
   - **教室选择**：调用 `GET /api/v1/classrooms`（获取可用教室列表），做成下拉选择或列表选择
   - **使用日期**：日期选择器（不早于明天）
   - **开始/结束时间**：时间选择器（两个），结束时间必须晚于开始时间
   - **用途说明**：多行文本框（必填，最多 200 字）
   - **预计人数**：数字输入
   - **联系电话**：手机号输入（选填）
3. 底部"提交申请"按钮：调用 `POST /api/v1/classroom-applications`
4. 提交成功后弹出确认提示，跳转到我的申请页

### 页面 2：我的申请进度（`pages/apply/status.vue`）

**功能**：
1. 列表展示当前学生的全部申请：`GET /api/v1/classroom-applications/my`（先确认接口是否存在）
2. 每条显示：
   - 教室名称（`building` + `room_number`）
   - 申请日期时段（`apply_date` + `start_time`~`end_time`）
   - 申请状态 badge（待审批-橙色 / 已通过-绿色 / 已拒绝-红色 / 已取消-灰色）
   - 用途说明（一行截断）
3. 点击每条可展开查看审批意见（若已审批）
4. 已通过的申请可以点击"取消申请"（若后端支持）

**【API 清单（新建 `src/api/apply.ts`）】**

```typescript
getClassroomList()                   // GET /api/v1/classrooms
submitApplication(data: ApplyForm)   // POST /api/v1/classroom-applications
getMyApplications()                  // GET /api/v1/classroom-applications/my（若无此接口，在报告里标注缺失）
cancelApplication(id: number)        // DELETE /api/v1/classroom-applications/{id}（若无此接口同样标注）
```

**ApplyForm 类型定义**（对应后端接收字段）：
```typescript
interface ApplyForm {
  classroomId: number
  applyDate: string       // "YYYY-MM-DD"
  startTime: string       // "HH:mm"
  endTime: string         // "HH:mm"
  purpose: string
  attendeeCount?: number
  contactPhone?: string
}
```

**【UI 设计要求】**

- 状态 badge 颜色：
  - 待审批：`#F59E0B`（橙黄）
  - 已通过：`#00685f`（主题绿）
  - 已拒绝：`#EF4444`（红）
  - 已取消 / 已过期：`#9CA3AF`（灰）
- 表单项之间有明显分隔，卡片式布局
- 时间选择器使用 uni-app 原生 `<picker mode="time">`

**【你的交付物】**

1. `apps/student-app/src/api/apply.ts`（API 函数封装含 TypeScript 类型）
2. `apps/student-app/pages/apply/classroom.vue`（申请表单页，功能完整）
3. `apps/student-app/pages/apply/status.vue`（我的申请列表页，功能完整）

**【禁止清单（严格遵守）】**

- ❌ 禁止修改 D1 已创建的 `request.ts`、`stores/user.ts`、`pages.json`
- ❌ 禁止修改 `pages/chat/` 或其他 D2 负责的文件（并行任务不交叉）
- ❌ 禁止修改后端任何代码
- ❌ 如果 `GET /api/v1/classroom-applications/my` 接口不存在，在报告里标注，不要自己去后端加接口
- ❌ 如果教室列表接口返回数据格式与期望不符，停下来说明，不要擅自改字段名

**【工作方式】**

第一步：阅读背景材料，读懂 `ClassroomApplicationController` 已有哪些接口，列出文件清单，等待我的"同意"。  
第二步：按 api/ → 申请表单页 → 申请列表页的顺序开发，每完成一个文件汇报。

**【完成标准】**

✅ H5 开发服务无编译报错  
✅ 进入 `/pages/apply/classroom`，表单完整可见，教室下拉已加载数据（或友好的加载失败提示）  
✅ 填写表单后点击提交，能调用后端接口（成功或出现明确的报错，不是白屏）  
✅ 进入 `/pages/apply/status`，能展示列表或空列表占位

**【完成汇报文件（必须交付，不可跳过）】**

满足完成标准后，将本次交付报告写入：  
`docs/test-reports/completion-reports/TASK-D3-apply-page-completion-report.md`

报告章节：① 实际创建/修改的文件清单 ② 验证结果 ③ 遗留问题（特别标注：后端缺missing 的接口列表） ④ 新发现错误模式 ⑤ 下一步建议

汇报文件写完后，请明确回复 **"阶段任务 D3 完成并停止"**。

**现在，请开始第一步：阅读背景材料，确认后端已有哪些接口，提交文件清单。**
