from sqlmodel import Field
from typing import List, Optional
from pydantic import field_validator
import datetime
from zoneinfo import ZoneInfo

from .base import Base

class BienbanBase(Base):
    so: int | None = Field(default=None)
    nam: int | None = Field(default=int(datetime.datetime.now(tz=ZoneInfo('Asia/Ho_Chi_Minh')).year))
    ngaytao: int | None = Field(default=None)
    loai: str | None = Field(default=None)


class BienbanCreate(BienbanBase):
    pass


class BienbanRead(BienbanBase):
    id: int | None = Field(default=None)