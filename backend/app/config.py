from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    app_env: Literal["development", "production"] = "development"
    allowed_origins: list[str] = ["http://localhost:5173"]
    anthropic_api_key: str = ""
    llm_model: str = "claude-sonnet-4-20250514"
    llm_batch_size: int = 10
    persistence_backend: Literal["memory", "sqlite"] = "memory"
    sqlite_path: str = "./data/runs.db"
    default_concurrency: int = 3
    max_concurrency: int = 10
    max_file_size_mb: int = 50
    max_retries: int = 3

    class Config:
        env_file = ".env"


settings = Settings()
