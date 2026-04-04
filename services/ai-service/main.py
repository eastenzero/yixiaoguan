"""
医小管 AI 服务 — FastAPI 入口
启动命令：uvicorn main:app --reload --port 8000
"""

import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.kb_vectorize import vector_store
from app.api import chat, links, kb, cluster, health, agent

# -- 结构化日志配置 --
logging.basicConfig(
    level=logging.INFO if not settings.app_debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    应用生命周期管理
    - 启动时：初始化 ChromaDB 连接
    - 关闭时：清理资源
    """
    logger.info("🚀 医小管 AI 服务启动中...")
    
    # 初始化向量存储
    try:
        vector_store.initialize()
        logger.info("✅ ChromaDB 向量存储初始化成功")
    except Exception as e:
        logger.error(f"❌ ChromaDB 初始化失败: {e}")
        # 不阻断启动，允许在运行时重试
    
    logger.info(f"📡 服务配置: 调试模式={settings.app_debug}, 向量库={settings.chroma_persist_dir}")
    
    yield
    
    # 关闭清理
    logger.info("🛑 医小管 AI 服务关闭中...")


app = FastAPI(
    title="医小管 AI 服务",
    description="封装 RAG 问答、链接匹配、知识草稿生成、相似聚类等 AI 能力，仅供 business-api 内部调用。",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
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
app.include_router(health.router)      # 健康检查（放在前面，无前缀）
app.include_router(chat.router)        # RAG 问答
app.include_router(links.router)       # 快捷链接匹配
app.include_router(kb.router)          # 知识库
app.include_router(cluster.router)     # 相似聚类
app.include_router(agent.router)       # 智能 Agent（意图提取）


@app.get("/", tags=["根路径"])
async def root():
    """服务根路径，返回基础信息"""
    return {
        "service": "ai-service",
        "name": "医小管 AI 服务",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
    }


# -- 全局异常处理 --
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """捕获未处理的异常，返回统一格式"""
    logger.error(f"未处理异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"code": 500, "msg": "服务器内部错误", "data": None},
    )
