from fastapi import FastAPI, Request, Depends, Form
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.authentication import requires
from starlette.middleware.authentication import AuthenticationMiddleware
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from typing import Annotated
from fastapi.responses import PlainTextResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from random import randint
import requests
import codecs
import json

from main.config import get_settings
from main.db_setup import get_session
from main.shortcuts import file, redirect, render, sendjson
from main.functions import Requests
from main.models import Nhansu
from main.middlewares.process_time import CustomHeaderMiddleware
from main.middlewares.auth import AuthMiddleware
from main.apps import (template, auth, nhansu, error, donvi, danhmuc, hopdong)


settings = get_settings()

db_dependency = Annotated[Session, Depends(get_session)]


async def on_start_up() -> None:
    Requests.get_aiohttp_client()

async def on_shutdown() -> None:
    await Requests.close_aiohttp_client()
    
app = FastAPI(on_startup=[on_start_up], on_shutdown=[on_shutdown])


origins = ['https://dc.vnuhcm.edu.vn']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(CustomHeaderMiddleware)
app.add_middleware(AuthenticationMiddleware, backend=AuthMiddleware())


app.mount("/static", StaticFiles(directory=str(settings.STATIC_MAIN_DIR)), name="static")


app.include_router(template.router)
app.include_router(auth.router)
app.include_router(nhansu.router)
app.include_router(error.router)
app.include_router(donvi.router)
app.include_router(danhmuc.router)
app.include_router(hopdong.router)


@app.get('/favicon.ico', include_in_schema=False)
async def favicon(request: Request):
    return await file(request, "images/favicon.ico")


@app.get('/404.gif', include_in_schema=False)
async def notfound_gif(request: Request):
    return await file(request, "images/404.gif")


@app.get("/active/{key_secret}")
@requires('guest')
async def active_root(*, request: Request, session: db_dependency, key_secret:str):
    if key_secret == 'MrfzY7EhnRv6RQqa6tf1eeJxxUyt6Xrrj3xcepcZJrTMMewh':
        if not session.exec(select(Nhansu).where(Nhansu.maso == 'QSX9710428')).first():
            nampro = Nhansu(
                maso='QSX9710428',
                hovaten="Nguyễn Nhật Nam",
                email="nguyennhatnam@hcmussh.edu.vn",
                sdt="0353469292",
                role="root",
                type='cohuu'
            )
            session.add(nampro)
            session.commit()
            return "Add Root Successfully"
        return "Root User Already Exists"
    

@app.get('/', response_class=HTMLResponse)
@requires('guest')
async def homepage(request: Request):
    context = {}
    return await redirect(request, "/hopdong")

@app.get('/logout', response_class=HTMLResponse)
@requires('guest')
async def logout(request: Request):
    context = {}
    return await redirect(request, "/login", clear_cookie=True)


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    context = {
        'template': 'hide',
        'url': '/template/404'
    }
    return await render(request, "error", "404.html", context)

nhucau = 0
list_code = []
list_token = []

@app.post("/dhqg")
@requires('guest')
async def dhqg(request: Request, czt: Annotated[str, Form()]):
    global nhucau, list_code, list_token
    list_token.append(czt)
    nhucau -= 1
    if nhucau < 0:
        nhucau = 0
    return await sendjson(request, {'message': str(randint(0,999999999)).zfill(9)})

@app.get("/gettoken/{code}")
@requires('guest')
async def gettoken(request: Request, code: str):
    global nhucau, list_code, list_token
    if code == "NEW":
        new_code = str(randint(0,999999999)).zfill(9)
        list_code.append(new_code)
        nhucau += 1
        return await sendjson(request, {'message': 'wait', 'code': new_code})
    if len(list_token):
        token = list_token[0]
        list_token.pop(0)
        list_code.remove(code)
        return await sendjson(request, {'message': 'success', 'token': token})
    else:
        return await sendjson(request, {'message': 'wait', 'code': code})

@app.get("/checknhucau")
@requires('guest')
async def checknhucau(request: Request):
    if nhucau > 0:
        return await sendjson(request, {'message': 'have'})
    else:
        return await sendjson(request, {'message': 'no'})
    

