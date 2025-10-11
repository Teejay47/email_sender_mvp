# backend/app/schemas/recipient.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class RecipientCreate(BaseModel):
    user_id: int
    email: EmailStr

class RecipientOut(BaseModel):
    id: int
    user_id: int
    email: str
    validated: bool
    suppressed: bool

    class Config:
        orm_mode = True
