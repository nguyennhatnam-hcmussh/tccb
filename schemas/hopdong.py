from typing import List
from pydantic import field_validator
from sqlmodel import Field, DateTime
import datetime

from main.functions import CheckEnum

from .base import Base

class HopdongBase(Base):
    id: int | None = Field(default=None)
    so_hopdong: str | None = Field(default=None)
    giangvien: str | None = Field(default=None)
    donvi_moigiang: str | None = Field(default=None)
    nguoi_phutrach: str | None = Field(default=None)
    he: str | None = Field(default=None)
    namhoc: str | None = Field(default=None)
    hocky: str | None = Field(default=None)
    ngayky_hopdong: str | None = Field(default=None)
    ngaytao_hopdong: str | None = Field(default=None)

class HopdongCreate(HopdongBase):
    ngayky_hopdong: str | None = Field(default=None)
    ngaytao_hopdong: str | None = Field(default=None)

    @field_validator('ngayky_hopdong','ngaytao_hopdong')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v


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