# backend/app/core/config.py
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # ---------------------------
    # Security / Encryption
    # ---------------------------
    ENCRYPTION_KEY: str = "b7QwupTMc3zQlbQbqpM2c--Vf7Z_mFEcM_Ct5EQMfHY="

    # ---------------------------
    # Database Configuration
    # ---------------------------
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "email_sender_db"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    # ---------------------------
    # Redis / Celery Configuration
    # ---------------------------
    REDIS_URL: str = "redis://redis:6379/0"
    CELERY_BROKER_URL: str = "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://redis:6379/0"

    # ---------------------------
    # SMTP / Email Configuration
    # ---------------------------
    from distutils.util import strtobool

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool = True  # keep this default

    @property
    def SMTP_CONFIG(self) -> dict:
        return {
            "host": self.SMTP_HOST,
            "port": self.SMTP_PORT,
            "username": self.SMTP_USERNAME,
            "password": self.SMTP_PASSWORD,
            "use_tls": bool(strtobool(str(self.SMTP_USE_TLS))),  # ✅ convert string "false"/"true"
        }

    FROM_NAME: str
    FROM_EMAIL: str
    REPLY_TO: str

    # ---------------------------
    # IMAP Configuration
    # ---------------------------
    IMAP_HOST: str = "imap.gmail.com"
    IMAP_PORT: int = 993
    IMAP_USERNAME: Optional[str] = None
    IMAP_PASSWORD: Optional[str] = None

    # ---------------------------
    # Utility Properties
    # ---------------------------
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def SMTP_CONFIG(self) -> dict:
        return {
            "host": self.SMTP_HOST,
            "port": self.SMTP_PORT,
            "username": self.SMTP_USERNAME,
            "password": self.SMTP_PASSWORD,
            "use_tls": self.SMTP_USE_TLS,
        }

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
