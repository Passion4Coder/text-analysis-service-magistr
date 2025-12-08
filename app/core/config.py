import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


class Config(BaseSettings):
    APP_TITLE: str = "Text Analysis Service"
    POSTGRES_URL: PostgresDsn
    DEBUG: bool = True
    ADMIN_SECRET: str

    OLLAMA_HOST: str
    EMBEDDING_MODEL: str
    LLM_SUMMARY_MODEL: str

    CORS_ORIGINS: str

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"), env_file_encoding="utf-8")


settings = Config()
