from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    DATABASE_URL: str
    REGION: str
    COGNITO_USER_POOL_ID: str
    COGNITO_CLIENT_ID: str
    REPORT_BUCKET: str
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache()
def get_settings():
    return Settings()

settings = get_settings()