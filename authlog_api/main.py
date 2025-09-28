# authlog_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from authlog_api.db.session import engine
from authlog_api.db.base import Base  # safe now
from authlog_api.api.v1.routers.routes.events import router as events_router
# If you actually have a users router, import it; otherwise remove the include line.
# from authlog_api.api.v1.routers.routes.users import router as users_router

app = FastAPI(title="AuthLog API")

# Routers
app.include_router(events_router, prefix="/api/v1")
# app.include_router(users_router, prefix="/api/v1")  # comment/remove if not defined

@app.on_event("startup")
def on_startup():
    # If using Alembic, prefer migrations over create_all.
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
