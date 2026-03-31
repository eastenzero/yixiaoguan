"""
知识库向量化引擎
- 接入阿里云 DashScope text-embedding-v3 模型生成向量
- 与 ChromaDB 持久化存储交互
- 提供标准化的 upsert/query 接口
"""

import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

import dashscope
from dashscope import TextEmbedding
import chromadb

from app.core.config import settings

logger = logging.getLogger(__name__)


@dataclass
class VectorEntry:
    """向量条目数据结构"""
    entry_id: str                    # 知识条目唯一标识（对应 yx_knowledge_entry.id）
    content: str                     # 向量化内容（标题 + 正文）
    metadata: Dict[str, Any]         # 元数据（标题、分类、标签等）


@dataclass
class SearchResult:
    """向量检索结果"""
    entry_id: str
    content: str
    metadata: Dict[str, Any]
    distance: float                  # 向量距离（越小越相似）
    score: float                     # 相似度分数（0-1，越大越相似）


class KBVectorStore:
    """
    知识库向量存储管理器
    负责：Embedding 生成、ChromaDB 操作、向量检索
    """
    
    # DashScope text-embedding-v3 模型配置
    EMBEDDING_MODEL = "text-embedding-v3"
    EMBEDDING_DIMENSION = 1024       # text-embedding-v3 输出维度
    
    def __init__(self):
        self._client: Optional[chromadb.Client] = None
        self._collection = None
        self._initialized = False
    
    def initialize(self) -> None:
        """初始化 ChromaDB 客户端和集合"""
        if self._initialized:
            return
        
        # 配置 DashScope API Key
        if settings.dashscope_api_key:
            dashscope.api_key = settings.dashscope_api_key
        
        # 初始化 ChromaDB 客户端（持久化模式）
        self._client = chromadb.PersistentClient(
            path=settings.chroma_persist_dir,
            settings=chromadb.Settings(anonymized_telemetry=False),
        )
        
        # 获取或创建知识库集合
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_kb,
            metadata={"description": "医小管知识库条目向量存储", "dimension": self.EMBEDDING_DIMENSION},
        )
        
        self._initialized = True
        logger.info(f"向量存储初始化完成: collection={settings.chroma_collection_kb}")
    
    def _ensure_initialized(self) -> None:
        """确保已初始化，否则自动初始化"""
        if not self._initialized:
            self.initialize()
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        调用 DashScope text-embedding-v3 生成文本向量
        
        Args:
            text: 输入文本（建议不超过模型最大 token 限制）
        
        Returns:
            1024 维向量列表
        
        Raises:
            RuntimeError: API 调用失败时抛出
        """
        self._ensure_initialized()
        
        if not settings.dashscope_api_key:
            raise RuntimeError("DashScope API Key 未配置")
        
        # 调用 DashScope Embedding API
        response = TextEmbedding.call(
            model=self.EMBEDDING_MODEL,
            input=text,
        )
        
        if response.status_code != 200:
            raise RuntimeError(f"DashScope API 调用失败: {response.message}")
        
        # 提取向量结果
        embedding = response.output["embeddings"][0]["embedding"]
        return embedding
    
    def upsert_kb_entry(
        self,
        entry_id: str,
        title: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        将知识条目向量化并存入 ChromaDB
        
        Args:
            entry_id: 知识条目 ID（字符串形式，如 "1001"）
            title: 知识标题
            content: 知识正文内容
            metadata: 额外元数据（如 category_id, tags, author_id 等）
        
        Returns:
            操作结果信息
        """
        self._ensure_initialized()
        
        # 组合标题和内容进行向量化
        combined_text = f"{title}\n\n{content}".strip()
        
        # 生成向量
        try:
            embedding = self.generate_embedding(combined_text)
        except Exception as e:
            logger.error(f"生成向量失败 [entry_id={entry_id}]: {e}")
            raise RuntimeError(f"向量生成失败: {e}")
        
        # 准备元数据
        doc_metadata = {
            "title": title,
            "entry_id": entry_id,
        }
        if metadata:
            # 过滤掉 None 值，避免 ChromaDB 序列化问题
            doc_metadata.update({k: v for k, v in metadata.items() if v is not None})
        
        # 存入 ChromaDB
        self._collection.upsert(
            ids=[entry_id],
            embeddings=[embedding],
            documents=[combined_text],
            metadatas=[doc_metadata],
        )
        
        logger.info(f"知识条目已向量化入库 [entry_id={entry_id}, title={title[:30]}...]")
        
        return {
            "entry_id": entry_id,
            "status": "success",
            "vector_dimension": len(embedding),
        }
    
    def search_similar(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """
        向量相似度检索
        
        Args:
            query: 查询文本
            top_k: 返回结果数量
            filter_metadata: 元数据过滤条件（可选）
        
        Returns:
            相似度排序后的结果列表
        """
        self._ensure_initialized()
        
        # 生成查询向量
        query_embedding = self.generate_embedding(query)
        
        # 执行向量检索
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filter_metadata,
            include=["documents", "metadatas", "distances"],
        )
        
        # 解析结果
        search_results = []
        if results["ids"] and len(results["ids"][0]) > 0:
            for i, entry_id in enumerate(results["ids"][0]):
                distance = results["distances"][0][i]
                # 将距离转换为相似度分数（归一化到 0-1）
                score = 1 / (1 + distance)
                
                search_results.append(
                    SearchResult(
                        entry_id=entry_id,
                        content=results["documents"][0][i],
                        metadata=results["metadatas"][0][i],
                        distance=distance,
                        score=round(score, 4),
                    )
                )
        
        logger.debug(f"向量检索完成 [query={query[:30]}..., found={len(search_results)}]")
        return search_results
    
    def delete_kb_entry(self, entry_id: str) -> bool:
        """
        删除知识条目向量
        
        Args:
            entry_id: 知识条目 ID
        
        Returns:
            是否删除成功
        """
        self._ensure_initialized()
        
        try:
            self._collection.delete(ids=[entry_id])
            logger.info(f"知识条目向量已删除 [entry_id={entry_id}]")
            return True
        except Exception as e:
            logger.error(f"删除向量失败 [entry_id={entry_id}]: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """获取集合统计信息"""
        self._ensure_initialized()
        
        count = self._collection.count()
        return {
            "collection_name": settings.chroma_collection_kb,
            "entry_count": count,
            "embedding_dimension": self.EMBEDDING_DIMENSION,
            "embedding_model": self.EMBEDDING_MODEL,
        }


# 全局单例实例
vector_store = KBVectorStore()
