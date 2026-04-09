# T2 (Kiro) 下发给 T3 (Kimi) 的提示词

> **用法**: 在 165 服务器上，T2 (Kiro) 把此提示词传给 Kimi Code 执行。
> 复制下方 `---PROMPT START---` 到 `---PROMPT END---` 之间的内容。

---PROMPT START---
你是 T3 执行器，当前任务：rework-01-pdf-supplement（F-V5D-01 返工：补齐 PDF）。

必须先读取以下文件（按顺序）：
1) ~/dev/yixiaoguan/.teb/antipatterns.md
2) ~/dev/yixiaoguan/.tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_task.md

规则冲突时以 _task.md 为准。你已获得"继续"授权，直接执行，不要等待交互确认。

允许修改路径（scope）：
- ~/dev/yixiaoguan/deploy/materials/

禁止修改：
- apps/
- services/
- deploy/nginx/
- deploy/docker-compose.yml
- knowledge-base/entries/

执行步骤（严格按 _task.md instructions 执行）：
1. which pandoc — 检查 pandoc 是否可用
2a. pandoc 可用 → 转换 student-handbook.md / knowledge-base-v2.md → .pdf
2b. pandoc 不可用 → 用 python3 生成最小合规 PDF 占位（内容见 _task.md step 2b）
3. 更新 material-index.json（filename 后缀改为 .pdf，format 改为 pdf）
4. chmod 644 deploy/materials/*.pdf
5. docker exec yx_nginx ls 确认 materials 目录挂载

硬约束：
- 只做以上 5 步，不顺手修改其他文件
- 遇到权限或命令不存在：标记 BLOCKED，继续执行下一步
- 执行过程中不重启任何容器（Nginx 已挂载 volume，无需重启）

完成后必须将报告写入：
~/dev/yixiaoguan/.tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_report.md

报告格式（严格按此四段）：
STEP-PLAN
STEP-EXECUTED
STEP-CHECK
BLOCKERS
---PROMPT END---

---

## T2 (Kiro) 调用 Kimi 的完整命令

在 165 服务器上运行：

```bash
cd ~/dev/yixiaoguan

NO_COLOR=1 kimi --print -p "
你是 T3 执行器，当前任务：rework-01-pdf-supplement（F-V5D-01 返工：补齐 PDF）。

必须先读取以下文件（按顺序）：
1) .teb/antipatterns.md
2) .tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_task.md

规则冲突时以 _task.md 为准。你已获得继续授权，直接执行，不要等待交互确认。

允许修改路径：deploy/materials/
禁止修改：apps/ services/ deploy/nginx/ deploy/docker-compose.yml

执行步骤（严格按 _task.md instructions 顺序）：
1. which pandoc
2a. pandoc 可用 → pandoc student-handbook.md -o student-handbook.pdf（类似 knowledge-base-v2）
2b. pandoc 不可用 → python3 生成最小 PDF 占位（见 _task.md step 2b）
3. python3 更新 material-index.json 的 filename 后缀为 .pdf、format 为 pdf
4. chmod 644 deploy/materials/*.pdf
5. docker exec yx_nginx ls 确认挂载

遇到 BLOCKED 就标记继续，不中断。不重启任何容器。
报告写入：.tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_report.md
仅输出：STEP-PLAN / STEP-EXECUTED / STEP-CHECK / BLOCKERS
"
```

---

## T2 验收清单（T3 执行完后执行）

```bash
# L0: 报告存在
test -f ~/dev/yixiaoguan/.tasks/v5d-source-material-viewer/rework-01-pdf-supplement/_report.md \
  && echo "L0 PASS" || echo "L0 FAIL"

# L0: PDF 文件存在
ls ~/dev/yixiaoguan/deploy/materials/student-handbook.pdf \
  && echo "L0-PDF PASS" || echo "L0-PDF FAIL"

# L1: JSON 合法且 format=pdf
python3 -c "
import json
with open('/root/dev/yixiaoguan/deploy/materials/material-index.json') as f:
    d = json.load(f)
formats = [m.get('format') for m in d.get('materials', [])]
print('L1 PASS' if all(f=='pdf' for f in formats) else f'L1 FAIL: formats={formats}')
"

# L2: HTTP 访问
CODE=$(curl -s -o /dev/null -w "%{http_code}" http://192.168.100.165/materials/student-handbook.pdf)
[ "$CODE" = "200" ] || [ "$CODE" = "206" ] && echo "L2 PASS ($CODE)" || echo "L2 FAIL ($CODE)"
```
