from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
import os
import sys

# Make sure app is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

load_dotenv()

# Alembic Config object
config = context.config

# Set DB URL from .env
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", ""))

# Setup loggers
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import all models so Alembic detects them
from app.database import Base
from app.models.instructor import Instructor  # noqa
from app.models.course import Course          # noqa
from app.models.student import Student        # noqa
from app.models.enrollment import Enrollment  # noqa

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
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
