from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./doctor_platform.db"
    SECRET_KEY: str = "change-this-secret-key-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7 days
    CREDIT_COST_PER_PROFILE: int = 10
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
