from pydantic import field_validator
from sqlmodel import Field
from typing import List

from .profile import ProfileRead
from main.db_setup import engine
from .base import Base

class HopdongBase(Base):
    sohd: str = Field(index=True, unique=True)
    giangvien: str | None = Field(default=None)
    donvi: str | None = Field(default=None)
    nguoilayso: str | None = Field(default=None)


class HopdongCreate(HopdongBase):
    pass

class HopdongRead(HopdongBase):
    id: int

class ListHopdongRead(Base):
    data: List[HopdongRead]