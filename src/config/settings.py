import os
from pathlib import Path

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General application settings
    APP_NAME: str
    PROJECT_DOMAIN: str

    # Base folder set
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

    # Mail settings
    MAIL_USERNAME: EmailStr
    MAIL_PASSWORD: str
    MAIL_FROM: EmailStr
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False

    # Database settings
    DATABASE_URL: str  # Reading the database URL from environment

    # JWT Auth Settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60

    # Model config
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }


# Instantiate the settings
settings = Settings()

# Absolute paths (These can be outside the BaseSettings class)
TEMPLATES_DIR = settings.BASE_DIR / "templates"
STATIC_DIR = settings.BASE_DIR / "static"
