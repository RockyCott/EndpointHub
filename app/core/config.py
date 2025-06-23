from functools import lru_cache
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    MONGO_URI: str
    MONGO_DB: str
    ENDPOINTS_COLLECTION: str
    MODULES_COLLECTION: str
    ALLOWED_ORIGINS: List[str]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("Configuration loaded from .env or environment variables.")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
