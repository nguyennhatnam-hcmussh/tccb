from urllib.parse import urlencode
import aiofiles
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
import pandas as pd
import datetime

from main.functions import Requests, stamp2date, stamp2datetime, date2stamp, now2stamp
from main.db_setup import get_session, engine
from main import config
from main.shortcuts import redirect, render, file, sendjson
from main.services import AuthGoogle, encode
from main.models import Donvi, Nhansu, Hopdong
from main.schemas import NhansuCreate, NhansuRead, NhansuCreateWithDonvimoi, NhansuReadWithDonvimoi, NhansuSearchWithDonvimoi, ListNhansuSearchWithDonvimoi, NhansuReadFull, NhansuSearch, ListNhansuSearch
from main.schemas import HopdongCreate, HopdongReadFull

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/nhansu', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def nhansu(request: Request):
    context = {
        'template': 'show',
        'tab': 'nhansu',
        'url': '/template/nhansu'
    }
    return await render(request, "main", "base.html", context)


@router.get('/template/nhansu', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_nhansu(request: Request):
    context = {}
    return await render(request, "nhansu", "nhansu.html", context)


@router.get('/template/nhansu/form/upload', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_nhansu_form_upload(request: Request):
    context = {}
    return await render(request, "nhansu", "form_upload.html", context)

################################################################

@router.get("/api/data/download")
@requires('auth', redirect='login')
async def api_nhansu_download(request: Request):
    bienban = pd.read_sql_table(table_name='bienban', con=engine)
    for i in bienban.index:
        if bienban.iloc[i].ngaytao:
            bienban.at[i,'ngaytao'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(bienban.iloc[i].ngaytao)))

    donvi = pd.read_sql_table(table_name='donvi', con=engine)
    gvtgofdonvi = pd.read_sql_table(table_name='gvtgofdonvi', con=engine)
    
    hopdong = pd.read_sql_table(table_name='hopdong', con=engine)
    for i in hopdong.index:
        if hopdong.iloc[i].ngayky:
            hopdong.at[i,'ngayky'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(hopdong.iloc[i].ngayky)))
        if hopdong.iloc[i].ngaycapnhat:
            hopdong.at[i,'ngaycapnhat'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(hopdong.iloc[i].ngaycapnhat)))

    hopdongofdonvi = pd.read_sql_table(table_name='hopdongofdonvi', con=engine)
    hopdongofgiangvien = pd.read_sql_table(table_name='hopdongofgiangvien', con=engine)
    hopdongofnguoiphutrach = pd.read_sql_table(table_name='hopdongofnguoiphutrach', con=engine)

    nhansu = pd.read_sql_table(table_name='nhansu', con=engine)
    for i in nhansu.index:
        if nhansu.iloc[i].ngaysinh:
            nhansu.at[i,'ngaysinh'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(nhansu.iloc[i].ngaysinh)))
        if nhansu.iloc[i].CCCD_ngay:
            nhansu.at[i,'CCCD_ngay'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(nhansu.iloc[i].CCCD_ngay)))
            
    nhansuofdonvi = pd.read_sql_table(table_name='nhansuofdonvi', con=engine)

    trangthai = pd.read_sql_table(table_name='trangthai', con=engine)
    for i in trangthai.index:
        if trangthai.iloc[i].ngaycapnhat:
            trangthai.at[i,'ngaycapnhat'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(trangthai.iloc[i].ngaycapnhat)))

    with pd.ExcelWriter(settings.STATIC_MAIN_DIR / 'files' / 'data_down.xlsx') as writer:
        bienban.to_excel(writer, sheet_name="bienban", index=False)
        donvi.to_excel(writer, sheet_name="donvi", index=False)
        gvtgofdonvi.to_excel(writer, sheet_name="gvtgofdonvi", index=False)
        hopdong.to_excel(writer, sheet_name="hopdong", index=False)
        hopdongofdonvi.to_excel(writer, sheet_name="hopdongofdonvi", index=False)
        hopdongofgiangvien.to_excel(writer, sheet_name="hopdongofgiangvien", index=False)
        hopdongofnguoiphutrach.to_excel(writer, sheet_name="hopdongofnguoiphutrach", index=False)
        nhansu.to_excel(writer, sheet_name="nhansu", index=False)
        nhansuofdonvi.to_excel(writer, sheet_name="nhansuofdonvi", index=False)
        trangthai.to_excel(writer, sheet_name="trangthai", index=False)
    return await file(request, "files/data_down.xlsx", filename="data.xlsx")


