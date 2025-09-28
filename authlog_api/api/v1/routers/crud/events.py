# CRUD layer: DB-only logic, no FastAPI here
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select
from authlog_api.models.authlog import AuthLoginEvent

def list_events(db: Session, limit: int, offset: int, outcome: Optional[str]) -> List[AuthLoginEvent]:
    stmt = select(AuthLoginEvent)
    if outcome:
        stmt = stmt.where(AuthLoginEvent.outcome == outcome)
    stmt = stmt.order_by(AuthLoginEvent.occurred_at.desc()).limit(limit).offset(offset)
    return db.execute(stmt).scalars().all()

def get_event(db: Session, event_id: int) -> Optional[AuthLoginEvent]:
    return db.get(AuthLoginEvent, event_id)

def create_event(db: Session, data: dict) -> AuthLoginEvent:
    obj = AuthLoginEvent(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def replace_event(db: Session, obj: AuthLoginEvent, data: dict) -> AuthLoginEvent:
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def patch_event(db: Session, obj: AuthLoginEvent, data: dict) -> AuthLoginEvent:
    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def delete_event(db: Session, obj: AuthLoginEvent) -> None:
    db.delete(obj)
    db.commit()
