"""
Application configuration using Pydantic Settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    database_url: str = "postgresql://cra_admin:change_me_locally@localhost:5432/contract_risk_auditor"
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "llama3.1:8b"
    ollama_embedding_model: str = "nomic-embed-text"
    embedding_dimension: int = 768  # nomic-embed-text dimension

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()