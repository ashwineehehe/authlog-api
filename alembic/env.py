from logging.config import fileConfig
import sys, os

from sqlalchemy import engine_from_config, pool
from alembic import context

#sys.path 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Import your Base
from authlog_api.core.config import settings
from authlog_api.db.base import Base

#Configobject
config = context.config

config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

#PYTHONLOGGING
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

#autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
