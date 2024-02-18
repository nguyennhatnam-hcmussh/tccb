from fastapi import APIRouter, Request, Depends
from typing import Annotated
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from main.db_setup import get_session
from main import config
from main.shortcuts import redirect, render, file

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/avatar', include_in_schema=False)
@requires('auth', redirect='login')
async def avatar(request: Request):
    return await file(request, "images/1.png")


@router.get('/template/footer', response_class=HTMLResponse)
@requires('guest')
async def template_footer(request: Request):
    context = {}
    return await render(request, "template", "footer.html", context)


@router.get('/template/header', response_class=HTMLResponse)
@requires('guest')
async def template_footer(request: Request):
    context = {}
    return await render(request, "template", "header.html", context)


@router.get('/template/nav/{tab}', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_nav(request: Request, tab: str):
    tabs = {
        'trangchu': {'Trang chủ':"fa-house"},
        'chucnang': {'Chức năng': 'fa-screwdriver-wrench'},
        'nhansu': {'Nhân sự': 'fa-address-book'},
        'hopdong': {'Hợp đồng': 'fa-file-contract'}
    }
    index = None
    keys = list(tabs.keys())
    for i in range(len(keys)):
        if keys[i] == tab:
            index = i + 1
    if index:
        context = {
            'tabs': tabs,
            'current_tab': index
        }
        return await render(request, "template", "nav.html", context)


@router.get('/template/screen/{tab}', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_screen(request: Request, tab: str):
    tabs = ['trangchu', 'chucnang', 'hopdong', 'nhansu']
    if tab in tabs:
        context = {
            'url': f'/template/{tab}'
        }
        return await render(request, "template", "screen.html", context)
    



@router.get('/test', response_class=HTMLResponse)
@requires('guest')
async def test(request: Request):
    context = {
        'template': 'hide',
        'url': '/template/test'
    }
    return await render(request, "main", "base.html", context)


@router.get('/template/test', response_class=HTMLResponse)
@requires('guest')
async def template_test(request: Request):
    context = {}
    return await render(request, "template", "test.html", context)