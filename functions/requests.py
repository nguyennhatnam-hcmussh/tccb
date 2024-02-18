import aiohttp
import aiofiles
import asyncio
from socket import AF_INET
from typing import Any, List, Dict
from collections.abc import Coroutine

from main.config import get_settings

settings = get_settings()

# aiohttp
SIZE_POOL_AIOHTTP = 100
class Requests:
    aiohttp_client: aiohttp.ClientSession | None = None

    @classmethod
    def get_aiohttp_client(cls) -> aiohttp.ClientSession:
        if cls.aiohttp_client is None:
            timeout = aiohttp.ClientTimeout(total=2)
            connector = aiohttp.TCPConnector(family=AF_INET, limit_per_host=SIZE_POOL_AIOHTTP)
            cls.aiohttp_client = aiohttp.ClientSession(timeout=timeout, connector=connector)

        return cls.aiohttp_client

    @classmethod
    async def close_aiohttp_client(cls) -> None:
        if cls.aiohttp_client:
            await cls.aiohttp_client.close()
            cls.aiohttp_client = None

    @classmethod
    async def post(cls, url: str, data: dict, headers: dict | None = None) -> Any:
        client = cls.get_aiohttp_client()
        # try:
        async with client.post(url, data=data, headers=headers) as response:
            if response.status != 200:
                return {"ERROR OCCURED" + str(await response.text())}

            result = await response.json()
        # except Exception as e:
        #     return {"ERROR": e}

        return result

    @classmethod
    async def get(cls, url: str, headers: dict | None = None) -> Any:
        client = cls.get_aiohttp_client()
        # try:
        async with client.get(url, headers=headers) as response:
            if response.status != 200:
                return {"ERROR OCCURED" + str(await response.text())}
            result = await response.json()

            return result

    @classmethod
    async def download_image(cls, url: str, filename:str) -> Any:
        client = cls.get_aiohttp_client()
        # try:
        async with client.get(url) as response:
            if response.status == 200:
                f = await aiofiles.open(str(settings.STATIC_MAIN_DIR / "images") + "\\" + filename + ".png", "wb")
                await f.write(await response.read())
                await f.close()