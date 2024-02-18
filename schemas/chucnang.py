from pydantic import field_validator
from sqlmodel import Field
from typing import List

from .profile import ProfileRead
from main.db_setup import engine
from .base import Base

class ChucnangBase(Base):
    chucnang: int

class ChucnangRead(ChucnangBase):
    pass
