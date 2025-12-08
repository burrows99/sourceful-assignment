# Application configuration
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings  # type: ignore[attr-defined]

from typing import List


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    
    Create a .env file in the backend directory to override defaults:
    
    APP_NAME="My Custom API"
    VERSION="2.0.0"
    DEBUG=false
    CORS_ORIGINS=["http://localhost:3000","http://myapp.com"]
    WORKER_POLL_INTERVAL=2.0
    IMAGE_PROVIDER_DELAY=3.0
    MAX_IMAGES_PER_JOB=20
    """
    
    # API Settings
    APP_NAME: str = "Image Generation API"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://frontend:3000"
    ]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Worker Settings
    WORKER_POLL_INTERVAL: float = 1.0
    
    # Provider Settings (5 seconds simulates realistic image generation API)
    IMAGE_PROVIDER_DELAY: float = 5.0
    
    # Job Settings
    MIN_IMAGES_PER_JOB: int = 1
    MAX_IMAGES_PER_JOB: int = 10
    
    # Database Settings
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres"
    
    # Debug Settings
    ENABLE_DEBUG: bool = True
    DEBUG_PORT: int = 5678
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()
