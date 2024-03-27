from sqlmodel import Field
from typing import List, Optional
from pydantic import field_validator
import datetime

from .base import Base

class TrangthaiBase(Base):
    trangthai: str | None = Field(default=None)
    ngaycapnhat: int | None = Field(default=None)


class TrangthaiCreate(TrangthaiBase):
    pass


class TrangthaiRead(TrangthaiBase):
    id: int | None = Field(default=None)