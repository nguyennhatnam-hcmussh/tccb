
from main.functions import Requests
from main.config import get_settings

settings = get_settings()

async def AuthGoogle(code:str):
    # exchange the authorization code for an access token
    response = await Requests.post(settings.GOOGLE_TOKEN_URL, data={
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
    }, headers={'Accept': 'application/json'})

    oauth2_token = response.get('access_token')
    
    if not oauth2_token:
        raise Exception('oauth2_token')
    
    # use the access token to get the user's email address
    response = await Requests.get(settings.GOOGLE_USERINFO_URL, headers={
        'Authorization': 'Bearer ' + oauth2_token,
        'Accept': 'application/json',
    })
    
    email = response.get('email')
    if not email:
        raise Exception('email')

    return response