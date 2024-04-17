from urllib.parse import urlencode
import aiofiles
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select, desc, or_
import pandas as pd
import datetime
import json

from main.functions import Requests, stamp2date, stamp2datetime, date2stamp, now2stamp
from main.db_setup import get_session, engine
from main import config
from main.shortcuts import redirect, render, file, sendjson
from main.services import AuthGoogle, encode
from main.models import Donvi, Nhansu, Hopdong, Trangthai, Bienban
from main.schemas import HopdongCreate, HopdongReadFull, ListHopdongRead, ListHopdongReadFull, TrangthaiCreate, HopdongRead, BienbanCreate, NhansuReadWithHopdongphutrach

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
        donvimoi_data = session.exec(select(Donvi).where(Donvi.ten == donvimoi)).first()
        new_hopdong.donvimoi = donvimoi_data
    if giangvien:
        giangvien_data = session.exec(select(Nhansu).where(Nhansu.maso == giangvien)).first()
        new_hopdong.giangvien = giangvien_data
    if nguoiphutrach:
        new_hopdong.nguoiphutrach = (session.exec(select(Nhansu).where(Nhansu.maso == nguoiphutrach)).first())

    # add đơn vị mời to giảng viên
    if donvimoi_data and giangvien_data:
        if donvimoi_data not in giangvien_data.donvi:
            giangvien_data.donvi.append(donvimoi_data)

    # Trang thai
    trangthai = TrangthaiCreate(trangthai=new_hopdong.trangthai, ngaycapnhat=str(new_hopdong.ngaycapnhat))
    new_trangthai = Trangthai.model_validate(trangthai)
    new_hopdong.trangthais.append(new_trangthai)

    session.add(new_hopdong)
    session.commit()
    session.refresh(new_hopdong)
    print(new_hopdong)

    return await sendjson(request, {'message': 'success', 'hopdong': f'{new_hopdong.so}/{new_hopdong.nam}/HĐMG-XHNV-TCCB'})

############################################################

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


####################################################################

@router.get("/api/hopdong/count")
@requires('auth', redirect='login')
async def api_hopdong_count(*, request: Request, session: db_dependency):
    role = request.user.data.get('role')
    data = {'data': {
        'cosan': 0,
        'danhan': 0,
        'trinhky': 0,
        'daky': 0,
        'hoanthanh': 0,
        'coloi': 0
    }}
    if role in ['admin','root']:
        cosan = session.query(Hopdong).filter(or_(Hopdong.trangthai == 'Đã tạo',Hopdong.trangthai == 'Có sẵn')).count()
        danhan = session.query(Hopdong).filter(Hopdong.trangthai == 'P.TCCB đã nhận').count()
        trinhky = session.query(Hopdong).filter(Hopdong.trangthai == 'Đang trình ký').count()
        daky = session.query(Hopdong).filter(Hopdong.trangthai == 'Đã ký - chờ nhận').count()
        hoanthanh = session.query(Hopdong).filter(Hopdong.trangthai == 'Hoàn thành').count()
        coloi = session.query(Hopdong).filter(Hopdong.trangthai == 'Có lỗi - chờ nhận').count()
        
        if cosan >= 0 and danhan >= 0 and trinhky >= 0 and hoanthanh >= 0 and coloi >= 0:
            data = {
                'message': 'success',
                'data': {
                    'cosan': cosan,
                    'danhan': danhan,
                    'trinhky': trinhky,
                    'daky': daky,
                    'hoanthanh': hoanthanh,
                    'coloi': coloi
                }
            }
        else:
            data = {'message': 'error'}
        
    elif role in ['user']:
        uuid = request.user.data.get('uuid')
        user = session.get(Nhansu, uuid)
        hopdongs = (NhansuReadWithHopdongphutrach.model_validate(user)).model_dump(exclude_unset=True)
        for hopdong in hopdongs['hopdongphutrach']:
            if hopdong['trangthai'] in ['Có sẵn', 'Đã tạo']:
                data['data']['cosan'] += 1
            elif hopdong['trangthai'] in ['P.TCCB đã nhận']:
                data['data']['danhan'] += 1
            elif hopdong['trangthai'] in ['Đang trình ký']:
                data['data']['trinhky'] += 1
            elif hopdong['trangthai'] in ['Đã ký - chờ nhận']:
                data['data']['daky'] += 1
            elif hopdong['trangthai'] in ['Hoàn thành']:
                data['data']['hoanthanh'] += 1
            elif hopdong['trangthai'] in ['Có lỗi - chờ nhận']:
                data['data']['coloi'] += 1
        data['message'] = 'success'
    else:
        data = {'message': 'error'}
        
    return await sendjson(request, data)

