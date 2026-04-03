"""
R1-v2 重映射处理器
解决 old_kb_id 一对多映射问题
"""

import csv
from collections import defaultdict
from pathlib import Path

# 路径配置
BASE_DIR = Path("C:/Users/Administrator/Documents/code/yixiaoguan")
MANIFESTS_DIR = BASE_DIR / "knowledge-base/raw/first-batch-processing/manifests"
DRAFTS_DIR = BASE_DIR / "knowledge-base/entries/first-batch-drafts"

# 输入文件
INPUT_REMAP_PLAN = MANIFESTS_DIR / "batch-r1-kb-id-remap-plan.csv"
INPUT_REBUILD_NEEDED = MANIFESTS_DIR / "batch-r1-kb-draft-rebuild-needed.csv"

# 输出文件
OUTPUT_REMAP_PLAN_V2 = MANIFESTS_DIR / "batch-r1-kb-id-remap-plan-v2.csv"
OUTPUT_REBUILD_NEEDED_V2 = MANIFESTS_DIR / "batch-r1-kb-draft-rebuild-needed-v2.csv"


def load_csv(filepath):
    """加载 CSV 文件"""
    rows = []
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_existing_kb_files():
    """获取草稿目录中实际存在的 KB 文件"""
    existing = set()
    if DRAFTS_DIR.exists():
        for f in DRAFTS_DIR.glob("KB-*.md"):
            kb_id = f.stem  # 去掉 .md
            existing.add(kb_id)
    return existing


def process_remap_v2():
    """处理 R1-v2 重映射"""
    
    # 加载输入数据
    remap_rows = load_csv(INPUT_REMAP_PLAN)
    rebuild_rows = load_csv(INPUT_REBUILD_NEEDED)
    existing_files = get_existing_kb_files()
    
    print(f"📊 输入统计:")
    print(f"   - remap-plan 条目数: {len(remap_rows)}")
    print(f"   - rebuild-needed 条目数: {len(rebuild_rows)}")
    print(f"   - 草稿目录现有文件: {len(existing_files)} 个")
    
    # 按 old_kb_id 分组，检测一对多
    old_kb_groups = defaultdict(list)
    for row in remap_rows:
        old_kb_id = row['old_kb_id']
        old_kb_groups[old_kb_id].append(row)
    
    # 统计冲突
    conflict_count = sum(1 for rows in old_kb_groups.values() if len(rows) > 1)
    print(f"   - 检测到一对多冲突: {conflict_count} 个 old_kb_id")
    
    # R1-v2 输出数据
    remap_v2_rows = []
    rebuild_v2_rows = []
    
    # 跳过计数
    skipped_rex = 0
    skipped_conflict = 0
    
    # 处理每个 old_kb_id 分组
    for old_kb_id, rows in old_kb_groups.items():
        # 规则 3: KB-REX-* 禁止进入重命名动作
        if old_kb_id.startswith("KB-REX-"):
            skipped_rex += len(rows)
            for row in rows:
                rebuild_v2_rows.append({
                    'source_batch': row['source_batch'],
                    'material_id': row['material_id'],
                    'old_kb_id': old_kb_id,
                    'target_new_kb_id': row['new_kb_id'],
                    'source_path': '',  # 需从原 rebuild-needed 查找
                    'status': 'need_rebuild',
                    'decision_reason': 'KB-REX-* 规则类条目禁止重命名',
                    'next_action': 'manual_review'
                })
            continue
        
        # 规则 1 & 2: 一对一映射，冲突时只保留第一条 rename，其余转 rebuild
        is_first = True
        for idx, row in enumerate(rows):
            source_batch = row['source_batch']
            material_id = row['material_id']
            new_kb_id = row['new_kb_id']
            reason = row.get('reason', '')
            
            if is_first:
                # 第一个：可以重命名
                remap_v2_rows.append({
                    'source_batch': source_batch,
                    'material_id': material_id,
                    'old_kb_id': old_kb_id,
                    'new_kb_id': new_kb_id,
                    'action': 'rename',
                    'reason': reason
                })
                is_first = False
            else:
                # 后续冲突项：转入 rebuild-needed
                skipped_conflict += 1
                rebuild_v2_rows.append({
                    'source_batch': source_batch,
                    'material_id': material_id,
                    'old_kb_id': old_kb_id,
                    'target_new_kb_id': new_kb_id,
                    'source_path': '',  # 需查找原始路径
                    'status': 'need_rebuild',
                    'decision_reason': f'old_kb_id={old_kb_id} 一对多冲突，已分配 {rows[0]["new_kb_id"]}',
                    'next_action': 'rebuild_from_source'
                })
    
    # 补充原 rebuild-needed 中的条目
    for row in rebuild_rows:
        old_kb_id = row['kb_id']
        # 检查是否已在 remap_v2 中处理
        if not any(r['old_kb_id'] == old_kb_id for r in remap_v2_rows):
            rebuild_v2_rows.append({
                'source_batch': row.get('source_batch', ''),
                'material_id': row.get('material_id', ''),
                'old_kb_id': old_kb_id,
                'target_new_kb_id': '',
                'source_path': row.get('source_path', ''),
                'status': 'need_rebuild',
                'decision_reason': row.get('reason', ''),
                'next_action': 'rebuild_from_source'
            })
    
    # 保存输出文件
    save_remap_plan_v2(remap_v2_rows)
    save_rebuild_needed_v2(rebuild_v2_rows)
    
    # 验收报告
    print(f"\n✅ R1-v2 处理完成:")
    print(f"   - remap-plan-v2: {len(remap_v2_rows)} 条 (可直接重命名)")
    print(f"   - rebuild-needed-v2: {len(rebuild_v2_rows)} 条 (需重建)")
    print(f"   - 跳过的 KB-REX-*: {skipped_rex} 条")
    print(f"   - 冲突转入 rebuild: {skipped_conflict} 条")
    
    # 验收门槛检查
    validate_v2(remap_v2_rows, rebuild_v2_rows, existing_files)


