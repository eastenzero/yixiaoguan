"""
快捷链接匹配路由
接口：POST /links/match
"""

from fastapi import APIRouter

router = APIRouter(prefix="/links", tags=["快捷链接匹配"])


@router.post("/match")
async def match_links():
    """意图匹配快捷链接（TODO：待实现）"""
    return {"code": 0, "msg": "TODO: 链接匹配接口待实现", "data": None}
