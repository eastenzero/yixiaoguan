"""
RAG 对话生成引擎（医小管智能问答核心）
- 集成 DashScope Qwen 系列大模型（qwen-max / qwen-turbo / qwen-plus）
- 支持知识库增强（RAG）与纯净大模型对话双模式
- 支持流式（SSE）与非流式响应
"""

import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass

import dashscope
from dashscope import Generation

from app.core.config import settings
from app.core.kb_vectorize import vector_store, SearchResult

logger = logging.getLogger(__name__)


@dataclass
class ChatMessage:
    """对话消息结构"""
    role: str  # 'system' | 'user' | 'assistant'
    content: str


@dataclass
class SourceItem:
    """引用来源结构"""
    entry_id: str
    title: str
    content: str
    score: float


@dataclass
class ChatResponse:
    """非流式对话响应"""
    answer: str
    sources: List[SourceItem]


class RAGChatEngine:
    """
    RAG 对话引擎
    负责：知识检索、Prompt 组装、大模型调用、流式生成
    """
    
    # 默认模型配置
    DEFAULT_CHAT_MODEL = "qwen-plus"
    DEFAULT_TOP_K = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.5  # 相似度阈值，低于此值的知识不引用
    
    # 医小管系统人设（背景设定）
    SYSTEM_PROMPT = """你是「医小管」，医学院校园智能服务助手。

你的职责：
1. 为学生、教师提供准确、简洁的校园事务咨询服务
2. 基于提供的背景知识优先回答，确保信息准确
3. 若背景知识不足，可基于通用知识补充，但需保持谨慎
4. 使用友善、专业的语气，避免过于生硬

回答规范：
- 优先使用背景知识中的具体信息（如时间、地点、流程）
- 如涉及多步骤流程，请用清晰的序号列出
- 若无法确定答案，诚实告知并建议咨询相关部门"""

    RAG_PROMPT_TEMPLATE = """基于以下背景知识回答用户问题：

{context}

---
用户问题：{query}

请根据上述背景知识回答。如果背景知识不足以完整回答问题，请补充你的通用知识，但请注意准确性。"""

    def __init__(self):
        self._model: str = settings.dashscope_chat_model or self.DEFAULT_CHAT_MODEL
        self._init_dashscope()
    
    def _init_dashscope(self) -> None:
        """初始化 DashScope 客户端"""
        if settings.dashscope_api_key:
            dashscope.api_key = settings.dashscope_api_key
            logger.info(f"DashScope 初始化完成，使用模型: {self._model}")
        else:
            logger.warning("DashScope API Key 未配置，大模型调用将失败")
    
    def _search_knowledge(self, query: str, top_k: int = 5) -> List[SearchResult]:
        """
        检索相关知识条目
        
        Args:
            query: 用户查询
            top_k: 返回条数
        
        Returns:
            相似度排序的知识条目列表
        """
        try:
            results = vector_store.search_similar(query, top_k=top_k)
            # 过滤低相似度结果
            filtered = [
                r for r in results 
                if r.score >= self.DEFAULT_SIMILARITY_THRESHOLD
            ]
            logger.info(f"知识检索完成 [query={query[:30]}...], 命中 {len(filtered)}/{len(results)} 条")
            return filtered
        except Exception as e:
            logger.error(f"知识检索失败: {e}")
            return []
    
    def _build_sources(self, results: List[SearchResult]) -> List[SourceItem]:
        """将检索结果转换为来源引用列表"""
        return [
            SourceItem(
                entry_id=r.entry_id,
                title=r.metadata.get("title", "未知标题"),
                content=r.content[:500] + "..." if len(r.content) > 500 else r.content,
                score=r.score,
            )
            for r in results
        ]
    
    def _build_messages(
        self, 
        query: str, 
        history: List[ChatMessage], 
        use_kb: bool = True
    ) -> tuple[List[Dict[str, str]], List[SourceItem]]:
        """
        构建发送给大模型的消息列表
        
        Returns:
            (messages列表, 引用来源列表)
        """
        messages: List[Dict[str, str]] = []
        sources: List[SourceItem] = []
        
        # 1. 系统消息（人设 + 背景知识）
        if use_kb:
            # 检索知识库
            kb_results = self._search_knowledge(query, top_k=self.DEFAULT_TOP_K)
            sources = self._build_sources(kb_results)
            
            if kb_results:
                # 组装背景知识上下文
                context_parts = []
                for i, result in enumerate(kb_results, 1):
                    title = result.metadata.get("title", "未命名")
                    content = result.content
                    context_parts.append(f"[{i}] 标题：{title}\n内容：{content}")
                
                context = "\n\n".join(context_parts)
                system_content = (
                    f"{self.SYSTEM_PROMPT}\n\n"
                    f"{self.RAG_PROMPT_TEMPLATE.format(context=context, query=query)}"
                )
                # 当使用 RAG 时，用户消息只保留问题（已包含在 system prompt 中）
                user_content = query
            else:
                # 知识库无命中，退化为纯净对话
                system_content = self.SYSTEM_PROMPT
                user_content = query
        else:
            # 纯净模式，不查知识库
            system_content = self.SYSTEM_PROMPT
            user_content = query
        
        messages.append({"role": "system", "content": system_content})
        
        # 2. 历史对话（仅限纯净模式或知识库未命中时；RAG 模式下通常无历史或简单处理）
        # 注意：为简化复杂度，历史记录直接追加（Java 端已处理好历史顺序）
        for msg in history[-10:]:  # 最多取最近 10 轮
            if msg.role in ("user", "assistant"):
                messages.append({"role": msg.role, "content": msg.content})
        
        # 3. 当前用户问题（如果历史里已包含当前问题则不再追加）
        if not history or history[-1].role != "user" or history[-1].content != query:
            messages.append({"role": "user", "content": user_content})
        
        return messages, sources
    
    def chat(
        self, 
        query: str, 
        history: Optional[List[ChatMessage]] = None,
        use_kb: bool = True,
    ) -> ChatResponse:
        """
        非流式对话（同步返回完整回答）
        
        Args:
            query: 用户当前问题
            history: 历史对话列表（可选）
            use_kb: 是否使用知识库增强
        
        Returns:
            完整回答及引用来源
        
        Raises:
            RuntimeError: 模型调用失败
        """
        if not settings.dashscope_api_key:
            raise RuntimeError("DashScope API Key 未配置")
        
        history = history or []
        messages, sources = self._build_messages(query, history, use_kb)
        
        logger.debug(f"发送非流式请求，消息数: {len(messages)}")
        
        try:
            response = Generation.call(
                model=self._model,
                messages=messages,
                result_format="message",
                stream=False,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"DashScope API 错误: {response.message}")
            
            answer = response.output.choices[0].message.content
            return ChatResponse(answer=answer, sources=sources)
            
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            raise RuntimeError(f"生成回答失败: {e}")
    
    async def chat_stream(
        self, 
        query: str, 
        history: Optional[List[ChatMessage]] = None,
        use_kb: bool = True,
    ) -> AsyncGenerator[tuple[str, List[SourceItem]], None]:
        """
        流式对话（SSE 风格生成器）
        
        Yields:
            (文本片段, 引用来源列表) —— 首次 yield 会携带 sources，后续为空列表
        
        Raises:
            RuntimeError: 模型调用失败
        """
        if not settings.dashscope_api_key:
            raise RuntimeError("DashScope API Key 未配置")
        
        history = history or []
        messages, sources = self._build_messages(query, history, use_kb)
        
        logger.debug(f"发送流式请求，消息数: {len(messages)}")
        
        try:
            response = Generation.call(
                model=self._model,
                messages=messages,
                result_format="message",
                stream=True,
            )
            
            first_chunk = True
            for chunk in response:
                if chunk.status_code != 200:
                    raise RuntimeError(f"DashScope 流式错误: {chunk.message}")
                
                # 提取文本增量
                delta = chunk.output.choices[0].message.get("content", "")
                if delta:
                    # 首次返回时带上 sources，后续仅返回文本
                    if first_chunk:
                        yield (delta, sources)
                        first_chunk = False
                    else:
                        yield (delta, [])
                        
        except Exception as e:
            logger.error(f"流式生成失败: {e}")
            raise RuntimeError(f"流式生成回答失败: {e}")


# 全局单例实例
rag_engine = RAGChatEngine()
