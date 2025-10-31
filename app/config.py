from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    APP_TITLE: str = "Text Analysis Service"
    
    POSTGRES_URL: PostgresDsn
    
    model_config = SettingsConfigDict(env_file="../.env")


settings = Config()

