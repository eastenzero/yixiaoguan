# T3 任务: v6 RAG 拒答准确率修复（机构名过滤 Scope Guard）

## 问题描述

RAG-EVAL v2 结果：
- Recall@5: 80.0% ✅
- 拒答准确率: 85.7% ❌（目标 ≥ 90%）

失败原因：以下 2 道 reject 题被错误命中（语义相似但属于其他机构）：
- eval-016: "北京大学图书馆几点开门？"（score=0.585）
- new-009: "山东大学图书馆几点开门？"（score=0.698）

## 修复方案

在 ai-service 的检索/回答逻辑中，增加**机构名前置过滤器（Scope Guard）**：

**规则**：若用户问题明确提到**其他高校名称**（非山东第一医科大学/山一大/SDFMU），则**直接拒答**，不进入检索。

## 执行步骤

### Step 1: 找到 ai-service 的检索入口

1. 读取 `/home/easten/dev/yixiaoguan/services/ai-service/` 目录结构
2. 找到处理 `/kb/search` 和 `/chat` 请求的路由文件（通常在 `app/routers/` 或 `app/api/`）
3. 找到实际执行检索逻辑的函数（通常在 `app/services/` 或 `app/core/`）

### Step 2: 实现 Scope Guard

在检索逻辑的**前置判断**处（query 进入 ChromaDB 检索之前），添加如下过滤：

```python
# Scope Guard: 过滤明确提及其他机构的问题
OTHER_INSTITUTIONS = [
    "北京大学", "清华大学", "复旦大学", "浙江大学", "南京大学",
    "山东大学", "中国人民大学", "上海交通大学", "武汉大学", "中南大学",
    "哈尔滨工业大学", "西安交通大学", "同济大学", "北京师范大学",
    "华中科技大学", "中山大学", "吉林大学", "四川大学", "厦门大学",
    "北京航空航天大学", "东南大学", "南开大学", "天津大学",
    # 简写形式
    "北大", "清华", "复旦", "浙大", "南大", "山大",
]

def is_out_of_scope(query: str) -> bool:
    """检查是否明确询问其他机构（非山一大）"""
    query_lower = query.lower()
    for inst in OTHER_INSTITUTIONS:
        if inst in query:
            return True
    return False
```

若 `is_out_of_scope(query)` 返回 `True`，则返回拒答响应（不进入 ChromaDB 检索）：
- 对于 `/kb/search`：返回空结果列表
- 对于 `/chat`：返回"抱歉，我只能回答山东第一医科大学的相关问题，无法提供其他学校的信息。"

### Step 3: 验证修改

1. 找到修改的文件和位置
2. 确认修改**最小化**（只在现有检索入口加前置判断，不重构其他代码）
3. 在 165 服务器上验证修改已存在

### Step 4: 重启 ai-service

在 165 服务器上，ai-service 以 root 身份运行于端口 8000（PID 已知）。
重启方式：找到是否有 systemctl 服务单元或启动脚本，或直接通过 hot-reload 重启。

检查是否有服务管理方式：
```bash
systemctl list-units | grep -i ai
# 或
ls /etc/systemd/system/ | grep -i ai
```

如果有 systemd 服务，使用：
```bash
echo "ZhaYeFan05.07.14" | sudo -S systemctl restart ai-service
```

如果没有，记录"需要手动重启"，暂不重启。

### Step 5: 重新运行评测（如果已重启）

如果 ai-service 已成功重启，在 165 服务器上运行：
```bash
cd /home/easten/dev/yixiaoguan
/home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v2.py
```

输出新的评测结果。

## 输出报告

完成后输出：
1. 修改了哪个文件的哪行代码
2. Scope Guard 的具体实现位置
3. ai-service 重启状态（是否成功）
4. 若评测已重跑：新的 Recall@5 和拒答准确率

## 注意事项
- **不修改 KB 文件和 ChromaDB 数据**，只修改检索前置逻辑
- **不影响正常的山一大问题检索**（不能把有效命中拦截掉）
- 修改必须兼容现有代码风格

请开始执行。
