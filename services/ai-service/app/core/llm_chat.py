"""
RAG 对话生成引擎（医小管智能问答核心）
- 集成 DashScope Qwen 系列大模型（qwen-max / qwen-turbo / qwen-plus）
- 支持知识库增强（RAG）与纯净大模型对话双模式
- 支持流式（SSE）与非流式响应
"""

import logging
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass, field

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
    grounded: bool = True
    guardrail_reason: Optional[str] = None
    retrieval_stats: Dict[str, Any] = field(default_factory=dict)


class RAGChatEngine:
    """
    RAG 对话引擎
    负责：知识检索、Prompt 组装、大模型调用、流式生成
    """
    
    # 默认模型配置
    DEFAULT_CHAT_MODEL = "qwen-plus"
    DEFAULT_TOP_K = 5
    DEFAULT_SIMILARITY_THRESHOLD = 0.5  # 相似度阈值，低于此值的知识不引用
    FALLBACK_NO_GROUNDING_ANSWER = "很抱歉，医小管目前尚未学习到相关说明，请咨询您的辅导员或相关负责老师。"
    
    # 医小管系统人设（背景设定）
    SYSTEM_PROMPT = """你是「医小管」，医学院校园智能服务助手。

你的职责：
1. 为学生、教师提供准确、简洁的校园事务咨询服务。
2. 你必须完全基于提供的背景知识进行回答，绝不能基于通用知识补充任何信息。
3. 使用友善、专业的语气，避免过于生硬。

回答红线规范（严格遵守）：
- 仅且只能提供背景知识中真实存在的具体信息（如时间、地点、流程）。
- 如果背景知识中未能找到答案或没有提供对应的流程，你必须明确并单一地回答：『很抱歉，医小管目前尚未学习到相关说明，请咨询您的辅导员或相关负责老师。』
- 严禁自行编造、补全任何未在背景知识中出现的系统名称、操作步骤或政策名称。
- 严禁提供任何互联网链接（URL）或虚假的联系电话。你没有任何提供外部链接的义务。"""

    RAG_PROMPT_TEMPLATE = """基于以下背景知识回答用户问题：

{context}

---
用户问题：{query}

请严格遵守上述背景知识回答！如果上述背景知识未能解答此问题，请遵循系统人设直接回复你无法解答，切勿补充任何外部知识或凭空捏造链接。"""

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
    
    def _search_knowledge(self, query: str, top_k: Optional[int] = None) -> List[SearchResult]:
        """
        检索相关知识条目
        
        Args:
            query: 用户查询
            top_k: 返回条数
        
        Returns:
            相似度排序的知识条目列表
        """
        try:
            top_k = top_k or settings.rag_top_k or self.DEFAULT_TOP_K
            results = vector_store.search_similar(query, top_k=top_k)
            # 过滤低相似度结果
            filtered = [
                r for r in results 
                if r.score >= settings.rag_min_score
            ]
            logger.info(f"知识检索完成 [query={query[:30]}...], 命中 {len(filtered)}/{len(results)} 条")
            return filtered
        except Exception as e:
            logger.error(f"知识检索失败: {e}")
            return []

    def _assess_grounding(self, results: List[SearchResult]) -> tuple[bool, str, Dict[str, Any]]:
        """评估检索结果是否满足防幻觉强约束门槛"""
        scores = [r.score for r in results]
        source_count = len(results)
        best_score = round(max(scores), 4) if scores else 0.0
        avg_score = round(sum(scores) / source_count, 4) if source_count > 0 else 0.0

        retrieval_stats = {
            "source_count": source_count,
            "best_score": best_score,
            "avg_score": avg_score,
            "threshold_min_score": settings.rag_min_score,
            "threshold_min_best_score": settings.rag_min_best_score,
            "threshold_min_avg_score": settings.rag_min_avg_score,
            "threshold_min_source_count": settings.rag_min_source_count,
            "top_k": settings.rag_top_k,
        }

        if source_count == 0:
            return False, "no_sources", retrieval_stats

        if source_count < settings.rag_min_source_count:
            return False, "insufficient_sources", retrieval_stats

        if best_score < settings.rag_min_best_score:
            return False, "best_score_too_low", retrieval_stats

        if avg_score < settings.rag_min_avg_score:
            return False, "avg_score_too_low", retrieval_stats

        return True, "ok", retrieval_stats
    
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
    ) -> tuple[List[Dict[str, str]], List[SourceItem], bool, str, Dict[str, Any]]:
        """
        构建发送给大模型的消息列表
        
        Returns:
            (messages列表, 引用来源列表, 是否满足强约束, 强约束原因, 检索统计)
        """
        messages: List[Dict[str, str]] = []
        sources: List[SourceItem] = []
        grounded = True
        guardrail_reason = "ok"
        retrieval_stats: Dict[str, Any] = {"use_kb": use_kb}
        
        # 1. 系统消息（人设 + 背景知识）
        if use_kb:
            # 检索知识库
            kb_results = self._search_knowledge(query, top_k=settings.rag_top_k)
            sources = self._build_sources(kb_results)
            grounded, guardrail_reason, retrieval_stats = self._assess_grounding(kb_results)
            retrieval_stats["use_kb"] = True
            
            if grounded and kb_results:
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
                # 未通过强约束时不拼接背景上下文，后续由上层执行拒答短路
                system_content = self.SYSTEM_PROMPT
                user_content = query
        else:
            # 纯净模式，不查知识库
            grounded = False
            guardrail_reason = "kb_disabled"
            retrieval_stats = {"use_kb": False}
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
        
        return messages, sources, grounded, guardrail_reason, retrieval_stats
    
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
        messages, sources, grounded, guardrail_reason, retrieval_stats = self._build_messages(query, history, use_kb)

        if use_kb and not grounded:
            logger.info(
                "RAG 强约束触发拒答 [query=%s..., reason=%s, stats=%s]",
                query[:30],
                guardrail_reason,
                retrieval_stats,
            )
            return ChatResponse(
                answer=self.FALLBACK_NO_GROUNDING_ANSWER,
                sources=sources,
                grounded=False,
                guardrail_reason=guardrail_reason,
                retrieval_stats=retrieval_stats,
            )
        
        logger.debug(f"发送非流式请求，消息数: {len(messages)}")
        
        try:
            response = Generation.call(
                model=self._model,
                messages=messages,
                result_format="message",
                stream=False,
                temperature=settings.rag_temperature,
            )
            
            if response.status_code != 200:
                raise RuntimeError(f"DashScope API 错误: {response.message}")
            
            answer = response.output.choices[0].message.content
            return ChatResponse(
                answer=answer,
                sources=sources,
                grounded=grounded,
                guardrail_reason=guardrail_reason,
                retrieval_stats=retrieval_stats,
            )
            
        except Exception as e:
            logger.error(f"大模型调用失败: {e}")
            raise RuntimeError(f"生成回答失败: {e}")
    
    async def chat_stream(
        self, 
        query: str, 
        history: Optional[List[ChatMessage]] = None,
        use_kb: bool = True,
    ) -> AsyncGenerator[tuple[str, List[SourceItem], Dict[str, Any]], None]:
        """
        流式对话（SSE 风格生成器）
        
        Yields:
            (文本片段, 引用来源列表) —— 首次 yield 会携带 sources，后续为空列表
        
        重要修复：
          1. incremental_output=True：让 DashScope 每次只返回新增 delta，
             而非累积全文（避免文字叠加重复显示的问题）
          2. asyncio.to_thread：将同步阻塞迭代器移到线程池执行，
             避免阻塞 FastAPI 事件循环（解决全量加载后才推送的问题）
        
        Raises:
            RuntimeError: 模型调用失败
        """
        import asyncio
        import queue
        
        if not settings.dashscope_api_key:
            raise RuntimeError("DashScope API Key 未配置")
        
        history = history or []
        messages, sources, grounded, guardrail_reason, retrieval_stats = self._build_messages(query, history, use_kb)

        guardrail_meta: Dict[str, Any] = {
            "grounded": grounded,
            "guardrail_reason": guardrail_reason,
            "retrieval_stats": retrieval_stats,
        }

        if use_kb and not grounded:
            logger.info(
                "流式 RAG 强约束触发拒答 [query=%s..., reason=%s, stats=%s]",
                query[:30],
                guardrail_reason,
                retrieval_stats,
            )
            yield (self.FALLBACK_NO_GROUNDING_ANSWER, sources, guardrail_meta)
            return
        
        logger.debug(f"发送流式请求，消息数: {len(messages)}")
        
        # 使用队列在线程和协程之间传递数据
        chunk_queue: queue.Queue = queue.Queue()
        _SENTINEL = object()  # 哨兵值，标记迭代结束
        
        def _sync_generate():
            """在独立线程中运行同步 DashScope 迭代器，结果放入队列"""
            try:
                response = Generation.call(
                    model=self._model,
                    messages=messages,
                    result_format="message",
                    stream=True,
                    incremental_output=True,  # ← 关键：每次只返回新增 delta
                    temperature=settings.rag_temperature,
                )
                for chunk in response:
                    chunk_queue.put(chunk)
            except Exception as exc:
                chunk_queue.put(exc)
            finally:
                chunk_queue.put(_SENTINEL)
        
        # 在线程池中启动同步生成，不阻塞事件循环
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, _sync_generate)
        
        first_chunk = True
        try:
            while True:
                # 非阻塞等待（每 20ms 轮询一次）
                try:
                    item = chunk_queue.get_nowait()
                except queue.Empty:
                    await asyncio.sleep(0.02)
                    continue
                
                # 迭代结束
                if item is _SENTINEL:
                    break
                
                # 传播线程中的异常
                if isinstance(item, Exception):
                    raise item
                
                chunk = item
                if chunk.status_code != 200:
                    raise RuntimeError(f"DashScope 流式错误: {chunk.message}")
                
                # 提取增量文本（incremental_output=True 保证每次只有新增部分）
                delta = chunk.output.choices[0].message.get("content", "")
                if delta:
                    if first_chunk:
                        yield (delta, sources, guardrail_meta)  # 首次携带 sources + 强约束元信息
                        first_chunk = False
                    else:
                        yield (delta, [], {})
                        
        except Exception as e:
            logger.error(f"流式生成失败: {e}")
            raise RuntimeError(f"流式生成回答失败: {e}")


# 全局单例实例
rag_engine = RAGChatEngine()
