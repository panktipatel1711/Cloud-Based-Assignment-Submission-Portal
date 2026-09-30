import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cloud Assignment Portal"
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    SECRET_KEY: str = "default-insecure-key-override-via-env"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    DATABASE_URL: str = "sqlite:///./cloud_portal.db"
    STORAGE_TYPE: str = "local"
    LOCAL_STORAGE_DIR: str = "./storage_bucket"
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = "us-east-1"
    S3_BUCKET_NAME: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
