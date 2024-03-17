import aiofiles
from fastapi import APIRouter, HTTPException, Request, Depends, UploadFile
from typing import Annotated, List
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select
import pandas as pd

from main.db_setup import get_session, engine
from main import config
from main.shortcuts import render, file, sendjson
from main.models import Donvi
from main.schemas import DonviCreate, DonviRead, DonviUpdate, ListDonviSearch, ListDonviRead

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/donvi', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def donvi(request: Request):
    context = {
        'template': 'show',
        'tab': 'donvi',
        'url': '/template/donvi'
    }
    return await render(request, "main", "base.html", context)


@router.get('/template/donvi', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_donvi(request: Request):
    context = {}
    return await render(request, "donvi", "donvi.html", context)


@router.get('/template/donvi/form/upload', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def template_donvi_form_upload(request: Request):
    context = {}
    return await render(request, "donvi", "form_upload.html", context)


@router.get('/api/donvi/table', response_class=HTMLResponse)
@requires('auth', redirect='login')
async def api_donvi_table(*, request: Request, session: db_dependency):
    data = session.exec(select(Donvi)).all()
    context = (ListDonviRead.model_validate({'data': data})).model_dump(exclude_unset=True)
    return await render(request, "donvi", "table.html", context)


@router.get("/api/donvi/download")
@requires('auth', redirect='login')
async def api_donvi_download(request: Request):
    donvi = pd.read_sql_table(table_name='donvi', con=engine)

    with pd.ExcelWriter(settings.STATIC_MAIN_DIR / 'files' / 'donvi_down.xlsx') as writer:
        donvi.to_excel(writer, sheet_name="donvi", index=False)
    return await file(request, "files/donvi_down.xlsx", filename="donvi.xlsx")


@router.post("/api/donvi/upload")
@requires('auth', redirect='login')
async def api_donvi_upload(*, request: Request, session: db_dependency, file: UploadFile):

    # save file
    async with aiofiles.open(settings.STATIC_MAIN_DIR / 'files' / 'donvi_up.xlsx', 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)


    donvi = pd.read_excel(settings.STATIC_MAIN_DIR / 'files' / 'donvi_up.xlsx', 'donvi', index_col='id', na_filter = False)
    
    for i in donvi.index:
        item = session.get(Donvi, i)
        create = DonviCreate(
            ten = donvi.loc[i].ten,
            loai = donvi.loc[i].loai,
            cap = donvi.loc[i].cap,
            is_phapnhan = bool(donvi.loc[i].is_phapnhan),
            is_nghiencuu = bool(donvi.loc[i].is_nghiencuu),
        )
        if item: # da ton tai tren he thong => update
            item_data = create.model_dump(exclude_unset=True)
            for key, value in item_data.items():
                setattr(item, key, value)
                session.add(item)
        else: # chua ton tai tren he thong => add new
            item = Donvi.model_validate(create)
            session.add(item)
    
    session.commit()

    context = {}
    return await render(request, "donvi", "form_upload_success.html", context)


@router.get("/api/donvi/read/{donvi_id}")
@requires('auth', redirect='login')
async def api_donvi_read(*, request: Request, session: db_dependency, donvi_id: int):
    donvi = session.get(Donvi, donvi_id)
    if not donvi:
        raise HTTPException(status_code=404, detail="Hero not found")
    data = (DonviRead.model_validate(donvi)).model_dump(exclude_unset=True)
    return await sendjson(request, data)

@router.post("/api/donvi/update")
@requires('auth', redirect='login')
async def api_donvi_update(*, request: Request, session: db_dependency, donvi_id: int, donvi: DonviUpdate):
    db_donvi = session.get(Donvi, donvi_id)
    if not db_donvi:
        raise HTTPException(status_code=404, detail="Hero not found")
    donvi_data = donvi.model_dump(exclude_unset=True)
    for key, value in donvi_data.items():
        setattr(db_donvi, key, value)
        session.add(db_donvi)
    session.commit()
    return await sendjson(request, {'message': 'success'})

@router.get("/api/donvi/search")
@requires('auth', redirect='login')
async def api_donvi_search(*, request: Request, session: db_dependency):
    donvis = session.exec(select(Donvi)).all()
    data = (ListDonviRead.model_validate({'data':donvis})).model_dump(exclude_unset=True)
    return await sendjson(request, data)

@router.get("/api/donvi/danhmuc")
@requires('auth', redirect='login')
async def api_donvi_danhmuc(*, request: Request, session: db_dependency):
    donvis = session.exec(select(Donvi)).all()
    data = (ListDonviSearch.model_validate({'data':donvis})).model_dump(exclude_unset=True)
    return await sendjson(request, data)