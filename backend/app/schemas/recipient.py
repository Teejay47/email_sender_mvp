# backend/app/schemas/recipient.py
from pydantic import BaseModel, EmailStr


class RecipientCreate(BaseModel):
    email: EmailStr
    validated: bool = False
    suppressed: bool = False
