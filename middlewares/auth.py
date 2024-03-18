from sqlmodel import Session

from main.db_setup import engine
from main.models import Auth
from main.services import decode, encode
from main.middlewares.authentication_copy import (
    AuthCredentials, 
    AuthenticationBackend, 
    UnauthenticatedUser, 
    SimpleUser
)

class AuthMiddleware(AuthenticationBackend):
    blacklist = [
        'http://localhost:8000/static/',
    ]
    async def authenticate(self, request):
        crypto = request.cookies.get('crypto')
        if not crypto:
            return AuthCredentials(['guest']), UnauthenticatedUser()
        else:
            if any(item in str(request.url) for item in self.blacklist):
                return AuthCredentials(['guest']), UnauthenticatedUser()
            else:
                # try:
                with Session(engine) as session:
                    data = await decode(crypto)
                    auth = session.get(Auth, data['id'])
                    if not auth:
                        raise Exception('Cant find auth')
                    
                    print(f"pin client = {data['pin']}, pin server = {auth.pin}")
                    if (auth.pin - data['pin']) > 20:
                        session.delete(auth)
                        session.commit()
                        raise Exception('old pin')
                    auth.pin = auth.pin + 1
                    session.add(auth)
                    session.commit()
                    session.refresh(auth)
                    crypto = await encode(auth)
                
                return AuthCredentials([data.get('role'), 'auth', 'guest']), SimpleUser(uuid=auth.user_id, newcrypto=crypto)
                # except Exception as e:
                #     return AuthCredentials(['guest']), UnauthenticatedUser()