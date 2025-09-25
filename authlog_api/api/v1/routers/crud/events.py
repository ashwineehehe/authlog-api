from typing import Optional, List
from sqlalchemy.orm import Session
from authlog_api.models.authlog import AuthLoginEvent

def list_events(db: Session, limit: int, offset: int, outcome: Optional[str]) -> List[AuthLoginEvent]:
    q = db.query(AuthLoginEvent).order_by(AuthLoginEvent.event_id.desc())
    if outcome:
        q = q.filter(AuthLoginEvent.outcome == outcome)
    return q.offset(offset).limit(limit).all()

def get_event(db: Session, event_id: int) -> Optional[AuthLoginEvent]:
    return db.get(AuthLoginEvent, event_id)

def create_event(db: Session, data: dict) -> AuthLoginEvent:
    if data.get("ip_address") is not None:
        data["ip_address"] = str(data["ip_address"])
    ev = AuthLoginEvent(**data)
    db.add(ev); db.commit(); db.refresh(ev)
    return ev

def replace_event(db: Session, ev: AuthLoginEvent, data: dict) -> AuthLoginEvent:
    if data.get("ip_address") is not None:
        data["ip_address"] = str(data["ip_address"])
    for k, v in data.items():
        setattr(ev, k, v)
    db.commit(); db.refresh(ev)
    return ev

def patch_event(db: Session, ev: AuthLoginEvent, changes: dict) -> AuthLoginEvent:
    if changes.get("ip_address") is not None:
        changes["ip_address"] = str(changes["ip_address"])
    for k, v in changes.items():
        setattr(ev, k, v)
    db.commit(); db.refresh(ev)
    return ev

def delete_event(db: Session, ev: AuthLoginEvent) -> None:
    db.delete(ev); db.commit()
