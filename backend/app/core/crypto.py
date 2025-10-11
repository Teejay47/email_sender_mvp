# backend/app/core/crypto.py
from typing import Optional
import os
from cryptography.fernet import Fernet, InvalidToken

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if not ENCRYPTION_KEY:
    # For dev only: generate ephemeral key and warn in logs.
    # In production, ALWAYS set ENCRYPTION_KEY in env.
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    # You might want to log a warning here.

_fernet = Fernet(ENCRYPTION_KEY.encode())


def encrypt_password(plain: str) -> str:
    """Encrypt a plain password and return token (str)."""
    return _fernet.encrypt(plain.encode()).decode()


def decrypt_password(token: str) -> Optional[str]:
    """Return decrypted password (str) or None on failure."""
    try:
        return _fernet.decrypt(token.encode()).decode()
    except (InvalidToken, Exception):
        return None


def generate_key() -> str:
    """Helper to generate a new key to put into .env (Fernet)."""
    return Fernet.generate_key().decode()
