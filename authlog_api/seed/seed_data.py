from sqlalchemy.orm import Session
from authlog_api.db.session import SessionLocal
from authlog_api.models.user import User
from authlog_api.core.security import hash_password
from authlog_api.models.authlog import AuthLoginEvent

def seed_users(db: Session):
    if not db.query(User).filter(User.email == "aswi@gmail.com").first():
        admin = User(
            email="aswi@gmail.com",
            password_hash=hash_password("Admin@123")
        )
        db.add(admin)
        db.commit()
        print("Admin user seeded")

def seed_events(db: Session):
    if not db.query(AuthLoginEvent).first():
        ev = AuthLoginEvent(
            actor_id=1,
            actor_type="admin",
            event_type="login",
            outcome="success",
            ip_address="127.0.0.1",
            user_agent="SeederScript/1.0",
            auth_method="password",
            provider="local",
            mfa_used=False,
            failure_reason=None,
            log_level="INFO"
        )
        db.add(ev)
        db.commit()
        print("Sample event seeded")

def run_seed():
    db = SessionLocal()
    try:
        seed_users(db)
        seed_events(db)
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()
