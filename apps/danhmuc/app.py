from fastapi import APIRouter, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires

from sqlmodel import Session

from main.db_setup import get_session
from main import config
from main.shortcuts import file


settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]

@router.get("/api/danhmuc/{filename}")
@requires('auth', redirect='login')
async def api_donvi_download(request: Request, filename: str):
    return await file(request, f"danhmuc/{filename}.json")
