"""
医小管 AI 服务 — FastAPI 入口
启动命令：uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, links, kb, cluster

app = FastAPI(
    title="医小管 AI 服务",
    description="封装 RAG 问答、链接匹配、知识草稿生成、相似聚类等 AI 能力，仅供 business-api 内部调用。",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# -- CORS（本地开发用，生产环境由 Nginx 处理） --
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -- 注册路由 --
app.include_router(chat.router)
app.include_router(links.router)
app.include_router(kb.router)
app.include_router(cluster.router)


@app.get("/", tags=["健康检查"])
async def root():
    """服务根路径，用于健康检查"""
    return {"service": "ai-service", "status": "running"}
