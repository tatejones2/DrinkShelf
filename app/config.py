"""Application configuration management"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "DrinkShelf"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    # Database
    DATABASE_URL: str = "sqlite:///./drinkshelf.db"
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Security
    SECRET_KEY: str = "your-secret-key-here-use-a-strong-random-string-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # OpenAI
    OPENAI_API_KEY: str = ""

    # Logging
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
