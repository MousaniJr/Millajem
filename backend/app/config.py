from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str = "sqlite:///./millajem.db"

    # Telegram
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    # Security
    secret_key: str = "change-this-secret-key"
    admin_username: str = "admin"
    admin_password: str = "millajem2026"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Environment
    environment: str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