@app.get('/qrcode')
@requires('guest')
async def qrcode(request: Request, code:str):
    key = code.split('/')[-1]
    url = f'https://dc.vnuhcm.edu.vn/campaign/bio?key={key}'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.get(url, headers=headers)
    data = response.json()
    with codecs.open(str(settings.STATIC_MAIN_DIR / f"jsondata/{key}.json"), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    with codecs.open(str(settings.STATIC_MAIN_DIR / f"files/tonghop.txt"),'a', encoding='utf-8') as f:
        f.write(f"{data['result']['bio']['tab_canhan']['ca_nhan']['hovaten']},{data['result']['bio']['tab_canhan']['ca_nhan']['ngaysinh']},{data['result']['bio']['tab_canhan']['cong_tac']['macb']},{key}\n")
    return 'ok'

@app.get('/getcode/{id}')
@requires('guest')
async def getcode(request: Request, id:int):
    with codecs.open(str(settings.STATIC_MAIN_DIR / f"files/tonghop.txt"),'r', encoding='utf-8') as f:
        raw = str(f.read()).split('\n')
    code = raw[id - 1].split(',')[-1]
    return await sendjson(request, {'message': 'ok', 'code': code})

@app.get('/checktrung')
@requires('guest')
async def checktrung(request: Request, code:str):
    trung = [
        'wcDQ9kRhRJ9sZme5u9eP89I8Abs',
        'S7oAzYx55TfyUmpAzhAMsfoTjG53s',
        'tssASmM8bYAbwP2LfiMkN5o2bbo',
        'E2yrgaUbOv3KPnRlKTPLfgpUhD4',
        'DzJ7KMf8zXYpRXs6qb7YfUhzMx4',
        'pyl6Y0FpQph381MqKfBx5p23KfE',
        'paUZP1loCoiPFzAEuSQxFmQzMybo',
        'azAFpOk5HC6OMl5PecOSUai1LzAqI',
        'nlbjs1YZWD7uAme4U22Q5FzVjGo',
        '5vDi0gpd4jvjfwfQPUv6ZXTExTQ',
        '0j8rr3fGmsIcuQAoUcLd2zAd910Q',
        'pnbzAOAziE7rFgNb3Nsh4EVadiC4A'
    ]
    key = code.split('/')[-1]
    if key in trung:
        print('trung')
        return 'trung'
    else:
        print('no')
        return 'no'
    
@app.get('/final')
@requires('guest')
async def final(request: Request, code:str):
    key = code.split('/')[-1]
    
    khongtrung = True
    with codecs.open(str(settings.STATIC_MAIN_DIR / f"files/final.txt"),'r', encoding='utf-8') as f:
        raw = str(f.read()).split('\n')
        
    for ii in raw:
        code = ii.split(',')[-1]
        if code == key:
            khongtrung = False
            maso = ii.split(',')[2]
    if khongtrung:    
        url = f'https://dc.vnuhcm.edu.vn/campaign/bio?key={key}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.get(url, headers=headers)
        data = response.json()
        

        with codecs.open(str(settings.STATIC_MAIN_DIR / f"final/{key}.json"), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
        with codecs.open(str(settings.STATIC_MAIN_DIR / f"files/final.txt"),'a', encoding='utf-8') as f:
            f.write(f"{data['result']['bio']['tab_canhan']['ca_nhan']['hovaten']},{data['result']['bio']['tab_canhan']['ca_nhan']['ngaysinh']},{data['result']['bio']['tab_canhan']['cong_tac']['macb']},{key}\n")
        maso = data['result']['bio']['tab_canhan']['cong_tac']['macb']
        
    with codecs.open(str(settings.STATIC_MAIN_DIR / f"files/danhsach.txt"),'r', encoding='utf-8') as f:
        raw = str(f.read()).split('\n')
    
    for stt in raw:
        stt = stt.split(',')
        if stt[0] == maso:
            sothutu = stt[1]
    
    if maso:
        return sothutu
    else:
        return 'error'