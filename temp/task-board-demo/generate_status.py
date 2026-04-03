#!/usr/bin/env python3
"""
Task Evidence Board — 状态聚合器
===========================================
扫描 tasks/ 目录，读取任务文件的 YAML frontmatter，
生成可读的状态报告（STATUS.md）和任务依赖图（task-graph.mmd）。

用法:
    python generate_status.py [tasks_dir] [output_dir]

    tasks_dir   任务文件目录（默认: tasks）
    output_dir  输出目录（默认: output）

依赖:
    pip install pyyaml

任务文件 frontmatter 字段:
    task_id        唯一标识符（英文，无空格）
    task_name      任务名称
    parent_id      父任务 task_id；根节点留空
    phase          阶段标签（如 kb-repair, kb-expansion）
    priority       high / medium / low
    status         pending / in_progress / blocked / L1-pass / L2-pass / skipped
    depends_on     依赖任务列表
    done_criterion 完成标准列表（自由文本）
    progress_items 原子工作项总数（默认 1）
    progress_done  已完成项数（L2-pass 时自动补全）
    executor       sub-agent / cascade / human
    verifier_l1    L1 验收负责人
    verifier_l2    L2 验收负责人
    created_at     创建日期
    updated_at     最后更新日期
    prompt_file    提示词文件路径（可选）
    report_file    完成报告路径（可选）
"""

import os
import re
import sys
from collections import defaultdict, deque
from datetime import datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("❌ 缺少依赖，请运行: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

# ── 配置 ─────────────────────────────────────────────────────────────────────

STATUS_ICONS = {
    "pending":     "⏳",
    "in_progress": "🔄",
    "blocked":     "🚫",
    "L1-pass":     "🔵",
    "L2-pass":     "✅",
    "skipped":     "⏭️",
}

STATUS_STYLE = {
    "pending":     "fill:#e9ecef,stroke:#adb5bd",
    "in_progress": "fill:#fff3cd,stroke:#ffc107",
    "blocked":     "fill:#f8d7da,stroke:#dc3545",
    "L1-pass":     "fill:#cce5ff,stroke:#0056b3",
    "L2-pass":     "fill:#d4edda,stroke:#28a745",
    "skipped":     "fill:#f8f9fa,stroke:#6c757d",
}

PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}


# ── 解析 ──────────────────────────────────────────────────────────────────────

def parse_frontmatter(filepath):
    """解析 Markdown 文件的 YAML frontmatter，返回 (data_dict, body_text)。"""
    text = Path(filepath).read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None, text
    try:
        data = yaml.safe_load(m.group(1)) or {}
        return data, text[m.end():].strip()
    except yaml.YAMLError as e:
        print(f"  ⚠️  YAML 错误 [{filepath.name}]: {e}", file=sys.stderr)
        return None, text


def load_tasks(tasks_dir):
    """加载所有有效任务文件，返回 {task_id: task_dict}。"""
    tasks = {}
    for fp in sorted(Path(tasks_dir).rglob("*.md")):
        data, body = parse_frontmatter(fp)
        if not data or "task_id" not in data:
            continue
        tid = str(data["task_id"])
        if tid in tasks:
            print(f"  ⚠️  重复 task_id [{tid}]，跳过: {fp.name}", file=sys.stderr)
            continue
        data["_body"] = body
        data["_file"] = fp.name
        tasks[tid] = data
    return tasks


# ── 计算 ──────────────────────────────────────────────────────────────────────

def calc_progress(task):
    """返回 (done, total)。L2-pass / skipped 视为全部完成。"""
    total = max(int(task.get("progress_items", 1)), 1)
    if task.get("status") in ("L2-pass", "skipped"):
        return total, total
    return min(int(task.get("progress_done", 0)), total), total


def topo_sort(tasks):
    """Kahn 拓扑排序，返回有序 task_id 列表。"""
    in_deg = defaultdict(int)
    adj = defaultdict(list)
    for tid, task in tasks.items():
        for dep in (task.get("depends_on") or []):
            if dep in tasks:
                adj[dep].append(tid)
                in_deg[tid] += 1
    q = deque(sorted(t for t in tasks if in_deg[t] == 0))
    order = []
    while q:
        n = q.popleft()
        order.append(n)
        for child in sorted(adj[n]):
            in_deg[child] -= 1
            if in_deg[child] == 0:
                q.append(child)
    rest = [t for t in tasks if t not in order]
    if rest:
        print(f"  ⚠️  循环依赖或孤立节点: {rest}", file=sys.stderr)
    return order + rest


