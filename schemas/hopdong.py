from typing import List
from pydantic import field_validator
from sqlmodel import Field, DateTime
import datetime

from main.functions import CheckEnum

from .base import Base

class HopdongBase(Base):
    id: int | None = Field(default=None)
    so: int | None = Field(default=None)
    nam: int = Field(default=None)
    giangvien: str | None = Field(default=None)
    donvimoi: str | None = Field(default=None)
    nguoiphutrach: str | None = Field(default=None)
    he: str | None = Field(default=None)
    namhoc: str | None = Field(default=None)
    hocky: str | None = Field(default=None)
    ngayky: str | None = Field(default=None)
    ngaytao: str | None = Field(default=None)
    nguoidaidien: str = Field(default="TS. Phạm Tấn Hạ")

class HopdongCreate(HopdongBase):
    ngayky: str | None = Field(default=None)
    ngaytao: str | None = Field(default=None)

    @field_validator('ngayky')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v

    @field_validator('ngaytao')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        date = str(int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds()))
        stamp = str(int(date))
        return stamp

class HopdongRead(HopdongBase):
    id: int
    ngayky_hopdong: str | None = Field(default=None)
    ngaytao_hopdong: str | None = Field(default=None)

    @field_validator('ngayky_hopdong','ngaytao_hopdong')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v