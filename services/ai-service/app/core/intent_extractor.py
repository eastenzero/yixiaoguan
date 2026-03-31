"""
意图识别与参数抽提引擎 — Function Calling 版

功能：
- 利用 DashScope Qwen 的 Function Calling / Tool Calling 能力
- 将自然语言转化为结构化的意图 + 参数 JSON
- 纯语义转换层，不直接操作业务数据库

设计原则：
- 只负责"语义到 JSON 参数"的转换提取
- 所有业务执行交还给 Java 后端
"""

import json
import logging
from typing import List, Dict, Any, Optional, Literal
from dataclasses import dataclass, field
from enum import Enum

import dashscope
from dashscope import Generation

from app.core.config import settings

logger = logging.getLogger(__name__)


class IntentType(str, Enum):
    """意图类型枚举"""
    BOOK_CLASSROOM = "book_classroom"
    SUBMIT_REPAIR_REQUEST = "submit_repair_request"
    QUERY_APPLICATION_STATUS = "query_application_status"
    CHAT = "chat"  # 普通聊天，非办事意图


@dataclass
class IntentResult:
    """意图识别结果"""
    intent: str                           # 意图类型（如 book_classroom）
    confidence: float                     # 置信度 0-1
    is_service_intent: bool               # 是否办事意图（非普通聊天）
    parameters: Dict[str, Any]            # 提取的参数
    missing_required: List[str]           # 缺失的必填参数
    reply_to_user: Optional[str]          # 给用户的回复/追问
    raw_tool_calls: Optional[List[Dict]] = field(default=None)  # 原始工具调用（调试用）


# ==================== Tools Schema 定义 ====================

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "book_classroom",
            "description": "当用户表达想要借用/预约教室、申请空教室、预订教室用于活动/上课/自习等场景时调用。提取用户意图中的时间、地点、用途等信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "building": {
                        "type": "string",
                        "description": "教学楼/楼宇名称，如 'C楼'、'教学楼A'、'实验楼'。若用户未明确指定，返回 null"
                    },
                    "room_number": {
                        "type": "string",
                        "description": "具体教室门牌号，如 '101'、'C202'。若用户未明确指定，返回 null"
                    },
                    "date": {
                        "type": "string",
                        "description": "预约日期，格式 YYYY-MM-DD。如用户说'明天'，请基于当前日期推断具体日期"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "开始时间，格式 HH:MM（24小时制）。从'下午3点'、'15:00'等描述中提取"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "结束时间，格式 HH:MM（24小时制）。若用户未明确，返回 null"
                    },
                    "purpose": {
                        "type": "string",
                        "description": "借用用途/原因，如 '班会'、'自习'、'社团活动'、'实验课'"
                    },
                    "attendees_count": {
                        "type": "integer",
                        "description": "预计参与人数。若用户提到如'30人左右'，提取数字 30"
                    },
                    "contact_phone": {
                        "type": "string",
                        "description": "用户留下的联系电话，如 '13800138000'"
                    }
                },
                "required": ["date", "purpose"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "submit_repair_request",
            "description": "当用户表达设备坏了、需要报修、申请维修等场景时调用。提取设备类型、故障位置、故障描述等信息。",
            "parameters": {
                "type": "object",
                "properties": {
                    "device_type": {
                        "type": "string",
                        "enum": ["投影仪", "电脑", "空调", "门窗", "桌椅", "灯具", "网络设备", "饮水机", "其他"],
                        "description": "故障设备类型"
                    },
                    "location": {
                        "type": "string",
                        "description": "故障发生地点，如 'C楼302教室'、'图书馆3楼'、'宿舍5号楼'"
                    },
                    "room_number": {
                        "type": "string",
                        "description": "具体房间号，如 '302'。若地点中已包含完整信息，可为 null"
                    },
                    "fault_description": {
                        "type": "string",
                        "description": "故障具体描述，如 '投影仪无法开机'、'空调不制冷'、'门锁坏了'"
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["普通", "紧急", "特急"],
                        "description": "紧急程度。用户说'尽快'、'很急'时为'紧急'；说'马上'、'立刻'时为'特急'"
                    },
                    "contact_name": {
                        "type": "string",
                        "description": "报修人姓名"
                    },
                    "contact_phone": {
                        "type": "string",
                        "description": "报修人联系电话"
                    },
                    "preferred_time": {
                        "type": "string",
                        "description": "希望维修人员上门时间，如 '明天下午'、'周三上午'"
                    }
                },
                "required": ["device_type", "location", "fault_description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "query_application_status",
            "description": "当用户询问申请进度、办事状态、审核结果、流程走到哪里了等场景时调用。提取业务类型和查询标识。",
            "parameters": {
                "type": "object",
                "properties": {
                    "business_type": {
                        "type": "string",
                        "enum": ["教室预约", "设备报修", "奖学金申请", "助学金申请", "学籍异动", "请假申请", "活动申请", "其他"],
                        "description": "业务类型/办事类别"
                    },
                    "application_id": {
                        "type": "string",
                        "description": "申请单号/工单号，如 'AP20250101-001'。若用户未提供，返回 null"
                    },
                    "applicant_name": {
                        "type": "string",
                        "description": "申请人姓名，用于身份核验"
                    },
                    "applicant_id": {
                        "type": "string",
                        "description": "学号/工号，如 '2021010001'"
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "description": "起始日期 YYYY-MM-DD"},
                            "end": {"type": "string", "description": "结束日期 YYYY-MM-DD"}
                        },
                        "description": "查询时间范围，如用户说'最近一周的申请'"
                    },
                    "status_filter": {
                        "type": "string",
                        "enum": ["全部", "待审核", "审核中", "已通过", "已驳回", "已完成"],
                        "description": "状态筛选条件"
                    }
                },
                "required": ["business_type"]
            }
        }
    }
]


