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
    ngayky: str | None = Field(default=None)
    trangthai: str | None = Field(default=None)
    ngaycapnhat: str | None = Field(default=str(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())))
    socapnhat: int | None = Field(default=int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()))
    nguoidaidien: str = Field(default="TS. Phạm Tấn Hạ")

class HopdongCreate(HopdongBase):

    @field_validator('ngayky')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v


class HopdongUpdate(HopdongBase):

    @field_validator('ngayky')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v

class HopdongReadFull(HopdongBase):
    giangvien: Optional["NhansuSearch"] = Field(default=None)
    nguoiphutrach : Optional["NhansuSearch"] = Field(default=None)
    donvimoi: Optional["DonviSearch"] = Field(default=None)
    trangthais: List["TrangthaiRead"]

    @field_validator('ngayky')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v
    
    @field_validator('ngaycapnhat')
    @classmethod
    def modify_ngaycapnhat(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%H:%M %d/%m/%Y")
            return date
        return v
    
class ListHopdongReadFull(Base):
    data: List[HopdongReadFull]