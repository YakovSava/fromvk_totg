from json import loads
from aiofiles import open as aiopen

class BinderError(Exception): pass

class Binder:

    def __init__(self, config_filename:str):
        self._filename = config_filename

    async def get_config(self):
        async with aiopen(self._filename, 'r', encoding='utf-8') as file:
            return loads(await file.read())

    def sync_get_config(self):
        with open(self._filename, 'r', encoding='utf-8') as file:
            return loads(file.read())