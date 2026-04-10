# T3 任务: v6-kb-expansion RAG-EVAL（评测脚本生成 + 执行）

## 任务目标
1. 在 `scripts/eval/` 目录下生成评测脚本 `run_eval_v2.py`
2. 在 165 服务器上运行该脚本，对 `eval-set-v2.yaml` 中的 52 道题进行 RAG 检索质量评测
3. 输出评测报告到 `scripts/eval/eval-report-v2.md`

## 评测方法

- 对每道 `expected_behavior: hit` 的题目，调用 `GET http://localhost:8000/kb/search?q={question}&top_k=5`
- 检查 `expected_entry_ids` 中至少有 1 个出现在 top-5 结果的 `entry_id` 中
- 对每道 `expected_behavior: reject` 或 `boundary` 的题目，调用 AI 聊天接口或仅检索接口，判断是否拒答
- 计算：
  - **Recall@5**：hit 题命中率（expected_entry_ids 中至少1个在top5中）
  - **拒答准确率**：reject 题中正确拒答的比例

## 评测脚本规格

生成 `scripts/eval/run_eval_v2.py`，内容如下：

```python
#!/usr/bin/env python3
"""
RAG Eval v2 - 医小管知识库检索质量评测
针对 eval-set-v2.yaml 运行，输出 Markdown 报告
"""
import yaml
import requests
import urllib.parse
import json
from datetime import datetime

EVAL_SET = "scripts/eval/eval-set-v2.yaml"
KB_SEARCH_URL = "http://localhost:8000/kb/search"
TOP_K = 5
REPORT_PATH = "scripts/eval/eval-report-v2.md"

def search(question: str, top_k: int = TOP_K):
    try:
        params = {"q": question, "top_k": top_k}
        r = requests.get(KB_SEARCH_URL, params=params, timeout=15)
        data = r.json()
        # 返回结果中的 entry_id 列表
        results = data.get("data", data.get("results", []))
        if isinstance(results, list):
            return [item.get("entry_id", item.get("id", "")) for item in results]
        return []
    except Exception as e:
        return [f"ERROR: {e}"]

def run_eval():
    with open(EVAL_SET, encoding="utf-8") as f:
        items = yaml.safe_load(f)

    hit_total = 0
    hit_correct = 0
    reject_total = 0
    reject_correct = 0
    boundary_total = 0

    results = []

    for item in items:
        qid = item["id"]
        question = item["question"]
        behavior = item["expected_behavior"]
        expected_ids = item.get("expected_entry_ids", [])

        if behavior == "hit" or item.get("category", "") in ("grounding-verify-in", "grounding-verify-boundary"):
            hit_total += 1
            top_ids = search(question)
            matched = any(eid in top_ids for eid in expected_ids) if expected_ids else False
            hit_correct += 1 if matched else 0
            results.append({
                "id": qid, "q": question, "behavior": behavior,
                "expected": expected_ids, "got": top_ids[:5],
                "pass": matched
            })

        elif behavior in ("reject",):
            if item.get("category", "") not in ("grounding-verify-in", "grounding-verify-boundary"):
                reject_total += 1
                top_ids = search(question)
                # 拒答判定：检索结果为空或相关度极低（返回空列表或含ERROR）
                is_rejected = len(top_ids) == 0 or all("ERROR" in str(i) for i in top_ids)
                reject_correct += 1 if is_rejected else 0
                results.append({
                    "id": qid, "q": question, "behavior": behavior,
                    "expected": [], "got": top_ids[:3],
                    "pass": is_rejected
                })

        elif behavior == "boundary":
            boundary_total += 1
            results.append({
                "id": qid, "q": question, "behavior": behavior,
                "expected": expected_ids, "got": [],
                "pass": None
            })

    recall_at5 = hit_correct / hit_total if hit_total > 0 else 0
    reject_acc = reject_correct / reject_total if reject_total > 0 else 0

    # 生成报告
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# RAG-EVAL Report v2",
        f"",
        f"**评测时间**: {now}",
        f"**评测集**: {EVAL_SET}（共 {len(items)} 题）",
        f"",
        f"## 核心指标",
        f"",
        f"| 指标 | 数值 | 基线要求 | 状态 |",
        f"|------|------|---------|------|",
        f"| Recall@5（hit题命中率） | {recall_at5:.1%} | ≥ 80% | {'✅' if recall_at5 >= 0.80 else '❌'} |",
        f"| 拒答准确率 | {reject_acc:.1%} | ≥ 90% | {'✅' if reject_acc >= 0.90 else '❌'} |",
        f"| Hit题数 | {hit_total} | - | - |",
        f"| Reject题数 | {reject_total} | - | - |",
        f"| Boundary题数 | {boundary_total} | - | - |",
        f"",
        f"## 详细结果",
        f"",
        f"### Hit 题（应命中）",
        f"",
        f"| ID | 问题 | 期望 | 命中 | 状态 |",
        f"|-----|------|------|------|------|",
    ]

    for r in results:
        if r["behavior"] in ("hit",) or True:
            if r["behavior"] == "hit":
                exp_str = ", ".join(r["expected"][:2]) if r["expected"] else "-"
                got_str = ", ".join(str(g) for g in r["got"][:2]) if r["got"] else "无结果"
                status = "✅" if r["pass"] else "❌"
                lines.append(f"| {r['id']} | {r['q'][:20]}... | {exp_str} | {got_str} | {status} |")

    lines += [
        f"",
        f"### Reject 题（应拒答）",
        f"",
        f"| ID | 问题 | 返回结果数 | 状态 |",
        f"|-----|------|-----------|------|",
    ]

    for r in results:
        if r["behavior"] == "reject":
            got_count = len(r["got"])
            status = "✅" if r["pass"] else "❌"
            lines.append(f"| {r['id']} | {r['q'][:20]}... | {got_count} | {status} |")

    lines += [
        f"",
        f"## 结论",
        f"",
    ]

    if recall_at5 >= 0.80 and reject_acc >= 0.90:
        lines.append("**✅ RAG-EVAL PASS** — 所有核心指标达标，可进入生产发布流程。")
    else:
        lines.append("**❌ RAG-EVAL PARTIAL** — 部分指标未达基线，需检查失败题目并修复。")

    report = "\n".join(lines)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n{'='*60}")
    print(f"RAG-EVAL v2 完成")
    print(f"  Recall@5: {recall_at5:.1%} ({'PASS' if recall_at5>=0.80 else 'FAIL'})")
    print(f"  拒答准确率: {reject_acc:.1%} ({'PASS' if reject_acc>=0.90 else 'FAIL'})")
    print(f"  报告: {REPORT_PATH}")
    print(f"{'='*60}\n")

    return recall_at5, reject_acc

if __name__ == "__main__":
    run_eval()
```

## 执行步骤

1. 将上述脚本写入 `scripts/eval/run_eval_v2.py`
2. 在 165 服务器上（SSH: easten@192.168.100.165）使用 venv Python 运行：
   ```bash
   cd /home/easten/dev/yixiaoguan
   /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v2.py
   ```
3. 读取并输出 `scripts/eval/eval-report-v2.md` 的完整内容

## 注意事项
- `/kb/search` 接口的响应结构需要适配，如果 `data` 字段结构不符，请读取接口文档或先 curl 一次查看响应格式，再调整代码
- 超时设置为 15 秒/题，全部 52 题约 5 分钟完成
- 如果接口返回 404，请先 `curl http://localhost:8000/kb/search?q=test&top_k=3` 查看实际响应格式

请开始执行。
