# T3 任务: 最终 RAG 评测（阈值调整后）

## 重要：所有命令必须通过 SSH 执行

```
ssh easten@10.80.3.165 "命令"
```

**绝对不要在本地直接执行 curl 或 python！**

## Step 1: 确认服务在线 + 文件已同步

```
ssh easten@10.80.3.165 "curl -s http://localhost:8000/kb/stats"
```

```
ssh easten@10.80.3.165 "head -20 /home/easten/dev/yixiaoguan/scripts/eval/run_eval_v3.py | grep REJECT"
```

确认 REJECT_SCORE_THRESHOLD = 0.60。如果仍是 0.55，说明文件未同步，等待几秒后重试。

## Step 2: 运行评测

```
ssh easten@10.80.3.165 "cd /home/easten/dev/yixiaoguan && /home/easten/dev/yixiaoguan/services/ai-service/venv/bin/python scripts/eval/run_eval_v3.py"
```

## Step 3: 查看报告

```
ssh easten@10.80.3.165 "cat /home/easten/dev/yixiaoguan/scripts/eval/eval-report-v3.md"
```

## Step 4: 写入本地报告

将 Step 3 的报告内容写入 `kimi/rag-eval-v7-final-report.md`。

输出最终结论：Recall@5 和拒答准确率是否均达标。
