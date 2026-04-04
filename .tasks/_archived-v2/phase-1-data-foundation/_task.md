---
id: "phase-1-data-foundation"
parent: ""
type: "feature"
status: "pending"
tier: "T1"
priority: "high"
risk: "high"
foundation: true

scope:
  - "knowledge-base/entries/first-batch-drafts/"
  - "knowledge-base/raw/first-batch-processing/manifests/"
  - "knowledge-base/templates/"
  - "docs/test-reports/completion-reports/"
  - "services/business-api/ruoyi-admin/src/main/java/com/yixiaoguan/ai/"
out_of_scope:
  - "services/ai-service/"
  - "apps/student-app/"
  - "apps/teacher-web/"

context_files:
  - ".tasks/_spec.yaml"
  - "AGENT.md"
  - "teb-starter-kit/antipatterns.md"

done_criteria:
  L0: "p1a/p1b/p1c/p1d 四个子目录均存在 _report.md"
  L1: "所有子任务 _report.md 中无 BLOCKED 记录（rex-manual-review 除外，人工项）"
  L2: "p1b 脚本输出显示 ChromaDB ↔ 磁盘文件差异已处理；p1c 格式校验脚本全通过；p1a r2 重命名总数=21"
  L3: "KB 草稿编号无冲突，material_id 归属全部正确；意图兜底链接可点击跳转官网"

depends_on: []
created_at: "2026-04-04 01:43:00"

batches:
  - name: "batch-1"
    tasks: ["r2-file-rename", "p1b-chroma-verify", "p1c-format-unify", "p1d-intent-fallback"]
    parallel: true
    note: "r2-file-rename 高风险需先验收 STEP-PLAN；其余 3 个相互独立可安全并行"
  - name: "batch-2"
    tasks: ["r3-queue-sync", "r4-a1-rebuild-analysis"]
    parallel: true
    depends_on: "batch-1（仅 r2-file-rename）"
  - name: "batch-3"
    tasks: ["r5-a1-rebuild-exec"]
    depends_on: "batch-2（仅 r4-a1-rebuild-analysis）"
  - name: "batch-4"
    tasks: ["rex-manual-review"]
    depends_on: "batch-3"
---

# Phase 1：数据地基

> KB 草稿编号正确无冲突、ChromaDB 与磁盘文件一致、条目格式统一为 `##`、办事意图兜底链接上线。
> 这是后续所有向量化入库和调参工作的前提，必须优先完成。

## 背景

项目 AI 回答不准确的根因是知识库数据质量差，不在代码层。Phase 1 聚焦四条并行轨道：

- **Track A（p1a）**：执行 KB 修复管道 R2 → R3/R4 → R5 → REX，使 90 条草稿编号正确、无冲突
- **Track B（p1b）**：验证 ChromaDB 与磁盘 `.md` 文件的一致性，发现则修复
- **Track C（p1c）**：统一条目格式（模板 `#` → `##`），确保入库脚本提取逻辑匹配
- **Track D（p1d）**：办事意图兜底到学校官网，独立于数据治理，改动量极低

## 已知陷阱

- R2 重命名是高风险文件操作，必须先收到子 agent 的 STEP-PLAN 并确认后再执行
- 禁止仅凭编号猜内容归属，必须以草稿 frontmatter `material_id` 为准（R1-v3 教训）
- p1d 仅改 `AiCoordinatorServiceImpl.java`，禁止顺手改其他 Java 文件
- p1b 和 p1c 均为只读验证或模板修改，不涉及 ChromaDB 写操作（写操作在 Phase 2）
