from urllib.parse import urlencode
from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Annotated
from starlette.authentication import requires
from fastapi.responses import HTMLResponse
from sqlmodel import Session, select

from main.functions import Requests
from main.db_setup import get_session
from main import config
from main.shortcuts import redirect, render
from main.services import AuthGoogle, encode
from main.models import Cohuu, Auth

settings = config.get_settings()

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]


@router.get('/login', response_class=HTMLResponse)
@requires('guest')
async def login(request: Request):
    context = {
        'template': 'hide',
        'url': '/template/login'
    }
    return await render(request, "main", "base.html", context, headers={'HX-Redirect': '/login'}, clear_cookie=True)


@router.get('/template/login', response_class=HTMLResponse)
@requires('guest')
async def template_login(request: Request):
    context = {}
    return await render(request, "auth", "login.html", context)


@router.get("/api/login/google")
@requires('guest')
async def api_login_google(request: Request):

    qs = urlencode({
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': ' '.join(settings.GOOGLE_SCOPE_URL),
    })
    
    url = settings.GOOGLE_AUTHORIZE_URL + '?' + qs
    
    return await redirect(request, url, status_code= 307)


@router.get("/api/auth/google")
@requires('guest')
async def api_user_auth_google(*, session: db_dependency, request: Request, code:str, error: str | None = None):
    if error:
        return HTTPException(status_code=404)

    result = await AuthGoogle(code)
    
    user = session.exec(select(Cohuu).where(Cohuu.email == result.get('email'))).one()
    
    await Requests.download_image(result.get('picture'), str(user.id))
    
    auth = session.exec(select(Auth).where(Auth.user_id == user.id)).first()
    if auth:
        session.delete(auth)
        
    auth = Auth(user_id=user.id,role=user.role)
    
    session.add(auth)
    session.commit()
    session.refresh(auth)
    
    print(auth)
    crypto = await encode(auth)

    return await redirect(request, url='/', cookie={"crypto": crypto})