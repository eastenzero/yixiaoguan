# DOC 重试转换与首批收口说明

## 1. 本次收口完成了什么

本次补齐了首批样本中仅剩的两份 `.doc` 转换失败材料：

- `MAT-20260323-0002`
- `MAT-20260323-0003`

补齐结果：

- 两份材料的 Markdown 已生成
- 清洗后总表已回写为 `success`
- 转换日志已回写为 `success`
- 阻塞清单已标记为 `resolved`

对应 Markdown 产物：

- `knowledge-base/raw/first-batch-processing/converted/markdown/MAT-20260323-0002__附件1：教育在线学生信息与班级实际情况核对方法.md`
- `knowledge-base/raw/first-batch-processing/converted/markdown/MAT-20260323-0003__附件5：学信网学籍注册信息核对方法指南.md`

## 2. 为什么之前看起来像“死循环”

之前的重试方案是：

- 复制到 ASCII 临时路径
- 用 `Word COM -> SaveAs2` 转 `docx`
- 再用 `pandoc` 转 `md`

实际现象是：

- `Word COM` 可以成功 `Open`
- 但会长时间卡在 `SaveAs2`
- 命令行只停在 `save` 阶段，看起来像没有输出

这不是脚本死循环，而是：

- Word COM 的 `SaveAs2` 对这两份旧 `.doc` 不稳定
- 后台会长时间卡住
- 还可能残留 `WINWORD` 进程，导致后续文件被占用

所以后续不要再把 `SaveAs2` 当成这类旧 `.doc` 的首选重试路径。

## 3. 本次实际可行的解决方案

本次验证通过的方案是：

1. 先把原始 `.doc` 复制到 ASCII 临时路径
2. 不再用 `Word COM SaveAs2`
3. 改用系统自带：
   - `C:\Program Files\Microsoft Office\root\Office16\Wordconv.exe`
4. 用 `Wordconv.exe` 先转出 `docx`
5. 再用 `pandoc` 把 `docx` 转成 `Markdown`

这条链路在当前机器上已实测成功。

## 4. 推荐的重试命令

推荐直接使用脚本：

- `scripts/retry_doc_conversion.ps1`

说明：

- 该脚本仍保留“复制到 ASCII 临时路径”的思路
- 但核心转换器已改为 `Wordconv.exe`
- 最后由 `pandoc` 完成 `docx -> md`

示例：

```powershell
& .\scripts\retry_doc_conversion.ps1 `
  -MaterialId 'MAT-20260323-0002' `
  -SourcePath '数据库部分材料\数据库部分材料\2025年工作\2025下-25级新生工作\2025年学籍注册\附件1：教育在线学生信息与班级实际情况核对方法.doc' `
  -OutputMarkdownPath 'knowledge-base\raw\first-batch-processing\converted\markdown\MAT-20260323-0002__附件1：教育在线学生信息与班级实际情况核对方法.md'
```

```powershell
& .\scripts\retry_doc_conversion.ps1 `
  -MaterialId 'MAT-20260323-0003' `
  -SourcePath '数据库部分材料\数据库部分材料\2025年工作\2025下-25级新生工作\2025年学籍注册\附件5：学信网学籍注册信息核对方法指南.doc' `
  -OutputMarkdownPath 'knowledge-base\raw\first-batch-processing\converted\markdown\MAT-20260323-0003__附件5：学信网学籍注册信息核对方法指南.md'
```

## 5. 如何判断不是卡死

脚本会按步骤输出：

- `[1/6] Copy source to ASCII temp path`
- `[2/6] Convert DOC to DOCX with Wordconv.exe`
- `[3/6] Verify DOCX output`
- `[4/6] Run pandoc`
- `[5/6] Verify Markdown output`
- `[6/6] Done`

如果当前脚本长时间没有推进到 `[3/6]`，优先检查两件事：

建议做法：

1. `Wordconv.exe` 路径是否存在
2. `pandoc` 是否可直接在当前终端调用

只有在你主动退回旧的 `Word COM / SaveAs2` 方案时，才需要考虑结束残留 `WINWORD` 进程。

## 6. 本次对产物的回写

已更新：

- `knowledge-base/raw/first-batch-processing/manifests/first-batch-material-index.cleaned.csv`
- `knowledge-base/raw/first-batch-processing/logs/conversion-log.csv`
- `knowledge-base/raw/first-batch-processing/manifests/first-batch-conversion-blockers.csv`

阻塞清单当前保留为历史记录，但已新增：

- `blocker_status`
- `resolution_notes`
- `resolved_at`

用于表明该问题已解决，而不是简单删除旧记录。

## 7. 关于字段命名 D 的结论

当前不建议强行把所有文件里的状态字段改成完全同名，因为会破坏已有产物兼容性。

本轮结论：

- 保留 `conversion-log.csv` 中的 `status`
- 保留 `first-batch-material-index.cleaned.csv` 中的 `conversion_status`
- 在后续自动化读取时做字段映射：
  - `conversion-log.status` 对应转换结果状态
  - `cleaned.csv.conversion_status` 对应总表视角的转换状态

也就是说：

- 现阶段采用“兼容保留 + 读取时映射”
- 不做高风险字段重命名

## 8. 当前首批样本是否可以进入下一阶段

可以。

当前首批样本已满足进入“规则抽取草案表”阶段的条件：

- 首批样本候选问题已细化
- 两份 `.doc` 阻塞已补齐
- 转换结果已完整可读
- PDF 产物已保留全套结构

后续可以继续：

1. 从现有 Markdown / PDF `full.md` 中抽取规则
2. 生成规则抽取草案表
3. 再进入知识条目草稿生产
