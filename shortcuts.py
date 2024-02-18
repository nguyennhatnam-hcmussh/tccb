from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pathlib import Path

from main.config import get_settings

settings = get_settings()

async def set_header(response, headers):
    if headers:
        for k, v in headers.items():
            response.headers[k] = v
    return response


async def set_cookie(response, request, cookie):
    if request.user.data.get('newcrypto'):
        response.set_cookie(key='crypto', value=request.user.data.get('newcrypto'), secure=True, httponly=True)

    if len(cookie.keys()) > 0:
        for k, v in cookie.items():
            response.set_cookie(key=k, value=v, secure=True, httponly=True)
    return response

async def delete_cookie(response, request, clear_cookie):
    if clear_cookie:
        for key in request.cookies.keys():
            response.delete_cookie(key=key, secure=True, httponly=True)
    return response

async def render(request: Request, template_dir:str, template_name:str, context:dict, cookie:dict={}, headers: dict | None = None, clear_cookie:bool=False, status_code:int=200):
    
    template = Jinja2Templates(directory=str(settings.TEMPLATE_DIR[template_dir]))
    
    ctx = context.copy()
    ctx.update({"request": request})

    t = template.get_template(template_name)
    html_str = t.render(ctx)

    response = HTMLResponse(html_str, status_code=status_code)

    response = await set_cookie(response, request, cookie)
    response = await delete_cookie(response, request, clear_cookie)
    respones = await set_header(response, headers)
    return response

async def redirect(request: Request, url:str, cookie:dict={}, clear_cookie:bool=False, status_code:int=307):

    response = RedirectResponse(url, status_code=status_code)

    response = await set_cookie(response, request, cookie)
    response = await delete_cookie(response, request, clear_cookie)

    return response

async def file(request: Request, path: str, filename:str|None=None, cookie:dict={}, clear_cookie:bool=False, status_code:int=200):

    response = FileResponse(str(settings.STATIC_MAIN_DIR / path), filename=filename, status_code=status_code)

    response = await set_cookie(response, request, cookie)
    response = await delete_cookie(response, request, clear_cookie)

    return response

async def sendjson(request: Request, data:list|dict=[], cookie:dict={}, clear_cookie:bool=False, status_code:int=200):

    response = JSONResponse(content=data, status_code=status_code)

    response = await set_cookie(response, request, cookie)
    response = await delete_cookie(response, request, clear_cookie)

    return response