####################################################################
@router.post("/api/hopdong/upgrade/{next}")
@requires('auth', redirect='login')
async def api_hopdong_upgrade(*, request: Request, session: db_dependency, next: str, id_hopdongs: List[int]):
    trangthai_query = None
    trangthai_next = None
    
    if next == 'nhanhopdong':
        bienban_loai = 'nhan'
        trangthai_query = ['Đã tạo', 'Có sẵn', 'Hoàn thành']
        trangthai_next= 'P.TCCB đã nhận'
    elif next == 'trinhky':
        bienban_loai = None
        trangthai_query = ['P.TCCB đã nhận']
        trangthai_next= 'Đang trình ký'
    elif next == 'daky':
        bienban_loai = None
        trangthai_query = ['Đang trình ký']
        trangthai_next= 'Đã ký - chờ nhận'    
    elif next == 'hoanthanh':
        bienban_loai = 'tra'
        trangthai_query = ['Đã ký - chờ nhận']
        trangthai_next= 'Hoàn thành'
    elif next == 'baoloi':
        bienban_loai = None
        trangthai_query = ['P.TCCB đã nhận', 'Đang trình ký']
        trangthai_next= 'Có lỗi - chờ nhận'
    elif next == 'tralai':
        bienban_loai = 'tra'
        trangthai_query = ['Có lỗi - chờ nhận']
        trangthai_next= 'Có sẵn'
        
    if trangthai_query and trangthai_next:
        # Tao bien ban moi
        if bienban_loai:
            bienban = BienbanCreate(ngaytao=await now2stamp(), loai=bienban_loai)
            bienban = bienban.model_dump(exclude_unset=True)  
            new_bienban = Bienban.model_validate_json(json.dumps(bienban))
            session.add(new_bienban)
            session.commit()
            session.refresh(new_bienban)
            # lay so bien ban
            bienban_pre = session.get(Bienban, (int(new_bienban.id) - 1))
            if (bienban_pre) and (bienban_pre.nam == new_bienban.nam):
                new_bienban.so = bienban_pre.so + 1
            else:
                new_bienban.so = 1
            session.add(new_bienban)
            session.commit()
            session.refresh(new_bienban)
        # start upgrade hopdong
        for i in id_hopdongs:
            hopdong = session.get(Hopdong, i)
            if hopdong and (hopdong.trangthai in trangthai_query):
                hopdong.trangthai = trangthai_next
                hopdong.ngaycapnhat = await now2stamp()
                if bienban_loai:
                    hopdong.bienban = f'{new_bienban.so}/{new_bienban.nam}'
                # Trang thai
                trangthai = TrangthaiCreate(trangthai=hopdong.trangthai, ngaycapnhat=str(hopdong.ngaycapnhat))
                new_trangthai = Trangthai.model_validate(trangthai)
                hopdong.trangthais.append(new_trangthai)
                if bienban_loai:
                    new_bienban.trangthais.append(new_trangthai)
                    session.add(new_bienban)
                session.add(hopdong)
                
        session.commit()
        
        hopdongs = session.exec(select(Hopdong).order_by(desc(Hopdong.ngaycapnhat))).all()
        data = (ListHopdongRead.model_validate({'data':hopdongs})).model_dump(exclude_unset=True)
        for i in range(len(data['data'])):
            data['data'][i]['ngayky'] = await stamp2date(data['data'][i]['ngayky'])
            data['data'][i]['ngaycapnhat'] = await stamp2datetime(data['data'][i]['ngaycapnhat'])
        data['message'] = 'success'
        return await sendjson(request, data)
    else:
        return await sendjson(request, {'message': 'error'})