from typing import List, Optional
from sqlmodel import Field, Relationship
from sqlalchemy.orm import relationship

from main.config import get_settings
from main.schemas import (
    Base, 
    DonviBase, 
    AuthBase, 
    NhansuBase,
    HopdongBase,
    TrangthaiBase,
    BienbanBase
)

settings = get_settings()

################# LINK ##################
class NhansuOfDonvi(Base, table=True):
    nhansu_id: int | None = Field(default=None, foreign_key="nhansu.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)

class GvtgOfDonvi(Base, table=True):
    nhansu_id: int | None = Field(default=None, foreign_key="nhansu.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)

class HopdongOfDonvi(Base, table=True):
    hopdong_id: int | None = Field(default=None, foreign_key="hopdong.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)

class HopdongOfGiangvien(Base, table=True):
    hopdong_id: int | None = Field(default=None, foreign_key="hopdong.id", primary_key=True)
    giangvien_id: int | None = Field(default=None, foreign_key="nhansu.id", primary_key=True)

class HopdongOfNguoiphutrach(Base, table=True):
    hopdong_id: int | None = Field(default=None, foreign_key="hopdong.id", primary_key=True)
    nguoiphutrach_id: int | None = Field(default=None, foreign_key="nhansu.id", primary_key=True)


################# TRANG THAI ##################

class Trangthai(TrangthaiBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hopdong_id: int | None = Field(default=None, foreign_key="hopdong.id")
    hopdong: Optional["Hopdong"] = Relationship(back_populates="trangthais")
    bienban_id: int | None = Field(default=None, foreign_key="bienban.id")
    bienban: Optional["Bienban"] = Relationship(back_populates="trangthais")
    
    
################# BIÊN BẢN ##################

class Bienban(BienbanBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    trangthais: List["Trangthai"] = Relationship(back_populates="bienban")
    
    
################# DON VI ##################
    
class Donvi(DonviBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    gvtg: List["Nhansu"] = Relationship(back_populates="donvimoi", link_model=GvtgOfDonvi)
    nhansu: List["Nhansu"] = Relationship(back_populates="donvi", link_model=NhansuOfDonvi)
    hopdong: List["Hopdong"] = Relationship(back_populates="donvimoi", link_model=HopdongOfDonvi)
    


################# HOP DONG ##################
    
class Hopdong(HopdongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    donvimoi: Optional["Donvi"] = Relationship(back_populates="hopdong", link_model=HopdongOfDonvi, sa_relationship_kwargs={'uselist': False})
    giangvien: Optional["Nhansu"] = Relationship(back_populates="hopdong", link_model=HopdongOfGiangvien, sa_relationship_kwargs={'uselist': False})
    nguoiphutrach: Optional["Nhansu"] = Relationship(back_populates="hopdongphutrach", link_model=HopdongOfNguoiphutrach, sa_relationship_kwargs={'uselist': False})
    trangthais: List["Trangthai"] = Relationship(back_populates="hopdong")



################# NHÂN SỰ ##################
    
class Nhansu(NhansuBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    donvimoi: List["Donvi"] = Relationship(back_populates="gvtg", link_model=GvtgOfDonvi)
    donvi: Optional["Donvi"] = Relationship(back_populates="nhansu", link_model=NhansuOfDonvi, sa_relationship_kwargs={'uselist': False})
    hopdong: List["Hopdong"] = Relationship(back_populates="giangvien", link_model=HopdongOfGiangvien)
    hopdongphutrach: List["Hopdong"] = Relationship(back_populates="nguoiphutrach", link_model=HopdongOfNguoiphutrach)


################# AUTH ##################
    
class Auth(AuthBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

