---
id: "v5d-source-material-viewer"
parent: ""
type: "feature"
status: "in_progress"
tier: "T1"
priority: "high"
risk: "medium"
foundation: false

batches:
  - name: "batch-1"
    tasks: ["f-v5d-01", "f-v5d-02"]
    parallel: false
    note: "F-V5D-02 depends on F-V5D-01 产出 materials/ + material-index.json；必须串行"
  - name: "batch-int"
    tasks: ["int-v5d-a"]
    depends_on: "batch-1"
    status: "done"
    note: "T1-A PASS (T0 签收 2026-04-07)"
  - name: "batch-t1b"
    tasks: ["f-v5d-03", "f-v5d-04", "f-v5d-05"]
    parallel: false
    status: "done"
    verified_at: "2026-04-07"
    note: "T1-B 全部 PASS: ChromaDB注入+API透传+前端升级+构建通过"

created_at: "2026-04-06"
t1b_completed_at: "2026-04-07"
---

# spec-v5d — 参考资料原件直览（T1-A: 数据 + Nginx）

## 目标

- 将原始材料标准化为 PDF，落地到 `deploy/materials/`
- 通过 Nginx 暴露 `/materials/` 静态路由，浏览器可直接预览 PDF

## 约束

- `deploy/materials/` 已被 `.gitignore` 排除，**不会提交到仓库**
- 优先处理 value_level=A 的高价值材料；跳过 C/过期与非文档类附件（xlsx/ppt/jpg）

## 已知风险

- 165 服务器可能未安装 libreoffice，doc/docx 转 pdf 需改用 Windows Office 导出后再上传
- materials 目录较大时同步慢，建议直接在 165 上生成/拷贝，或用 scp 单文件上传
