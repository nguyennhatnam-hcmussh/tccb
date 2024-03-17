from fastapi import APIRouter, Request, Depends
from typing import Annotated
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session

from main.db_setup import get_session
from main import config
from main.shortcuts import render

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/template/404', response_class=HTMLResponse)
@requires('guest')
async def template_404(request: Request):
    context = {}
    return await render(request, "error", "404.html", context)