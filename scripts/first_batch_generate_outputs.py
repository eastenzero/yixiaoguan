from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(".")
INDEX_PATH = ROOT / "knowledge-base/raw/first-batch-material-index.csv"
CONVERSION_LOG_PATH = ROOT / "knowledge-base/raw/first-batch-processing/logs/conversion-log.csv"
OUT_DIR = ROOT / "knowledge-base/raw/first-batch-processing/manifests"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with INDEX_PATH.open("r", encoding="utf-8-sig", newline="") as f:
    index_rows = list(csv.DictReader(f))

with CONVERSION_LOG_PATH.open("r", encoding="utf-8-sig", newline="") as f:
    conversion_rows = list(csv.DictReader(f))

conversion_map = {row["material_id"]: row for row in conversion_rows}

cleaned_fields = list(index_rows[0].keys()) + ["conversion_status", "conversion_path", "conversion_error_type", "conversion_error_message"]
cleaned_rows: list[dict[str, str]] = []

for row in index_rows:
    r = dict(row)
    c = conversion_map.get(row["material_id"], {})
    r["conversion_status"] = c.get("status", "not_run")
    r["conversion_path"] = c.get("output_main", "")
    r["conversion_error_type"] = c.get("error_type", "")
    r["conversion_error_message"] = c.get("error_message", "")
    cleaned_rows.append(r)

cleaned_path = OUT_DIR / "first-batch-material-index.cleaned.csv"
with cleaned_path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=cleaned_fields)
    writer.writeheader()
    writer.writerows(cleaned_rows)

annotation_fields = [
    "material_id",
    "source_path",
    "title_guess",
    "knowledge_category",
    "audience",
    "material_type",
    "value_level",
    "timeliness",
    "is_template",
    "is_duplicate",
    "primary_reference",
    "processing_action",
    "cleaning_label",
    "version_relation",
    "conversion_status",
    "annotation_reason",
]

annotation_rows: list[dict[str, str]] = []

for row in cleaned_rows:
    action = row["processing_action"]
    if action == "可转知识":
        label = "可转知识"
    elif action == "提炼规则后入库":
        label = "提炼规则后入库"
    elif action == "仅作附件":
        label = "仅作附件"
    elif action == "待OCR":
        label = "待OCR"
    elif action == "待解包":
        label = "待解包"
    elif action == "待确认":
        label = "待确认"
    elif action == "过期归档":
        label = "过期归档"
    else:
        label = "暂缓"

    if row["is_duplicate"] == "是":
        if row["timeliness"] == "过期":
            relation = "历史版本"
        elif row["is_template"] == "是":
            relation = "模板平行版本"
        else:
            relation = "近重复版本"
    else:
        relation = "主参考或独立材料"

    reason_parts = [
        f"价值分级={row['value_level']}",
        f"时效={row['timeliness']}",
        f"模板={row['is_template']}",
        f"重复={row['is_duplicate']}",
    ]

    if row["conversion_status"] == "failed":
        reason_parts.append(f"转换失败={row['conversion_error_type']}")

    annotation_rows.append(
        {
            "material_id": row["material_id"],
            "source_path": row["source_path"],
            "title_guess": row["title_guess"],
            "knowledge_category": row["knowledge_category"],
            "audience": row["audience"],
            "material_type": row["material_type"],
            "value_level": row["value_level"],
            "timeliness": row["timeliness"],
            "is_template": row["is_template"],
            "is_duplicate": row["is_duplicate"],
            "primary_reference": row["primary_reference"],
            "processing_action": row["processing_action"],
            "cleaning_label": label,
            "version_relation": relation,
            "conversion_status": row["conversion_status"],
            "annotation_reason": "；".join(reason_parts),
        }
    )

annotation_path = OUT_DIR / "first-batch-cleaning-annotations.csv"
with annotation_path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=annotation_fields)
    writer.writeheader()
    writer.writerows(annotation_rows)

