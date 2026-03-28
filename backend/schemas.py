from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr


# ── User ─────────────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Transaction ───────────────────────────────────────────────────────────────

class TransactionBase(BaseModel):
    description: str
    amount: float
    category: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionRead(TransactionBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ── Health ────────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    database: str
