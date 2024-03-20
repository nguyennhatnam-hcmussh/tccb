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
from main.models import Donvi, Nhansu, Hopdong
from main.schemas import NhansuCreate, NhansuRead, NhansuSearch, NhansuCreateWithDonvi, NhansuReadWithDonvi, NhansuSearchWithDonvi, ListNhansuSearch, ListNhansuSearchWithDonvi
from main.schemas import HopdongCreate, HopdongReadFull

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


# @router.get('/template/hopdong/form/upload', response_class=HTMLResponse)
# @requires('auth', redirect='login')
# async def template_hopdong_form_upload(request: Request):
#     context = {}
#     return await render(request, "hopdong", "form_upload.html", context)


# @router.get("/api/hopdong/download")
# @requires('auth', redirect='login')
# async def api_hopdong_download(request: Request):
#     hopdong = pd.read_sql_table(table_name='hopdong', con=engine)

#     for i in hopdong.index:
#         if hopdong.iloc[i].ngayky:
#             hopdong.at[i,'ngayky'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(hopdong.iloc[i].ngayky)))
#         if hopdong.iloc[i].ngaytao:
#             hopdong.at[i,'ngaytao'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(hopdong.iloc[i].ngaytao)))

#     with pd.ExcelWriter(settings.STATIC_MAIN_DIR / 'files' / 'hopdong_down.xlsx') as writer:
#         hopdong.to_excel(writer, sheet_name="hopdong", index=False)
#     return await file(request, "files/hopdong_down.xlsx", filename="hopdong.xlsx")


# @router.post("/api/hopdong/upload")
# @requires('auth', redirect='login')
# async def api_hopdong_upload(*, request: Request, session: db_dependency, file: UploadFile):

#     # save file
#     async with aiofiles.open(settings.STATIC_MAIN_DIR / 'files' / 'hopdong_up.xlsx', 'wb') as out_file:
#         while content := await file.read(1024):  # async read chunk
#             await out_file.write(content)


#     hopdong = pd.read_excel(settings.STATIC_MAIN_DIR / 'files' / 'hopdong_up.xlsx', 'hopdong', index_col='id', na_filter = False)
    
#     for i in hopdong.index:
#         contract = session.get(Hopdong, i)
#         print(contract)
#         create = HopdongCreate(
#             maso = hopdong.loc[i].maso if hopdong.loc[i].maso else None,
#             email = hopdong.loc[i].email if hopdong.loc[i].email else None,
#             hovaten = hopdong.loc[i].hovaten if hopdong.loc[i].hovaten else None,
#             gioitinh = hopdong.loc[i].gioitinh if hopdong.loc[i].gioitinh else None,
#             ngaysinh = hopdong.loc[i].ngaysinh.strftime('%d/%m/%Y') if hopdong.loc[i].ngaysinh else None,
#             quoctich = hopdong.loc[i].quoctich if hopdong.loc[i].quoctich else 'Việt Nam',
#             hocvi = hopdong.loc[i].hocvi if hopdong.loc[i].hocvi else None,
#             hocvi_nganh = hopdong.loc[i].hocvi_nganh if hopdong.loc[i].hocvi_nganh else None,
#             hocham = hopdong.loc[i].hocham if hopdong.loc[i].hocham else None,
#             hocham_nganh = hopdong.loc[i].hocham_nganh if hopdong.loc[i].hocham_nganh else None,
#             CCCD_so = hopdong.loc[i].CCCD_so if hopdong.loc[i].CCCD_so else None,
#             CCCD_ngay = hopdong.loc[i].CCCD_ngay.strftime('%d/%m/%Y') if hopdong.loc[i].CCCD_ngay else None,
#             chucdanh = hopdong.loc[i].chucdanh if hopdong.loc[i].chucdanh else None,
#             donvicongtac = hopdong.loc[i].donvicongtac if hopdong.loc[i].donvicongtac else None,
#             co_bang = hopdong.loc[i].co_bang if isinstance(hopdong.loc[i].co_bang,bool) else False,
#             co_llkh = hopdong.loc[i].co_llkh if isinstance(hopdong.loc[i].co_llkh,bool) else False,
#             co_nvsp = hopdong.loc[i].co_nvsp if isinstance(hopdong.loc[i].co_nvsp,bool) else False,
#             type = hopdong.loc[i].type if hopdong.loc[i].type else "thinhgiang",
#             role = hopdong.loc[i].role if hopdong.loc[i].role else "user",
#         )
#         if person: # da ton tai tren he thong => update
#             print('rồi rồi rồi')
#             person_data = create.model_dump(exclude_unset=True)
#             for key, value in person_data.items():
#                 setattr(person, key, value)
#                 session.add(person)
#         else: # chua ton tai tren he thong => add new
#             print('chưa chưa chưa')
#             person = Nhansu.model_validate(create)
#             session.add(person)
    