@router.post("/api/nhansu/upload")
@requires('auth', redirect='login')
async def api_nhansu_upload(*, request: Request, session: db_dependency, file: UploadFile):

    # save file
    async with aiofiles.open(settings.STATIC_MAIN_DIR / 'files' / 'nhansu_up.xlsx', 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)


    nhansu = pd.read_excel(settings.STATIC_MAIN_DIR / 'files' / 'nhansu_up.xlsx', 'nhansu', index_col='id', na_filter = False)
    
    for i in nhansu.index:
        person = session.get(Nhansu, i)
        print(person)
        create = NhansuCreate(
            maso = nhansu.loc[i].maso if nhansu.loc[i].maso else None,
            email = nhansu.loc[i].email if nhansu.loc[i].email else None,
            hovaten = nhansu.loc[i].hovaten if nhansu.loc[i].hovaten else None,
            gioitinh = nhansu.loc[i].gioitinh if nhansu.loc[i].gioitinh else None,
            ngaysinh = nhansu.loc[i].ngaysinh.strftime('%d/%m/%Y') if nhansu.loc[i].ngaysinh else None,
            quoctich = nhansu.loc[i].quoctich if nhansu.loc[i].quoctich else 'Việt Nam',
            hocvi = nhansu.loc[i].hocvi if nhansu.loc[i].hocvi else None,
            hocvi_nganh = nhansu.loc[i].hocvi_nganh if nhansu.loc[i].hocvi_nganh else None,
            hocham = nhansu.loc[i].hocham if nhansu.loc[i].hocham else None,
            hocham_nganh = nhansu.loc[i].hocham_nganh if nhansu.loc[i].hocham_nganh else None,
            CCCD_so = nhansu.loc[i].CCCD_so if nhansu.loc[i].CCCD_so else None,
            CCCD_ngay = nhansu.loc[i].CCCD_ngay.strftime('%d/%m/%Y') if nhansu.loc[i].CCCD_ngay else None,
            chucdanh = nhansu.loc[i].chucdanh if nhansu.loc[i].chucdanh else None,
            donvicongtac = nhansu.loc[i].donvicongtac if nhansu.loc[i].donvicongtac else None,
            co_bang = nhansu.loc[i].co_bang if isinstance(nhansu.loc[i].co_bang,bool) else False,
            co_llkh = nhansu.loc[i].co_llkh if isinstance(nhansu.loc[i].co_llkh,bool) else False,
            co_nvsp = nhansu.loc[i].co_nvsp if isinstance(nhansu.loc[i].co_nvsp,bool) else False,
            type = nhansu.loc[i].type if nhansu.loc[i].type else "thinhgiang",
            role = nhansu.loc[i].role if nhansu.loc[i].role else "user",
        )
        if person: # da ton tai tren he thong => update
            print('rồi rồi rồi')
            person_data = create.model_dump(exclude_unset=True)
            for key, value in person_data.items():
                setattr(person, key, value)
                session.add(person)
        else: # chua ton tai tren he thong => add new
            print('chưa chưa chưa')
            person = Nhansu.model_validate(create)
            session.add(person)
    
    session.commit()

    context = {}
    return await render(request, "nhansu", "form_upload_success.html", context)

################################################################

@router.get("/api/nhansu/read/{maso}")
@requires('auth', redirect='login')
async def api_nhansu_thinhgiang_read(*, request: Request, session: db_dependency, maso: str):
    thinhgiang = session.exec(select(Nhansu).where(maso == Nhansu.maso)).first()
    if not thinhgiang:
        raise HTTPException(status_code=404, detail="Hero not found")
    data = (NhansuReadFull.model_validate(thinhgiang)).model_dump(exclude_unset=True)
    data['hopdong'] = sorted(data['hopdong'], key=lambda d: d['ngaycapnhat'], reverse=True)
    if data['CCCD_ngay']:
        data['CCCD_ngay'] = await stamp2date(data['CCCD_ngay'])
    for i in range(len(data['hopdong'])):
            data['hopdong'][i]['ngaycapnhat'] = await stamp2datetime(data['hopdong'][i]['ngaycapnhat'])
    return await sendjson(request, data)


@router.get("/api/nhansu/remove/{maso}")
@requires('root', redirect='login')
async def api_nhansu_thinhgiang_remove(*, request: Request, session: db_dependency, maso: str):
    thinhgiang = session.exec(select(Nhansu).where(maso == Nhansu.maso)).first()
    if not thinhgiang:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(thinhgiang)
    session.commit()
    return await sendjson(request, {'message': "delete successful"})


