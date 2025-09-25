from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, String, Text, UniqueConstraint
from authlog_api.db.session import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(254), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text, nullable=False)
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)
