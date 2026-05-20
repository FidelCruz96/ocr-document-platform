from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "OCR Document Platform"
    environment: str = "development"
    secret_key: str = Field(default="dev-secret-change-me")
    access_token_expire_minutes: int = 60

    database_url: str = "postgresql+psycopg2://ocr:ocr@postgres:5432/ocr"
    redis_url: str = "redis://redis:6379/0"

    minio_endpoint: str = "minio:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_bucket: str = "documents"
    minio_secure: bool = False

    seed_user_email: str = "admin@test.com"
    seed_user_password: str = "admin123"

    max_upload_size_bytes: int = 10 * 1024 * 1024
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
