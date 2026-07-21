import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "offline_ads")

    # Local PostgreSQL connection
    LOCAL_DATABASE_URL = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    # Use Render DATABASE_URL if available
    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        # Render may provide postgres:// instead of postgresql://
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = LOCAL_DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False