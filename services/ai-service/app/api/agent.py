"""
智能 Agent 接口 — 意图识别与参数抽提

提供：
  - POST /api/agent/extract    提取用户意图和参数（Function Calling）

设计原则：
  - 纯语义转换层，只负责"理解用户意图 -> 输出结构化 JSON"
  - 所有业务执行交还给 Java 后端处理
"""

import logging
from typing import Optional, List, Dict, Any

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from app.core.intent_extractor import intent_extractor, IntentResult

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/agent", tags=["智能 Agent"])


# ==================== Pydantic 请求/响应模型 ====================

class ExtractRequest(BaseModel):
    """意图提取请求"""
    text: str = Field(..., min_length=1, max_length=4096, description="用户输入的自然语言文本")
    context: Optional[str] = Field(default=None, description="上下文信息（可选，用于多轮对话）")


class ExtractResponseData(BaseModel):
    """意图提取响应数据体"""
    intent: str = Field(..., description="识别出的意图类型（如 book_classroom）")
    confidence: float = Field(..., ge=0, le=1, description="置信度 0-1")
    is_service_intent: bool = Field(..., description="是否办事意图（非普通聊天）")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="提取的参数键值对")
    missing_required: List[str] = Field(default_factory=list, description="缺失的必填参数列表")
    reply_to_user: Optional[str] = Field(default=None, description="给用户的追问/确认语句")


class ExtractResponse(BaseModel):
    """统一 API 响应格式（code/msg/data）"""
    code: int = Field(default=0, description="状态码，0 表示成功")
    msg: str = Field(default="success", description="消息说明")
    data: Optional[ExtractResponseData] = Field(default=None, description="响应数据")


class IntentTypeResponse(BaseModel):
    """支持的意图类型列表响应"""
    code: int = Field(default=0)
    msg: str = Field(default="success")
    data: List[Dict[str, Any]]


# ==================== 接口端点 ====================

@router.post("/extract", response_model=ExtractResponse)
async def extract_intent(request: ExtractRequest):
    """
    意图识别与参数抽提（Function Calling）
    
    接收用户自然语言输入，使用 DashScope Function Calling 识别办事意图，
    并提取结构化参数。支持教室预约、设备报修、进度查询三类意图。
    
    **注意**：本接口只做语义转换，不直接执行业务操作！
    
    Example Request:
    ```json
    {
      "text": "明天下午我想借 C楼 的教室开班会"
    }
    ```
    
    Example Response (办事意图):
    ```json
    {
      "code": 0,
      "msg": "success",
      "data": {
        "intent": "book_classroom",
        "confidence": 0.95,
        "is_service_intent": true,
        "parameters": {
          "building": "C楼",
          "date": "2025-04-02",
          "start_time": "14:00",
          "purpose": "班会"
        },
        "missing_required": ["end_time"],
        "reply_to_user": "好的，C楼，请问结束时间是几点呢？"
      }
    }
    ```
    
    Example Response (普通聊天):
    ```json
    {
      "code": 0,
      "msg": "success",
      "data": {
        "intent": "chat",
        "confidence": 0.92,
        "is_service_intent": false,
        "parameters": {},
        "missing_required": [],
        "reply_to_user": null
      }
    }
    ```
    """
    try:
        # 调用意图提取引擎
        result: IntentResult = intent_extractor.extract(request.text)
        
        # 组装响应
        response_data = ExtractResponseData(
            intent=result.intent,
            confidence=result.confidence,
            is_service_intent=result.is_service_intent,
            parameters=result.parameters,
            missing_required=result.missing_required,
            reply_to_user=result.reply_to_user,
        )
        
        return ExtractResponse(code=0, msg="success", data=response_data)
        
    except RuntimeError as e:
        logger.error(f"意图提取失败: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": f"意图提取失败: {str(e)}", "data": None},
        )
    except Exception as e:
        logger.error(f"未预期错误: {e}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": "服务器内部错误", "data": None},
        )


@router.get("/intents", response_model=IntentTypeResponse)
async def list_supported_intents():
    """
    获取支持的意图类型列表
    
    返回当前 Agent 支持的所有办事意图及其参数定义。
    供 Java 后端或前端了解可用的意图类型。
    
    Example Response:
    ```json
    {
      "code": 0,
      "msg": "success",
      "data": [
        {
          "name": "book_classroom",
          "description": "预约/借用教室",
          "required_params": ["date", "purpose"],
          "optional_params": ["building", "room_number", "start_time", "end_time"]
        },
        {
          "name": "submit_repair_request",
          "description": "设备报修",
          "required_params": ["device_type", "location", "fault_description"],
          "optional_params": ["urgency", "contact_phone"]
        },
        {
          "name": "query_application_status",
          "description": "查询办事进度",
          "required_params": ["business_type"],
          "optional_params": ["application_id", "applicant_id"]
        }
      ]
    }
    ```
    """
    from app.core.intent_extractor import TOOLS_SCHEMA
    
    try:
        intents = []
        for tool in TOOLS_SCHEMA:
            func = tool.get("function", {})
            params = func.get("parameters", {}).get("properties", {})
            required = func.get("parameters", {}).get("required", [])
            
            all_params = list(params.keys())
            optional_params = [p for p in all_params if p not in required]
            
            intents.append({
                "name": func.get("name"),
                "description": func.get("description", ""),
                "required_params": required,
                "optional_params": optional_params,
            })
        
        return IntentTypeResponse(code=0, msg="success", data=intents)
        
    except Exception as e:
        logger.error(f"获取意图列表失败: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"code": 500, "msg": "获取意图列表失败", "data": None},
        )


@router.get("/health")
async def agent_health():
    """
    Agent 模块健康检查
    
    返回意图提取引擎的状态信息，供 Java 后端探测。
    """
    return {
        "status": "ok",
        "module": "agent",
        "features": ["intent_extraction", "function_calling"],
        "supported_intents": ["book_classroom", "submit_repair_request", "query_application_status"],
    }
