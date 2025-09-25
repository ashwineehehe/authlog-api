from fastapi import FastAPI
from authlog_api.api.v1.routers.routes.events import router as events_router
from authlog_api.api.v1.routers.routes.users import router as users_router

app = FastAPI(
    title="AuthLog API",
    version="1.0.0",
    description="API for authentication logs and user management"
)
from fastapi.middleware.cors import CORSMiddleware
# include routers
app.include_router(events_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

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
