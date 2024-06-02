from asyncio import gather, create_task, sleep
from aiohttp import ClientSession
from aiofiles import open as aiopen
from vkbottle.user import User

from plugins.binder import Binder

class UserBotError(Exception): pass

class UserBot:

    def __init__(self, token:str=None, config_getter:Binder=None):
        if token is None:
            raise UserBotError("Токен не найден!")
        if config_getter is None:
            raise UserBotError("Класс Binder не найден!")
        self._bot = User(token=token)
        self._binder = config_getter

    async def worker(self):
        while True:
            config = await self._binder.get_config()
            for domain in config['domains']:
                await self._work(domain)

    async def _work(self, dom:str):
        data = self._get_wall(dom)


    async def _get_wall(self, dom:str):
        wall_data = await self._bot.api.wall.get(
            domain=dom
        )
        # ...
        return {
            "text": wall_data,
            "photos": []
        }

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
                return await resp.read()