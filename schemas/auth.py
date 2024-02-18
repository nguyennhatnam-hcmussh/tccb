from sqlmodel import Field
import random

from .base import Base

class AuthBase(Base):
    user_id: int = Field(nullable=False)
    role: str = Field(nullable=False)
    pin: int = Field(default=random.randint(0,90000000))

class AuthRead(AuthBase):
    id: int