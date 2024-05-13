from typing import List, Optional
from pydantic import field_validator
from sqlmodel import Field, DateTime
import datetime

from main.functions import CheckEnum

from .base import Base
from .donvi import DonviSearch
from .hopdong_phu import HopdongReadNhansu

class NhansuBase(Base):
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
    donvingoai: str | None = Field(default=None)
    co_bang: bool = Field(default=True)
    co_llkh: bool = Field(default=True)
    co_nvsp: bool = Field(default=True)
    type: str = Field(default='thinhgiang') # cohuu - thinhgiang
    role: str = Field(default='user') # user - mod - admin - root
    
    
class NhansuCreate(NhansuBase):

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


class NhansuCreateWithDonvimoi(NhansuBase):
    donvimoi: List["DonviSearch"] | None = Field(default=None)
    donvi: Optional["DonviSearch"] = Field(default=None)

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


class NhansuRead(NhansuBase):
    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v


class NhansuReadWithDonvimoi(NhansuBase):
    donvimoi: List["DonviSearch"]
    donvi: Optional["DonviSearch"]

    @field_validator('ngaysinh','CCCD_ngay')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v

class NhansuSearch(Base):
    id: int
    maso: str | None = Field(default=None)
    hovaten: str | None = Field(default=None)
    ngaysinh: str | None = Field(default=None)
    donvi: Optional["DonviSearch"] = Field(default=None)
    donvingoai: str | None = Field(default=None)
    
    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v


class ListNhansuSearch(Base):
    data: List[NhansuSearch]
    

class NhansuSearchWithDonvimoi(NhansuSearch):
    donvimoi: List["DonviSearch"]
    donvi: Optional["DonviSearch"]
    
    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v
    
class ListNhansuSearchWithDonvimoi(Base):
    data: List[NhansuSearchWithDonvimoi]
    

class NhansuReadFull(NhansuBase):
    donvimoi: List["DonviSearch"]
    donvi: Optional["DonviSearch"]
    hopdong: List["HopdongReadNhansu"]
    
    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str | None) -> str | None:
        if v:
            date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(v))).strftime("%d/%m/%Y")
            return date
        return v
    
class ListNhansuReadFull(Base):
    data: List[NhansuReadFull]


class NhansuReadWithHopdongphutrach(Base):
    hopdongphutrach: List["HopdongReadNhansu"]