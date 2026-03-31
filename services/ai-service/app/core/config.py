"""
应用配置 — 通过环境变量或 .env 文件读取
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """AI 服务配置项"""

    # -- 服务 --
    app_name: str = "医小管 AI 服务"
    debug: bool = False

    # -- DashScope（阿里云大模型） --
    dashscope_api_key: str = ""
    dashscope_chat_model: str = "qwen-plus"
    dashscope_embedding_model: str = "text-embedding-v3"

    # -- ChromaDB --
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_kb: str = "kb_entries"
    chroma_collection_links: str = "quick_links"

    # -- business-api 回调（可选） --
    business_api_base_url: str = "http://business-api:8080"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 全局单例
settings = Settings()
