# authlog_api/api/v1/routers/events.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from authlog_api.db.session import get_db
from authlog_api.models.authlog import AuthLoginEvent
from authlog_api.schemas.events import AuthLogCreate, AuthLogUpdate, AuthLogOut

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[AuthLogOut])
def list_events(
    db: Session = Depends(get_db),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    outcome: str | None = Query(None, pattern="^(success|failure)$"),
):
    q = db.query(AuthLoginEvent).order_by(AuthLoginEvent.event_id.desc())
    if outcome:
        q = q.filter(AuthLoginEvent.outcome == outcome)
    return q.offset(offset).limit(limit).all()

@router.get("/{event_id}", response_model=AuthLogOut)
def get_event(
    event_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    ev = db.get(AuthLoginEvent, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    return ev

@router.post("", response_model=AuthLogOut, status_code=201)
def create_event(payload: AuthLogCreate, db: Session = Depends(get_db)):
    ev = AuthLoginEvent(**payload.model_dump())
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

@router.patch("/{event_id}", response_model=AuthLogOut)
def update_event(
    event_id: int = Path(ge=1),
    patch: AuthLogUpdate = ...,
    db: Session = Depends(get_db),
):
    ev = db.get(AuthLoginEvent, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    for k, v in patch.model_dump(exclude_none=True).items():
        setattr(ev, k, v)
    db.commit()
    db.refresh(ev)
    return ev
