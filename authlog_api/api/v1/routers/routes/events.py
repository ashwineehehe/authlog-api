from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from authlog_api.db.session import get_db
from authlog_api.schemas.events import AuthLogCreate, AuthLogUpdate, AuthLogOut
from authlog_api.api.v1.routers.crud import events as crud
from authlog_api.api.deps import get_current_user  # <-- add

router = APIRouter(prefix="/events", tags=["events"])

@router.get("", response_model=List[AuthLogOut])
def list_events(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    outcome: str | None = Query(None, pattern="^(success|failure)$"),
):
    return crud.list_events(db, limit, offset, outcome)

@router.get("/{event_id}", response_model=AuthLogOut)
def get_event(event_id: int = Path(ge=1), db: Session = Depends(get_db),current_user = Depends(get_current_user),):
    ev = crud.get_event(db, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    return ev

@router.post("", response_model=AuthLogOut, status_code=201)
def create_event(payload: AuthLogCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user),):
    return crud.create_event(db, payload.model_dump())

@router.put("/{event_id}", response_model=AuthLogOut)
def replace_event(event_id: int = Path(ge=1), payload: AuthLogCreate = ..., db: Session = Depends(get_db),current_user = Depends(get_current_user),):
    ev = crud.get_event(db, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    return crud.replace_event(db, ev, payload.model_dump())

@router.patch("/{event_id}", response_model=AuthLogOut)
def update_event(event_id: int = Path(ge=1), patch: AuthLogUpdate = ..., db: Session = Depends(get_db),
                 current_user = Depends(get_current_user),):
    ev = crud.get_event(db, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    return crud.patch_event(db, ev, patch.model_dump(exclude_none=True))

@router.delete("/{event_id}", status_code=204)
def delete_event(event_id: int = Path(ge=1), db: Session = Depends(get_db),current_user = Depends(get_current_user),):
    ev = crud.get_event(db, event_id)
    if not ev:
        raise HTTPException(404, "Event not found")
    crud.delete_event(db, ev)
    return None
