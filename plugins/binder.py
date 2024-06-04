from json import loads, dumps
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

    async def _write(self, config:dict) -> None:
        async with aiopen(self._filename, 'w', encoding='utf-8') as file:
            await file.write(dumps(config))

class FiltersBinder(Binder):

    async def add_new_stop(self, new_word:str) -> bool:
        old = await self.get_config()
        if new_word in old['stop']:
            return False
        old['stop'].append(new_word)
        await self._write(old)
        return True

    async def get_stop(self) -> list:
        return (await self.get_config())['stop']

    async def del_stop(self, to_delete:str) -> bool:
        config = await self.get_config()
        if to_delete in config['stop']:
            config['stop'].remove(to_delete)
            await self._write(config)
            return True
        return False

    async def add_new_replace(self, repl:str, repl_to:str) -> bool:
        config = await self.get_config()
        if [repl, repl_to] in config['replace']:
            return False
        config['replace'].append([repl, repl_to])
        await self._write(config)
        return True

    async def get_replace(self) -> list[str]:
        return (await self.get_config())['replace']

    async def del_replace(self, to_delete:list[str]) -> bool:
        config = await self.get_config()
        if to_delete in config['replace']:
            return False
        config['replace'].remove(to_delete)
        await self._write(config)
        return True


class ConfigBinder(Binder):

    async def add_new_domain(self, new_dom:str) -> bool:
        config = await self.get_config()
        if new_dom in config['domains']:
            return False
        config['domains'].append(new_dom)
        await self._write(config)
        return True

    async def del_new_group(self, to_delete:str) -> bool:
        config = await self.get_config()
        if to_delete in config['domains']:
            config['domains'].remove(to_delete)
            await self._write(config)
            return True
        return False

    async def get_domains(self) -> list[str]:
        return (await self.get_config())['domains']
        