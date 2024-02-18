from jwcrypto import jwt, jwk
from typing import Dict
import json

from main.config import get_settings
from main.models import Auth

settings = get_settings()

secret_key = jwk.JWK(**settings.SECRET_KEY)

async def encode(auth:Auth) -> str:
    crypto = jwt.JWT(header=settings.ENCRYPT_ALGO, claims=auth.model_dump())
    crypto.make_encrypted_token(secret_key)

    token = crypto.serialize().replace('eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.','TCCB-')

    return token

async def decode(token:str) -> Dict[str,str]:
    crypto = token.replace('TCCB-','eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.')
    ET = jwt.JWT(key=secret_key, jwt=crypto, expected_type="JWE")

    return json.loads(ET.claims)