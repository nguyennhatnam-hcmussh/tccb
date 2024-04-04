from typing import List, Optional
from sqlmodel import Field
import datetime

from .base import Base
from main.schemas.donvi import DonviSearch


class HopdongReadNhansu(Base):
    id: int | None = Field(default=None)
    so: int | None = Field(default=None)
    nam: int | None = Field(default=int(datetime.datetime.today().year))
    donvimoi: Optional["DonviSearch"] = Field(default=None)
    he: str | None = Field(default=None)
    namhoc: str | None = Field(default=None)
    hocky: str | None = Field(default=None)
    trangthai: str | None = Field(default=None)
    ngaycapnhat: int | None = Field(default=None)
