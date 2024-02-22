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
from main.models import User, Auth, Thinhgiang
from main.schemas import UserList, ThinhgiangCreate, ThinhgiangSearch, ChucnangRead

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/chucnang', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def chucnang(request: Request):
    context = {
        'template': 'show',
        'tab': 'chucnang',
        'url': '/template/chucnang'
    }
    return await render(request, "main", "base.html", context)


@router.get('/template/chucnang', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_chucnang(request: Request):
    context = {}
    return await render(request, "chucnang", "chucnang.html", context)

@router.get("/api/chucnang/loai")
@requires('auth', redirect='login')
async def api_chucnang_loai(*, request: Request):
    data = [
        {'id': 1, 'loai': 'Nhận hợp đồng mới'},
        {'id': 2, 'loai': 'Kiểm tra hợp đồng'},
        {'id': 3, 'loai': 'Nhận hợp đồng đã trình ký'},
        {'id': 4, 'loai': 'Trả hợp đồng'},
    ]
    return data

@router.post("/template/chucnang/loai")
@requires('auth', redirect='login')
async def template_chucnang_loai(*, request: Request, chucnang: ChucnangRead):
    print(chucnang)
    context = {}
    return await render(request, "chucnang", "nhanmoi.html", context)


@router.get("/api/chucnang/danhsach-hd-moi")
@requires('auth', redirect='login')
async def api_chucnang_danhsachhdmoi(*, request: Request, session: db_dependency):
    
    data = await GSheet.get_all_row()
    
    for item in data:
        db_hopdong = session.exec(select(Hopdong).where(Hopdong.sohd == item['SỐ HĐ'])).first()
        hopdong = Hopdong(
            sohd = item['SỐ HĐ'],
            giangvien = item['Tên GV mời giảng'],
            donvi = item['Đơn vị mời giảng'],
            nguoilayso = item['Người lấy số HĐ']
        )
        if db_hopdong:
            data_hopdong = hopdong.model_dump(exclude_unset=True)
            for key, value in data_hopdong.items():
                setattr(db_hopdong, key, value)
                session.add(db_hopdong)
        else:
            db_hopdong = Hopdong.model_validate(hopdong)
            session.add(db_hopdong)
    
    session.commit()
    
    hopdongs = session.exec(select(Hopdong)).all()

    results = ListHopdongRead.model_validate({'data': hopdongs}).model_dump(exclude_unset=True)
    
    return await sendjson(request, results)