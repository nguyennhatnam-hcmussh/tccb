from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Dict
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # DATABASE
    DATABASE_URI: str = Field(..., env='DATABASE_URI')
    # ENCRIPT
    SECRET_KEY: Dict[str,str] = Field(..., env='SECRET_KEY')
    ENCRYPT_ALGO: Dict[str,str] = Field({"alg": "A256KW", "enc": "A256CBC-HS512"})
    # PATH
    MAIN_DIR: Path = Path(__file__).resolve().parent
    TEMPLATE_DIR: Dict[str,Path] = Field({
        "main": MAIN_DIR / "templates",
        "template": MAIN_DIR / "apps" / "template" / "templates",
        "auth": MAIN_DIR / "apps" / "auth" / "templates",
        "nhansu": MAIN_DIR / "apps" / "nhansu" / "templates",
        "error": MAIN_DIR / "apps" / "error" / "templates",
        "chucnang": MAIN_DIR / "apps" / "chucnang" / "templates",
        "donvi": MAIN_DIR / "apps" / "donvi" / "templates",
    })
    STATIC_MAIN_DIR: Path = MAIN_DIR / "static"
    # GOOGLE OAUTH2
    GOOGLE_CLIENT_ID: str = Field(..., env='GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET: str = Field(..., env='GOOGLE_CLIENT_SECRET')
    GOOGLE_AUTHORIZE_URL: str = Field('https://accounts.google.com/o/oauth2/auth')
    GOOGLE_TOKEN_URL: str = Field('https://accounts.google.com/o/oauth2/token')
    GOOGLE_SCOPE_URL: List[str] = Field(['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile'])
    GOOGLE_REDIRECT_URI: str = Field('http://localhost:8000/api/auth/google')
    GOOGLE_USERINFO_URL: str = Field('https://www.googleapis.com/oauth2/v3/userinfo')

    class Config:
        env_file = '.env'

@lru_cache
def get_settings():
    return Settings()