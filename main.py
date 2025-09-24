
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, IPvAnyAddress
from datetime import datetime

from sqlalchemy import create_engine, BigInteger, Text, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import declarative_base, sessionmaker, Mapped, mapped_column, Session

#fastapi
app = FastAPI(title="AuthLog Login Events", debug=True)

#db
DATABASE_URL = "postgresql+psycopg2://postgres:12345@localhost:5432/postgres"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#ormmodels
class AuthLoginEvent(Base):
    __tablename__ = "authlog_login_events"  

    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    actor_type: Mapped[str] = mapped_column(Text, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    auth_method: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mfa_used: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    log_level: Mapped[str] = mapped_column(Text, nullable=False)

#tables
Base.metadata.create_all(bind=engine)

#schemas
class AuthLogCreate(BaseModel):
    actor_id: int
    actor_type: str
    event_type: str
    outcome: str
    log_level: str
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = None
    auth_method: Optional[str] = None
    provider: Optional[str] = None
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = None

class AuthLogUpdate(BaseModel):
    actor_type: Optional[str] = None
    event_type: Optional[str] = None
    outcome: Optional[str] = None
    log_level: Optional[str] = None
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = None
    auth_method: Optional[str] = None
    provider: Optional[str] = None
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = None

class AuthLogOut(BaseModel):
    event_id: int
    actor_id: int
    actor_type: str
    event_type: str
    outcome: str
    occurred_at: datetime
    ip_address: Optional[IPvAnyAddress] = None  
    user_agent: Optional[str] = None
    auth_method: Optional[str] = None
    provider: Optional[str] = None
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = None
    log_level: str

    class Config:
        from_attributes = True

class BulkUpdateItem(BaseModel):
    event_id: int
    actor_id: Optional[int] = None
    actor_type: Optional[str] = None
    event_type: Optional[str] = None
    outcome: Optional[str] = None
    log_level: Optional[str] = None
    ip_address: Optional[IPvAnyAddress] = None
    user_agent: Optional[str] = None
    auth_method: Optional[str] = None
    provider: Optional[str] = None
    mfa_used: Optional[bool] = None
    failure_reason: Optional[str] = None
    
#routes
@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

#Create
@app.post("/events", response_model=AuthLogOut, status_code=201)
def create_event(payload: AuthLogCreate, db: Session = Depends(get_db)):
    data = payload.model_dump()
    if data.get("ip_address") is not None:
        data["ip_address"] = str(data["ip_address"])  
    ev = AuthLoginEvent(**data)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

#Read
@app.get("/events", response_model=List[AuthLogOut])
def list_events(
    db: Session = Depends(get_db),
    actor_id: Optional[int] = None,
    event_type: Optional[str] = None,
    outcome: Optional[str] = None,
    limit: int = 100,
):
    q = db.query(AuthLoginEvent)
    if actor_id is not None:
        q = q.filter(AuthLoginEvent.actor_id == actor_id)
    if event_type is not None:
        q = q.filter(AuthLoginEvent.event_type == event_type)
    if outcome is not None:
        q = q.filter(AuthLoginEvent.outcome == outcome)
    return q.order_by(AuthLoginEvent.event_id.desc()).limit(limit).all()

#ReadbyID
@app.get("/events/{event_id}", response_model=AuthLogOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.get(AuthLoginEvent, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    return ev

# Update 
@app.put("/events", response_model=List[AuthLogOut])
def bulk_update_events(items: List[BulkUpdateItem], db: Session = Depends(get_db)):
    updated = []
    for item in items:
        ev = db.get(AuthLoginEvent, item.event_id)
        if not ev:
            continue  # or raise

        data = item.model_dump(exclude_none=True)
        if "ip_address" in data:
            data["ip_address"] = str(data["ip_address"])
        data.pop("event_id", None)

        for k, v in data.items():
            setattr(ev, k, v)

        updated.append(ev)

    db.commit()
    for ev in updated:
        db.refresh(ev)
    return updated


#UpdatebyID 
@app.patch("/events/{event_id}", response_model=AuthLogOut)
def update_event(event_id: int, patch: AuthLogUpdate, db: Session = Depends(get_db)):
    ev = db.get(AuthLoginEvent, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    patch_data = patch.model_dump(exclude_none=True)
    if "ip_address" in patch_data and patch_data["ip_address"] is not None:
        patch_data["ip_address"] = str(patch_data["ip_address"])  
    for k, v in patch_data.items():
        setattr(ev, k, v)
    db.commit()
    db.refresh(ev)
    return ev

#Delete
@app.delete("/events/{event_id}", status_code=204)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    ev = db.get(AuthLoginEvent, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    db.delete(ev)
    db.commit()
    return
