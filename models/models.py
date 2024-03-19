from typing import List, Optional
from sqlmodel import Field, Relationship

from main.config import get_settings
from main.schemas import (
    Base, 
    DonviBase, 
    AuthBase, 
    NhansuBase,
    HopdongBase
)

settings = get_settings()

################# LINK ##################

class NhansuOfDonvi(Base, table=True):
    nhansu_id: int | None = Field(default=None, foreign_key="nhansu.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)


################# DON VI ##################
    
class Donvi(DonviBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    nhansu: List["Nhansu"] = Relationship(back_populates="donvi", link_model=NhansuOfDonvi)
    hopdongmoigiangs: List["Hopdong"] = Relationship(back_populates="donvimoi")



################# HOP DONG ##################
    
class Hopdong(HopdongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    giangvien: Optional["Nhansu"] = Relationship(back_populates="hopdongs")
    nguoiphutrach: Optional["Nhansu"] = Relationship(back_populates="hopdongphutrachs")
    donvimoi: Optional["Donvi"] = Relationship(back_populates="hopdongmoigiangs")


class Test(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    sohd: str


################# CƠ HỮU ##################
    
class Nhansu(NhansuBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    donvi: List["Donvi"] = Relationship(back_populates="nhansu", link_model=NhansuOfDonvi)
    hopdongs: List["Hopdong"] = Relationship(back_populates="giangvien")
    hopdongphutrachs: List["Hopdong"] = Relationship(back_populates="nguoiphutrach")


################# AUTH ##################
    
class Auth(AuthBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

