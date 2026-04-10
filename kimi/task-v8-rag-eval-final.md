# T3 任务: Phase 8 RAG-EVAL — 全量回归评测（entry_count=731）

## ⚠️ 所有命令通过 SSH 执行，服务器 IP: 192.168.100.165

## Step 1: 确认服务状态

```powershell
ssh easten@192.168.100.165 "curl -s http://localhost:8000/api/kb/stats 2>/dev/null || curl -s http://localhost:8000/kb/stats"
```

## Step 2: 运行官方评测脚本

```powershell
ssh easten@192.168.100.165 "cd /home/easten/dev/yixiaoguan && python3 scripts/eval/run_eval_v3.py --out /tmp/eval-v8-final.json 2>&1 | tail -30"
```

如果脚本路径不对，先查找：
```powershell
ssh easten@192.168.100.165 "find /home/easten/dev/yixiaoguan/scripts -name 'run_eval*.py' 2>/dev/null"
```

## Step 3: 读取评测结果

```powershell
ssh easten@192.168.100.165 "cat /tmp/eval-v8-final.json 2>/dev/null | python3 -m json.tool"
```

## Step 4: 如果没有官方脚本，手动抽测10题（v8新增方向）

通过 SSH 内的 curl 测试以下问题，记录是否有实质答案：

```powershell
ssh easten@192.168.100.165 @"
for query in '通勤车时刻表' '图书馆暑假开馆时间' '国庆节后勤安排' '出国留学奖学金申请' '研究生推免简章' '心理咨询怎么预约' '新生入学指南' '个人所得税汇算怎么办' '餐厅一卡通怎么用' '校园招聘会时间'; do
  result=\$(curl -s -X POST http://localhost:8000/api/chat -H 'Content-Type: application/json' -d "{\"message\":\"\$query\",\"session_id\":\"eval\"}" 2>/dev/null | python3 -c 'import sys,json; d=json.load(sys.stdin); a=d.get("answer",""); print("PASS" if len(a)>50 and "不知道" not in a and "无法" not in a else "FAIL")')
  echo "\$query: \$result"
done
"@
```

## Step 5: 生成评测报告写入 `kimi/rag-eval-v8-final-report.md`

格式：
```markdown
# RAG-EVAL v8 Final Report

- 评测时间: 2026-04-10
- entry_count: 731
- 测试题数: XX
- PASS: XX  FAIL: XX
- 通过率: XX%

## 详细结果
| 问题 | 结果 | 答案摘要 |
|------|------|---------|

## v8 新增 KB 效果评估
- 通勤车/后勤类: X/3
- 图书馆类: X/2
- 国际交流类: X/2
- 财务/就业类: X/3

## 结论
```

请开始执行。
