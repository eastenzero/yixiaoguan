# docs/api — 接口契约文档

本目录存放前后端、服务间的接口约定文档。

## 待写文档

- [ ] `api-conventions.md` — 通用接口规范（URL 风格、响应格式、错误码、认证方式）
- [ ] `business-api-spec.md` — 主业务接口定义（认证 / 会话 / 知识库 / 申请审批 / 通知）
- [ ] `ai-service-spec.md` — AI 服务接口定义（RAG 问答 / 链接匹配 / 草稿生成 / 聚类）
- [ ] `student-api-spec.md` — 学生端消费的接口清单（从 business-api 中筛选）
- [ ] `teacher-api-spec.md` — 教师端消费的接口清单（从 business-api 中筛选）

## 接口规范约定（先定，后细化）

- 基础路径：`/api/v1/`
- 认证：JWT Bearer Token，放在 `Authorization` Header
- 响应格式统一：
  ```json
  {
    "code": 200,
    "msg": "success",
    "data": {}
  }
  ```
- 分页参数统一：`pageNum` / `pageSize`
- 时间字段统一：ISO 8601 格式（`2026-03-31T18:00:00+08:00`）
