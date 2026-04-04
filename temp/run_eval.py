#!/usr/bin/env python3
"""
医小馆 RAG 检索质量自动化评测脚本
功能：
1. 调用 ai-service 的 /api/chat 或 /kb/search 接口
2. 计算 Recall@5 与拒答准确率
3. 输出详细评测报告

用法：
    python temp/run_eval.py [--service-url http://localhost:8000] [--eval-file docs/test-reports/eval-set-v1.yaml]
"""

import argparse
import sys
import yaml
import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from pathlib import Path

import requests


@dataclass
class EvalItem:
    """评测项"""
    id: str
    question: str
    expected_behavior: str  # hit / reject / boundary
    expected_entry_ids: List[str]


@dataclass
class EvalResult:
    """单个评测结果"""
    item: EvalItem
    actual_entry_ids: List[str] = field(default_factory=list)
    grounded: bool = True
    guardrail_reason: Optional[str] = None
    answer: str = ""
    hit_expected_in_top5: bool = False  # 期望条目是否在前5中
    recall_at_5: float = 0.0  # 该题的Recall@5
    correct_reject: bool = False  # 是否正确拒答
    error: Optional[str] = None


def load_eval_set(file_path: str) -> List[EvalItem]:
    """加载评测集"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    items = []
    for item in data:
        items.append(EvalItem(
            id=item['id'],
            question=item['question'],
            expected_behavior=item['expected_behavior'],
            expected_entry_ids=item.get('expected_entry_ids', [])
        ))
    return items


def search_kb(service_url: str, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """调用知识库检索接口"""
    url = f"{service_url}/kb/search"
    payload = {
        "query": query,
        "top_k": top_k
    }
    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get('data', [])
    except Exception as e:
        print(f"  [ERROR] 检索请求失败: {e}")
        return []


def chat_query(service_url: str, query: str) -> Dict[str, Any]:
    """调用对话接口"""
    url = f"{service_url}/api/chat"
    payload = {
        "query": query,
        "history": [],
        "use_kb": True,
        "top_k": 5
    }
    try:
        resp = requests.post(url, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"code": 500, "msg": str(e), "data": None}


def calculate_recall_at_5(expected_ids: List[str], actual_ids: List[str]) -> float:
    """计算单题的 Recall@5
    
    Recall@5 = 期望条目中出现在前5结果中的数量 / 期望条目总数
    （支持 chunk 模式下的 entry_id 前缀匹配）
    """
    if not expected_ids:
        return 0.0
    
    hit_count = 0
    for eid in expected_ids:
        for aid in actual_ids[:5]:
            if eid in aid:  # chunk ID 如 KB-0001__chunk_0 包含原始 entry_id
                hit_count += 1
                break
    return hit_count / len(expected_ids)


def is_hit_expected(expected_ids: List[str], actual_ids: List[str]) -> bool:
    """检查是否至少有一个期望条目出现在前5结果中"""
    if not expected_ids:
        return True  # 无期望条目时视为命中
    for eid in expected_ids:
        for aid in actual_ids[:5]:
            if eid in aid:
                return True
    return False


def evaluate_item(item: EvalItem, service_url: str, use_chat: bool = True) -> EvalResult:
    """评测单个问题"""
    result = EvalResult(item=item)
    
    try:
        if use_chat:
            # 使用对话接口
            resp = chat_query(service_url, item.question)
            if resp.get('code') != 0:
                result.error = f"API错误: {resp.get('msg', 'unknown')}"
                return result
            
            data = resp.get('data', {})
            sources = data.get('sources', [])
            result.actual_entry_ids = [s['entry_id'] for s in sources]
            result.grounded = data.get('grounded', True)
            result.guardrail_reason = data.get('guardrail_reason')
            result.answer = data.get('answer', '')
        else:
            # 使用检索接口
            results = search_kb(service_url, item.question, top_k=5)
            result.actual_entry_ids = [r['entry_id'] for r in results]
            result.grounded = True
        
        # 计算指标
        result.recall_at_5 = calculate_recall_at_5(
            item.expected_entry_ids, 
            result.actual_entry_ids
        )
        result.hit_expected_in_top5 = is_hit_expected(
            item.expected_entry_ids, 
            result.actual_entry_ids
        )
        
        # 判断是否拒答
        is_rejected = not result.grounded or (
            result.guardrail_reason and result.guardrail_reason != 'ok'
        )
        
        # 检查是否正确拒答
        if item.expected_behavior in ('reject', 'boundary'):
            # 应拒答的情况
            result.correct_reject = is_rejected or '很抱歉' in result.answer or '尚未学习到' in result.answer
        else:
            # 应命中的情况
            result.correct_reject = False  # 不需要拒答
            
    except Exception as e:
        result.error = str(e)
    
    return result


def run_evaluation(service_url: str, eval_file: str, use_chat: bool = True) -> Dict[str, Any]:
    """执行完整评测"""
    print(f"=" * 60)
    print(f"医小馆 RAG 检索质量评测")
    print(f"=" * 60)
    print(f"服务地址: {service_url}")
    print(f"评测文件: {eval_file}")
    print(f"调用接口: {'/api/chat' if use_chat else '/kb/search'}")
    print(f"-" * 60)
    
    # 加载评测集
    items = load_eval_set(eval_file)
    print(f"加载评测集: {len(items)} 题")
    
    # 分类统计
    hit_items = [i for i in items if i.expected_behavior == 'hit']
    reject_items = [i for i in items if i.expected_behavior == 'reject']
    boundary_items = [i for i in items if i.expected_behavior == 'boundary']
    life_reject_items = [i for i in items if i.expected_behavior == 'reject' and '宿舍' in i.question or '电费' in i.question or '网' in i.question or '热水' in i.question or '卡' in i.question]
    
    print(f"  - 应命中(hit): {len(hit_items)} 题")
    print(f"  - 应拒答(reject): {len(reject_items)} 题")
    print(f"  - 边界情况(boundary): {len(boundary_items)} 题")
    print(f"  - 生活服务类(应拒答): {len(life_reject_items)} 题")
    print(f"-" * 60)
    
    # 执行评测
    results: List[EvalResult] = []
    for i, item in enumerate(items, 1):
        print(f"[{i}/{len(items)}] {item.id}: {item.question[:30]}...", end=' ')
        result = evaluate_item(item, service_url, use_chat)
        results.append(result)
        
        if result.error:
            print(f"[FAIL] {result.error}")
        else:
            if item.expected_behavior == 'hit':
                status = "HIT" if result.hit_expected_in_top5 else "MISS"
            else:
                status = "REJECT_OK" if result.correct_reject else "REJECT_FAIL"
            print(f"[{status}] R@5={result.recall_at_5:.2f}")
        
        time.sleep(0.1)  # 避免请求过快
    
    print(f"-" * 60)
    
    # 计算指标
    metrics = calculate_metrics(results)
    
    # 输出结果
    print_metrics(metrics)
    
    return {
        'metrics': metrics,
        'results': results
    }


def calculate_metrics(results: List[EvalResult]) -> Dict[str, Any]:
    """计算评测指标"""
    
    # 按类别分组
    hit_results = [r for r in results if r.item.expected_behavior == 'hit']
    reject_results = [r for r in results if r.item.expected_behavior == 'reject']
    boundary_results = [r for r in results if r.item.expected_behavior == 'boundary']
    
    # 生活服务类（在reject中，关键词匹配）
    life_keywords = ['宿舍', '电费', '网', '热水', '卡', '报修']
    life_results = [r for r in reject_results if any(k in r.item.question for k in life_keywords)]
    
    # Recall@5: 应命中题目中，期望条目出现在前5的比例
    hit_correct = sum(1 for r in hit_results if r.hit_expected_in_top5)
    recall_at_5 = hit_correct / len(hit_results) if hit_results else 0.0
    
    # 平均 Recall@5
    avg_recall_at_5 = sum(r.recall_at_5 for r in hit_results) / len(hit_results) if hit_results else 0.0
    
    # 拒答准确率: 应拒答题目中被正确拒答的比例
    # 包括 reject 和 boundary 两类
    all_reject = reject_results + boundary_results
    reject_correct = sum(1 for r in all_reject if r.correct_reject)
    reject_accuracy = reject_correct / len(all_reject) if all_reject else 0.0
    
    # 生活服务类拒答准确率
    life_reject_correct = sum(1 for r in life_results if r.correct_reject)
    life_reject_accuracy = life_reject_correct / len(life_results) if life_results else 0.0
    
    # 按类别的详细统计
    category_stats = {}
    for behavior in ['hit', 'reject', 'boundary']:
        cat_results = [r for r in results if r.item.expected_behavior == behavior]
        category_stats[behavior] = {
            'total': len(cat_results),
            'correct': sum(1 for r in cat_results if 
                (behavior == 'hit' and r.hit_expected_in_top5) or 
                (behavior != 'hit' and r.correct_reject)),
            'avg_recall_at_5': sum(r.recall_at_5 for r in cat_results) / len(cat_results) if cat_results else 0.0
        }
    
    return {
        'total': len(results),
        'recall_at_5': round(recall_at_5, 4),
        'avg_recall_at_5': round(avg_recall_at_5, 4),
        'reject_accuracy': round(reject_accuracy, 4),
        'life_reject_accuracy': round(life_reject_accuracy, 4),
        'hit_count': len(hit_results),
        'hit_correct': hit_correct,
        'reject_count': len(reject_results),
        'boundary_count': len(boundary_results),
        'life_reject_count': len(life_results),
        'reject_correct': reject_correct,
        'life_reject_correct': life_reject_correct,
        'category_stats': category_stats
    }


def print_metrics(metrics: Dict[str, Any]):
    """打印评测指标"""
    print("\n" + "=" * 60)
    print("评测结果汇总")
    print("=" * 60)
    
    print(f"\n【核心指标】")
    print(f"  Recall@5 (期望条目命中前5比例): {metrics['recall_at_5']:.2%}")
    print(f"  平均 Recall@5: {metrics['avg_recall_at_5']:.2%}")
    print(f"  拒答准确率: {metrics['reject_accuracy']:.2%}")
    print(f"  生活服务类拒答准确率: {metrics['life_reject_accuracy']:.2%}")
    
    print(f"\n【分类统计】")
    for cat, stats in metrics['category_stats'].items():
        acc = stats['correct'] / stats['total'] if stats['total'] > 0 else 0
        print(f"  {cat}: 总计={stats['total']}, 正确={stats['correct']}, 准确率={acc:.2%}")
    
    print(f"\n【详细数据】")
    print(f"  应命中(hit): {metrics['hit_correct']}/{metrics['hit_count']} 正确")
    print(f"  应拒答(reject+boundary): {metrics['reject_correct']}/{metrics['reject_count'] + metrics['boundary_count']} 正确")
    print(f"  生活服务类(应拒答): {metrics['life_reject_correct']}/{metrics['life_reject_count']} 正确")
    
    print("\n" + "=" * 60)


def save_report(results: List[EvalResult], metrics: Dict[str, Any], output_file: str):
    """保存详细报告"""
    report = {
        'metrics': metrics,
        'details': []
    }
    
    for r in results:
        detail = {
            'id': r.item.id,
            'question': r.item.question,
            'expected_behavior': r.item.expected_behavior,
            'expected_entry_ids': r.item.expected_entry_ids,
            'actual_entry_ids': r.actual_entry_ids[:5],
            'grounded': r.grounded,
            'guardrail_reason': r.guardrail_reason,
            'hit_expected_in_top5': r.hit_expected_in_top5,
            'recall_at_5': round(r.recall_at_5, 4),
            'correct_reject': r.correct_reject,
            'error': r.error,
            'answer_preview': r.answer[:200] + '...' if len(r.answer) > 200 else r.answer
        }
        report['details'].append(detail)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(report, f, allow_unicode=True, sort_keys=False)
    
    print(f"\n详细报告已保存: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='医小馆 RAG 检索质量评测')
    parser.add_argument('--service-url', default='http://localhost:8000',
                        help='ai-service 服务地址 (默认: http://localhost:8000)')
    parser.add_argument('--eval-file', default='docs/test-reports/eval-set-v1.yaml',
                        help='评测集文件路径')
    parser.add_argument('--use-chat', action='store_true', default=True,
                        help='使用 /api/chat 接口 (默认)')
    parser.add_argument('--use-search', action='store_true',
                        help='使用 /kb/search 接口')
    parser.add_argument('--output', default='docs/test-reports/eval-report-v1.yaml',
                        help='输出报告文件路径')
    
    args = parser.parse_args()
    
    use_chat = not args.use_search
    
    # 检查评测集文件
    if not Path(args.eval_file).exists():
        print(f"错误: 评测集文件不存在: {args.eval_file}")
        sys.exit(1)
    
    # 执行评测
    result = run_evaluation(args.service_url, args.eval_file, use_chat)
    
    # 保存报告
    save_report(result['results'], result['metrics'], args.output)
    
    # 返回码: 如果指标不达标则返回非0
    metrics = result['metrics']
    exit_code = 0
    
    if metrics['recall_at_5'] < 0.85:
        print(f"\n[WARNING] Recall@5 ({metrics['recall_at_5']:.2%}) < 目标 (85%)")
        exit_code = 1
    
    if metrics['reject_accuracy'] < 0.90:
        print(f"\n[WARNING] 拒答准确率 ({metrics['reject_accuracy']:.2%}) < 目标 (90%)")
        exit_code = 1
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
