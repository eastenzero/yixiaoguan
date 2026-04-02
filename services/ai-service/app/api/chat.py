"""
RAG 问答接口路由
提供：
  - POST /api/chat       非流式问答（返回完整 JSON）
  - POST /api/chat/stream 流式问答（返回 SSE 流）

设计原则：
  - 无状态：不维护会话，历史记录由 Java 后端传入
  - 无鉴权：信任内部网络调用，JWT 校验由 Java 层处理
"""

import logging
import json
from typing import List, Optional

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from app.core.llm_chat import rag_engine, ChatMessage, SourceItem

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["RAG 问答"])


# ============== Pydantic 请求/响应模型 ==============

class ChatMessageDTO(BaseModel):
    """对话消息传输对象（与 Java 端约定格式）"""
    role: str = Field(..., description="角色: system/user/assistant")
    content: str = Field(..., description="消息内容")


class ChatRequest(BaseModel):
    """非流式对话请求"""
    query: str = Field(..., min_length=1, max_length=4096, description="用户问题")
    history: List[ChatMessageDTO] = Field(default=[], description="历史对话记录")
    use_kb: bool = Field(default=True, description="是否使用知识库增强")
    top_k: int = Field(default=5, ge=1, le=10, description="检索条数（可选）")


class SourceItemDTO(BaseModel):
    """引用来源传输对象"""
    entry_id: str = Field(..., description="知识条目 ID")
    title: str = Field(..., description="知识标题")
    content: str = Field(..., description="知识内容摘要")
    score: float = Field(..., description="相似度分数 0-1")


class ChatResponseData(BaseModel):
    """非流式响应数据体"""
    answer: str = Field(..., description="AI 回答内容")
    sources: List[SourceItemDTO] = Field(default=[], description="引用的知识来源")


class ChatResponse(BaseModel):
    """统一 API 响应格式（code/msg/data）"""
    code: int = Field(default=0, description="状态码，0 表示成功")
    msg: str = Field(default="success", description="消息说明")
    data: Optional[ChatResponseData] = Field(default=None, description="响应数据")


class ChatStreamRequest(BaseModel):
    """流式对话请求（参数同非流式）"""
    query: str = Field(..., min_length=1, max_length=4096, description="用户问题")
    history: List[ChatMessageDTO] = Field(default=[], description="历史对话记录")
    use_kb: bool = Field(default=True, description="是否使用知识库增强")


# ============== 辅助函数 ==============

def _convert_history(dto_list: List[ChatMessageDTO]) -> List[ChatMessage]:
    """将 DTO 列表转换为内部 ChatMessage 列表"""
    return [
        ChatMessage(role=item.role, content=item.content)
        for item in dto_list
        if item.role in ("user", "assistant", "system") and item.content
    ]


def _convert_sources(sources: List[SourceItem]) -> List[SourceItemDTO]:
    """将内部 SourceItem 列表转换为 DTO 列表"""
    return [
        SourceItemDTO(
            entry_id=s.entry_id,
            title=s.title,
            content=s.content,
            score=s.score,
        )
        for s in sources
    ]


# ============== 接口端点 ==============

@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    非流式 RAG 问答
    
    接收用户问题与历史记录，返回完整回答及引用来源。
    适合需要完整答案后再展示的场景。
    
    Example Request:
    ```json
    {
      "query": "学校图书馆几点关门？",
      "history": [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "您好！我是医小管，有什么可以帮您？"}
      ],
      "use_kb": true
    }
    ```
    
    Example Response:
    ```json
    {
      "code": 0,
      "msg": "success",
      "data": {
        "answer": "根据图书馆管理规定，夏季闭馆时间为 22:00，冬季为 21:30...",
        "sources": [
          {
            "entry_id": "1001",
            "title": "图书馆开放时间",
            "content": "夏季：8:00-22:00，冬季：8:00-21:30...",
            "score": 0.92
          }
        ]
      }
    }
    ```
    """
    try:
        # 转换历史记录格式
        history = _convert_history(request.history)
        
        # 调用 RAG 引擎（非流式）
        result = rag_engine.chat(
            query=request.query,
            history=history,
            use_kb=request.use_kb,
        )
        
        # 组装响应
        response_data = ChatResponseData(
            answer=result.answer,
            sources=_convert_sources(result.sources),
        )
        
        return ChatResponse(code=0, msg="success", data=response_data)
        
    except RuntimeError as e:
        logger.error(f"对话生成失败: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": f"生成失败: {str(e)}", "data": None},
        )
    except Exception as e:
        logger.error(f"未预期错误: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": "服务器内部错误", "data": None},
        )


@router.post("/stream")
async def chat_stream(request: ChatStreamRequest):
    """
    流式 RAG 问答（SSE 协议）
    
    返回 text/event-stream，每行格式：
    `data: {"chunk": "文本片段", "is_end": false, "sources": [...]}\n\n`
    
    适合打字机效果的实时展示。
    
    Example Request:
    ```json
    {
      "query": "学校几点关门",
      "history": [],
      "use_kb": true
    }
    ```
    
    Example SSE Stream:
    ```
    data: {"chunk": "根据", "is_end": false, "sources": [{"entry_id": "...", "title": "...", "score": 0.95}]}
    
    data: {"chunk": "学校", "is_end": false, "sources": []}
    
    data: {"chunk": "规定", "is_end": false, "sources": []}
    
    data: {"chunk": "...", "is_end": true, "sources": []}
    ```
    """
    async def sse_generator():
        """SSE 流生成器"""
        first_chunk = True
        
        try:
            history = _convert_history(request.history)
            
            # 调用流式生成
            async for chunk_text, sources in rag_engine.chat_stream(
                query=request.query,
                history=history,
                use_kb=request.use_kb,
            ):
                # 构造 SSE 数据包（首次携带 sources，后续为空）
                payload = {
                    "chunk": chunk_text,
                    "is_end": False,
                    "sources": [s.dict() for s in _convert_sources(sources)] if first_chunk else [],
                }
                first_chunk = False
                
                # 发送 data: {...}\n\n
                yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n".encode('utf-8')
            
            # 发送结束标记
            end_payload = {"chunk": "", "is_end": True, "sources": []}
            yield f"data: {json.dumps(end_payload, ensure_ascii=False)}\n\n".encode('utf-8')
            
        except RuntimeError as e:
            logger.error(f"流式生成失败: {e}")
            error_payload = {"chunk": "", "is_end": True, "error": str(e)}
            yield f"data: {json.dumps(error_payload, ensure_ascii=False)}\n\n".encode('utf-8')
        except Exception as e:
            logger.error(f"流式处理异常: {e}", exc_info=True)
            error_payload = {"chunk": "", "is_end": True, "error": "服务器内部错误"}
            yield f"data: {json.dumps(error_payload, ensure_ascii=False)}\n\n".encode('utf-8')
    
    return StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 禁用 Nginx 缓冲
        },
    )


@router.get("/health")
async def chat_health():
    """对话模块健康检查（供 Java 后端探测）"""
    return {
        "status": "ok",
        "model": rag_engine._model,
        "kb_available": True,  # 只要 ChromaDB 初始化成功即可
    }
