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
    
    # Image Generation Provider Settings
    IMAGE_PROVIDER: str = "openrouter"  # Options: openrouter, mock
    IMAGE_MODEL: str = "sourceful/riverflow-v2-max-preview"
    IMAGE_TIMEOUT: float = 60.0
    IMAGE_PROVIDER_DELAY: float = 2.0  # Only for mock provider
    
    # Vision Provider Settings
    VISION_PROVIDER: str = "openrouter"  # Options: openrouter, openai, mock
    VISION_MODEL: str = ""  # Empty uses provider default, or specify like "openai/gpt-4o-mini"
    VISION_TIMEOUT: float = 30.0
    
    # OpenRouter Settings (when VISION_PROVIDER=openrouter)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_SITE_URL: str = "http://localhost:8000"
    OPENROUTER_SITE_NAME: str = "Image Classification API"
    
    # OpenAI Settings (when VISION_PROVIDER=openai)
    OPENAI_API_KEY: str = ""
    
    # MinIO S3 Storage Settings
    MINIO_ENDPOINT: str = "minio:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "generated-images"
    MINIO_PUBLIC_URL: str = "http://localhost:9000"
    MINIO_SECURE: bool = False  # Use HTTPS
    
    # Storage Settings
    STORAGE_BACKEND: str = "minio"  # Options: "minio", "none" (keeps base64)
    
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