# ── 渲染工具 ──────────────────────────────────────────────────────────────────

def ascii_bar(done, total, w=16):
    if total == 0:
        return "░" * w
    n = round(w * done / total)
    return "█" * n + "░" * (w - n)


def pct_str(done, total):
    p = int(100 * done / total) if total else 0
    return f"{done}/{total} ({p}%)"


# ── STATUS.md ────────────────────────────────────────────────────────────────

def gen_status(tasks, out_path):
    order = topo_sort(tasks)

    def is_root(tid):
        return not tasks[tid].get("parent_id")

    leaves = {tid for tid in tasks if not is_root(tid)}

    lines = [
        "# 任务状态板 (Task Evidence Board)",
        "",
        f"> 🕐 自动生成于 **{datetime.now().strftime('%Y-%m-%d %H:%M')}**",
        "> ⚠️  本文件由脚本派生，请勿手动编辑。修改任务请编辑 `tasks/` 目录下对应文件。",
        "",
    ]

    # ── 总体进度 ──
    phases = defaultdict(list)
    for tid in order:
        if tid in leaves:
            phases[tasks[tid].get("phase", "other")].append(tid)

    lines += ["## 总体进度", "", "```"]
    all_d, all_n = 0, 0
    for phase, tids in phases.items():
        d = sum(calc_progress(tasks[t])[0] for t in tids)
        n = sum(calc_progress(tasks[t])[1] for t in tids)
        all_d += d
        all_n += n
        lines.append(f"  {phase:<20}  {ascii_bar(d, n)}  {pct_str(d, n)}")
    sep = "─" * 20
    lines += [
        f"  {sep}  {'─'*16}  {'─'*14}",
        f"  {'全局合计':<18}    {ascii_bar(all_d, all_n)}  {pct_str(all_d, all_n)}",
        "```",
        "",
    ]

    # ── 明细（按父任务分组）──
    lines += ["## 任务明细", ""]

    TABLE_HEAD = [
        "| task_id | 任务名称 | 状态 | 进度 | 优先级 | 依赖 | 执行者 | 报告 |",
        "|:--------|:--------|:-----|:-----|:------:|:-----|:-------|:----:|",
    ]

    def leaf_row(tid):
        t = tasks[tid]
        st = t.get("status", "pending")
        d, n = calc_progress(t)
        deps = " ".join(f"`{x}`" for x in (t.get("depends_on") or [])) or "—"
        prio = PRIORITY_ICONS.get(t.get("priority", "medium"), "⚪")
        name = t.get("task_name", tid)
        pf = t.get("prompt_file", "")
        name_cell = f"[{name}]({pf})" if pf else name
        rf = t.get("report_file", "")
        report_cell = f"[📄]({rf})" if rf else "—"
        return (
            f"| `{tid}` | {name_cell} | {STATUS_ICONS.get(st,'❓')} `{st}` | "
            f"`{ascii_bar(d,n,8)}` {pct_str(d,n)} | {prio} | {deps} | "
            f"{t.get('executor','—')} | {report_cell} |"
        )

    child_map = defaultdict(list)
    for tid in order:
        pid = tasks[tid].get("parent_id")
        if pid and pid in tasks:
            child_map[pid].append(tid)

    for pid in [t for t in order if is_root(t)]:
        p = tasks[pid]
        children = child_map.get(pid, [])
        if not children:
            continue
        pd = sum(calc_progress(tasks[c])[0] for c in children)
        pn = sum(calc_progress(tasks[c])[1] for c in children)
        st_icon = STATUS_ICONS.get(p.get("status", "pending"), "📁")
        lines += [
            f"### {st_icon} `{pid}` — {p.get('task_name', pid)}",
            "",
            f"进度：`{ascii_bar(pd, pn, 20)}` **{pct_str(pd, pn)}**",
            "",
            *TABLE_HEAD,
            *[leaf_row(c) for c in children],
            "",
        ]

    orphans = [t for t in order if t in leaves and tasks[t].get("parent_id") not in tasks]
    if orphans:
        lines += ["### 📁 未分组任务", "", *TABLE_HEAD, *[leaf_row(t) for t in orphans], ""]

    # ── 待处理清单（含 done_criterion）──
    pending = [
        t for t in order
        if t in leaves and tasks[t].get("status") not in ("L2-pass", "skipped")
    ]
    if pending:
        lines += ["## 待处理任务 & 完成标准", ""]
        for tid in pending:
            t = tasks[tid]
            st = t.get("status", "pending")
            d, n = calc_progress(t)
            lines.append(
                f"### {STATUS_ICONS.get(st,'❓')} `{tid}` — {t.get('task_name', tid)}"
                f"  `{pct_str(d, n)}`"
            )
            criteria = t.get("done_criterion") or []
            if criteria:
                lines.append("")
                for c in criteria:
                    lines.append(f"- [ ] {c}")
            lines.append("")

    lines += [
        "---", "",
        "## 图例", "",
        *[f"- {icon} `{st}`" for st, icon in STATUS_ICONS.items()],
        "",
        f"*由 [`generate_status.py`](../generate_status.py) 生成 · 数据源: `tasks/`*",
    ]

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ STATUS.md      → {out_path}")


