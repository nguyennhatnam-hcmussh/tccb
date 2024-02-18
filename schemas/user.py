from pydantic import field_validator
from sqlmodel import Field
from typing import List

from .profile import ProfileRead
from main.db_setup import engine
from .base import Base

class UserBase(Base):
    maso: str | None = Field(default=None, index=True, unique=True)
    email: str = Field(index=True, unique=True)
    sdt: str = Field(unique=True)
    hovaten: str = Field(index=True)

    @field_validator('hovaten')
    @classmethod
    def hovaten_proper(cls, v: str) -> str:
        return v.title()

    @field_validator('email')
    @classmethod
    def email_lower(cls, v: str) -> str:
        return v.lower()

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int | None = None
    
class UserList(Base):
    data: List[UserRead]

class UserProfile(UserBase):
    profile: ProfileRead
