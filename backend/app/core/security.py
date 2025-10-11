from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Fernet using your encryption key from .env
fernet = Fernet(settings.ENCRYPTION_KEY.encode())
