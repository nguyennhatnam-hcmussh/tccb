from sqlmodel import Field
from typing import List, Optional
from pydantic import field_validator
import datetime

from .base import Base

class TrangthaiBase(Base):
    id: int | None = Field(default=None)
    trangthai: str | None = Field(default=None)
    ngaycapnhat: str | None = Field(default=None)


class TrangthaiCreate(TrangthaiBase):
    
    @field_validator('ngaycapnhat')
    @classmethod
    def modify_ngaycapnhat(cls, v: str | None) -> str | None:
        date = str(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()))
        stamp = str(int(date))
        return stamp


class TrangthaiRead(TrangthaiBase):
    pass