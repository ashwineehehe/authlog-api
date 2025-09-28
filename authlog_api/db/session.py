# authlog_api/db/session.py
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine.url import make_url

from authlog_api.core.config import settings

# Log which DSN is used (mask password)
url = make_url(settings.DATABASE_URL)
safe_url = url._replace(password="***")
print(f"[DB] Using DSN -> {safe_url!s}")

connect_args = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
