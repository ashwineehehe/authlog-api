# authlog_api/core/config.py
from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Resolve project root: D:\FASTAPI_CRUD
ROOT = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    # Give a safe default so app starts even if .env missing
    DATABASE_URL: str = f"sqlite:///{(ROOT / 'dev.db').as_posix()}"
    SECRET_KEY: str = "dev-secret-change-me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CORS_ORIGINS: List[str] = ["http://localhost:5173", "http://127.0.0.1:5173"]

    # Look for .env in BOTH the project root and CWD
    model_config = SettingsConfigDict(
        env_file=[str(ROOT / ".env"), ".env"],
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()
