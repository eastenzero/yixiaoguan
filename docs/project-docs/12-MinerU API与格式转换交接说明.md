# MinerU API 与格式转换交接说明

## 1. 当前定版口径

这套格式转换方案已经定版：

- `docx -> pandoc -> Markdown`
- `doc -> Word COM -> docx -> pandoc -> Markdown`
- `xlsx -> Excel COM -> CSV`
- `xls -> Excel COM -> xlsx -> CSV`
- `pdf -> MinerU API`

详细规则见：

- [11-格式转换执行方案.md](C:/Users/Administrator/Documents/code/yixiaoguan/docs/11-格式转换执行方案.md)

## 2. MinerU API 已实测跑通

当前机器上，MinerU API 已经完成两次闭环测试：

1. 上传本地 PDF
2. 轮询解析状态
3. 下载结果 zip
4. 保存 API 返回元数据
5. 解压完整结果目录
6. 抽出 `full.md`

测试产物目录：

- [mineru-api-test](C:/Users/Administrator/Documents/code/yixiaoguan/knowledge-base/raw/mineru-api-test)
- [mineru-api-test-script](C:/Users/Administrator/Documents/code/yixiaoguan/knowledge-base/raw/mineru-api-test-script)

## 3. 当前脚本位置

脚本实际位置是：

- [scripts/mineru_api_extract.py](C:/Users/Administrator/Documents/code/yixiaoguan/scripts/mineru_api_extract.py)

不是仓库根目录。

## 4. 环境变量与认证

不要把 API Key 写进仓库。

优先推荐两种方式：

1. 当前终端环境变量
2. 仓库本地密钥文件 `.secrets/mineru.env`

环境变量方式：

```powershell
$env:MINERU_API_KEY='你的_api_key'
```

文件方式：

1. 复制模板文件：

```powershell
Copy-Item .secrets\\mineru.env.example .secrets\\mineru.env
```

2. 编辑：

```text
MINERU_API_KEY=你的_api_key
```

脚本默认按以下顺序读取：

1. `--api-key`
2. 环境变量 `MINERU_API_KEY`
3. 本地文件 `.secrets/mineru.env`

也支持命令行显式传入：

```powershell
python scripts/mineru_api_extract.py --api-key '你的_api_key' ...
```

但不建议长期这么使用。

## 5. 脚本当前产物

对每个 PDF，脚本当前会产出：

- `batch_id.zip`
- `batch_id.result.json`
- `batch_id.full.md`
- `batch_id/` 解压目录

其中：

- `result.json` 是 API 返回的元数据，不是 MinerU 的正文结构化 JSON
- MinerU 的正文结构化结果在解压目录里，例如：
  - `content_list_v2.json`
  - `layout.json`
  - `images/`

后续知识抽取默认优先读取：

1. `batch_id/full.md`
2. 必要时补读解压目录中的 JSON

## 6. 基本用法

```powershell
$env:MINERU_API_KEY='你的_api_key'
python scripts/mineru_api_extract.py `
  --input "C:\path\to\input.pdf" `
  --output-dir "C:\path\to\output"
```

脚本输出会包含：

- `batch_id`
- zip 路径
- API 元数据路径
- 提取出的 `full.md` 路径
- 解压目录路径

## 7. 推荐执行顺序

建议后续统一按这个顺序执行：

1. `doc/docx`
2. `xls/xlsx`
3. `pdf -> MinerU API`

原因是：

- Office 文件数量更多，先转出来更利于建立主文本层
- PDF 结构更复杂，单独走 API 通道更清晰

## 8. 给其他 AI 的最小交接口径

如果未来把这部分工作交给其他 AI，最少要明确以下几点：

1. `PDF` 正式方案是 `MinerU API`
2. 不再依赖桌面版手工操作
3. API Key 优先从 `MINERU_API_KEY` 或 `.secrets/mineru.env` 读取
4. 脚本在 `scripts/mineru_api_extract.py`
5. `doc/docx` 走 `pandoc`
6. `doc` 先转 `docx`
7. `xls/xlsx` 导出 `CSV`
8. 主文本统一沉淀到 `Markdown`
9. MinerU 结构化 JSON 在解压目录，不在 API 元数据文件里

## 9. 官方参考

- [MinerU API 文档](https://mineru.net/doc/docs/)
- [MinerU 限额说明](https://mineru.net/doc/docs/limit)
- [MinerU 控制台](https://mineru.net/apiManage/kie-usage)
- [Pandoc 文档](https://pandoc.org/)
