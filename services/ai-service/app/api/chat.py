"""
RAG 问答路由
接口：POST /chat
"""

from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["RAG 问答"])


@router.post("")
async def chat_with_ai():
    """RAG 问答 — 返回流式 SSE（TODO：待实现）"""
    return {"code": 0, "msg": "TODO: RAG 问答接口待实现", "data": None}
