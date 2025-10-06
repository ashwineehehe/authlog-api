# authlog_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from authlog_api.db.session import engine
from authlog_api.db.base import Base
from authlog_api.api.v1.routers.routes.events import router as events_router
from authlog_api.api.v1.routers.routes.users import router as users_router

app = FastAPI(title="AuthLog API")

# Add CORS middleware 
origins = [
    "http://localhost:5173",  # React default dev port
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers 
app.include_router(events_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

# DB setup and routes
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}
