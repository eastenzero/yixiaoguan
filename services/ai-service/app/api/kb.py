"""
知识库路由
接口：
- POST /kb/vectorize — 知识条目向量化入库
- POST /kb/search — 向量检索相似知识
- DELETE /kb/vectorize/{entry_id} — 删除向量
- GET /kb/stats — 向量库统计
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

from fastapi import APIRouter, HTTPException, status

from app.core.kb_vectorize import vector_store, SearchResult

router = APIRouter(prefix="/kb", tags=["知识库"])


# -- 请求/响应模型 --

class VectorizeRequest(BaseModel):
    """知识条目向量化请求"""
    entry_id: str = Field(..., description="知识条目唯一标识")
    title: str = Field(..., min_length=1, max_length=200, description="知识标题")
    content: str = Field(..., min_length=1, description="知识正文内容")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="额外元数据（如 category_id, tags）")


class VectorizeResponse(BaseModel):
    """向量化响应"""
    code: int = 200
    msg: str = "success"
    data: Optional[Dict[str, Any]] = None


class SearchRequest(BaseModel):
    """向量检索请求"""
    query: str = Field(..., min_length=1, max_length=1000, description="查询文本")
    top_k: int = Field(default=5, ge=1, le=20, description="返回结果数量")
    filter_metadata: Optional[Dict[str, Any]] = Field(default=None, description="元数据过滤条件")


class SearchResultItem(BaseModel):
    """检索结果项"""
    entry_id: str
    title: str
    content_preview: str
    score: float
    metadata: Dict[str, Any]


class SearchResponse(BaseModel):
    """检索响应"""
    code: int = 200
    msg: str = "success"
    data: List[SearchResultItem]


class StatsResponse(BaseModel):
    """统计响应"""
    code: int = 200
    msg: str = "success"
    data: Dict[str, Any]


class DeleteResponse(BaseModel):
    """删除响应"""
    code: int = 200
    msg: str = "success"
    data: Dict[str, Any]


# -- 接口实现 --

@router.post("/vectorize", response_model=VectorizeResponse)
async def vectorize_entry(request: VectorizeRequest):
    """
    知识条目向量化入库到 ChromaDB
    
    流程：
    1. 组合标题和内容
    2. 调用 DashScope text-embedding-v3 生成向量
    3. 存入 ChromaDB kb_entries 集合
    """
    try:
        result = vector_store.upsert_kb_entry(
            entry_id=request.entry_id,
            title=request.title,
            content=request.content,
            metadata=request.metadata,
        )
        return VectorizeResponse(
            code=200,
            msg="知识条目向量化入库成功",
            data=result,
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"向量化处理失败: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"系统错误: {str(e)}",
        )


@router.post("/search", response_model=SearchResponse)
async def search_kb(request: SearchRequest):
    """
    向量检索相似知识条目
    
    流程：
    1. 对查询文本生成向量
    2. 在 ChromaDB 中检索相似向量
    3. 返回按相似度排序的结果
    """
    try:
        results: List[SearchResult] = vector_store.search_similar(
            query=request.query,
            top_k=request.top_k,
            filter_metadata=request.filter_metadata,
        )
        
        # 转换为响应格式
        items = []
        for r in results:
            content_preview = r.content[:200] + "..." if len(r.content) > 200 else r.content
            items.append(
                SearchResultItem(
                    entry_id=r.entry_id,
                    title=r.metadata.get("title", ""),
                    content_preview=content_preview,
                    score=r.score,
                    metadata=r.metadata,
                )
            )
        
        return SearchResponse(
            code=200,
            msg=f"检索完成，命中 {len(items)} 条",
            data=items,
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"检索失败: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"系统错误: {str(e)}",
        )


@router.delete("/vectorize/{entry_id}", response_model=DeleteResponse)
async def delete_vector(entry_id: str):
    """
    删除知识条目的向量数据
    
    用于知识条目下线或删除时同步清理向量库
    """
    try:
        success = vector_store.delete_kb_entry(entry_id)
        if success:
            return DeleteResponse(
                code=200,
                msg="向量删除成功",
                data={"entry_id": entry_id, "deleted": True},
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="向量删除失败",
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"系统错误: {str(e)}",
        )


@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """
    获取知识库向量存储统计信息
    
    返回：条目数量、向量维度、模型信息等
    """
    try:
        stats = vector_store.get_stats()
        return StatsResponse(
            code=200,
            msg="获取统计信息成功",
            data=stats,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取统计信息失败: {str(e)}",
        )


@router.post("/draft")
async def generate_draft():
    """
    根据问答自动生成知识草稿（二期实现）
    
    TODO: 待实现
    - 接收会话历史
    - 调用大模型生成标准化知识条目
    - 返回草稿内容供人工审核
    """
    return {"code": 0, "msg": "TODO: 知识草稿生成接口待实现（二期）", "data": None}
