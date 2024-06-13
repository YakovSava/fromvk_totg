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

    async def _set_config(self, new_config:dict) -> None:
        async with aiopen(self._filename, 'w', encoding='utf-8') as file:
            await file.write(dumps(new_config))


class FilterBinder(Binder):

    async def new_stop(self, stop:str) -> bool:
        conf = await self.get_config()
        try:
            conf['stop'].index(stop)
        except:
            conf['stop'].append(stop)
            to_ret = True
        else:
            to_ret = False
        await self._set_config(conf)
        return to_ret

    async def del_stop(self, stop:str) -> bool:
        conf = await self.get_config()
        try:
            conf['stop'].index(stop)
        except:
            to_ret = False
        else:
            conf['stop'].remove(stop)
            to_ret = True
        await self._set_config(conf)
        return to_ret

    async def new_repl(self, replace:list[str]) -> bool:
        # Replace arg is: [replace, replace to]
        conf = await self.get_config()
        try:
            conf['replace'].index(replace)
        except:
            conf['replace'].append(replace)
            to_ret = True
        else:
            to_ret = False
        await self._set_config(conf)
        return to_ret

    async def del_repl(self, replace:list[str]) -> bool:
        conf = await self.get_config()
        try:
            conf['replace'].index(replace)
        except:
            to_ret = False
        else:
            conf['replace'].remove(replace)
            to_ret = True
        await self._set_config(conf)
        return to_ret


class VKBinder(Binder):

    async def new_domain(self, domain:str) -> bool:
        conf = await self.get_config()
        try:
            conf['domains'].index(domain)
        except:
            conf['domains'].append(domain)
            to_ret = True
        else:
            to_ret = False
        await self._set_config(conf)
        return to_ret

    async def del_domain(self, domain:str) -> bool:
        conf = await self.get_config()
        try:
            conf['domains'].index(domain)
        except:
            to_ret = False
        else:
            conf['domains'].remove(domain)
            to_ret = True
        await self._set_config(conf)
        return to_ret