# ── task-graph.mmd ───────────────────────────────────────────────────────────

def safe_id(tid):
    return re.sub(r"[^A-Za-z0-9_]", "_", str(tid))


def gen_mermaid(tasks, out_path):
    order = topo_sort(tasks)

    def is_root(tid):
        return not tasks[tid].get("parent_id")

    child_map = defaultdict(list)
    for tid in order:
        pid = tasks[tid].get("parent_id")
        if pid and pid in tasks:
            child_map[pid].append(tid)

    lines = ["graph TD", ""]
    rendered = set()

    for pid in [t for t in order if is_root(t)]:
        p = tasks[pid]
        children = child_map.get(pid, [])
        pd = sum(calc_progress(tasks[c])[0] for c in children)
        pn = sum(calc_progress(tasks[c])[1] for c in children)
        sub_id = safe_id(pid)
        sub_label = f'{p.get("task_name", pid)} — {pct_str(pd, pn)}'
        lines.append(f'    subgraph {sub_id} ["{sub_label}"]')

        for cid in children:
            t = tasks[cid]
            st = t.get("status", "pending")
            icon = STATUS_ICONS.get(st, "❓")
            d, n = calc_progress(t)
            lbl = f'{icon} {cid}\\n{t.get("task_name", cid)}\\n{pct_str(d, n)}'
            nid = safe_id(cid)
            if st == "L2-pass":
                lines.append(f'        {nid}(["{lbl}"])')
            elif st == "in_progress":
                lines.append(f'        {nid}[/"{lbl}"/]')
            elif st == "blocked":
                lines.append(f'        {nid}{{"{lbl}"}}')
            else:
                lines.append(f'        {nid}["{lbl}"]')
            rendered.add(cid)

        lines += ["    end", f"    style {sub_id} fill:#f8f9fa,stroke:#dee2e6", ""]

    for tid in order:
        if tid not in rendered and not is_root(tid):
            t = tasks[tid]
            st = t.get("status", "pending")
            icon = STATUS_ICONS.get(st, "❓")
            d, n = calc_progress(t)
            lbl = f'{icon} {tid}\\n{t.get("task_name", tid)}\\n{pct_str(d, n)}'
            lines.append(f'    {safe_id(tid)}["{lbl}"]')
            rendered.add(tid)

    lines.append("")
    for tid in order:
        for dep in (tasks[tid].get("depends_on") or []):
            if dep in tasks:
                lines.append(f"    {safe_id(dep)} --> {safe_id(tid)}")

    lines.append("")
    for tid in rendered:
        st = tasks[tid].get("status", "pending")
        if st in STATUS_STYLE:
            lines.append(f"    style {safe_id(tid)} {STATUS_STYLE[st]}")

    Path(out_path).write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✅ task-graph.mmd → {out_path}")


# ── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    tasks_dir = sys.argv[1] if len(sys.argv) > 1 else "tasks"
    out_dir   = sys.argv[2] if len(sys.argv) > 2 else "output"

    if not Path(tasks_dir).is_dir():
        print(f"❌ 任务目录不存在: {tasks_dir}", file=sys.stderr)
        sys.exit(1)

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    print(f"📂 扫描: {Path(tasks_dir).resolve()}")
    tasks = load_tasks(tasks_dir)
    print(f"📋 发现 {len(tasks)} 个任务\n")

    gen_status(tasks, os.path.join(out_dir, "STATUS.md"))
    gen_mermaid(tasks, os.path.join(out_dir, "task-graph.mmd"))

    print(f"\n🎉 完成！输出目录: {Path(out_dir).resolve()}")


if __name__ == "__main__":
    main()
