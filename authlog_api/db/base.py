from authlog_api.db.session import Base
# Import models here so Alembic can detect them
from authlog_api.models.authlog import AuthLoginEvent  # noqa: F401
