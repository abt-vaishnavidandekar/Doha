import os
from logging.config import fileConfig

from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

from alembic import context
from src.configs.model import Base
from src.modules.auth.admin.models import Admin
from src.modules.auth.student.models import Student
from src.modules.batch.base.admin.models import Batch
from src.modules.course.base.admin.models import Course
from src.modules.enrollments.base.student.models import Enrollment

load_dotenv()

config = context.config

pg_url = os.getenv("DATABASE_URL")

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

sync_pg_url = pg_url.replace(
    "postgresql+asyncpg://", "postgresql+psycopg://"
)

config.set_main_option("sqlalchemy.url", sync_pg_url)


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