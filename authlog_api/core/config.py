from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg2://postgres:12345@localhost:5432/postgres"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
