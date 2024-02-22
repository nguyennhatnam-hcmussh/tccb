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
from main.shortcuts import redirect, render, file
from main.services import AuthGoogle, encode
from main.models import User, Auth, Thinhgiang
from main.schemas import UserList, ThinhgiangCreate, ThinhgiangSearch, ThinhgiangRead

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


@router.get('/api/nhansu/table', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def api_nhansu_table(*, request: Request, session: db_dependency):
    data = session.exec(select(User)).all()
    context = UserList.model_validate({'data': data}).model_dump()
    return await render(request, "nhansu", "table.html", context)


@router.get("/api/nhansu/download")
@requires('auth', redirect='login')
async def api_nhansu_download(request: Request):
    thinhgiang = pd.read_sql_table(table_name='thinhgiang', con=engine)

    for i in thinhgiang.index:
        if thinhgiang.iloc[i].ngaysinh:
            thinhgiang.at[i,'ngaysinh'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(thinhgiang.iloc[i].ngaysinh)))
        if thinhgiang.iloc[i].CCCD_ngay:
            thinhgiang.at[i,'CCCD_ngay'] = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(thinhgiang.iloc[i].CCCD_ngay)))

    with pd.ExcelWriter(settings.STATIC_MAIN_DIR / 'files' / 'nhansu_down.xlsx') as writer:
        thinhgiang.to_excel(writer, sheet_name="nhansu", index=False)
    return await file(request, "files/nhansu_down.xlsx", filename="nhansu.xlsx")


@router.post("/api/nhansu/upload")
@requires('auth', redirect='login')
async def api_nhansu_upload(*, request: Request, session: db_dependency, file: UploadFile):

    # save file
    async with aiofiles.open(settings.STATIC_MAIN_DIR / 'files' / 'nhansu_up.xlsx', 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)


    nhansu = pd.read_excel(settings.STATIC_MAIN_DIR / 'files' / 'nhansu_up.xlsx', 'nhansu', index_col='id', na_filter = False)
    
    for i in nhansu.index:
        print('nampro')
        print(i)
        person = session.get(Thinhgiang, i)
        print(person)
        create = ThinhgiangCreate(
            maso = nhansu.loc[i].maso if nhansu.loc[i].maso else None,
            email = nhansu.loc[i].email if nhansu.loc[i].email else None,
            hovaten = nhansu.loc[i].hovaten if nhansu.loc[i].hovaten else None,
            gioitinh = nhansu.loc[i].gioitinh if nhansu.loc[i].gioitinh else None,
            ngaysinh = nhansu.loc[i].ngaysinh.strftime('%d/%m/%Y') if nhansu.loc[i].ngaysinh else None,
            quoctich = nhansu.loc[i].quoctich if nhansu.loc[i].quoctich else None,
            noisinh = nhansu.loc[i].noisinh if nhansu.loc[i].noisinh else None,
            dantoc = nhansu.loc[i].dantoc if nhansu.loc[i].dantoc else None,
            tongiao = nhansu.loc[i].tongiao if nhansu.loc[i].tongiao else None,
            hocvi = nhansu.loc[i].hocvi if nhansu.loc[i].hocvi else None,
            hocvi_nganh = nhansu.loc[i].hocvi_nganh if nhansu.loc[i].hocvi_nganh else None,
            hocham = nhansu.loc[i].hocham if nhansu.loc[i].hocham else None,
            hocham_nganh = nhansu.loc[i].hocham_nganh if nhansu.loc[i].hocham_nganh else None,
            hocham_nam = nhansu.loc[i].hocham_nam if nhansu.loc[i].hocham_nam else None,
            CCCD_so = nhansu.loc[i].CCCD_so if nhansu.loc[i].CCCD_so else None,
            CCCD_ngay = nhansu.loc[i].CCCD_ngay.strftime('%d/%m/%Y') if nhansu.loc[i].CCCD_ngay else None,
            CCCD_noi = nhansu.loc[i].CCCD_noi if nhansu.loc[i].CCCD_noi else None,
            chucdanh = nhansu.loc[i].chucdanh if nhansu.loc[i].chucdanh else None,
            donvicongtac = nhansu.loc[i].donvicongtac if nhansu.loc[i].donvicongtac else None,
            co_bang = nhansu.loc[i].co_bang if isinstance(nhansu.loc[i].co_bang,bool) else False,
            co_llkh = nhansu.loc[i].co_llkh if isinstance(nhansu.loc[i].co_llkh,bool) else False,
            co_nvsp = nhansu.loc[i].co_nvsp if isinstance(nhansu.loc[i].co_nvsp,bool) else False,
        )
        if person: # da ton tai tren he thong => update
            print('rồi rồi rồi')
            person_data = create.model_dump(exclude_unset=True)
            for key, value in person_data.items():
                setattr(person, key, value)
                session.add(person)
        else: # chua ton tai tren he thong => add new
            print('chưa chưa chưa')
            person = Thinhgiang.model_validate(create)
            session.add(person)
    
    session.commit()

    context = {}
    return await render(request, "nhansu", "form_upload_success.html", context)


@router.get("/api/nhansu/thinhgiang/read/{thinhgiang_maso}", response_model=ThinhgiangRead)
@requires('auth', redirect='login')
async def api_donvi_read(*, request: Request, session: db_dependency, thinhgiang_maso: str):
    thinhgiang = session.exec(select(Thinhgiang).where(thinhgiang_maso == Thinhgiang.maso)).first()
    if not thinhgiang:
        raise HTTPException(status_code=404, detail="Hero not found")
    return thinhgiang


@router.get("/api/nhansu/search", response_model=List[ThinhgiangSearch])
@requires('auth', redirect='login')
async def api_nhansu_search(*, request: Request, session: db_dependency):
    thinhgiangs = session.exec(select(Thinhgiang)).all()
    # results = ListThinhgiangSearch.model_validate({'data':thinhgiangs})
    return thinhgiangs
