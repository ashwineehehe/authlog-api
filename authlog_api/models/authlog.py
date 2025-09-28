# authlog_api/models/authlog.py
from typing import Optional
from datetime import datetime
from sqlalchemy import BigInteger, Text, Boolean, TIMESTAMP, func, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.orm import Mapped, mapped_column   # <-- you need mapped_column here

from authlog_api.db.base_class import Base   # import Base from base_class, not session

class AuthLoginEvent(Base):
    __tablename__ = "authlog_login_events"

    event_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    actor_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    actor_type: Mapped[str] = mapped_column(Text, nullable=False)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    outcome: Mapped[str] = mapped_column(Text, nullable=False)
    occurred_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    auth_method: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    mfa_used: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    failure_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    log_level: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("actor_id > 0", name="ck_actor_id_positive"),
        CheckConstraint("outcome IN ('success','failure')", name="ck_outcome_enum"),
        CheckConstraint("actor_type IN ('user','admin','service')", name="ck_actor_type_enum"),
        CheckConstraint("log_level IN ('INFO','WARN','ERROR')", name="ck_log_level_enum"),
        Index("ix_authlog_occurred_at", "occurred_at"),
        Index("ix_authlog_actor_outcome", "actor_id", "outcome"),
    )
