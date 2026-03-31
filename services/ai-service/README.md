# ai-service — AI 与知识服务（FastAPI）

## 定位

本服务封装所有 AI 能力，与主业务后端（business-api）解耦。
AI 层迭代快，独立部署可避免实验性调整影响业务稳定性。

## 技术栈

- Python 3.11+
- FastAPI + Uvicorn
- DashScope SDK（通义千问大模型 + text-embedding-v3）
- ChromaDB（向量存储，本地持久化）
- Pydantic（数据校验）

## 对外接口（供 business-api 调用）

| 接口 | 功能 |
|---|---|
| `POST /chat` | RAG 问答（返回流式 SSE） |
| `POST /links/match` | 意图匹配快捷链接 |
| `POST /kb/draft` | 根据问答生成知识草稿 |
| `POST /cluster/similar` | 相似问题聚类（高频问题归并） |
| `POST /kb/vectorize` | 知识条目向量化入库 |

## 向量集合结构（ChromaDB）

| 集合名 | 内容 | 说明 |
|---|---|---|
| `kb_entries` | 知识库条目 | 主检索集合，RAG 问答使用 |
| `quick_links` | 快捷链接库 | 意图匹配链接推荐使用 |

## 现有脚本复用

- `scripts/kb_vectorize.py`：知识条目向量化，可直接迁移为 `/kb/vectorize` 接口
- `scripts/kb_demo_app.py`：RAG 问答 Demo，可作为 `/chat` 接口的实现参考

## 模型配置

| 用途 | 模型 | 供应商 |
|---|---|---|
| 对话生成 | qwen-plus / qwen-turbo | 阿里云 DashScope |
| 向量化 | text-embedding-v3 | 阿里云 DashScope |
| 图像生成（AI 头像，可选） | wanx-v1 | 阿里云 DashScope |

API Key 存放于 `.secrets/.env`，不提交到 Git。

## 开发文档

- `docs/api/ai-service-spec.md`（接口定义与入参出参）
- `docs/dev-guides/ai-service-guide.md`（RAG 策略与 Prompt 规范）
