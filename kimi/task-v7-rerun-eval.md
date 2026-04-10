# T3 任务: 重跑 RAG 评测（修正后）

## 重要：执行方式

**必须使用 `ssh` 在远程服务器执行所有命令。**
**Shell 工具中请这样调用：**

```
ssh easten@10.80.3.165 "具体命令"
```

**绝对不要直接执行 curl 或 python，必须包裹在 ssh 命令中！**

## Step 1: 确认服务在线

```
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats"
```

期望返回 entry_count >= 260。

## Step 2: 运行评测脚本

评测集 `scripts/eval/eval-set-v3.yaml` 已修正，通过 Mutagen 同步到服务器。

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v3.py"
```

## Step 3: 查看报告

```
ssh easten@10.80.3.165 "cat /home/easten/dev/yixiaoguan/scripts/eval/eval-report-v3.md"
```

## Step 4: 复制报告到本地

将 Step 3 的输出内容写入本地文件 `kimi/rag-eval-v7-final-report.md`。

完成后输出 Recall@5 和拒答准确率的最终结果。
