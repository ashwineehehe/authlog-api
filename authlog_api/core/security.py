from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # or ["bcrypt"]
def hash_password(plain: str) -> str: return pwd_context.hash(plain)
def verify_password(plain: str, password_hash: str) -> bool: return pwd_context.verify(plain, password_hash)

from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from authlog_api.core.config import settings

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")  # or ["bcrypt"]

def hash_password(plain: str) -> str:
    return pwd_context.hash(plain)

def verify_password(plain: str, password_hash: str) -> bool:
    return pwd_context.verify(plain, password_hash)

def create_access_token(sub: str, expires_minutes: Optional[int] = None) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"sub": sub, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
