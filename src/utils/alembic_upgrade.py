import os
from alembic.config import Config
from alembic import command

from ..config.settings import settings

def run_alembic_migrations():

    # Create alembic config object and load .env values
    alembic_cfg = Config("alembic.ini")

    db_url = settings.DATABASE_URL
    if db_url:
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)

    # Apply all pending migrations
    command.upgrade(alembic_cfg, "head")
