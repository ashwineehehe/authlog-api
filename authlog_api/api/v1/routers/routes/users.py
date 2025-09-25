from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from authlog_api.db.session import get_db
from authlog_api.schemas.users import UserCreate, UserOut
from authlog_api.schemas.auth import TokenOut
from authlog_api.api.v1.routers.crud import users as crud
from authlog_api.core.security import create_access_token

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    if crud.get_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db, payload.email, payload.password)

# Accept either JSON email/password or OAuth2 form-data
@router.post("/login", response_model=TokenOut)
def login(
    form: OAuth2PasswordRequestForm = Depends(),  # expects username + password
    db: Session = Depends(get_db),
):
    user = crud.authenticate(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token(sub=user.email)
    return {"access_token": token, "token_type": "bearer"}
