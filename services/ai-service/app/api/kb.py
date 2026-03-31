"""
知识库路由
接口：POST /kb/draft — 知识草稿生成
接口：POST /kb/vectorize — 知识条目向量化入库
"""

from fastapi import APIRouter

router = APIRouter(prefix="/kb", tags=["知识库"])


@router.post("/draft")
async def generate_draft():
    """根据问答自动生成知识草稿（TODO：待实现）"""
    return {"code": 0, "msg": "TODO: 知识草稿生成接口待实现", "data": None}


@router.post("/vectorize")
async def vectorize_entry():
    """知识条目向量化入库到 ChromaDB（TODO：待实现）"""
    return {"code": 0, "msg": "TODO: 向量化入库接口待实现", "data": None}
