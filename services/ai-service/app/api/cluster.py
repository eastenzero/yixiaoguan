"""
相似问题聚类路由
接口：POST /cluster/similar
"""

from fastapi import APIRouter

router = APIRouter(prefix="/cluster", tags=["相似聚类"])


@router.post("/similar")
async def cluster_similar():
    """相似问题聚类归并（TODO：待实现）"""
    return {"code": 0, "msg": "TODO: 相似聚类接口待实现", "data": None}
