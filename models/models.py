from typing import List, Optional
from sqlmodel import Field, Relationship

from main.config import get_settings
from main.schemas import (
    Base, 
    UserBase, 
    DonviBase, 
    MinhchungBase, 
    AuthBase, 
    ProfileBase,
    ThinhgiangBase,
    HopdongBase,
)

settings = get_settings()

################# LINK ##################

class ThinhgiangOfDonvi(Base, table=True):
    thinhgiang_id: int | None = Field(default=None, foreign_key="thinhgiang.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)


################# MINH CHỨNG ##################

class Minhchung(MinhchungBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    link_to: List['UserOfDonvi'] = Relationship(back_populates="minhchung")


################# TỔ CHỨC ##################
    
class Donvi(DonviBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    user: List['UserOfDonvi'] = Relationship(back_populates="donvi")
    thinhgiang: List["Thinhgiang"] = Relationship(back_populates="donvi", link_model=ThinhgiangOfDonvi)

################# NHÂN SỰ ##################

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    role: str = Field(default='user')

    of_donvi: List['UserOfDonvi'] | None = Relationship(back_populates="user")
    profile: Optional['Profile'] = Relationship(back_populates="user")


class Profile(ProfileBase, table=True):
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)
    user: User | None = Relationship(back_populates="profile")


class UserOfDonvi(Base, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    donvi_id: int | None = Field(default=None, foreign_key="donvi.id", primary_key=True)
    is_default: bool = False
    minhchung_id: int | None = Field(default=None, foreign_key="minhchung.id")
    
    user: User | None = Relationship(back_populates="of_donvi")
    donvi: Donvi | None = Relationship(back_populates="user")
    minhchung: Minhchung | None = Relationship(back_populates="link_to")
    
class Auth(AuthBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


################# THỈNH GIẢNG ##################
class Thinhgiang(ThinhgiangBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    donvi: List["Donvi"] = Relationship(back_populates="thinhgiang", link_model=ThinhgiangOfDonvi)


################# HOP DONG THỈNH GIẢNG ##################
class Hopdong(HopdongBase, table=True):
    id: int | None = Field(default=None, primary_key=True)