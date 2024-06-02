from asyncio import gather, create_task
from aiohttp import ClientSession
from aiofiles import open as aiopen
from vkbottle.user import User

class UserBotError(Exception): pass

class UserBot:

    def __init__(self, token:str=None):
        if token is None:
            raise UserBotError("Токен не найден")
        self._bot = User(token=token)

    async def worker(self):
        pass

    async def _get_wall(self, id:int):
        pass

    async def _write_temp(self, urls:list[str]):
        async def _internal(num, url):
            async with aiopen(f"{num}.jpg", "wb") as file:
                await file.write(
                    await self._get_photo(url)
                )
            return f"{num}.jpg"

        return await gather(
            *[create_task(_internal(num, url)) for num, url in enumerate(urls)]
        )

    async def _get_photo(self, url:str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as resp:
                return resp.content