from pydantic import field_validator
from sqlmodel import Field

from main.functions import check_enum
from .base import Base
class MinhchungBase(Base):
    so: str = Field(default=None, unique=True)
    loai: str

    @field_validator('loai')
    @classmethod
    def check_loai(cls, v: str) -> str:
        loai = {'Công văn':'CV', 'Quyết định':'QĐ', 'Tờ trình':'TTr', 'Giấy mời':'GM', 'khác': 'K'}
        check_enum(v, loai)
        return v