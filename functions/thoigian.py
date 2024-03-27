import datetime
from zoneinfo import ZoneInfo

async def stamp2date(target:int) -> str:
    date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(target))).strftime("%d/%m/%Y")
    return date
async def stamp2datetime(target:int) -> str:
    date = (datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=int(target))).strftime("%H:%M %d/%m/%Y")
    return date
async def date2stamp(target:str) -> int:
    date = int((datetime.datetime.strptime(target, '%d/%m/%Y') - datetime.datetime(1970, 1, 1)).total_seconds())
    return date
async def now2stamp() -> int:
    date = int((datetime.datetime.now(tz=ZoneInfo('Asia/Ho_Chi_Minh')) - datetime.datetime(1970, 1, 1,tzinfo=ZoneInfo('Asia/Ho_Chi_Minh'))).total_seconds())
    return date