def save_remap_plan_v2(rows):
    """保存重映射计划 v2"""
    fieldnames = ['source_batch', 'material_id', 'old_kb_id', 'new_kb_id', 'action', 'reason']
    with open(OUTPUT_REMAP_PLAN_V2, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"\n📄 已生成: {OUTPUT_REMAP_PLAN_V2.name}")


def save_rebuild_needed_v2(rows):
    """保存重建需求 v2"""
    fieldnames = ['source_batch', 'material_id', 'old_kb_id', 'target_new_kb_id', 
                  'source_path', 'status', 'decision_reason', 'next_action']
    with open(OUTPUT_REBUILD_NEEDED_V2, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"📄 已生成: {OUTPUT_REBUILD_NEEDED_V2.name}")


def validate_v2(remap_rows, rebuild_rows, existing_files):
    """验收门槛验证"""
    print(f"\n🔍 验收门槛检查:")
    
    # 门槛 1: old_kb_id 去重后数量 == 总行数
    old_kb_ids = [r['old_kb_id'] for r in remap_rows]
    unique_count = len(set(old_kb_ids))
    total_count = len(remap_rows)
    
    if unique_count == total_count:
        print(f"   ✅ 门槛 1: old_kb_id 唯一性检查通过 ({unique_count} == {total_count})")
    else:
        print(f"   ❌ 门槛 1: old_kb_id 存在重复 ({unique_count} != {total_count})")
    
    # 门槛 2: action=rename 条目能找到源文件
    rename_rows = [r for r in remap_rows if r['action'] == 'rename']
    found_count = 0
    for row in rename_rows:
        old_kb_id = row['old_kb_id']
        if old_kb_id in existing_files:
            found_count += 1
    
    if found_count == len(rename_rows):
        print(f"   ✅ 门槛 2: 所有 rename 条目源文件存在 ({found_count}/{len(rename_rows)})")
    else:
        print(f"   ⚠️ 门槛 2: 部分 rename 条目源文件缺失 ({found_count}/{len(rename_rows)})")
    
    # 门槛 3: rebuild-needed 条目 status=need_rebuild
    need_rebuild_count = sum(1 for r in rebuild_rows if r['status'] == 'need_rebuild')
    if need_rebuild_count == len(rebuild_rows):
        print(f"   ✅ 门槛 3: 所有 rebuild 条目状态正确 ({need_rebuild_count})")
    else:
        print(f"   ⚠️ 门槛 3: 部分 rebuild 条目状态异常")
    
    # 门槛 4: 统计文档
    print(f"\n📊 最终统计:")
    print(f"   - 可直接重命名: {len(remap_rows)} 条")
    print(f"   - 必须重建: {len(rebuild_rows)} 条")
    print(f"   - 被跳过的 KB-REX-*: {sum(1 for r in remap_rows if r['old_kb_id'].startswith('KB-REX-'))} 条")


if __name__ == "__main__":
    process_remap_v2()
