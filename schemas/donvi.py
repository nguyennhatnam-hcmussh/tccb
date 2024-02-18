from pydantic import field_validator
from sqlmodel import Field
from typing import List

from main.functions import check_enum
from .base import Base

class DonviBase(Base):
    ten: str = Field(unique=True) # vd: Phòng Tổ chức - Cán bộ
    loai: str # phòng, khoa, trung tâm, ban, bảo tàng, thư viện, công ty, bộ môn, văn phòng
    cap: str # trường, đơn vị
    is_phapnhan: bool = False # đơn vị có pháp nhân?
    is_nghiencuu: bool = False # là đơn vị nghiên cứu?

    @field_validator('loai')
    @classmethod
    def check_loai(cls, v: str) -> str:
        loai = ['phòng', 'khoa', 'trung tâm', 'ban', 'bảo tàng', 'thư viện', 'công ty', 'bộ môn', 'văn phòng']
        check_enum(v, loai)
        return v.lower()

    @field_validator('cap')
    @classmethod
    def check_cap(cls, v: str) -> str:
        loai = ['trường', 'đơn vị']
        check_enum(v, loai)
        return v.lower()

class DonviCreate(DonviBase):
    pass

class DonviRead(DonviBase):
    id: int

class DonviList(Base):
    data: List[DonviRead]