#     session.commit()

#     context = {}
#     return await render(request, "nhansu", "form_upload_success.html", context)


@router.get("/api/nhansu/read/{maso}")
@requires('auth', redirect='login')
async def api_nhansu_thinhgiang_read(*, request: Request, session: db_dependency,maso: str):
    thinhgiang = session.exec(select(Nhansu).where(maso == Nhansu.maso)).first()
    if not thinhgiang:
        raise HTTPException(status_code=404, detail="Hero not found")
    data = (NhansuReadWithDonvi.model_validate(thinhgiang)).model_dump(exclude_unset=True)
    return await sendjson(request, data)


@router.post("/api/nhansu/update")
@requires('auth', redirect='login')
async def api_nhansu_update(*, request: Request, session: db_dependency, id: int, thinhgiang: NhansuCreateWithDonvi):
    donvi = thinhgiang.donvi
    thinhgiang.donvi = []

    db_thinhgiang = session.get(Nhansu, id)
    if not db_thinhgiang:
        raise HTTPException(status_code=404, detail="Thinhgiang not found")
    
    thinhgiang_data = thinhgiang.model_dump(exclude_unset=True)
    for key, value in thinhgiang_data.items():
        setattr(db_thinhgiang, key, value)

    for i in range(len(donvi)):
        db_thinhgiang.donvi.append(session.get(Donvi, donvi[i].id))

    session.add(db_thinhgiang)
    session.commit()
    session.refresh(db_thinhgiang)
    data = (NhansuSearchWithDonvi.model_validate(db_thinhgiang)).model_dump(exclude_unset=True)
    return await sendjson(request, data)

################################################################

@router.post("/api/nhansu/thinhgiang/create")
@requires('auth', redirect='login')
async def api_nhansu_thinhgiang_create(*, request: Request, session: db_dependency, thinhgiang: NhansuCreateWithDonvi):
    donvi = thinhgiang.donvi
    thinhgiang.donvi = []
    thinhgiang.type = 'thinhgiang'
    new_person = Nhansu.model_validate(thinhgiang)
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    if donvi:
        for i in range(len(donvi)):
            new_person.donvi.append(session.get(Donvi, donvi[i].id))
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    data = (NhansuSearchWithDonvi.model_validate(new_person)).model_dump(exclude_unset=True)
    return await sendjson(request, data)


@router.get("/api/nhansu/thinhgiang/search")
@requires('auth', redirect='login')
async def api_nhansu_thinhgiang_search(*, request: Request, session: db_dependency):
    thinhgiangs = session.exec(select(Nhansu).where(Nhansu.type == 'thinhgiang')).all()
    data = (ListNhansuSearch.model_validate({'data':thinhgiangs})).model_dump(exclude_unset=True)
    return await sendjson(request, data)


############################################################

@router.post("/api/nhansu/cohuu/create")
@requires('auth', redirect='login')
async def api_nhansu_cohuu_create(*, request: Request, session: db_dependency, cohuu: NhansuCreateWithDonvi):
    donvi = cohuu.donvi
    cohuu.donvi = []
    cohuu.type = 'cohuu'
    new_person = Nhansu.model_validate(cohuu)
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    if donvi:
        for i in range(len(donvi)):
            new_person.donvi.append(session.get(Donvi, donvi[i].id))
    session.add(new_person)
    session.commit()
    session.refresh(new_person)
    data = (NhansuSearchWithDonvi.model_validate(new_person)).model_dump(exclude_unset=True)
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

@router.post("/api/hopdong/create")
@requires('auth', redirect='login')
async def api_hopdong_create(*, request: Request, session: db_dependency, hopdong: HopdongCreate):
    donvimoi = hopdong.donvimoi
    giangvien = hopdong.giangvien
    nguoiphutrach = hopdong.nguoiphutrach
    hopdong.donvimoi = None
    hopdong.giangvien = None
    hopdong.nguoiphutrach = None

    new_hopdong = Hopdong.model_validate(hopdong)
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
    session.add(new_hopdong)
    session.commit()
    return await sendjson(request, {'message': 'success', 'hopdong': f'{new_hopdong.so}/{new_hopdong.nam}/HĐMG-XHNV-TCCB'})

@router.get("/api/hopdong/read/{id}")
@requires('auth', redirect='login')
async def api_hopdong_read(*, request: Request, session: db_dependency, id: int):
    hopdong = session.exec(select(Hopdong).where(id == Hopdong.id)).first()
    if not hopdong:
        raise HTTPException(status_code=404, detail="Hero not found")
    data = (HopdongReadFull.model_validate(hopdong)).model_dump(exclude_unset=True)
    return await sendjson(request, data)