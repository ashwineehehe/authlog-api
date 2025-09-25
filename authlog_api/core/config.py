from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:12345@localhost:5432/postgres"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# authlog_api/core/config.py
class Settings(BaseSettings):
    DATABASE_URL: str  # e.g. postgresql+psycopg2://user:pass@localhost:5432/dbname
    SECRET_KEY: str = "change_me_to_a_long_random_string"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # pydantic v2 style config
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
