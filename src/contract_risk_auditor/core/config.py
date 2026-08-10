"""
Application configuration using Pydantic Settings.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database
    database_url: str = (
        "postgresql://cra_admin:change_me_locally@localhost:5432/contract_risk_auditor"
    )

    # Ollama
    ollama_base_url: str = "http://localhost:11434"
    ollama_chat_model: str = "tinyllama"
    ollama_embedding_model: str = "nomic-embed-text"
    embedding_dimension: int = 768

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
