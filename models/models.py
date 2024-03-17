from typing import List, Optional
from sqlmodel import Field, Relationship

from main.config import get_settings
from main.schemas import (
    Base, 
    DonviBase, 
    AuthBase, 
    ThinhgiangBase,
    CohuuBase,
)

settings = get_settings()

################# LINK ##################

class ThinhgiangOfDonvi(Base, table=True):
    thinhgiang_id: int | None = Field(default=None, foreign_key="thinhgiang.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)


class CohuuOfDonvi(Base, table=True):
    cohuu_id: int | None = Field(default=None, foreign_key="cohuu.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)


################# DON VI ##################
    
class Donvi(DonviBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    cohuu: List["Cohuu"] = Relationship(back_populates="donvi", link_model=CohuuOfDonvi)
    thinhgiang: List["Thinhgiang"] = Relationship(back_populates="donvi", link_model=ThinhgiangOfDonvi)



################# CƠ HỮU ##################
    
class Cohuu(CohuuBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    donvi: List["Donvi"] = Relationship(back_populates="cohuu", link_model=CohuuOfDonvi)



################# THỈNH GIẢNG ##################
    
class Thinhgiang(ThinhgiangBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    donvi: List["Donvi"] = Relationship(back_populates="thinhgiang", link_model=ThinhgiangOfDonvi)



################# AUTH ##################
    
class Auth(AuthBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
