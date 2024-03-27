from urllib.parse import urlencode
import aiofiles
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, desc
import pandas as pd
import datetime
import json

from main.functions import Requests, stamp2date, stamp2datetime, date2stamp, now2stamp
from main.db_setup import get_session, engine
from main import config
from main.shortcuts import redirect, render, file, sendjson
from main.services import AuthGoogle, encode
from main.models import Donvi, Nhansu, Hopdong, Trangthai
from main.schemas import HopdongCreate, HopdongReadFull, ListHopdongRead, ListHopdongReadFull, TrangthaiCreate

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/hopdong', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def hopdong(request: Request):
    context = {
        'template': 'show',
        'tab': 'hopdong',
        'url': '/template/hopdong'
    }
    return await render(request, "main", "base.html", context)


@router.get('/template/hopdong', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_hopdong(request: Request):
    context = {}
    return await render(request, "hopdong", "hopdong.html", context)


############################################################

@router.post("/api/hopdong/create")
@requires('auth', redirect='login')
async def api_hopdong_create(*, request: Request, session: db_dependency, hopdong: HopdongCreate):
    donvimoi = hopdong.donvimoi
    giangvien = hopdong.giangvien
    nguoiphutrach = hopdong.nguoiphutrach
    hopdong.donvimoi = None
    hopdong.giangvien = None
    hopdong.nguoiphutrach = None
    hopdong.ngayky = await date2stamp(hopdong.ngayky)
    hopdong.trangthai = 'Đã tạo'
    hopdong.ngaycapnhat = await now2stamp()
    
    test = hopdong.model_dump(exclude_unset=True)
    print(json.dumps(test))
    
    new_hopdong = Hopdong.model_validate_json(json.dumps(test))
    # new_hopdong = Hopdong.model_validate(hopdong)
    session.add(new_hopdong)
    session.commit()
    session.refresh(new_hopdong)
    
    # lay so hop dong
    hopdong_pre = session.get(Hopdong, (int(new_hopdong.id) - 1))
    if (hopdong_pre) and (hopdong_pre.nam == new_hopdong.nam):
        new_hopdong.so = hopdong_pre.so + 1
    else:
        new_hopdong.so = 1

    if donvimoi:
        new_hopdong.donvimoi = (session.exec(select(Donvi).where(Donvi.ten == donvimoi)).first())
    if giangvien:
        new_hopdong.giangvien = (session.exec(select(Nhansu).where(Nhansu.maso == giangvien)).first())
    if nguoiphutrach:
        new_hopdong.nguoiphutrach = (session.exec(select(Nhansu).where(Nhansu.maso == nguoiphutrach)).first())

    # Trang thai
    trangthai = TrangthaiCreate(trangthai=new_hopdong.trangthai, ngaycapnhat=str(new_hopdong.ngaycapnhat))
    new_trangthai = Trangthai.model_validate(trangthai)
    new_hopdong.trangthais.append(new_trangthai)

    session.add(new_hopdong)
    session.commit()
    session.refresh(new_hopdong)
    print(new_hopdong)

    return await sendjson(request, {'message': 'success', 'hopdong': f'{new_hopdong.so}/{new_hopdong.nam}/HĐMG-XHNV-TCCB'})

@router.get("/api/hopdong/read/{id}")
@requires('auth', redirect='login')
async def api_hopdong_read(*, request: Request, session: db_dependency, id: int):
    hopdong = session.exec(select(Hopdong).where(id == Hopdong.id)).first()
    if not hopdong:
        raise HTTPException(status_code=404, detail="Hero not found")
    data = (HopdongReadFull.model_validate(hopdong)).model_dump(exclude_unset=True)
    return await sendjson(request, data)

####################################################################

@router.get("/api/hopdong/search")
@requires('auth', redirect='login')
async def api_hopdong_search(*, request: Request, session: db_dependency):
    hopdongs = session.exec(select(Hopdong).order_by(desc(Hopdong.ngaycapnhat))).all()
    data = (ListHopdongRead.model_validate({'data':hopdongs})).model_dump(exclude_unset=True)
    for i in range(len(data['data'])):
        data['data'][i]['ngayky'] = await stamp2date(data['data'][i]['ngayky'])
        data['data'][i]['ngaycapnhat'] = await stamp2datetime(data['data'][i]['ngaycapnhat'])
    return await sendjson(request, data)