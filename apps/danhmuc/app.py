from urllib.parse import urlencode
import aiofiles
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
import pandas as pd
import datetime

from main.functions import Requests
from main.db_setup import get_session, engine
from main import config
from main.shortcuts import redirect, render, file, sendjson
from main.services import AuthGoogle, encode
from main.models import User, Auth, Donvi
from main.schemas import UserList, DonviCreate, DonviRead, DonviUpdate

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]

@router.get("/api/danhmuc/{filename}")
@requires('auth', redirect='login')
async def api_donvi_download(request: Request, filename: str):
    return await file(request, f"danhmuc/{filename}.json")
