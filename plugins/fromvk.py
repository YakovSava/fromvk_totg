from string import ascii_lowercase
from os import makedirs
from os.path import exists
from random import choice, randint
from typing import Coroutine
from asyncio import gather, create_task, sleep, run
from aiohttp import ClientSession
from aiofiles import open as aiopen
from vkbottle.user import User

from plugins.binder import Binder

def _get_rand_name() -> str:
    return "".join(choice(ascii_lowercase) for _ in range(randint(5, 15))) + str(randint(1000, 5000))

async def saveids(ids:list[str]) -> None:
    async with aiopen('savedids.bin', 'wb') as file:
        await file.write(str(ids).encode())

async def getids() -> list[str]:
    try:
        async with aiopen('saveids.bin', 'rb') as file:
            return eval((await file.read()).decode())
    except:
        return []

class UserBotError(Exception): pass

class UserBot:

    def __init__(self, token:str=None, config_getter:Binder=None, dump_data_func:Coroutine=None):
        if token is None:
            raise UserBotError("Token not found!")
        if config_getter is None:
            raise UserBotError("Class Binder not found!")
        if dump_data_func is None:
            raise UserBotError("Function for dump data not found!")
        if not exists('temp'):
            makedirs('temp')
        self._bot = User(token=token)
        self._binder = config_getter
        self._ddf = dump_data_func
        self._ids = run(getids())

    async def worker(self):
        while True:
            config = await self._binder.get_config()
            for domain in config['domains']:
                await self._work(domain)

    async def _work(self, dom:str):
        data = await self._get_wall(dom)
        photos_name = await self._write_temp(data['photos'])
        return {
            'text': data['text'],
            'photos': photos_name,
            'ids': ids
        }

    async def _get_wall(self, dom:str):
        wall_data = await self._bot.api.wall.get(
            domain=dom
        )
        texts = []
        photos = []
        ids = []
        for all_data in wall_data.items:
            texts.append(all_data.text)
            for photo in all_data.attachments:
                if photo.photo is not None:
                    photos.append(photo.photo.sizes[-1].url)
            ids.append(f'{all_data.from_id}_{all_data.id}')
        return {
            "text": texts,
            "photos": photos,
            "ids": ids
        }

    async def _write_temp(self, urls:list[str]):
        async def _internal(url):
            name = _get_rand_name()
            async with aiopen(f"./temp/{name}.jpg", "wb") as file:
                await file.write(
                    await self._get_photo(url)
                )
            return f"./temp/{name}.jpg"

        return await gather(
            *[create_task(_internal(url)) for url in urls]
        )

    async def _get_photo(self, url:str) -> bytes:
        async with ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.read()