# ==================== 核心引擎 ====================

class IntentExtractor:
    """
    意图提取引擎
    
    使用 DashScope Function Calling 将自然语言转换为结构化意图
    """
    
    DEFAULT_MODEL = "qwen-plus"  # 使用支持 Function Calling 的模型
    
    SYSTEM_PROMPT = """你是「医小管」的意图识别助手，负责分析用户输入并提取办事意图。

任务规则：
1. 仔细分析用户输入，判断是否属于以下三类办事意图之一：
   - book_classroom：预约/借用教室
   - submit_repair_request：设备报修
   - query_application_status：查询办事进度

2. 如果用户意图是办事类（非闲聊），必须调用对应 function，并尽可能提取所有参数

3. 日期时间处理：
   - 用户说"明天"，请假设今天是 2025-04-01，返回 "2025-04-02"
   - 用户说"后天"，返回 "2025-04-03"
   - 时间统一用 24 小时制 HH:MM

4. 如果缺少必填参数，仍然要调用 function，并将已提取的参数填入，缺失的保持 null

5. 如果用户意图明显是普通聊天（如"你好"、"谢谢"、"今天天气怎样"），不要调用任何 function"""
    
    def __init__(self):
        self._model: str = settings.dashscope_chat_model or self.DEFAULT_MODEL
        self._init_dashscope()
    
    def _init_dashscope(self) -> None:
        """初始化 DashScope 客户端"""
        if settings.dashscope_api_key:
            dashscope.api_key = settings.dashscope_api_key
            logger.info(f"意图提取引擎初始化完成，使用模型: {self._model}")
        else:
            logger.warning("DashScope API Key 未配置，意图提取将失败")
    
    def extract(self, text: str) -> IntentResult:
        """
        从自然语言中提取意图和参数
        
        Args:
            text: 用户输入文本
        
        Returns:
            IntentResult 包含意图类型、参数、缺失项等
        
        Raises:
            RuntimeError: API 调用失败
        """
        if not settings.dashscope_api_key:
            raise RuntimeError("DashScope API Key 未配置")
        
        if not text or not text.strip():
            return IntentResult(
                intent=IntentType.CHAT,
                confidence=1.0,
                is_service_intent=False,
                parameters={},
                missing_required=[],
                reply_to_user="您好，请问有什么可以帮您？"
            )
        
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT},
            {"role": "user", "content": text.strip()}
        ]
        
        try:
            response = Generation.call(
                model=self._model,
                messages=messages,
                tools=TOOLS_SCHEMA,
                result_format="message",
                stream=False,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"DashScope API 错误: {response.message}")
            
            # 解析响应
            message = response.output.choices[0].message
            tool_calls = getattr(message, "tool_calls", None)
            
            # 如果没有工具调用，说明是普通聊天
            if not tool_calls:
                return IntentResult(
                    intent=IntentType.CHAT,
                    confidence=0.9,
                    is_service_intent=False,
                    parameters={},
                    missing_required=[],
                    reply_to_user=None,
                    raw_tool_calls=None
                )
            
            # 提取第一个工具调用（通常只有一个）
            tool_call = tool_calls[0]
            function_name = tool_call.get("function", {}).get("name", "")
            arguments_str = tool_call.get("function", {}).get("arguments", "{}")
            
            try:
                parameters = json.loads(arguments_str) if isinstance(arguments_str, str) else arguments_str
            except json.JSONDecodeError:
                parameters = {}
            
            # 获取该工具的必填参数列表
            required_params = self._get_required_params(function_name)
            
            # 检查缺失的必填参数
            missing_required = [
                param for param in required_params
                if param not in parameters or parameters.get(param) is None
            ]
            
            # 构建追问语句
            reply_to_user = self._build_follow_up_question(function_name, missing_required, parameters)
            
            return IntentResult(
                intent=function_name,
                confidence=0.9,  # DashScope Function Calling 通常置信度较高
                is_service_intent=True,
                parameters=parameters,
                missing_required=missing_required,
                reply_to_user=reply_to_user,
                raw_tool_calls=tool_calls
            )
            
        except Exception as e:
            logger.error(f"意图提取失败: {e}")
            raise RuntimeError(f"意图提取失败: {e}")
    
    def _get_required_params(self, function_name: str) -> List[str]:
        """获取指定函数的必填参数列表"""
        for tool in TOOLS_SCHEMA:
            func = tool.get("function", {})
            if func.get("name") == function_name:
                return func.get("parameters", {}).get("required", [])
        return []
    
    def _build_follow_up_question(
        self,
        function_name: str,
        missing_params: List[str],
        extracted_params: Dict[str, Any]
    ) -> Optional[str]:
        """
        根据缺失的参数构建追问语句
        
        Args:
            function_name: 意图类型
            missing_params: 缺失的必填参数
            extracted_params: 已提取的参数
        
        Returns:
            追问语句，或 None 如果参数完整
        """
        if not missing_params:
            return None
        
        # 根据意图类型和已提取信息，构建个性化追问
        if function_name == "book_classroom":
            building = extracted_params.get("building", "")
            date = extracted_params.get("date", "")
            
            if "date" in missing_params and "purpose" in missing_params:
                return f"好的{('，' + building) if building else ''}，请问您想预约哪一天的教室？用于什么用途呢？"
            elif "date" in missing_params:
                return f"好的{('，' + building) if building else ''}，请问您想预约哪一天的教室？"
            elif "purpose" in missing_params:
                return "请问您借用教室是用于什么用途呢？（如班会、自习、活动等）"
            else:
                return f"我还需要了解以下信息：{', '.join(missing_params)}"
        
        elif function_name == "submit_repair_request":
            if "device_type" in missing_params:
                return "请问是什么设备需要报修呢？（如投影仪、空调、电脑等）"
            elif "location" in missing_params:
                return "请问故障设备在哪个位置呢？（如 C楼302、图书馆等）"
            elif "fault_description" in missing_params:
                return "请问设备具体是什么故障呢？"
            else:
                return f"我还需要了解以下信息：{', '.join(missing_params)}"
        
        elif function_name == "query_application_status":
            if "business_type" in missing_params:
                return "请问您想查询哪类业务的进度呢？（如教室预约、奖学金申请等）"
            else:
                return "请提供您的申请单号或身份信息以便查询。"
        
        return f"我还需要了解以下信息：{', '.join(missing_params)}"


# ==================== 全局单例 ====================

intent_extractor = IntentExtractor()
