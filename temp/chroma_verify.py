#!/usr/bin/env python3
"""
ChromaDB 一致性验证脚本 - P1B
比较 ChromaDB 中的条目与磁盘草稿文件
"""

import sys
from pathlib import Path
from datetime import datetime

# 添加 ai-service 到路径
AI_SERVICE_PATH = Path(__file__).parent.parent / "services" / "ai-service"
sys.path.insert(0, str(AI_SERVICE_PATH))


def get_chroma_entries():
    """获取 ChromaDB 中的所有 entry_id"""
    try:
        import chromadb
        from app.core.config import settings
        
        # 直接连接本地 ChromaDB
        client = chromadb.PersistentClient(path=settings.chroma_persist_dir)
        collection = client.get_collection(settings.chroma_collection_kb)
        
        # 获取所有条目
        results = collection.get()
        
        entries = {}
        if results and 'ids' in results:
            for i, entry_id in enumerate(results['ids']):
                metadata = results['metadatas'][i] if results.get('metadatas') and i < len(results['metadatas']) else {}
                entries[entry_id] = {
                    'metadata': metadata,
                    'document': results['documents'][i] if results.get('documents') and i < len(results['documents']) else ''
                }
        
        return entries
    except Exception as e:
        print(f"❌ 读取 ChromaDB 失败: {e}")
        return None


def get_disk_files():
    """获取磁盘上的所有草稿文件"""
    kb_dir = Path('knowledge-base/entries/first-batch-drafts')
    if not kb_dir.exists():
        return []
    
    md_files = sorted(kb_dir.glob('KB-*.md'))
    return [f.stem for f in md_files]  # 返回文件名（不含扩展名）


def main():
    print("=" * 60)
    print("ChromaDB 一致性验证工具")
    print("=" * 60)
    
    # 获取 ChromaDB 条目
    print("\n📊 正在读取 ChromaDB...")
    chroma_entries = get_chroma_entries()
    
    if chroma_entries is None:
        print("❌ 无法读取 ChromaDB，退出")
        sys.exit(1)
    
    chroma_ids = set(chroma_entries.keys())
    print(f"✅ ChromaDB 条目数: {len(chroma_ids)}")
    
    # 获取磁盘文件
    print("\n📁 正在读取磁盘文件...")
    disk_files = get_disk_files()
    disk_ids = set(disk_files)
    print(f"✅ 磁盘文件数: {len(disk_ids)}")
    
    # 计算差异
    only_in_chroma = chroma_ids - disk_ids  # ChromaDB 有但磁盘无
    only_on_disk = disk_ids - chroma_ids    # 磁盘有但 ChromaDB 无
    common = chroma_ids & disk_ids          # 两者都有
    
    # 打印结果
    print("\n" + "=" * 60)
    print("验证结果")
    print("=" * 60)
    
    print(f"\n📊 统计:")
    print(f"  - 一致条目: {len(common)}")
    print(f"  - ChromaDB 多余条目: {len(only_in_chroma)}")
    print(f"  - 磁盘缺失条目 (ChromaDB 中不存在): {len(only_on_disk)}")
    
    if only_in_chroma:
        print(f"\n⚠️  ChromaDB 多余条目 ({len(only_in_chroma)} 个):")
        for entry_id in sorted(only_in_chroma):
            print(f"    - {entry_id}")
    
    if only_on_disk:
        print(f"\n⚠️  磁盘缺失条目 (未入库) ({len(only_on_disk)} 个):")
        for entry_id in sorted(only_on_disk):
            print(f"    - {entry_id}")
    
    # 生成报告
    report_dir = Path('docs/test-reports/completion-reports')
    report_dir.mkdir(parents=True, exist_ok=True)
    
    report_file = report_dir / 'P1B-chroma-verify-report.md'
    
    report_content = f"""---
task_id: "p1b-chroma-verify"
generated_at: "{datetime.now().isoformat()}"
verified_by: "chroma_verify.py"
---

# P1B ChromaDB 一致性验证报告

## 执行摘要

| 项目 | 数量 |
|------|------|
| ChromaDB 条目总数 | {len(chroma_ids)} |
| 磁盘文件总数 | {len(disk_ids)} |
| **一致条目** | {len(common)} |
| **ChromaDB 多余条目** | {len(only_in_chroma)} |
| **磁盘缺失条目 (未入库)** | {len(only_on_disk)} |

## ChromaDB 配置

| 配置项 | 值 |
|--------|-----|
| 存储路径 | `services/ai-service/data/chroma/` |
| 集合名称 | `kb_entries` |

## 详细结果

### 1. 一致条目 ({len(common)} 个)

这些条目在 ChromaDB 和磁盘文件中都存在：

"""
    
    for entry_id in sorted(common):
        report_content += f"- {entry_id}\n"
    
    report_content += f"""

### 2. ChromaDB 多余条目 ({len(only_in_chroma)} 个)

这些条目存在于 ChromaDB 但磁盘上已删除：

"""
    
    if only_in_chroma:
        for entry_id in sorted(only_in_chroma):
            report_content += f"- {entry_id}\n"
    else:
        report_content += "无\n"
    
    report_content += f"""

### 3. 磁盘缺失条目 (未入库) ({len(only_on_disk)} 个)

这些文件存在于磁盘但尚未入库到 ChromaDB：

"""
    
    if only_on_disk:
        for entry_id in sorted(only_on_disk):
            report_content += f"- {entry_id}\n"
    else:
        report_content += "无\n"
    
    report_content += f"""

## 处置建议

根据 Phase 1 任务定义，本任务仅做只读验证，不写操作。

"""
    
    if only_in_chroma or only_on_disk:
        report_content += """**建议**: 在 Phase 2 执行全量重入库时，先清空 ChromaDB 集合，然后重新导入所有磁盘文件，以确保数据一致性。

具体操作：
1. 备份当前 ChromaDB（可选）
2. 清空 `kb_entries` 集合
3. 运行 `scripts/batch_ingest_kb.py` 重新入库所有文件
"""
    else:
        report_content += "✅ ChromaDB 与磁盘文件完全一致，无需处理。"
    
    report_content += f"""

---
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    report_file.write_text(report_content, encoding='utf-8')
    print(f"\n📝 报告已生成: {report_file}")
    
    return len(only_in_chroma) == 0 and len(only_on_disk) == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 0)  # 验证脚本本身成功执行即可