@router.post("/api/nhansu/update")
@requires('auth', redirect='login')
async def api_nhansu_update(*, request: Request, session: db_dependency, id: int, thinhgiang: NhansuCreateWithDonvimoi):
    donvimoi = thinhgiang.donvimoi
    thinhgiang.donvimoi = []
    
    if thinhgiang.type == 'cohuu' and thinhgiang.donvi:
        donvi = session.get(Donvi, thinhgiang.donvi.id)
        thinhgiang.donvi = None
        thinhgiang.donvingoai = None
    elif thinhgiang.type == 'thinhgiang' and thinhgiang.donvingoai:
        thinhgiang.donvi = None
        donvi = None
    else:
        thinhgiang.donvingoai = None
        thinhgiang.donvi = None
        donvi = None

    db_thinhgiang = session.get(Nhansu, id)
    if not db_thinhgiang:
        raise HTTPException(status_code=404, detail="Thinhgiang not found")
    
    thinhgiang_data = thinhgiang.model_dump(exclude_unset=True)
    for key, value in thinhgiang_data.items():
        setattr(db_thinhgiang, key, value)

    for i in range(len(donvimoi)):
        db_thinhgiang.donvimoi.append(session.get(Donvi, donvimoi[i].id))

    # cập nhật đơn vị (cơ hữu)
    db_thinhgiang.donvi = None
    session.add(db_thinhgiang)
    session.commit()
    db_thinhgiang.donvi = donvi
    
    
    session.add(db_thinhgiang)
    session.commit()
    session.refresh(db_thinhgiang)
    data = (NhansuSearch.model_validate(db_thinhgiang)).model_dump(exclude_unset=True)
    return await sendjson(request, data)


@router.post("/api/nhansu/create")
@requires('auth', redirect='login')
async def api_nhansu_create(*, request: Request, session: db_dependency, thinhgiang: NhansuCreateWithDonvimoi):
    
    donvimoi = thinhgiang.donvimoi
    thinhgiang.donvimoi = []
    
    if thinhgiang.type == 'cohuu' and thinhgiang.donvi:
        donvi = session.get(Donvi, thinhgiang.donvi.id)
        thinhgiang.donvi = None
        thinhgiang.donvingoai = None
    elif thinhgiang.type == 'thinhgiang' and thinhgiang.donvingoai:
        thinhgiang.donvi = None
        donvi = None
    else:
        thinhgiang.donvingoai = None
        thinhgiang.donvi = None
        donvi = None
    
    new_person = Nhansu.model_validate(thinhgiang)
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    
    if donvimoi:
        for i in range(len(donvimoi)):
            new_person.donvimoi.append(session.get(Donvi, donvimoi[i].id))
            
    # cập nhật đơn vị (cơ hữu)
    new_person.donvi = None
    session.add(new_person)
    session.commit()
    new_person.donvi = donvi
            
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    data = (NhansuSearch.model_validate(new_person)).model_dump(exclude_unset=True)
    return await sendjson(request, data)

################################################################

@router.get("/api/nhansu/thinhgiang/search")
@requires('auth', redirect='login')
async def api_nhansu_thinhgiang_search(*, request: Request, session: db_dependency):
    thinhgiangs = session.exec(select(Nhansu).where(Nhansu.type == 'thinhgiang')).all()
    data = (ListNhansuSearch.model_validate({'data':thinhgiangs})).model_dump(exclude_unset=True)
    return await sendjson(request, data)


@router.get("/api/nhansu/cohuu/search")
@requires('auth', redirect='login')
async def api_nhansu_cohuu_search(*, request: Request, session: db_dependency):
    cohuus = session.exec(select(Nhansu).where(Nhansu.type == 'cohuu')).all()
    data = (ListNhansuSearch.model_validate({'data':cohuus})).model_dump(exclude_unset=True)
    return await sendjson(request, data)

###################################################

@router.get("/api/nhansu/me/search")
@requires('auth', redirect='login')
async def api_nhansu_me_search(*, request: Request, session: db_dependency):
    uuid = request.user.data.get('uuid')
    nhansu = session.get(Nhansu, uuid)
    data = (NhansuSearch.model_validate(nhansu)).model_dump(exclude_unset=True)
    return await sendjson(request, data)


############################################################

@router.get("/api/nhansu/donvingoai/danhmuc")
@requires('auth', redirect='login')
async def api_nhansu_me_search(*, request: Request, session: db_dependency):
    values = session.query(Nhansu.donvingoai).distinct().all()
    i = 0
    data = []
    for value in values:
        if value[0]:
            i+=1
            data.append({"id": i, "ten": value[0]})
            
    return await sendjson(request, data)