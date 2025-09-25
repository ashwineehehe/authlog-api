from typing import Optional
from sqlalchemy.orm import Session
from authlog_api.models.user import User
from authlog_api.core.security import hash_password, verify_password

def get_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    u = User(email=email, password_hash=hash_password(password))
    db.add(u); db.commit(); db.refresh(u)
    return u

def authenticate(db: Session, email: str, password: str) -> Optional[User]:
    u = get_by_email(db, email)
    if not u or not verify_password(password, u.password_hash):
        return None
    return u
