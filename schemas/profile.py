from pydantic import field_validator
from sqlmodel import Field, DateTime
import random
import datetime

from main.functions import check_enum

from .base import Base

class ProfileBase(Base):
    gioitinh: str
    ngaysinh: str
    # quoctich: str
    # noisinh: str
    # quequan: str
    # dantoc: str
    # tongiao: str
    # CCCD_so: str
    # CCCD_ngay: datetime
    # CCCD_noi: str = Field(default="Cục CS QLHC về TTXH")

    @field_validator('gioitinh')
    @classmethod
    def enum_check_gioitinh(cls, v: str) -> str:
        enum = ['nam', 'nữ']
        check_enum(v, enum)
        return v

class ProfileCreate(ProfileBase):
    ngaysinh: str

    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str) -> str:
        date = datetime.datetime.strptime(v, '%d/%m/%Y').timestamp()
        stamp = str(int(date))
        return stamp

class ProfileRead(ProfileBase):
    user_id: int
    ngaysinh: str

    @field_validator('ngaysinh')
    @classmethod
    def modify_ngaysinh(cls, v: str) -> str:
        date = datetime.datetime.fromtimestamp(int(v)).strftime("%d/%m/%Y")
        return date