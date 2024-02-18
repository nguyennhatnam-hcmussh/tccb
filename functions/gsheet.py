from typing import Any
from gspread import Client
from authlib.integrations.requests_client import AssertionSession

from main.config import get_settings

settings = get_settings()

class GSheet:
    gspread_client: Client | None = None

    @classmethod
    def get_gspread_client(cls) -> Client:
        if cls.gspread_client is None:
            print('phai chay lai')
            session = AssertionSession(
                grant_type=AssertionSession.JWT_BEARER_GRANT_TYPE,
                token_endpoint=settings.GSHEET_TOKEN_URI,
                issuer=settings.GSHEET_CLIENT_EMAIL,
                audience=settings.GSHEET_TOKEN_URI,
                claims=settings.GSHEET_SCOPE,
                subject=None,
                key=settings.GSHEET_PRIVATE_KEY,
                header=settings.GSHEET_HEADER,
            )
            cls.gspread_client = Client(None, session)
            # cls.gspread_client = gspread.service_account(filename=settings.STATIC_MAIN_DIR / 'files' / 'Cred.json')
        return cls.gspread_client
        
    @classmethod
    async def get_all_row(cls) -> Any:
        client = cls.get_gspread_client()
        
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Wzlp1s76ZWbwgd-YW0oyTxcdClA06d6bunbzloJyWzY").worksheet("nampro")
        val = sheet.get_all_records()

        return val