candidate_question_map = {
    "MAT-20260323-0001": "学生手册中与学工相关的核心办事规则有哪些？",
    "MAT-20260323-0002": "新生如何核对教育在线中的学籍信息与班级实际情况？",
    "MAT-20260323-0003": "学信网学籍注册信息应如何核对，常见错误怎么处理？",
    "MAT-20260323-0004": "2025级新生入学资格复查要准备什么、按什么流程办理？",
    "MAT-20260323-0005": "家庭经济困难认定与助学金评审的时间和条件是什么？",
    "MAT-20260323-0006": "助学金评审在一网通办系统里如何操作？",
    "MAT-20260323-0008": "秋季学期勤工助学岗位申报有哪些流程和节点？",
    "MAT-20260323-0009": "新生心理健康测评的时间安排和测评要求是什么？",
    "MAT-20260323-0010": "学生端心理测评系统从登录到提交应如何操作？",
    "MAT-20260323-0011": "心理测评平台常见问题有哪些、分别如何解决？",
    "MAT-20260323-0012": "校园卡丢失后如何补卡、多久可以恢复使用？",
    "MAT-20260323-0013": "第二课堂成绩单实施办法中的学分与认定规则是什么？",
    "MAT-20260323-0014": "第二课堂录入流程中学生端和管理员端分别怎么操作？",
    "MAT-20260323-0015": "毕业离校手续有哪些环节，办理顺序是什么？",
    "MAT-20260323-0018": "毕业证和学位证代领需要满足哪些条件并提交哪些材料？",
    "MAT-20260323-0019": "毕业生应征入伍可享受哪些政策，办理路径是什么？",
    "MAT-20260323-0020": "毕业生档案去向核对应注意哪些信息和时间节点？",
    "MAT-20260323-0021": "助学金评审通知模板中哪些规则可沉淀为通用知识？",
    "MAT-20260323-0022": "一网通办助学金申请模板中的关键填写规则有哪些？",
}

candidate_fields = [
    "material_id",
    "candidate_question",
    "knowledge_category",
    "audience",
    "priority",
    "source_path",
]

candidate_rows: list[dict[str, str]] = []

for row in cleaned_rows:
    if row["processing_action"] not in {"可转知识", "提炼规则后入库"}:
        continue
    if row["material_id"] not in candidate_question_map:
        continue
    if row["is_duplicate"] == "是" and row["is_template"] == "是":
        priority = "P2"
    elif row["value_level"] == "A" and row["processing_action"] == "可转知识":
        priority = "P0"
    elif row["value_level"] in {"A", "B"}:
        priority = "P1"
    else:
        priority = "P2"

    candidate_rows.append(
        {
            "material_id": row["material_id"],
            "candidate_question": candidate_question_map[row["material_id"]],
            "knowledge_category": row["knowledge_category"],
            "audience": row["audience"],
            "priority": priority,
            "source_path": row["source_path"],
        }
    )

candidate_path = OUT_DIR / "first-batch-candidate-knowledge-list.csv"
with candidate_path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=candidate_fields)
    writer.writeheader()
    writer.writerows(candidate_rows)

blocker_fields = [
    "material_id",
    "source_path",
    "stage",
    "error_type",
    "error_message",
    "impact_scope",
    "fallback_plan",
]

blocker_rows = []
for row in cleaned_rows:
    if row["conversion_status"] != "failed":
        continue
    blocker_rows.append(
        {
            "material_id": row["material_id"],
            "source_path": row["source_path"],
            "stage": "doc_to_docx",
            "error_type": row["conversion_error_type"],
            "error_message": row["conversion_error_message"],
            "impact_scope": "该材料暂无markdown文本，后续知识抽取需等待重试转换",
            "fallback_plan": "复制到ASCII临时路径后用Word COM另存为docx，再用pandoc转md",
        }
    )

blocker_path = OUT_DIR / "first-batch-conversion-blockers.csv"
with blocker_path.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=blocker_fields)
    writer.writeheader()
    writer.writerows(blocker_rows)

print(str(cleaned_path))
print(str(annotation_path))
print(str(candidate_path))
print(str(blocker_path))
