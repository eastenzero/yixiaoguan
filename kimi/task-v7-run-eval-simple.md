# T3 任务: 在 165 服务器上运行 RAG 评测脚本

## 重要提醒
**所有命令必须通过 SSH 执行，格式如下：**
```
ssh easten@10.80.3.165 "command here"
```
**绝对不要在本地执行 curl 或 python 命令！**

## 步骤

### Step 1: 确认服务在线
```bash
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats"
```

### Step 2: 运行评测脚本
```bash
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v3.py"
```

### Step 3: 查看评测报告
```bash
ssh easten@10.80.3.165 "cat /home/easten/dev/yixiaoguan/scripts/eval/eval-report-v3.md"
```

### Step 4: 将报告复制到本地 kimi 目录
读取上一步的报告内容，写入本地文件 `kimi/rag-eval-v7-report.md`。

完成后输出评测结论（PASS/FAIL）。
