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
    
    @field_validator('ngaycapnhat')
    @classmethod
    def modify_ngaycapnhat(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%H:%M %d/%m/%Y")
            return date
        return v