from fastapi import FastAPI
from authlog_api.api.v1.routers.events import router as events_router
from authlog_api.db.session import Base, engine  # TEMP ONLY (dev auto-create)

app = FastAPI(title="AuthLog API")

# Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}

app.include_router(events_router, prefix="/api/v1")
