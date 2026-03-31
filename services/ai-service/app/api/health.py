"""
健康检查路由
提供服务和依赖组件的健康状态检查
"""

from fastapi import APIRouter, status
from pydantic import BaseModel
from typing import Dict, Any

from app.core.config import settings
from app.core.kb_vectorize import vector_store

router = APIRouter(tags=["健康检查"])


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str
    service: str
    version: str
    components: Dict[str, Any]


class HealthCheckResult(BaseModel):
    """组件健康检查结果"""
    status: str  # healthy / unhealthy
    message: str
    details: Dict[str, Any] = {}


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """
    详细健康检查接口
    检查服务本身及依赖组件（ChromaDB）状态
    """
    components = {}
    overall_status = "healthy"
    
    # 检查 ChromaDB 状态
    try:
        stats = vector_store.get_stats()
        components["chromadb"] = {
            "status": "healthy",
            "message": "向量数据库连接正常",
            "details": stats,
        }
    except Exception as e:
        components["chromadb"] = {
            "status": "unhealthy",
            "message": f"向量数据库连接异常: {str(e)}",
            "details": {},
        }
        overall_status = "degraded"
    
    # 检查配置状态
    components["config"] = {
        "status": "healthy" if settings.dashscope_api_key else "warning",
        "message": "配置加载正常" if settings.dashscope_api_key else "DashScope API Key 未配置",
        "details": {
            "debug": settings.debug,
            "embedding_model": settings.dashscope_embedding_model,
            "chroma_collection": settings.chroma_collection_kb,
        },
    }
    
    if not settings.dashscope_api_key:
        overall_status = "degraded"
    
    return HealthResponse(
        status=overall_status,
        service="ai-service",
        version="0.1.0",
        components=components,
    )


@router.get("/health/simple", status_code=status.HTTP_200_OK)
async def health_check_simple():
    """
    简单健康检查接口
    仅返回服务是否存活，用于负载均衡器探针
    """
    return {"status": "ok", "service": "ai-service"}
