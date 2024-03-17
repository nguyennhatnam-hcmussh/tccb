from typing import List
from pydantic import field_validator
from sqlmodel import Field, DateTime
import datetime

from main.functions import CheckEnum

from .base import Base
from .donvi import DonviSearch

class ThinhgiangBase(Base):
    id: int | None = Field(default=None)
    maso: str | None = Field(default=None, index=True)
    email: str | None = Field(default=None, index=True)
    sdt: str | None = Field(default=None)
    hovaten: str | None = Field(index=True)
    gioitinh: str | None = Field(default=None)
    ngaysinh: str | None = Field(default=None, index=True)
    quoctich: str | None = Field(default="Việt Nam")
    hocvi: str | None = Field(default=None)
    hocvi_nganh: str | None = Field(default=None)
    hocham: str | None = Field(default=None)
    hocham_nganh: str | None = Field(default=None)
    CCCD_so: str | None = Field(default=None)
    CCCD_ngay: str | None = Field(default=None)
    chucdanh: str | None = Field(default=None)
    donvicongtac: str | None = Field(default=None)
    co_bang: bool = Field(default=False)
    co_llkh: bool = Field(default=False)
    co_nvsp: bool = Field(default=False)


class ThinhgiangCreate(ThinhgiangBase):
    ngaysinh: str | None = Field(default=None)
    CCCD_ngay: str | None = Field(default=None)
    email: str | None = Field(default=None)
    gioitinh: str | None = Field(default=None)

    @field_validator('gioitinh')
    @classmethod
    def enum_check_gioitinh(cls, v: str | None) -> str | None:
        if v:
            enum = ['nam', 'nữ']
            CheckEnum(v, enum)
            return v
        return v

    @field_validator('email')
    @classmethod
    def email_lower(cls, v: str | None) -> str | None:
        if v:
            return v.lower()
        return v

    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v


class ThinhgiangCreateWithDonvi(ThinhgiangBase):
    ngaysinh: str | None = Field(default=None)
    CCCD_ngay: str | None = Field(default=None)
    email: str | None = Field(default=None)
    gioitinh: str | None = Field(default=None)
    donvi: List["DonviSearch"] | None = Field(default=None)

    @field_validator('gioitinh')
    @classmethod
    def enum_check_gioitinh(cls, v: str | None) -> str | None:
        if v:
            enum = ['nam', 'nữ']
            CheckEnum(v, enum)
            return v
        return v

    @field_validator('email')
    @classmethod
    def email_lower(cls, v: str | None) -> str | None:
        if v:
            return v.lower()
        return v

    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = str(int((datetime.datetime.strptime(v, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds()))
            stamp = str(int(date))
            return stamp
        return v


class ThinhgiangRead(ThinhgiangBase):
    id: int
    ngaysinh: str | None

    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v


class ThinhgiangReadWithDonvi(ThinhgiangBase):
    id: int
    ngaysinh: str | None
    donvi: List["DonviSearch"]

    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v


class ThinhgiangSearchWithDonvi(Base):
    id: int
    maso: str | None = Field(default=None)
    hovaten: str | None = Field(default=None)
    ngaysinh: str | None = Field(default=None)
    donvi: List["DonviSearch"]
    

    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v
    
class ListThinhgiangSearchWithDonvi(Base):
    data: List[ThinhgiangSearchWithDonvi]
    