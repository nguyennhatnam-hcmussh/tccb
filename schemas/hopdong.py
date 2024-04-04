from typing import List, Optional
from pydantic import field_validator
from sqlmodel import Field, DateTime
import datetime

from main.functions import CheckEnum
from main.schemas.nhansu import NhansuSearch
from main.schemas.donvi import DonviSearch
from main.schemas.trangthai import TrangthaiRead

from .base import Base

class HopdongBase(Base):
    id: int | None = Field(default=None)
    so: int | None = Field(default=None)
    nam: int | None = Field(default=int(datetime.datetime.today().year))
    giangvien: str | None = Field(default=None)
    donvimoi: str | None = Field(default=None)
    nguoiphutrach: str | None = Field(default=None)
    he: str | None = Field(default=None)
    namhoc: str | None = Field(default=None)
    hocky: str | None = Field(default=None)
    ngayky: int | None = Field(default=None)
    trangthai: str | None = Field(default=None)
    ngaycapnhat: int | None = Field(default=None)
    bienban: str | None = Field(default=None)
    nguoidaidien: str = Field(default="TS. Phạm Tấn Hạ")

class HopdongCreate(HopdongBase):
    ngayky: str | None = Field(default=None)

class HopdongUpdate(HopdongBase):
    pass

class HopdongReadFull(HopdongBase):
    giangvien: Optional["NhansuSearch"] = Field(default=None)
    nguoiphutrach : Optional["NhansuSearch"] = Field(default=None)
    donvimoi: Optional["DonviSearch"] = Field(default=None)
    trangthais: List["TrangthaiRead"]

class HopdongRead(HopdongBase):
    giangvien: Optional["NhansuSearch"] = Field(default=None)
    nguoiphutrach : Optional["NhansuSearch"] = Field(default=None)
    donvimoi: Optional["DonviSearch"] = Field(default=None)

class ListHopdongReadFull(Base):
    data: List[HopdongReadFull]
    
class ListHopdongRead(Base):
    data: List[HopdongRead]

class HopdongReadNhansu(Base):
    so: int | None = Field(default=None)
    nam: int | None = Field(default=int(datetime.datetime.today().year))
    trangthai: str | None = Field(default=None)
